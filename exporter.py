import bpy

from . import object

class DisplayData(bpy.types.Operator):
    bl_idname = "mesh.display_data"
    bl_label = "Export Data"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):
        scene = context.scene
        target_collection = scene.target_collection

        if not target_collection:
            self.report({'ERROR'}, "Please choose a collection first")
            return {'CANCELLED'}

        start_frame = scene.frame_start
        end_frame = scene.frame_end

        print(f"--- Exporting frame-by-frame data for collection '{target_collection.name}' ---")
        print(f"Frame range: {start_frame} → {end_frame}")
        print(f"Export mode selected '{scene.export_mode}'\n")

        if scene.export_mode == 'OBJECT_LOCATION':
            objects_data = export_object_location(target_collection, start_frame, end_frame, scene)
        elif scene.export_mode == 'VERTICES_LOCATION':
            objects_data = export_vertices_location(target_collection, start_frame, end_frame, scene)
        
        if scene.data_format == 'JSON':
            objects_data.saveToFile(bpy.path.abspath(scene.save_filepath), scene.save_filename, False)
        elif scene.data_format == 'BINARY':
            objects_data.saveToFile(bpy.path.abspath(scene.save_filepath), scene.save_filename, True)

        return {'FINISHED'}

def export_object_location(target_collection, start_frame, end_frame, scene):
    objects_data = object.Objects()
    objects_data.fps = scene.render.fps

    for obj in target_collection.objects:
            object_data = object.Object()

            for frame in range(start_frame, end_frame + 1):
                scene.frame_set(frame)  # Update the scene to this frame
                pos = obj.location

                keyframe = object.KeyFrame(frame=frame)
                keyframe.position = object.Vector3(pos.x, pos.y, pos.z)
                keyframe.color = object.Vector3(1.0, 1.0, 1.0)  # White by default
                object_data.addKeyFrame(keyframe)

            objects_data.addObject(object_data)

    scene.frame_set(start_frame) # Reset to starting frame
    return objects_data

def export_vertices_location(target_collection, start_frame, end_frame, scene):
    objects_data = object.Objects()
    objects_data.fps = scene.render.fps

    for obj in target_collection.objects:
            for v in obj.data.vertices:
                object_data = object.Object()

                for frame in range(start_frame, end_frame + 1):
                    scene.frame_set(frame)  # Update the scene to this frame
                    co = obj.matrix_world @ v.co  # World coordinates of vertex

                    keyframe = object.KeyFrame(frame=frame)
                    keyframe.position = object.Vector3(co.x, co.y, co.z)
                    keyframe.color = object.Vector3(1.0, 1.0, 1.0)  # White by default
                    object_data.addKeyFrame(keyframe)
            
                objects_data.addObject(object_data)

    scene.frame_set(start_frame) # Reset to starting frame
    return objects_data


def register():
    bpy.utils.register_class(DisplayData)

def unregister():
    bpy.utils.unregister_class(DisplayData)
