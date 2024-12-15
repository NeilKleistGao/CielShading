# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
  "name": "Cielshading",
  "author": "Fa1sePRoMiSe",
  "description": "",
  "blender": (2, 80, 0),
  "version": (0, 0, 1),
  "location": "",
  "warning": "",
  "category": "Render",
}

import bpy
from . import CielPanel
from . import CelShading


def register():
  bpy.types.Scene.color_texture_output = bpy.props.StringProperty \
    (name = "Color Texture Output", description="Directory storing color textures", default="")
  bpy.types.Scene.normal_map_output = bpy.props.StringProperty \
    (name = "Normal Map Output", description="Directory storing normal maps", default="")
  bpy.utils.register_class(CelShading.CelShadingOperator)
  bpy.utils.register_class(CielPanel.CielPanel)
  
  print("CielShading registered.")

def unregister():
  bpy.utils.unregister_class(CelShading.CelShadingOperator)
  bpy.utils.unregister_class(CielPanel.CielPanel)
  del bpy.types.Scene.normal_map_output
  del bpy.types.Scene.color_texture_output
