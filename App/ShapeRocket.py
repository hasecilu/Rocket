# ***************************************************************************
# *   Copyright (c) 2021 David Carter <dcarter@davidcarter.ca>              *
# *                                                                         *
# *   This program is free software; you can redistribute it and/or modify  *
# *   it under the terms of the GNU Lesser General Public License (LGPL)    *
# *   as published by the Free Software Foundation; either version 2 of     *
# *   the License, or (at your option) any later version.                   *
# *   for detail see the LICENCE text file.                                 *
# *                                                                         *
# *   This program is distributed in the hope that it will be useful,       *
# *   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
# *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
# *   GNU Library General Public License for more details.                  *
# *                                                                         *
# *   You should have received a copy of the GNU Library General Public     *
# *   License along with this program; if not, write to the Free Software   *
# *   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  *
# *   USA                                                                   *
# *                                                                         *
# ***************************************************************************
"""Class for rocket assemblies"""

__title__ = "FreeCAD Rocket Assembly"
__author__ = "David Carter"
__url__ = "https://www.davesrocketshop.com"

import FreeCAD

from PySide import QtCore

from App.ShapeBase import ShapeBase
from App.Constants import FEATURE_ROCKET, FEATURE_STAGE

class ShapeRocket(ShapeBase):

    def __init__(self, obj):
        super().__init__(obj)
        self.Type = FEATURE_ROCKET
        
        if not hasattr(obj,"Group"):
            obj.addExtension("App::GroupExtensionPython")

    def execute(self,obj):
        if not hasattr(obj,'Shape'):
            return

    def eligibleChild(self, childType):
        return childType == FEATURE_STAGE

    def positionChildren(self):
        # print("Rocket::positionChildren()")
        # Dynamic placements
        length = 0.0
        i = len(self._obj.Group) - 1
        while i >= 0:
            child = self._obj.Group[i]
            # print(child.Label)
            child.Proxy.setAxialPosition(length)

            length += float(child.Proxy.getAxialLength())
            # print("length = %f" % length)
            i -= 1

        FreeCAD.ActiveDocument.recompute()

def hookChildren(obj, group, oldGroup):
    for child in group:
        if child not in oldGroup:
            child.Proxy.resetPlacement()
            # child.Proxy.edited.connect(obj.Proxy.positionChildren, QtCore.Qt.QueuedConnection)
            child.Proxy.connect(obj.Proxy.positionChildren, QtCore.Qt.QueuedConnection)

    for child in oldGroup:
        if child not in group:
            try:
                # child.Proxy.edited.connect(None)
                child.Proxy.disconnect()
            except ReferenceError:
                pass # object may be deleted

    obj.Proxy.positionChildren()
