import tensornetwork as tn
from .cons import backend as backend
from typing import Any, Sequence

Tensor = Any

class FiniteMPS(tn.FiniteMPS):
    center_position: int | None
    def apply_two_site_gate(self, gate: Tensor, site1: int, site2: int, max_singular_values: int | None = None, max_truncation_err: float | None = None, center_position: int | None = None, relative: bool = False) -> Tensor:
        '''
        Apply a two-site gate to an MPS. This routine will in general destroy
        any canonical form of the state. If a canonical form is needed, the user
        can restore it using `FiniteMPS.position`.

        :param gate: A two-body gate.
        :type gate: Tensor
        :param site1: The first site where the gate acts.
        :type site1: int
        :param site2: The second site where the gate acts.
        :type site2: int
        :param max_singular_values: The maximum number of singular values to keep.
        :type max_singular_values: Optional[float], optional
        :param max_truncation_err: The maximum allowed truncation error.
        :type max_truncation_err: Optional[float], optional
        :param center_position: An optional value to choose the MPS tensor at
            `center_position` to be isometric after the application of the gate.
            Defaults to `site1`. If the MPS is canonical (i.e.`BaseMPS.center_position != None`),
            and if the orthogonality center
            coincides with either `site1` or `site2`,  the orthogonality center will
            be shifted to `center_position` (`site1` by default).
            If the orthogonality center does not coincide with `(site1, site2)` then
            `MPS.center_position` is set to `None`.
        :type center_position: Optional[int],optional
        :param relative: Multiply `max_truncation_err` with the largest singular value.
        :type relative: bool
        :raises ValueError: "rank of gate is {} but has to be 4", "site1 = {} is not between 0 <= site < N - 1 = {}",
            "site2 = {} is not between 1 <= site < N = {}","Found site2 ={}, site1={}. Only nearest
            neighbor gates are currently supported",
            "f center_position = {center_position} not  f in {(site1, site2)} ", or
            "center_position = {}, but gate is applied at sites {}, {}. Truncation should only be done if the gate
            is applied at the center position of the MPS."
        :return: A scalar tensor containing the truncated weight of the truncation.
        :rtype: Tensor
        '''
    def copy(self) -> FiniteMPS: ...
    def conj(self) -> FiniteMPS: ...
    def measure_local_operator(self, ops: list[Tensor], sites: Sequence[int]) -> list[Tensor]:
        """
        Measure the expectation value of local operators `ops` site `sites`.

        :param ops: A list Tensors of rank 2; the local operators to be measured.
        :type ops: List[Tensor]
        :param sites: Sites where `ops` act.
        :type sites: Sequence[int]
        :returns: measurements :math:`\\langle` `ops[n]`:math:`\\rangle` for n in `sites`
        :rtype: List[Tensor]
        """
    def measure_two_body_correlator(self, op1: Tensor, op2: Tensor, site1: int, sites2: Sequence[int]) -> list[Tensor]:
        """
        Compute the correlator
        :math:`\\langle` `op1[site1], op2[s]`:math:`\\rangle`
        between `site1` and all sites `s` in `sites2`. If `s == site1`,
        `op2[s]` will be applied first.

        :param op1: Tensor of rank 2; the local operator at `site1`.
        :type op1: Tensor
        :param op2: Tensor of rank 2; the local operator at `sites2`.
        :type op2: Tensor
        :param site1: The site where `op1`  acts
        :type site1: int
        :param sites2: Sites where operator `op2` acts.
        :type sites2: Sequence[int]
        :returns: Correlator :math:`\\langle` `op1[site1], op2[s]`:math:`\\rangle` for `s` :math:`\\in` `sites2`.
        :rtype: List[Tensor]
        """
