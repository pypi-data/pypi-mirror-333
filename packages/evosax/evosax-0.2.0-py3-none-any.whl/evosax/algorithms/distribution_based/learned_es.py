"""Learned Evolution Strategy (Lange et al., 2023).

[1] https://arxiv.org/abs/2211.11260
Note: This is an independent reimplementation which does not use the same meta-trained
checkpoint used to generate the results in the paper. It has been independently
meta-trained and tested on a handful of Brax tasks. The results may therefore differ
from the ones shown in the paper.
"""

import pkgutil
from collections.abc import Callable

import jax
import jax.numpy as jnp
from flax import struct

from evosax.core.fitness_shaping import identity_fitness_shaping_fn
from evosax.types import Fitness, Population, PyTree, Solution

from ...learned_evolution.les_tools import (
    AttentionWeights,
    EvolutionPath,
    EvoPathMLP,
    FitnessFeatures,
    load_pkl_object,
    tanh_timestamp,
)
from ..base import update_best_solution_and_fitness
from .base import (
    DistributionBasedAlgorithm,
    Params as BaseParams,
    State as BaseState,
    metrics_fn,
)


@struct.dataclass
class State(BaseState):
    mean: jax.Array
    std: jax.Array
    p_std: jax.Array
    p_c: jax.Array
    best_solution_shaped: Solution
    best_fitness_shaped: float


@struct.dataclass
class Params(BaseParams):
    std_init: float
    params: PyTree


class LearnedES(DistributionBasedAlgorithm):
    """Learned Evolution Strategy (LES)."""

    def __init__(
        self,
        population_size: int,
        solution: Solution,
        params: PyTree | None = None,
        params_path: str | None = None,
        fitness_shaping_fn: Callable = identity_fitness_shaping_fn,
        metrics_fn: Callable = metrics_fn,
    ):
        """Initialize LES."""
        super().__init__(population_size, solution, fitness_shaping_fn, metrics_fn)

        # LES components
        self.fitness_features = FitnessFeatures(centered_rank=True, z_score=True)
        self.weight_layer = AttentionWeights(8)
        self.lr_layer = EvoPathMLP(8)
        self.evopath = EvolutionPath(
            num_dims=self.num_dims, timescales=jnp.array([0.1, 0.5, 0.9])
        )

        if params is not None:
            # Set params provided
            self.les_params = params
        elif params_path is not None:
            # Load params from checkpoint
            self.les_params = load_pkl_object(params_path)
        else:
            # Load default params
            ckpt_fname = "2023_10_les_v2.pkl"
            data = pkgutil.get_data(__name__, f"../ckpt/les/{ckpt_fname}")
            self.les_params = load_pkl_object(data, pkg_load=True)

    @property
    def _default_params(self) -> Params:
        return Params(
            std_init=1.0,
            params=self.les_params,
        )

    def _init(self, key: jax.Array, params: Params) -> State:
        init_p_c = self.evopath.init()
        init_p_std = self.evopath.init()
        return State(
            mean=jnp.full((self.num_dims,), jnp.nan),
            std=params.std_init * jnp.ones(self.num_dims),
            p_c=init_p_c,
            p_std=init_p_std,
            best_solution_shaped=jnp.full((self.num_dims,), jnp.nan),
            best_fitness_shaped=jnp.inf,
            best_solution=jnp.full((self.num_dims,), jnp.nan),
            best_fitness=jnp.inf,
            generation_counter=0,
        )

    def _ask(
        self,
        key: jax.Array,
        state: State,
        params: Params,
    ) -> tuple[Population, State]:
        z = jax.random.normal(key, (self.population_size, self.num_dims))
        population = state.mean + state.std[None, ...] * z
        return population, state

    def _tell(
        self,
        key: jax.Array,
        population: Population,
        fitness: Fitness,
        state: State,
        params: Params,
    ) -> State:
        # Fitness features
        fitness_features = self.fitness_features.apply(
            population, fitness, state.best_fitness_shaped
        )
        time_embed = tanh_timestamp(state.generation_counter)

        # Fitness shaping
        weights = self.weight_layer.apply(
            params.params["recomb_weights"], fitness_features
        )
        weight_diff = (weights * (population - state.mean)).sum(axis=0)
        weight_noise = (weights * (population - state.mean) / state.std).sum(axis=0)

        # Update evolution paths
        p_c = self.evopath.update(state.p_c, weight_diff)
        p_std = self.evopath.update(state.p_std, weight_noise)

        # Learning rates
        lrs_mean, lrs_std = self.lr_layer.apply(
            params.params["lrate_modulation"],
            p_c,
            p_std,
            time_embed,
        )

        # Update mean and std
        weighted_mean = jnp.sum(weights * population, axis=0)
        weighted_std = jnp.sqrt(
            jnp.sum(weights * (population - state.mean) ** 2, axis=0) + 1e-8
        )
        mean = state.mean + lrs_mean * (weighted_mean - state.mean)
        std = state.std + lrs_std * (weighted_std - state.std)
        std = jnp.clip(std, min=0)

        # Update best solution and fitness shaped
        best_solution_shaped, best_fitness_shaped = update_best_solution_and_fitness(
            population, fitness, state.best_solution_shaped, state.best_fitness_shaped
        )

        return state.replace(
            mean=mean,
            std=std,
            p_c=p_c,
            p_std=p_std,
            best_solution_shaped=best_solution_shaped,
            best_fitness_shaped=best_fitness_shaped,
        )
