from enum import Enum
import bpy
import os
from . import Merge17, AnimationData

class RenderType(Enum):
  COLOR = 0
  NORMAL_MAP = 1


class CelShadingOperator(bpy.types.Operator):
  """Output color textures and normal maps"""
  bl_idname = "export.cel_shading"
  bl_label = "Cel Shading Rendering"
  bl_options = { "REGISTER", "UNDO" }

  base_output_dir = ""

  def render_once(self, path: str, prefix: str, render_type: RenderType, context: bpy.types.Context | None):
    path = os.path.join(self.base_output_dir, path)
    print("output: " + path)
    context.scene.render.filepath = path

    origin_engine = context.scene.render.engine
    origin_lighting = context.scene.display.shading.light
    origin_studio_light = context.scene.display.shading.studio_light
    origin_backface_culling = context.scene.display.shading.show_backface_culling
    origin_freestyle = context.scene.render.use_freestyle
    if render_type == RenderType.COLOR:
      context.scene.render.engine = "BLENDER_EEVEE_NEXT"
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
    output_name = "../" + prefix + ".png" if render_type == RenderType.COLOR else "../" + prefix + "Normal.png"
    Merge17.merge(path, output_name, context.scene.render.resolution_x, context.scene.render.resolution_y, context.scene.atlas_row_num)

    context.scene.render.use_freestyle = origin_freestyle
    context.scene.display.shading.show_backface_culling = origin_backface_culling
    context.scene.render.filepath = self.base_output_dir
    context.scene.render.engine = origin_engine
    context.scene.display.shading.light = origin_lighting
    context.scene.display.shading.studio_light = origin_studio_light

  def execute(self, context: bpy.types.Context | None):
    armature = bpy.data.armatures.get(context.scene.armature_name) if len(context.scene.armature_name) > 0 else None
    self.base_output_dir = context.scene.render.filepath
    if len(context.scene.config_file) > 0:
      fp = open(os.path.join(self.base_output_dir, context.scene.config_file), "r")
      content = fp.read()
      fp.close()
      data, content = AnimationData.parse_animation_data(content.strip())
      while data.isDefined():
        print("Generating " + data.name)
        context.scene.frame_start = data.begin
        context.scene.frame_end = data.end
        context.scene.frame_step = data.step

        if armature is not None:
          if armature.animation_data is None:
            armature.animation_data_create()
          print("Update action")
          armature.animation_data.action = bpy.data.actions.get(data.action)

        self.render_once(os.path.join(context.scene.color_texture_output, data.name + "/"), data.name, RenderType.COLOR, context)
        if context.scene.normal_map_output != "":
          self.render_once(os.path.join(context.scene.normal_map_output, data.name + "/"), data.name, RenderType.NORMAL_MAP, context)
        if len(content) == 0:
          break
        data, content = AnimationData.parse_animation_data(content.strip())
    else:
      self.render_once(context.scene.color_texture_output, context.scene.output_prefix, RenderType.COLOR, context)
      if context.scene.normal_map_output != "":
        self.render_once(context.scene.normal_map_output, context.scene.output_prefix, RenderType.NORMAL_MAP, context)
    return { "FINISHED" }
  