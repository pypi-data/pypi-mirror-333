import jax
import jax.numpy as jnp
from flax import linen as nn

from .fitness_shaping import normalize, standardize


def tanh_age(x: jax.Array, generation_counter: float) -> jax.Array:
    """Return normalized tanh age."""
    return jnp.tanh(x / jnp.float32(generation_counter) - 1.0)


class MultiHeadSelfAttention(nn.Module):
    num_heads: int = 1
    num_features: int = 16

    @nn.compact
    def __call__(self, x: jax.Array) -> jax.Array:
        """Apply multi-head dot product self-attention on the input data.

        Args:
            x: input of shape `[length, features_in]`.

        Returns:
            output of shape `[length, num_features]`.

        """
        assert self.num_features % self.num_heads == 0, (
            "Memory dimension must be divisible by number of heads."
        )
        head_dim = self.num_features // self.num_heads
        # project x to multi-headed q/k/v + apply dot-product attention
        # dimensions are then [length, n_heads, n_features_per_head]
        query = multi_head_embedding(x, self.num_heads, head_dim, "query")
        key = multi_head_embedding(x, self.num_heads, head_dim, "key")
        value = multi_head_embedding(x, self.num_heads, head_dim, "value")
        x_att = scaled_dot_product(query, key, value)
        # Only apply out mixing of heads if more than one head - else squeeze
        if self.num_heads > 1:
            out = mix_head_outputs(x_att, self.num_features, "out")
        else:
            out = jnp.squeeze(x_att, axis=1)
        return out


class MultiHeadCrossAttention(nn.Module):
    num_heads: int = 1
    num_features: int = 16

    @nn.compact
    def __call__(self, x: jax.Array, y: jax.Array) -> jax.Array:
        """Apply multi-head dot product self-attention on the input data.

        Args:
          x: input of shape `[length_1, features_in]`. - Key/value input.
          y: input of shape `[length_2, features_in]`. - Query input.

        Returns:
            output of shape `[length_2, num_features]`.

        """
        assert self.num_features % self.num_heads == 0, (
            "Memory dimension must be divisible by number of heads."
        )
        head_dim = self.num_features // self.num_heads
        # project x to multi-headed q/k/v + apply dot-product attention
        # dimensions are then [length, n_heads, n_features_per_head]
        query = multi_head_embedding(y, self.num_heads, head_dim, "query")
        key = multi_head_embedding(x, self.num_heads, head_dim, "key")
        value = multi_head_embedding(x, self.num_heads, head_dim, "value")
        x_att = scaled_dot_product(query, key, value)
        # Only apply out mixing of heads if more than one head - else squeeze
        if self.num_heads > 1:
            out = mix_head_outputs(x_att, self.num_features, "out")
        else:
            out = jnp.squeeze(x_att, axis=1)
        return out


def multi_head_embedding(
    x: jax.Array, num_heads: int, head_dim: int, label: str
) -> jax.Array:
    """Dense general embedding layer."""
    return nn.linear.DenseGeneral(
        features=(num_heads, head_dim),
        use_bias=True,
        name=label,
    )(x)


def mix_head_outputs(x: jax.Array, num_features: int, label: str) -> jax.Array:
    """Dense mixing of heads layer."""
    return nn.linear.DenseGeneral(
        features=num_features,
        axis=(-2, -1),
        use_bias=True,
        name=label,
    )(x)


def scaled_dot_product(q: jax.Array, k: jax.Array, v: jax.Array) -> jax.Array:
    """Compute dot-product attention given multi-headed query, key, and value.

    Args:
        q: queries for calculating attention with shape of
            `[length, heads, embed_dim]`.
        k: keys for calculating attention with shape of
            `[length, heads, embed_dim]`.
        v: values for calculating attention with shape of
            `[length, heads, embed_dim]`.

    Returns:
        output of shape [length, heads, embed_dim]

    """
    d_k = q.shape[-1]
    attn_logits = jnp.matmul(
        jnp.transpose(q, (1, 0, 2)),
        jnp.transpose(k, (1, 2, 0)),
    )
    attn_logits = attn_logits / jnp.sqrt(d_k)
    attention = nn.softmax(attn_logits, axis=-1)
    values = jnp.matmul(attention, jnp.swapaxes(v, 0, 1))
    return jnp.swapaxes(values, 0, 1)  # [h, l, d] -> [l, h, d]


class SamplingAttention(nn.Module):
    num_att_heads: int
    att_hidden_dims: int

    @nn.compact
    def __call__(self, F_E: jax.Array) -> jax.Array:
        # Perform cross-attention between kids and parents
        S = MultiHeadSelfAttention(self.num_att_heads, self.att_hidden_dims)(F_E)
        logits = nn.Dense(1)(S)
        return nn.softmax(logits.squeeze(axis=-1))


class SelectionAttention(nn.Module):
    num_att_heads: int
    att_hidden_dims: int

    @nn.compact
    def __call__(self, key: jax.Array, F_X: jax.Array, F_E: jax.Array) -> jax.Array:
        # Perform cross-attention between kids and parents
        A = MultiHeadCrossAttention(self.num_att_heads, self.att_hidden_dims)(F_X, F_E)
        # Construct raw selection matrix with row-wise logits
        queries_S = nn.Dense(self.att_hidden_dims)(A)
        keys_S = nn.Dense(self.att_hidden_dims)(F_X)
        # Selection matrix (elite_population_size, population_size)
        S = (queries_S @ keys_S.T) / jnp.sqrt(self.att_hidden_dims)
        # Selection matrix w. parent (elite_population_size, population_size + 1)
        S_p = jnp.concatenate([S, jnp.ones((S.shape[0], 1))], axis=1)
        # Sample kid id to replace or parent id to keep
        idx = jax.random.categorical(key, S_p, axis=1)
        S_M = jnp.zeros(S_p.shape).at[jnp.arange(S.shape[0]), idx].set(1)
        # Return mask w/o final column corresponding to parent
        return S_M[:, : F_X.shape[0]]


class MutationAttention(nn.Module):
    num_att_heads: int
    att_hidden_dims: int

    @nn.compact
    def __call__(self, sigma: jax.Array, F: jax.Array) -> jax.Array:
        z_feat = standardize(sigma)
        norm_feat = normalize(sigma)
        conc_inputs = jnp.concatenate([F, z_feat, norm_feat], axis=1)
        M = MultiHeadSelfAttention(self.num_att_heads, self.att_hidden_dims)(
            conc_inputs
        )
        log_var = nn.Dense(1)(M)
        multiplier = jnp.exp(0.5 * log_var)
        sigma_out = sigma * multiplier
        return sigma_out
