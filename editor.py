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

        # ASCII Signature Header
        box = layout.box()
        col = box.column(align=True)
        col.scale_y = 0.6
        col.label(text="  [---]                             [---]        >>          MADE BY          <<")
        col.label(text="       \\      DroneShow         /             >>    Thibault Clodion   <<")
        col.label(text="        \\____________________/              >> Pablo Couprie-Diaz <<")
        col.label(text="        /                                  \\              >>         Peizhe Liu         <<")
        col.label(text="       /       MFSM2024         \\            >>  Jounaïd Boudefar   <<")
        col.label(text="  [---]                              [---]       >>      Iwan Derouet      <<")
        
        layout.separator()
        
        # Collection Selection Section
        box = layout.box()
        box.label(text="Collection Settings", icon='OUTLINER_COLLECTION')
        box.prop(scene, "target_collection")
        
        layout.separator()
        
        # Decimation Section
        box = layout.box()
        box.label(text="Decimation Settings", icon='MOD_DECIM')
        box.prop(scene, "decimation_ratio")
        
        # Info about decimation
        info_box = box.box()
        info_box.scale_y = 0.7
        col = info_box.column(align=True)
        col.label(text="Decimation reduces the number of vertices", icon='INFO')
        col.label(text="1.0 = Keep all vertices (no decimation)")
        col.label(text="0.5 = Keep 50% of vertices")
        col.label(text="Lower values = Smaller file size")
        
        box.prop(scene, "keep_decimated_collection")
        
        layout.separator()
        
        # Export Format Section
        box = layout.box()
        box.label(text="Export Format", icon='EXPORT')
        box.prop(scene, "data_format")
        
        # Info about formats
        info_box = box.box()
        info_box.scale_y = 0.7
        col = info_box.column(align=True)
        col.label(text="Format Information:", icon='INFO')
        col.label(text="• Binary: Optimized for MFSM2024 system")
        col.label(text="• JSON: Human-readable format")
        
        layout.separator()
        
        # File Output Section
        box = layout.box()
        box.label(text="Output Settings", icon='FILE_FOLDER')
        box.prop(scene, "save_filepath")
        box.prop(scene, "save_filename")
        
        layout.separator()
        
        # Export Button
        row = layout.row()
        row.scale_y = 1.5
        row.operator("mesh.display_data", text="Export Data", icon='EXPORT')

def register():
    bpy.utils.register_class(DroneShowExportPanel)

def unregister():
    bpy.utils.unregister_class(DroneShowExportPanel)
