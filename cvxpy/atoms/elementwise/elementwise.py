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

import abc
from cvxpy.atoms.atom import Atom

class Elementwise(Atom):
    """ Abstract base class for elementwise atoms. """
    __metaclass__ = abc.ABCMeta
    # The shape is the same as the argument's shape.
    def shape_from_args(self):
        return self.args[0].shape

    def validate_arguments(self):
        """
        Verify that all the shapes are the same
        or can be promoted.
        """
        shape = self.args[0].shape
        for arg in self.args[1:]:
            shape = shape + arg.shape