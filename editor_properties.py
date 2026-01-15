import bpy

def register():
    bpy.types.Scene.target_collection = bpy.props.PointerProperty(
        name="Target Collection",
        description="Collection that contains the location data to export",
        type=bpy.types.Collection,
    )

    bpy.types.Scene.decimation_ratio = bpy.props.FloatProperty(
        name="Decimation Ratio",
        description="Ratio of vertices to keep (1.0 = all vertices, 0.0 = maximum decimation)",
        default=1.0,
        min=0.0,
        max=1.0,
        step=1,
        precision=2
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

    bpy.types.Scene.keep_decimated_collection = bpy.props.BoolProperty(
        name="Keep Decimated Collection",
        description="Keep the decimated collection visible after export (if unchecked, it will be deleted)",
        default=False
    )

def unregister():
    del bpy.types.Scene.target_collection
    del bpy.types.Scene.decimation_ratio
    del bpy.types.Scene.data_format
    del bpy.types.Scene.save_filepath
    del bpy.types.Scene.save_filename
    del bpy.types.Scene.keep_decimated_collection
