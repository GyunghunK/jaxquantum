""" Helpers. """

from typing import List
from jax import config
from math import prod

import jax.numpy as jnp
from jax.nn import one_hot

from jaxquantum.core.qarray import Qarray, Qtypes, tensor
from jaxquantum.core.dims import Qtypes

config.update("jax_enable_x64", True)


def isvec(A: Qarray) -> bool:
    """Check if A is a ket.

    Args:
        A: state.

    Returns:
        True if A is a ket, False otherwise.
    """
    return A.qtype == Qtypes.ket or A.qtype == Qtypes.bra

# Calculations ----------------------------------------------------------------

def overlap(A: Qarray, B: Qarray) -> complex:
    """Overlap between two states.

    Args:
        A: state.
        B: state.

    Returns:
        Overlap between A and B.
    """
    # A.qtype

    if isvec(A) and isvec(B):
        return jnp.abs(((A.to_ket().dag() @ B.to_ket()).trace()))**2
    elif isvec(A):
        A = A.to_ket()
        res = (A.dag() @ B @ A).data
        return res.squeeze(-1).squeeze(-1)
    elif isvec(B):
        return overlap(B, A)
    else:
        return (A.dag() @ B).trace()


# def fidelity(A: Qarray, B: Qarray) -> float:
#     """Fidelity between two states.

#     Args:
#         A: state.
#         B: state.

#     Returns:
#         Fidelity between A and B.
#     """


#     if isvec(A) or isvec(B):
#         return overlap(A, B)
#     else:
        