from _typeshed import Incomplete
from collections.abc import Generator

class QueuingManager:
    """Singleton global entry point for managing active recording contexts.

    """
    @classmethod
    def add_active_queue(cls, queue) -> None:
        """Makes a queue the currently active recording context."""
    @classmethod
    def remove_active_queue(cls):
        """Ends recording on the currently active recording queue."""
    @classmethod
    def recording(cls):
        """Whether a queuing context is active and recording operations"""
    @classmethod
    def active_context(cls):
        """Returns the currently active queuing context."""
    @classmethod
    def stop_recording(cls) -> Generator[None]: ...
    @classmethod
    def append(cls, obj, **kwargs) -> None:
        """Append an object to the queue(s).

        Args:
            obj: the object to be appended
        """
    @classmethod
    def remove(cls, obj) -> None:
        """Remove an object from the queue(s) if it is in the queue(s).

        Args:
            obj: the object to be removed
        """
    @classmethod
    def update_info(cls, obj, **kwargs) -> None:
        """Updates information of an object in the active queue if it is already in the queue.

        Args:
            obj: the object with metadata to be updated
        """
    @classmethod
    def safe_update_info(cls, obj, **kwargs) -> None: ...
    @classmethod
    def get_info(cls, obj): ...

class AnnotatedQueue:
    """Lightweight class that maintains a basic queue of operations, in addition
    to metadata annotations."""
    def __init__(self) -> None: ...
    def __enter__(self):
        """Adds this instance to the global list of active contexts.

        Returns:
            AnnotatedQueue: this instance
        """
    def __exit__(self, exception_type: type[BaseException] | None, exception_value: BaseException | None, traceback: types.TracebackType | None) -> None:
        """Remove this instance from the global list of active contexts."""
    def append(self, obj, **kwargs) -> None:
        """Append ``obj`` into the queue with ``kwargs`` metadata."""
    def remove(self, obj) -> None:
        """Remove ``obj`` from the queue.  Raises ``KeyError`` if ``obj`` is not already in the queue."""
    def update_info(self, obj, **kwargs) -> None:
        """Update ``obj``'s metadata with ``kwargs`` if it exists in the queue."""
    def safe_update_info(self, obj, **kwargs) -> None:
        """Update ``obj``'s metadata with ``kwargs`` if it exists in the queue."""
    def get_info(self, obj):
        """Retrieve the metadata for ``obj``.  Raises a ``QueuingError`` if obj is not in the queue."""
    @property
    def queue(self):
        """Returns a list of objects in the annotated queue"""

class QuantumTape(AnnotatedQueue):
    """A quantum tape recorder, that records and stores variational quantum programs.

    """
    def __init__(self) -> None: ...
    def __enter__(self): ...
    def __exit__(self, exception_type: type[BaseException] | None, exception_value: BaseException | None, traceback: types.TracebackType | None) -> None: ...

class PQ_QNode:
    func: Incomplete
    def __init__(self, func) -> None: ...
    @property
    def tape(self):
        """The quantum tape"""
    def __call__(self, *args, **kwargs): ...
    @property
    def operations(self): ...
    @property
    def parameters(self): ...
    def bind_parameters(self, in_param) -> None: ...

class RX_H:
    def __call__(self, qubits, idxs, w): ...

class RX:
    def __call__(self, qubits, idxs, w): ...

class RZ_H:
    def __call__(self, qubits, idxs, w): ...

class RZ:
    def __call__(self, qubits, idxs, w): ...

class RY:
    def __call__(self, qubits, idxs, w): ...

class RY_H:
    def __call__(self, qubits, idxs, w): ...

class CNOT:
    def __call__(self, qubits, idxs): ...

class CNOT_H:
    def __call__(self, qubits, idxs): ...

class X:
    def __call__(self, qubits, idxs): ...

class Y:
    def __call__(self, qubits, idxs): ...

class Z:
    def __call__(self, qubits, idxs): ...

class X_H:
    def __call__(self, qubits, idxs): ...

class Y_H:
    def __call__(self, qubits, idxs): ...

class Z_H:
    def __call__(self, qubits, idxs): ...

class QuantumMeasure:
    def __call__(self, measure_qubits, prog, machine, qlists, shots): ...

class ProbsMeasure:
    def __call__(self, measure_qubits: list, prog, machine, qlists): ...

class EXP:
    def __call__(self, machine, pauli_str_dict, prog, qlists, idxs): ...

qnode: Incomplete
PQ_1BIT_VQC_GATES: Incomplete
PQ_1BIT_NONVQC_GATES: Incomplete
PQ_2BIT_NONVQC_GATES: Incomplete
PQ_MEASURE: Incomplete
