import bpy
import numpy as np

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
        print(f"Decimation ratio: {scene.decimation_ratio}\n")

        # Create duplicate collection with decimation if needed
        decimation_ratio = scene.decimation_ratio
        decimated_collection = None
        export_collection = target_collection
        
        if decimation_ratio < 1.0:
            decimated_collection = duplicate_collection_with_decimate(target_collection, decimation_ratio)
            export_collection = decimated_collection
            print(f"Created decimated collection: '{decimated_collection.name}'")
        
        try:
            objects_data = export_vertices_location(export_collection, start_frame, end_frame, scene)
            
            if scene.data_format == 'JSON':
                objects_data.saveToFile(bpy.path.abspath(scene.save_filepath), scene.save_filename, False)
            elif scene.data_format == 'BINARY':
                objects_data.saveToFile(bpy.path.abspath(scene.save_filepath), scene.save_filename, True)
        finally:
            # Clean up decimated collection if user doesn't want to keep it
            if decimated_collection and not scene.keep_decimated_collection:
                delete_collection(decimated_collection)

        return {'FINISHED'}

def delete_collection(collection):
    """Delete a collection and all its objects"""
    # Remove all objects from the collection
    for obj in collection.objects:
        bpy.data.objects.remove(obj, do_unlink=True)
    
    # Remove the collection itself
    bpy.data.collections.remove(collection)

def duplicate_collection_with_decimate(target_collection, ratio):
    """Create a duplicate collection and apply decimate modifier to all mesh objects"""
    # Create new collection
    new_collection_name = f"{target_collection.name}_Decimated"
    new_collection = bpy.data.collections.new(new_collection_name)
    bpy.context.scene.collection.children.link(new_collection)
    
    # Duplicate objects and link to new collection
    for obj in target_collection.objects:
        if obj.type == 'MESH':
            # Duplicate the object and its data
            new_obj = obj.copy()
            new_obj.data = obj.data.copy()
            
            # Link to new collection
            new_collection.objects.link(new_obj)
            
            # Add and apply decimate modifier
            decimate_mod = new_obj.modifiers.new(name="Decimate", type='DECIMATE')
            decimate_mod.ratio = ratio
            decimate_mod.decimate_type = 'COLLAPSE'
            
            # Apply the modifier
            bpy.context.view_layer.objects.active = new_obj
            with bpy.context.temp_override(object=new_obj):
                bpy.ops.object.modifier_apply(modifier=decimate_mod.name)
    
    return new_collection

def export_vertices_location(target_collection, start_frame, end_frame, scene):
    objects_data = object.Objects()
    objects_data.fps = scene.render.fps
    objects = [[object.Object() for v in obj.data.vertices] for obj in target_collection.objects if obj.type == 'MESH']

    # Precompute vertex colors
    vertex_colors = compute_color_cache(target_collection)

    # Frame-by-frame processing
    for frame in range(start_frame, end_frame + 1):
        scene.frame_set(frame)
        
        # Process each object in the collection
        for i, obj in enumerate([o for o in target_collection.objects if o.type == 'MESH']):
            matrix = obj.matrix_world
    
            # Process each vertex of the object
            for j,v in enumerate(obj.data.vertices):
                world_co = matrix @ v.co
                color = vertex_colors[i][j]

                keyframe = object.KeyFrame(frame = frame,
                                           position = object.Vector3(world_co[0], world_co[1], world_co[2]),
                                           color = object.Vector3(color[0], color[1], color[2]))
                objects[i][j].addKeyFrame(keyframe)

    [[objects_data.addObject(vert) for vert in objdat] for objdat in objects]

    scene.frame_set(start_frame)
    return objects_data

def compute_color_cache(target_collection):
    vertex_colors_cache = []
    
    for obj in target_collection.objects:
        if obj.type != 'MESH':
            continue
            
        mesh = obj.data
        num_verts = len(mesh.vertices)
        
        # By default, white color
        colors = np.ones((num_verts, 4), dtype=np.float32)
        
        # Find image texture if exists
        image = None
        if obj.material_slots and obj.material_slots[0].material:
            mat = obj.material_slots[0].material
            if mat.use_nodes:
                for node in mat.node_tree.nodes:
                    if node.type == 'TEX_IMAGE' and node.image:
                        image = node.image
                        break
        
        if image and mesh.uv_layers:
            width, height = image.size
            
            # Read all pixel data
            num_pixels = width * height * 4
            pixel_data = np.empty(num_pixels, dtype=np.float32)
            image.pixels.foreach_get(pixel_data)

            # Reshape to 2D array for easier indexing
            pixel_data = pixel_data.reshape((height, width, 4))
            
            # Get all UVs and corresponding vertex indices
            uv_layer = mesh.uv_layers.active.data
            num_loops = len(mesh.loops)
            loop_uvs = np.empty(num_loops * 2, dtype=np.float32)
            loop_vert_indices = np.empty(num_loops, dtype=np.int32)
            uv_layer.foreach_get("uv", loop_uvs)
            mesh.loops.foreach_get("vertex_index", loop_vert_indices)

            # Reshape UVs to Nx2 array
            loop_uvs = loop_uvs.reshape((-1, 2))
            
            # Find unique vertex indices and their first occurrence
            _, unique_indices = np.unique(loop_vert_indices, return_index=True)
            
            # Get UVs corresponding to unique vertex indices
            u_verts = loop_vert_indices[unique_indices]
            u_uvs = loop_uvs[unique_indices]
            
            # Fill a temporary array of UVs aligned with vertices
            vert_uvs = np.zeros((num_verts, 2), dtype=np.float32)
            vert_uvs[u_verts] = u_uvs
            
            # Map UVs to pixel coordinates
            u = vert_uvs[:, 0] % 1.0
            v = vert_uvs[:, 1] % 1.0
            
            x = (u * width).astype(np.int32)
            y = (v * height).astype(np.int32)
            
            # Clamp to valid pixel indices
            np.clip(x, 0, width - 1, out=x)
            np.clip(y, 0, height - 1, out=y)
            
            # Fetch colors for each vertex
            colors = pixel_data[y, x]
            
        # Append RGB colors (ignore alpha for now)
        vertex_colors_cache.append(colors[:, :3].tolist())

    return vertex_colors_cache

def register():
    bpy.utils.register_class(DisplayData)

def unregister():
    bpy.utils.unregister_class(DisplayData)
