"""
raeon Blender builder v0.3

Usage inside Blender:
    blender --background --python build_manifold.py -- /path/to/render_spec.json /path/to/output.glb

This script builds:
- anchor emissive spheres,
- Bezier curves with bevel geometry,
- optional soft field shell placeholder,
- materials keyed by semantic field color,
- GLB export.

Final runtime animation belongs in Metal; Blender is the visual authoring/mesh bake stage.
"""
import json, math, sys
from pathlib import Path

try:
    import bpy
    from mathutils import Vector
except ImportError:
    raise RuntimeError("Run this script inside Blender's Python environment.")

def args_after_double_dash():
    if "--" not in sys.argv:
        return []
    return sys.argv[sys.argv.index("--")+1:]

def clear_scene():
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)

def make_material(name, emission_strength=6.0):
    m=bpy.data.materials.new(name)
    m.use_nodes=True
    nodes=m.node_tree.nodes
    links=m.node_tree.links
    for n in list(nodes):
        nodes.remove(n)
    out=nodes.new("ShaderNodeOutputMaterial")
    em=nodes.new("ShaderNodeEmission")
    # Semantic yellow/gold baseline; production palette should be renderer-owned.
    em.inputs["Color"].default_value=(1.0,0.55,0.03,1.0)
    em.inputs["Strength"].default_value=emission_strength
    links.new(em.outputs["Emission"],out.inputs["Surface"])
    return m

def add_anchor(location, radius, material):
    bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=2,radius=radius,location=location)
    obj=bpy.context.object
    obj.data.materials.append(material)
    return obj

def add_bezier(edge, material):
    curve=bpy.data.curves.new(f"edge_{edge['edge_id']}",type='CURVE')
    curve.dimensions='3D'
    curve.resolution_u=16
    curve.bevel_depth=edge["tube_radius"]
    curve.bevel_resolution=5
    spline=curve.splines.new('BEZIER')
    spline.bezier_points.add(1)
    a=spline.bezier_points[0]
    b=spline.bezier_points[1]
    a.co=edge["p0"]; b.co=edge["p3"]
    a.handle_right=edge["p1"]; b.handle_left=edge["p2"]
    a.handle_left_type='FREE'; a.handle_right_type='FREE'
    b.handle_left_type='FREE'; b.handle_right_type='FREE'
    obj=bpy.data.objects.new(f"edge_{edge['edge_id']}",curve)
    bpy.context.collection.objects.link(obj)
    obj.data.materials.append(material)
    return obj

def build(spec):
    clear_scene()
    mat=make_material("raeon_field",spec["animation"]["emission_power"])
    for a in spec["anchors"]:
        add_anchor(a["position"],0.08,mat)
    for e in spec["spline_edges"]:
        add_bezier(e,mat)

    # Optional subtle central node for visual coherence, not topology.
    add_anchor((0,0,0),0.05,mat)

def main():
    args=args_after_double_dash()
    if len(args)<2:
        raise SystemExit("Need render_spec.json and output.glb")
    spec=json.loads(Path(args[0]).read_text())
    build(spec)
    bpy.ops.export_scene.gltf(filepath=args[1],export_format='GLB')

if __name__=="__main__":
    main()
