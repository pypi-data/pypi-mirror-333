-------------------------
Inclusion/Exclusion (PIE)
-------------------------

|Fragment| provides multiple strategies for solving inclusion/exclusion for large systems. [PIE]_ This is the core principle behind the generalized many-body expansion(GMBE) [GMBE]_ which is a more general expression of the many-body expansion (MBE). [MBE]_ See the section on :ref:`fragmentation <Fragmentation>` for more details, but brief, we are trying to solve two equations

.. math::
    :name: eq:s_update

    S_{x + 1} = S_x \cup \{ F_{\alpha} \} \cup \big\{ F_{\alpha} \cap F_{i}: F_{i} \in S_{x} \big\} \; .

and

.. math:: 
    :name: eq:E_update

    E^{(x + 1)} = E^{(x)} + \Delta E^{(x + 1)}

where

.. math::
    :name: eq:E_delta

    \Delta E^{(x + 1)} = E_\alpha - \sum_{i \in S_x} C_{i,x} E_{i \cap \alpha} \;

Where :math:`S_{x + 1}` is a set of sets representing each individual fragment in the fragmentation scheme and :math:`E^{(x + 1)}` weights the systems energies by a set-specifc weighting coefficients to prevent double counting.

Available Solvers
=====================

|Fragment| provides two 

A Simple PIE Solver
===================

The most basic PIE solver stores information in dictionary where the keys are  Python :py:obj:`frozenset` objects and the keys are integers.

.. code-block:: python

    S: dict[frozenset[int], int] = {}

The to update the scheme with a new fragment, the new fragment is compared against all existing members of :math:`S_{(x)}`. The intersection of the new fragment and the existing fragment has a weight equal an oposite of the existing fragment.

.. code-block:: python

    def update(S: dict, n: frozenset[int], coef: int = 1):
        """Method to add new fragment `n` to scheme `S`"""

        # Dictionary to store all changes to S
        # We cannot mutate S while iterating
        deltas = {n: coef}

        # Calculate overlaps and new coefs
        for n2, n2_coef in S.items():
            new_n = n.intersection(n2)
            # Many intersections will produce the same overlap
            try:
                deltas[new_n] += -coef * n2_coef
            except KeyError:
                deltas[new_n] = -coef * n2_coef
        
        # Update S
        for new_n, dn in deltas.items():    
            try:
                S[new_n] += dn
            except KeyError:
                S[new_n] = dn

That's really it. A slightly more optimized implementation is provided with |Fragment| in the :py:mod:`fragment.core.quickPIE` module.

.. note::

    Why not just calculate the coefficients explicitly *à la* the MBE?

    Firstly, |Fragment| supports overlapping systems and the MBE
    cannot handle this.

    Secondly, using the PIE-based scheme allows term cancellations in the expansion leading to both accuracy improvements *and* cost savings.

    Take the example of the trimer *ABC* approximated by the  dimers *AB* and *BC*. The starting scheme would be::

        AB:  1
        BC:  1
        B:  -1

    **Expanding with PIE**

    Expanding this scheme with *ABC* using a PIE solver yields a delta of::

        ABD: 1
        AB: -1
        BC: -1
        B:   1

    and the final scheme would be::

        ABC: 1

    Using PIE-based schemes, large fragments which make low-level fragments redundent simply replace them.

    **Expanding with MBE Coefficients**

    Expanding this scheme with *ABC* using a the MBE (:math:`\Delta E_{ABC}`) gives a delta of::

        ABD: 1
        AB: -1
        AC: -1
        BC: -1
        A:   1
        B:   1
        C:   1

    and the final MBE-based scheme would be::

        ABC: 1
        AC: -1
        A:   1
        C:   1

    In this case, the terms *AC*, *A*, and *C* correction for not having those terms in the original expansion. What's worse is these terms require three more |ab initio| calculations to construct this deleterious correction.

    