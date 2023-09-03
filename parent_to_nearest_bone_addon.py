# Blender add-on information
bl_info = {
  "name": "Parent to Nearest Bone",
  "category": "Object",
  "author": "ChatGPT with A LOOOOOOOOOOOOOT of help from Redrat",
  "location": "Press F3 > type 'Parent to Nearest Bone' > press 'Enter'",
  "description": "This addon allows you to parent objects to the nearest bone, similar to parenting with automatic weights. To use it, select the objects you want to parent and the armature you want to parent them to (the armature must be active), then press F3 > type 'Parent to Nearest Bone' > press 'Enter'.",
  "version": (1, 0),
  "blender": (2, 80, 0),
  "warning": "May not be totally stable :(.",
  "doc_url": "",
}

import bpy
from mathutils import Vector

# Function to parent an object to the nearest bone in an armature
def parent_to_nearest_bone(obj, armature):
  # Check if valid object and armature are provided
  if not obj or not armature:
    print("Error: Please provide a valid object and armature.")
    return

  # Check if the provided object is a mesh
  if obj.type != 'MESH':
    print("Error: The provided object is not a mesh.")
    return

  # Check if the provided armature is an armature
  if armature.type != 'ARMATURE':
    print("Error: The provided armature is not an armature.")
    return

  # Get the location of the object
  obj_location = obj.location
  nearest_bone = None
  min_distance = float('inf')

  # Find the nearest bone in the armature
  for bone in armature.pose.bones:
    loc1 = armature.matrix_world @ bone.head
    loc2 = armature.matrix_world @ bone.tail
    distance = max((obj_location - loc2).length, (obj_location - loc1).length)

    if distance < min_distance:
      min_distance = distance
      nearest_bone = bone

  if nearest_bone:
    # Unselect all objects and then select the object and armature
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    armature.select_set(True)
    bpy.context.view_layer.objects.active = armature

    # Select the nearest bone
    armature.data.bones.active = nearest_bone.bone

    # Parent the object to the nearest bone
    bpy.ops.object.parent_set(type='BONE', keep_transform=False)

  else:
    print("Error: No bones found in the armature.")

# Define an operator class to execute the parenting operation
class OBJECT_OT_ParentToNearestBone(bpy.types.Operator):
  bl_idname = "object.parent_to_nearest_bone"
  bl_label = "Parent to Nearest Bone"
  bl_description = "Parent selected objects to the nearest bone in the active armature"

  def execute(self, context):
    # Get the selected objects and the active armature
    selected_objects = bpy.context.selected_objects
    active_armature = bpy.context.active_object

    # Check if valid selections are made
    if not selected_objects or not active_armature or active_armature.type != 'ARMATURE':
      self.report({'ERROR'}, "Please select objects and an armature.")
      return {'CANCELLED'}

    # Loop through selected objects and parent them to the nearest bone
    for obj in selected_objects:
      parent_to_nearest_bone(obj, active_armature)

    return {'FINISHED'}

# Define a function to add the operator to the Blender UI
def menu_func(self, context):
  self.layout.operator(OBJECT_OT_ParentToNearestBone.bl_idname)

# Register the operator and add it to the Blender UI
def register():
  bpy.utils.register_class(OBJECT_OT_ParentToNearestBone)
  bpy.types.VIEW3D_MT_object.append(menu_func)

# Unregister the operator and remove it from the Blender UI
def unregister():
  bpy.utils.unregister_class(OBJECT_OT_ParentToNearestBone)
  bpy.types.VIEW3D_MT_object.remove(menu_func)

# Entry point to register the add-on
if __name__ == "__main__":
  register()
