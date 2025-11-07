from . import editor, editor_properties, exporter

def register():
    editor_properties.register()
    exporter.register()
    editor.register()

def unregister():
    editor_properties.unregister()
    exporter.unregister()
    editor.unregister()

if __name__ == "__main__":
    register()