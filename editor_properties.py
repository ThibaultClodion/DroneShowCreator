import bpy

def register():
    bpy.types.Scene.target_collection = bpy.props.PointerProperty(
        name="Target Collection",
        description="Collection that contains the location data to export",
        type=bpy.types.Collection,
    )

    location_types = [
        ('OBJECT_LOCATION', "Object Location", "Export only the center location of object"),
        ('VERTICES_LOCATION', "Vertices Location", "Export all vertices locations")
    ]

    bpy.types.Scene.export_mode = bpy.props.EnumProperty(
        name="Export Mode",
        description="Choose what to export for the drones",
        items=location_types,
        default='OBJECT_LOCATION'
    )

    data_formats = [
        ('JSON', "JSON", "Export data in JSON format"),
        ('BINARY', "Binary", "Export data in Binary format")
    ]

    bpy.types.Scene.data_format = bpy.props.EnumProperty(
        name="Data Format",
        description="Choose the data format for the export",
        items=data_formats,
        default='JSON'
    )

    bpy.types.Scene.save_filepath = bpy.props.StringProperty(
        name="File Path",
        description="Where to save the export file",
        default="~/Downloads/",
        subtype='FILE_PATH'
    )

    bpy.types.Scene.save_filename = bpy.props.StringProperty(
        name="File Name",
        description="Name of the export file",
        default="file_name",
        subtype='FILE_NAME'
    )

def unregister():
    del bpy.types.Scene.target_collection
    del bpy.types.Scene.export_mode
    del bpy.types.Scene.data_format
    del bpy.types.Scene.save_filepath
    del bpy.types.Scene.save_filename
