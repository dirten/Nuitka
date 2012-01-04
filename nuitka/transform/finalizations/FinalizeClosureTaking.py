#
#     Copyright 2012, Kay Hayen, mailto:kayhayen@gmx.de
#
#     Part of "Nuitka", an optimizing Python compiler that is compatible and
#     integrates with CPython, but also works on its own.
#
#     If you submit Kay Hayen patches to this software in either form, you
#     automatically grant him a copyright assignment to the code, or in the
#     alternative a BSD license to the code, should your jurisdiction prevent
#     this. Obviously it won't affect code that comes to him indirectly or
#     code you don't submit to him.
#
#     This is to reserve my ability to re-license the code at a later time to
#     the PSF. With this version of Nuitka, using it for a Closed Source and
#     distributing the binary only is not allowed.
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, version 3 of the License.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#     Please leave the whole of this copyright notice intact.
#
""" Finalize the closure.

If a taker wants a variable, make sure that the closure taker in between all do forward it
for this use or else it will not be available. We do this late so it is easier to remove
closure variables and keep track of references, by not having it spoiled with these
transitive only references.

"""

from .FinalizeBase import FinalizationVisitorScopedBase

class FinalizeClosureTaking( FinalizationVisitorScopedBase ):
    def __call__( self, node ):
        assert node.isClosureVariableTaker(), node

        # print node, node.provider

        for variable in node.getClosureVariables():
            referenced = variable.getReferenced()
            referenced_owner = referenced.getOwner()

            assert not referenced.isModuleVariable()

            current = node.getParent()

            # print referenced

            while current is not referenced_owner:
                if current.isClosureVariableTaker():
                    for current_variable in current.getClosureVariables():
                        if current_variable.getReferenced() is referenced:
                            break
                    else:
                        # print "ADD", current, referenced
                        current.addClosureVariable( referenced )


                current = current.getParent()
