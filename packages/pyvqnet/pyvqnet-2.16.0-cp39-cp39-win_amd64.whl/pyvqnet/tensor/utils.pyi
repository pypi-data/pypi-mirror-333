from ..config import get_if_grad_enabled as get_if_grad_enabled, set_if_grad_enabled as set_if_grad_enabled
from ..dtype import kcomplex128 as kcomplex128, kcomplex32 as kcomplex32, kcomplex64 as kcomplex64, kfloat16 as kfloat16, kfloat32 as kfloat32, kfloat64 as kfloat64, vqnet_complex_dtypes as vqnet_complex_dtypes
from _typeshed import Incomplete

slice_none_Placeholder: int

def FLOAT_2_COMPLEX(param): ...

class no_grad:
    prev: bool
    def __init__(self) -> None: ...
    def __enter__(self) -> None: ...
    def __exit__(self, exc_type: type[BaseException] | None, exc_value: BaseException | None, traceback: types.TracebackType | None) -> None: ...

def has_duplicates(lst): ...
def maybe_wrap_dim(dim: list[int] | tuple[int, ...] | int, dim_post_expr, wrap_scalar: bool = True):
    """
    check dim valid
    """

use_qtensor_graphnode: bool

def set_use_qtensor_graphnode(flag) -> None: ...
def get_use_qtensor_graphnode(): ...

global_cache_map: Incomplete

def erase_global_cache_map() -> None: ...
def get_global_cache_map(id): ...
def del_kv_in_global_cache_map(key) -> None: ...
def set_global_cache_map(id, fake) -> None: ...

class DummyTensor:
    id: Incomplete
    nodes: Incomplete
    device: Incomplete
    requires_grad: Incomplete
    shape: Incomplete
    dtype: Incomplete
    grad: Incomplete
    data: Incomplete
    def __init__(self, input_id, t) -> None:
        """
        
        """

def create_fake_tensor(input_id, if_weights, t): ...
def maybe_wrap_dim_unsqueeze(dim, dim_post_expr, wrap_scalar: bool = True):
    """    check dim valid
    """

class keep_activation_in_graph:
    prev: bool
    def __init__(self) -> None: ...
    def __enter__(self) -> None: ...
    def __exit__(self, exc_type: type[BaseException] | None, exc_value: BaseException | None, traceback: types.TracebackType | None) -> None: ...

class AutoGradNode:
    """
    A dummy autograd node for internal gradients calculation.
    It simply mocks QTensor without real data reference to save some storage.
    For internal activation may not need real data for backward.
    """
    tensor: Incomplete
    name: Incomplete
    df: Incomplete
    device: Incomplete
    def __init__(self, tensor, df, name: str = '') -> None: ...
