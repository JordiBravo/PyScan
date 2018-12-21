import bpy
import os

C = bpy.context
D = bpy.data

script_path = os.path.dirname(os.path.abspath(__file__))

# User input
save_name = input('Mesh name: ')
save_path = script_path + '\\output\\' + save_name

# Rename mesh
m = D.objects['Mesh']
m.name = save_name
m.data.name = save_name

# Remove material
m.active_material_index = 0
for i in range(len(m.material_slots)):
    bpy.ops.object.material_slot_remove({'object': m})

# Select mesh only
bpy.ops.object.select_all(action='DESELECT')
m.select_set(True)


# EXPORTS
#################################################################
# FBX
bpy.ops.export_scene.fbx(
    filepath = save_path + '.fbx',
    use_selection = True,
    object_types = set(['MESH']),
    mesh_smooth_type = 'EDGE',
    bake_anim = False,
    use_mesh_modifiers = False
)

# OBJ
bpy.ops.export_scene.obj(
    filepath = save_path + '.obj',
    use_selection = True,
    check_existing = False,
    use_materials = False,
    use_animation = False,
    use_mesh_modifiers = False
)

# DAE
bpy.ops.wm.collada_export(
    filepath = save_path + '.dae',
    selected = True,
    apply_modifiers = False,
    triangulate = False
)
