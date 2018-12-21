import bpy
import os
# import datetime

C = bpy.context
D = bpy.data


# SETTINGS
#################################################################
script_path = os.path.dirname(os.path.abspath(__file__))
mesh_path = script_path + '\\input\mesh.fbx'
tex_path = script_path + '\\input\mesh_u1_v1.png'
# now = datetime.datetime.now().time()
# now = str(now.hour).zfill(2) + str(now.minute).zfill(2) + str(now.second).zfill(2)
output_path = script_path + '\\output\output.blend'
mat_name = 'Material'


# MODEL PREP
#################################################################
# Import mesh
bpy.ops.import_scene.fbx(filepath=mesh_path)
m = C.selected_objects[0]
C.view_layer.objects.active = m

# Name
m.name = 'Mesh'
m.data.name = 'Mesh'
# Smoothing
bpy.ops.object.shade_smooth()
m.data.use_auto_smooth = False
# Clear split normals
bpy.ops.mesh.customdata_custom_splitnormals_clear()


# MATERIAL
#################################################################
# Assign or append material
mat = D.materials.get(mat_name)
if m.data.materials:
    m.data.materials[0] = mat
else:
    m.data.materials.append(mat)

# Assign Base Color texture
nodes = mat.node_tree.nodes
img_node = nodes.get('Image')

print(script_path)
img = D.images.load(tex_path)
img_node.image = img


# SAVE
#################################################################
bpy.ops.wm.save_mainfile(filepath=output_path)
