"""
Copyright 2013 Steven Diamond

This file is part of CVXPY.

CVXPY is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

CVXPY is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with CVXPY.  If not, see <http://www.gnu.org/licenses/>.
"""

import cvxpy.utilities as u
import cvxpy.lin_ops.lin_utils as lu
from cvxpy.atoms.atom import Atom
from cvxpy.atoms.affine.index import index
from cvxpy.atoms.affine.transpose import transpose
from cvxpy.constraints.semi_definite import SDP
import scipy.sparse as sp
from numpy import linalg as LA

class lambda_max(Atom):
    """ Maximum eigenvalue; :math:`\lambda_{\max}(A)`.

    """
    def __init__(self, A):
        super(lambda_max, self).__init__(A)

    # Returns the smallest eigenvalue of A.
    # Requires that A be symmetric.
    @Atom.numpy_numeric
    def numeric(self, values):
        if not (values[0].T == values[0]).all():
            raise Exception("lambda_max called on a non-symmetric matrix.")
        w, v = LA.eig(values[0])
        return max(w)

    # Resolves to a scalar.
    def shape_from_args(self):
        return u.Shape(1,1)

    # Verify that the argument A is square.
    def validate_arguments(self):
        if not self.args[0].size[0] == self.args[0].size[1]:
            raise TypeError("The argument '%s' to lambda_max must resolve to a square matrix."
                % self.args[0].name())

    # Always unknown.
    def sign_from_args(self):
        return u.Sign.UNKNOWN

    # Default curvature.
    def func_curvature(self):
        return u.Curvature.CONVEX

    def monotonicity(self):
        return [u.monotonicity.NONMONOTONIC]

    @staticmethod
    def graph_implementation(arg_objs, size, data=None):
        """Reduces the atom to an affine expression and list of constraints.

        Parameters
        ----------
        arg_objs : list
            LinExpr for each argument.
        size : tuple
            The size of the resulting expression.
        data :
            Additional data required by the atom.

        Returns
        -------
        tuple
            (LinOp for objective, list of constraints)
        """
        A = arg_objs[0]
        n, _ = A.size
        # Requires that A is symmetric.
        # A == A.T
        obj, constraints = transpose.graph_implementation([A], (n, n))
        constraints.append(lu.create_eq(A, obj))
        # SDP constraint.
        t = lu.create_var((1, 1))
        I = lu.create_const(sp.eye(n, n), (n, n))
        # I*t - A
        expr = lu.sub_expr(lu.mul_expr(I, t, (n, n)), A)
        return (t, [SDP(expr)] + constraints)
