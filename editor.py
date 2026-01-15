import bpy

class DroneShowExportPanel(bpy.types.Panel):
    bl_label = "Drone Show Export"
    bl_idname = "VIEW3D_PT_drone_export"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Drone Show"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        layout.prop(scene, "target_collection")
        layout.prop(scene, "decimation_ratio")
        layout.prop(scene, "keep_decimated_collection")
        layout.prop(scene, "data_format")
        layout.prop(scene, "save_filepath")
        layout.prop(scene, "save_filename")
        layout.operator("mesh.display_data", text="Export Data")

def register():
    bpy.utils.register_class(DroneShowExportPanel)

def unregister():
    bpy.utils.unregister_class(DroneShowExportPanel)
