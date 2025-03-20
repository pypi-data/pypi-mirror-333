from .backends import check_not_default_backend as check_not_default_backend, get_backend as get_backend

if_show_bp_info: bool
if_grad_enabled: int
is_dist_init: bool

def get_is_dist_init():
    """
    global flag if vqnet distributed is initialed.

    """
def set_is_dist_init(flag) -> None:
    """
    set global flag if vqnet distributed is initialed.
    
    """
def default_if_grad_enabled():
    """
    get default pyvqnet if_grad_enabled
    """
def set_default_if_grad_enabled(flag) -> None:
    """
    set default pyvqnet value of if_grad_enabled
    """
def get_if_grad_enabled():
    """
    get if_grad_enabled
    """
def set_if_grad_enabled(flag) -> None:
    """
    set value of if_grad_enabled
    """
def get_if_show_bp_info():
    """
    get flag of if_show_bp_info
    """
def set_if_show_bp_info(flag) -> None:
    """
    set flag of if_show_bp_info
    """
def init_if_show_bp() -> None:
    """
    init flag of if_show_bp_info to False
    """
def is_opt_einsum_available() -> bool:
    """Return a bool indicating if opt_einsum is currently available."""
