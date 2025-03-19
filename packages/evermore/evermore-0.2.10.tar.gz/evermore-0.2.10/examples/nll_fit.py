import equinox as eqx
import jax
import jax.numpy as jnp
import optax
from model import hists, model, observation

import evermore as evm

optim = optax.sgd(learning_rate=1e-2)
opt_state = optim.init(eqx.filter(model, eqx.is_inexact_array))


@eqx.filter_jit
def loss(dynamic_model, static_model, hists, observation):
    model = eqx.combine(dynamic_model, static_model)
    expectations = model(hists)
    constraints = evm.loss.get_log_probs(model)
    loss_val = (
        evm.pdf.Poisson(evm.util.sum_over_leaves(expectations))
        .log_prob(observation)
        .sum()
    )
    # add constraint
    loss_val += evm.util.sum_over_leaves(constraints)
    return -jnp.sum(loss_val)


@eqx.filter_jit
def make_step(model, opt_state, events, observation):
    # differentiate full analysis
    dynamic_model, static_model = eqx.partition(
        model, evm.parameter.value_filter_spec(model)
    )
    grads = eqx.filter_grad(loss)(dynamic_model, static_model, events, observation)
    updates, opt_state = optim.update(grads, opt_state)
    # apply nuisance parameter and DNN weight updates
    model = eqx.apply_updates(model, updates)
    return model, opt_state


# minimize model with 1000 steps
for step in range(1000):
    if step % 100 == 0:
        dynamic_model, static_model = eqx.partition(
            model, evm.parameter.value_filter_spec(model)
        )
        loss_val = loss(dynamic_model, static_model, hists, observation)
        print(f"{step=} - {loss_val=:.6f}")
    model, opt_state = make_step(model, opt_state, hists, observation)


# For low overhead it is recommended to use jax.lax.fori_loop.
# In case you want to jit the for loop, you can use the following function,
# this will prevent jax from unrolling the loop and creating a huge graph
@jax.jit
def fit(steps: int = 1000) -> tuple[eqx.Module, tuple]:
    def fun(step, model_optstate):
        model, opt_state = model_optstate
        return make_step(model, opt_state, hists, observation)

    return jax.lax.fori_loop(0, steps, fun, (model, opt_state))
