from enum import Enum
import bpy

class RenderType(Enum):
  COLOR = 0
  NORMAL_MAP = 1


class CelShadingOperator(bpy.types.Operator):
  """Output color textures and normal maps"""
  bl_idname = "export.cel_shading"
  bl_label = "Cel Shading Rendering"
  bl_options = { "REGISTER", "UNDO" }

  def execute(self, context):
    print("TODO")
    return { "FINISHED" }
