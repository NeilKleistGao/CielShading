import bpy

class CielPanel(bpy.types.Panel):
  """Creates a Panel in the Object properties window"""
  bl_label = "Ciel Shading"
  bl_idname = "OBJECT_PT_ciel"
  bl_space_type = "PROPERTIES"
  bl_region_type = "WINDOW"
  bl_context = "output"

  def draw(self, context):
    layout = self.layout
    if bpy.context.scene.camera == None:
      row = layout.row()
      row.label(text="Please add a camera first.", icon="ERROR")
    else:
      row = layout.row()
      row.prop(context.scene, "color_texture_output") # TODO: file dialog?
      row = layout.row()
      row.prop(context.scene, "normal_map_output") # TODO: file dialog?
      row = layout.row()
      row.prop(context.scene, "output_prefix")
      row = layout.row()
      row.prop(context.scene, "config_file") # TODO: file dialog?
      try:
        import PIL.Image
        row = layout.row()
        row.prop(context.scene, "atlas_row_num")
      except:
        row = layout.row()
        row.label(text="Cannot install PIL.", icon="ERROR")
      row = layout.row()
      row.operator("export.cel_shading")
