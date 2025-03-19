"""Particle Swarm Optimization (Kennedy & Eberhart, 1995).

[1] https://ieeexplore.ieee.org/document/488968
"""

from collections.abc import Callable

import jax
import jax.numpy as jnp
from flax import struct

from evosax.core.fitness_shaping import identity_fitness_shaping_fn
from evosax.types import Fitness, Population, Solution

from .base import (
    Params as BaseParams,
    PopulationBasedAlgorithm,
    State as BaseState,
    metrics_fn,
)


@struct.dataclass
class State(BaseState):
    population: Population
    fitness: Fitness
    population_best: Population
    fitness_best: Fitness
    velocity: jax.Array


@struct.dataclass
class Params(BaseParams):
    inertia_coeff: float  # w momentum of velocity
    cognitive_coeff: float  # c_1 cognitive "force" multiplier
    social_coeff: float  # c_2 social "force" multiplier


class PSO(PopulationBasedAlgorithm):
    """Particle Swarm Optimization (PSO)."""

    def __init__(
        self,
        population_size: int,
        solution: Solution,
        fitness_shaping_fn: Callable = identity_fitness_shaping_fn,
        metrics_fn: Callable = metrics_fn,
    ):
        """Initialize PSO."""
        super().__init__(population_size, solution, fitness_shaping_fn, metrics_fn)

    @property
    def _default_params(self) -> Params:
        return Params(
            inertia_coeff=0.75,
            cognitive_coeff=1.5,
            social_coeff=2.0,
        )

    def _init(self, key: jax.Array, params: Params) -> State:
        state = State(
            population=jnp.full((self.population_size, self.num_dims), jnp.nan),
            fitness=jnp.full((self.population_size,), jnp.inf),
            population_best=jnp.full((self.population_size, self.num_dims), jnp.nan),
            fitness_best=jnp.full((self.population_size,), jnp.inf),
            velocity=jnp.zeros((self.population_size, self.num_dims)),
            best_solution=jnp.full((self.num_dims,), jnp.nan),
            best_fitness=jnp.inf,
            generation_counter=0,
        )
        return state

    def _ask(
        self,
        key: jax.Array,
        state: State,
        params: Params,
    ) -> tuple[Population, State]:
        # Get global best
        population_best = jnp.where(
            jnp.isnan(state.population_best), state.population, state.population_best
        )
        fitness_best = jnp.where(
            jnp.isnan(state.fitness_best), state.fitness, state.fitness_best
        )
        best_global_idx = jnp.argmin(fitness_best)
        best_global = population_best[best_global_idx]

        def _ask_velocity(key, velocity, member, member_best):
            # Sharing r1, r1 across dimensions seems more robust
            r1, r2 = jax.random.uniform(key, (2,))
            return (
                params.inertia_coeff * velocity
                + params.cognitive_coeff * r1 * (member_best - member)
                + params.social_coeff * r2 * (best_global - member)
            )

        # Update particle positions with velocity
        keys = jax.random.split(key, self.population_size)
        velocity = jax.vmap(_ask_velocity)(
            keys, state.velocity, state.population, population_best
        )
        x = state.population + velocity
        return x, state.replace(velocity=velocity)

    def _tell(
        self,
        key: jax.Array,
        population: Population,
        fitness: Fitness,
        state: State,
        params: Params,
    ) -> State:
        replace = fitness <= state.fitness_best
        population_best = jnp.where(
            replace[..., None], population, state.population_best
        )
        fitness_best = jnp.where(replace, fitness, state.fitness_best)
        return state.replace(
            population=population,
            fitness=fitness,
            population_best=population_best,
            fitness_best=fitness_best,
        )
