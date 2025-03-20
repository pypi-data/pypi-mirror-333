from ..backends import check_not_default_backend as check_not_default_backend, get_backend as get_backend, get_backend_name as get_backend_name
from ..config import default_if_grad_enabled as default_if_grad_enabled, get_if_show_bp_info as get_if_show_bp_info, get_is_dist_init as get_is_dist_init, is_opt_einsum_available as is_opt_einsum_available
from ..types import _device_type, _dtype_type, _size_type
from .utils import AutoGradNode as AutoGradNode, maybe_wrap_dim as maybe_wrap_dim, maybe_wrap_dim_unsqueeze as maybe_wrap_dim_unsqueeze, slice_none_Placeholder as slice_none_Placeholder
from _typeshed import Incomplete
from collections import OrderedDict as OrderedDict
from functools import reduce as reduce
from pyvqnet.device import DEV_CPU as DEV_CPU, DEV_GPU_0 as DEV_GPU_0, get_readable_device_str as get_readable_device_str
from pyvqnet.dtype import dtype_map as dtype_map, get_default_dtype as get_default_dtype, kbool as kbool, kcomplex128 as kcomplex128, kcomplex64 as kcomplex64, kfloat32 as kfloat32, kfloat64 as kfloat64, vqnet_complex_dtypes as vqnet_complex_dtypes

long = int
integer_types: Incomplete
numeric_types: Incomplete
MIN_FLOAT: Incomplete
MAX_FLOAT: Incomplete

def set_select(t, index, set_tensor): ...
def unsqueeze(t, axis): ...
def narrow(input, dim, start, length):
    """
    
    """
def select(t, index: list):
    """
    default vqnet impl.
    """
def getitem(self, item): ...
def setitem(self, key, value) -> None: ...
def size(data): ...
def stride(data): ...
def get_vqnet_device(device): ...
def get_vqnet_dtype(dtype): ...
def to_numpy(self):
    """
    Copy self.data to a new np.array.

    :return: a numpy array

    Example::

        t3  =  QTensor([2,3,4,5],requires_grad = True)
        t4 = t3.to_numpy()
    """
def zeros_grad(self) -> None: ...
def transpose(t, dim): ...
permute = transpose

def requires_grad_getter(self): ...
def requires_grad_setter(data, new_value) -> None: ...
def create_tensor(data, device, dtype): ...
def zeros(shape: _size_type, device: _device_type = 0, dtype: _dtype_type = None): ...
