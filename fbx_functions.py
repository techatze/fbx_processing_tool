import fbx
import os

def load_fbx(file_path):
    manager = fbx.FbxManager.Create()

    ios = fbx.FbxIOSettings.Create(manager, fbx.IOSROOT)
    manager.SetIOSettings(ios)

    importer = fbx.FbxImporter.Create(manager, "")

    if not importer.Initialize(file_path, -1, manager.GetIOSettings()):
        error = importer.GetStatus().GetErrorString()
        raise Exception(f"Import failed: {error}")

    scene = fbx.FbxScene.Create(manager, "scene")

    importer.Import(scene)
    importer.Destroy()

    return manager, scene



def traverse_scene(scene):
    result = []

    def traverse(node, depth=0):
        if not node:
            return

        name = node.GetName()
        attr = node.GetNodeAttribute()

        attr_type = "None"

        if attr:
            attr_type = attr.GetAttributeType()

        result.append(f"{'  '*depth}- {name} (type: {attr_type})")

        for i in range(node.GetChildCount()):
            traverse(node.GetChild(i), depth + 1)

    root = scene.GetRootNode()
    traverse(root)

    return result



def get_mesh_nodes(scene):
    mesh_nodes = []

    def traverse(node):
        if not node:
            return

        attr = node.GetNodeAttribute()

        if attr:
            try:
                is_mesh = attr.GetAttributeType() == fbx.FbxNodeAttribute.EType.eMesh
            except:
                is_mesh = attr.GetAttributeType() == 2

            if is_mesh:
                mesh_nodes.append(node)


        for i in range(node.GetChildCount()):
            traverse(node.GetChild(i))

    root = scene.GetRootNode()
    traverse(root)

    return mesh_nodes



def export_single_mesh(manager,mesh_node,output_path):
    new_scene = fbx.FbxScene.Create(manager,"new_scene")

    mesh_clone = mesh_node.Clone()

    new_scene.GetRootNode().AddChild(mesh_clone)

    exporter = fbx.FbxExporter.Create(manager, "")

    if not exporter.Initialize(output_path, -1, manager.GetIOSettings()):
        raise Exception("Export failed")

    exporter.Export(new_scene)
    exporter.Destroy()



def make_output_name(input_path,mesh_node,index):
    base_name = os.path.splitext(os.path.basename(input_path))[0]

    node_name = mesh_node.GetName()
    safe_name = node_name.replace(" ", "_")

    return f"{base_name}_{index}_{safe_name}.fbx"



def convert_axis(scene,axis_option):
    if axis_option == "Maya (Y-Up)":
        axis = fbx.FbxAxisSystem.MayaYUp

    elif axis_option == "OpenGL (Z-Up)":
        axis = fbx.FbxAxisSystem.OpenGL

    elif axis_option == "DirectX":
        axis = fbx.FbxAxisSystem.DirectX

    else:
        return

    axis.ConvertScene(scene)



