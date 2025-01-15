from enum import Enum
import bpy
import os
from . import Merge17

class RenderType(Enum):
  COLOR = 0
  NORMAL_MAP = 1


class CelShadingOperator(bpy.types.Operator):
  """Output color textures and normal maps"""
  bl_idname = "export.cel_shading"
  bl_label = "Cel Shading Rendering"
  bl_options = { "REGISTER", "UNDO" }

  base_output_dir = ""

  def render_once(self, path: str, render_type: RenderType, context: bpy.types.Context | None):
    path = os.path.join(self.base_output_dir, path)
    print("output: " + path)
    context.scene.render.filepath = path

    origin_engine = context.scene.render.engine
    origin_lighting = context.scene.display.shading.light
    origin_studio_light = context.scene.display.shading.studio_light
    origin_backface_culling = context.scene.display.shading.show_backface_culling
    origin_freestyle = context.scene.render.use_freestyle
    if render_type == RenderType.COLOR:
      context.scene.render.engine = "CYCLES" # TODO: config
      context.scene.display.shading.light = "STUDIO"
    else:
      context.scene.render.engine = "BLENDER_WORKBENCH"
      context.scene.display.shading.light = "MATCAP"
      context.scene.display.shading.studio_light = "check_normal+y.exr"
      context.scene.display.shading.color_type = "OBJECT"
      context.scene.display.shading.show_backface_culling = True
      context.scene.render.use_freestyle = False

    context.scene.render.film_transparent = True
    context.scene.render.image_settings.file_format = "PNG"
    bpy.ops.render.render(animation=True)
    Merge17.merge(path, "../res.png", context.scene.render.resolution_x, context.scene.render.resolution_y, context.scene.atlas_row_num) # TODO: config

    context.scene.render.use_freestyle = origin_freestyle
    context.scene.display.shading.show_backface_culling = origin_backface_culling
    context.scene.render.filepath = self.base_output_dir
    context.scene.render.engine = origin_engine
    context.scene.display.shading.light = origin_lighting
    context.scene.display.shading.studio_light = origin_studio_light

  def execute(self, context: bpy.types.Context | None):
    self.base_output_dir = context.scene.render.filepath
    self.render_once(context.scene.color_texture_output, RenderType.COLOR, context)
    if context.scene.normal_map_output != "":
      self.render_once(context.scene.normal_map_output, RenderType.NORMAL_MAP, context)
    return { "FINISHED" }
