import re
import math
import xml.etree.ElementTree as ET
from shapely.geometry import Polygon
from shapely.ops import triangulate, unary_union
from shapely import affinity  # for applying affine transforms
from svgpathtools import parse_path
import numpy as np

IDENTITY = (1, 0, 0, 1, 0, 0)

def tuple_to_matrix(T):
    a, b, d, e, xoff, yoff = T
    return np.array([[a, b, xoff],
                     [d, e, yoff],
                     [0, 0, 1]])

def matrix_to_tuple(M):
    return (M[0, 0], M[0, 1], M[1, 0], M[1, 1], M[0, 2], M[1, 2])

def compose_transforms(T1, T2):
    M1 = tuple_to_matrix(T1)
    M2 = tuple_to_matrix(T2)
    M = M1 @ M2
    return matrix_to_tuple(M)

def parse_float(value, default=0.0):
    try:
        return float(value)
    except (TypeError, ValueError):
        return default

def parse_transform(transform_str):
    if not transform_str:
        return IDENTITY
    M = np.eye(3)
    pattern = re.compile(r'(\w+)\s*\(([^)]+)\)')
    for cmd, params in pattern.findall(transform_str):
        params = list(map(parse_float, re.split(r'[ ,]+', params.strip())))
        if cmd == "matrix" and len(params) == 6:
            T = np.array([[params[0], params[2], params[4]],
                          [params[1], params[3], params[5]],
                          [0, 0, 1]])
        elif cmd == "translate":
            tx = params[0]
            ty = params[1] if len(params) > 1 else 0.0
            T = np.array([[1, 0, tx],
                          [0, 1, ty],
                          [0, 0, 1]])
        elif cmd == "scale":
            sx = params[0]
            sy = params[1] if len(params) > 1 else sx
            T = np.array([[sx, 0, 0],
                          [0, sy, 0],
                          [0, 0, 1]])
        elif cmd == "rotate":
            angle = math.radians(params[0])
            cos_a = math.cos(angle)
            sin_a = math.sin(angle)
            if len(params) > 2:
                cx, cy = params[1], params[2]
                T1 = np.array([[1, 0, -cx],
                               [0, 1, -cy],
                               [0, 0, 1]])
                R = np.array([[cos_a, -sin_a, 0],
                              [sin_a,  cos_a, 0],
                              [0,      0,     1]])
                T2 = np.array([[1, 0, cx],
                               [0, 1, cy],
                               [0, 0, 1]])
                T = T1 @ R @ T2
            else:
                T = np.array([[cos_a, -sin_a, 0],
                              [sin_a,  cos_a, 0],
                              [0,      0,     1]])
        else:
            T = np.eye(3)
        M = M @ T
    return matrix_to_tuple(M)

def parse_style(style_str):
    styles = {}
    for part in style_str.split(';'):
        if ':' in part:
            key, value = part.split(':', 1)
            styles[key.strip()] = value.strip()
    return styles

# --- Geometry Creation Functions ---
def create_rect(elem):
    x = parse_float(elem.get("x", "0"))
    y = parse_float(elem.get("y", "0"))
    width = parse_float(elem.get("width"))
    height = parse_float(elem.get("height"))
    return Polygon([(x, y), (x + width, y), (x + width, y + height), (x, y + height)])

def create_circle(elem, num_points=100):
    cx = parse_float(elem.get("cx"))
    cy = parse_float(elem.get("cy"))
    r = parse_float(elem.get("r"))
    angles = np.linspace(0, 2 * np.pi, num_points, endpoint=False)
    x = cx + r * np.cos(angles)
    y = cy + r * np.sin(angles)
    return Polygon(np.column_stack((x, y)))

def create_ellipse(elem, num_points=100):
    cx = parse_float(elem.get("cx"))
    cy = parse_float(elem.get("cy"))
    rx = parse_float(elem.get("rx"))
    ry = parse_float(elem.get("ry"))
    angles = np.linspace(0, 2 * np.pi, num_points, endpoint=False)
    x = cx + rx * np.cos(angles)
    y = cy + ry * np.sin(angles)
    return Polygon(np.column_stack((x, y)))

def create_polygon(elem):
    points_str = elem.get("points")
    points = []
    for pair in points_str.strip().split():
        coords = pair.split(',') if ',' in pair else pair.split()
        if len(coords) >= 2:
            points.append((float(coords[0]), float(coords[1])))
    return Polygon(points)

def create_polyline(elem):
    points_str = elem.get("points")
    points = []
    for pair in re.split(r'\s+', points_str.strip()):
        if not pair:
            continue
        coords = pair.split(',') if ',' in pair else pair.split()
        if len(coords) >= 2:
            points.append((float(coords[0]), float(coords[1])))
    if len(points) > 2 and (np.allclose(points[0], points[-1]) or math.hypot(points[0][0]-points[-1][0], points[0][1]-points[-1][1]) < 1e-2):
        points[-1] = points[0]
        return Polygon(points)
    else:
        return None

def create_line(elem):
    return None

def create_path(elem, num_points=100):
    """
    Create a Polygon from an SVG path element.
    For filled shapes, force closure by sampling points and connecting the last point to the first.
    """
    d = elem.get("d")
    path = parse_path(d)
    tol = 1e-6
    if not path.iscontinuous():
        return None
    t_values = np.linspace(0, 1, num_points + 1)
    points = [complex(path.point(t)) for t in t_values]
    if abs(points[0] - points[-1]) > tol:
        points[-1] = points[0]
    pts = [(pt.real, pt.imag) for pt in points]
    return Polygon(pts)

def extract_geometry(elem, current_transform=IDENTITY, inherited_fill=None):
    tag = elem.tag.split('}')[-1]
    style = elem.get("style")
    fill = None
    if style:
        style_dict = parse_style(style)
        fill = style_dict.get("fill")
    if fill is None:
        fill = elem.get("fill")
    if fill is None:
        fill = inherited_fill
    if fill is None or fill.lower() == "none":
        return None, None

    geometry = None
    if tag == "rect":
        geometry = create_rect(elem)
    elif tag == "circle":
        geometry = create_circle(elem)
    elif tag == "ellipse":
        geometry = create_ellipse(elem)
    elif tag == "polygon":
        geometry = create_polygon(elem)
    elif tag == "polyline":
        geometry = create_polyline(elem)
    elif tag == "line":
        geometry = create_line(elem)
    elif tag == "path":
        geometry = create_path(elem)
    if geometry is not None:
        geometry = affinity.affine_transform(geometry, current_transform)
    return geometry, fill

def collect_defs(root):
    defs_dict = {}
    for elem in root.iter():
        elem_id = elem.get("id")
        if elem_id:
            defs_dict[elem_id] = elem
    return defs_dict

def process_use(elem, parent_transform, defs_dict, inherited_fill=None):
    href = elem.get("href") or elem.get("{http://www.w3.org/1999/xlink}href")
    if not href:
        return []
    ref_id = href.lstrip("#")
    ref_elem = defs_dict.get(ref_id)
    if ref_elem is None:
        return []
    x = parse_float(elem.get("x", "0"))
    y = parse_float(elem.get("y", "0"))
    use_transform = (1, 0, 0, 1, x, y)
    local_transform = parse_transform(elem.get("transform"))
    total_transform = compose_transforms(parent_transform, compose_transforms(use_transform, local_transform))
    new_elem = ET.Element(ref_elem.tag, ref_elem.attrib)
    new_elem.extend(list(ref_elem))
    if elem.get("style"):
        new_elem.set("style", elem.get("style"))
    if elem.get("fill"):
        new_elem.set("fill", elem.get("fill"))
    return traverse_svg(new_elem, total_transform, defs_dict, inherited_fill=inherited_fill)

def traverse_svg(elem, parent_transform=IDENTITY, defs_dict=None, inherited_fill=None):
    if defs_dict is None:
        defs_dict = {}
    shapes = []
    tag = elem.tag.split('}')[-1]
    elem_fill = None
    if 'fill' in elem.attrib:
        elem_fill = elem.attrib['fill']
    elif elem.get("style"):
        style = parse_style(elem.get("style"))
        elem_fill = style.get("fill")
    current_inherited_fill = elem_fill if elem_fill is not None else inherited_fill

    if tag == "use":
        return process_use(elem, parent_transform, defs_dict, inherited_fill=current_inherited_fill)
    local_transform = parse_transform(elem.get("transform"))
    current_transform = compose_transforms(parent_transform, local_transform)
    geometry, color = extract_geometry(elem, current_transform, inherited_fill=current_inherited_fill)
    if geometry is not None:
        shapes.append((geometry, color))
    for child in elem:
        shapes.extend(traverse_svg(child, current_transform, defs_dict, inherited_fill=current_inherited_fill))
    return shapes

def get_shapes_from_svg(path):
    tree = ET.parse(path)
    root = tree.getroot()
    defs_dict = collect_defs(root)
    shapes = traverse_svg(root, IDENTITY, defs_dict)
    return shapes

def interior_triangles(polygon, tol=1e-10):
    all_triangles = triangulate(polygon)
    interior = []
    for tri in all_triangles:
        clipped = tri.intersection(polygon)
        if clipped.is_empty:
            continue
        if clipped.geom_type == 'Polygon':
            coords = list(clipped.exterior.coords)
            if len(coords) - 1 == 3:
                if abs(clipped.area - tri.area) < tol:
                    interior.append(clipped)
    return interior

def triangulation_sampling(polygon, num_samples, *, rng):
    triangles = interior_triangles(polygon)
    n_tri = len(triangles)
    if n_tri == 0:
        raise ValueError("No interior triangles found; check the polygon geometry.")
    triangle_vertices = []
    areas = []
    for tri in triangles:
        coords = list(tri.exterior.coords)[:3]
        triangle_vertices.append(coords)
        areas.append(tri.area)
    triangle_vertices = np.array(triangle_vertices)  # shape: (n_tri, 3, 2)
    areas = np.array(areas)
    cum_areas = np.cumsum(areas)
    total_area = cum_areas[-1]
    r = rng.uniform(0, total_area, num_samples)
    indices = np.searchsorted(cum_areas, r)
    u = rng.random(num_samples)
    v = rng.random(num_samples)
    mask = u + v > 1
    u[mask] = 1 - u[mask]
    v[mask] = 1 - v[mask]
    A = triangle_vertices[indices, 0, :]
    B = triangle_vertices[indices, 1, :]
    C = triangle_vertices[indices, 2, :]
    pts = A + np.expand_dims(u, axis=1) * (B - A) + np.expand_dims(v, axis=1) * (C - A)
    return pts

def resolve_overlaps_upper_only(shapes):
    resolved = []
    union_upper = None
    for geometry, color in reversed(shapes):
        if not geometry.is_valid:
            geometry = geometry.buffer(0)
        if union_upper is not None:
            try:
                geometry = geometry.difference(union_upper)
            except Exception:
                geometry = geometry.buffer(0).difference(union_upper.buffer(0))
        if not geometry.is_empty:
            resolved.append((geometry, color))
            if union_upper is None:
                union_upper = geometry
            else:
                union_upper = unary_union([union_upper, geometry])
                if not union_upper.is_valid:
                    union_upper = union_upper.buffer(0)
    resolved.reverse()
    return resolved

def sample_from_svg(path, total_samples, sample_setting="equal_over_classes",
                    overlap_mode="all", normalize=False, *, seed):
    rng = np.random.default_rng(seed)
    s = get_shapes_from_svg(path)
    if overlap_mode == "upper_only":
        s = resolve_overlaps_upper_only(s)
    shape_groups = {}
    for shape, color in s:
        shape_groups.setdefault(color, []).append(shape)
    if sample_setting == "equal_over_classes":
        union_groups = {color: unary_union(shapes) for color, shapes in shape_groups.items()}
        n_classes = len(union_groups)
        samples_per_class = int(total_samples / n_classes)
        X_list, y_list = [], []
        label_dict = {color: i for i, color in enumerate(union_groups.keys())}
        for color, union in union_groups.items():
            pts = triangulation_sampling(union, samples_per_class, rng=rng)
            X_list.append(pts)
            y_list.append(np.full(pts.shape[0], label_dict[color]))
        X, y = np.concatenate(X_list, axis=0), np.concatenate(y_list, axis=0)
    elif sample_setting == "equal_over_shapes":
        n_shapes = len(s)
        samples_per_shape = int(total_samples / n_shapes)
        X_list, y_list = [], []
        label_dict = {}
        for shape, color in s:
            if color not in label_dict:
                label_dict[color] = len(label_dict)
        for shape, color in s:
            pts = triangulation_sampling(shape, samples_per_shape, rng=rng)
            X_list.append(pts)
            y_list.append(np.full(pts.shape[0], label_dict[color]))
        X, y = np.concatenate(X_list, axis=0), np.concatenate(y_list, axis=0)
    elif sample_setting == "based_on_area":
        union_groups = {color: unary_union(shapes) for color, shapes in shape_groups.items()}
        total_area = sum(union.area for union in union_groups.values())
        X_list, y_list = [], []
        label_dict = {color: i for i, color in enumerate(union_groups.keys())}
        for color, union in union_groups.items():
            n_samples = int(round(total_samples * union.area / total_area))
            pts = triangulation_sampling(union, n_samples, rng=rng)
            X_list.append(pts)
            y_list.append(np.full(pts.shape[0], label_dict[color]))
        X, y = np.concatenate(X_list, axis=0), np.concatenate(y_list, axis=0)
    else:
        raise ValueError(f"Chosen sampling setting '{sample_setting}' does not exist.")
    
    if normalize:
        min_x, max_x = X[:, 0].min(), X[:, 0].max()
        min_y, max_y = X[:, 1].min(), X[:, 1].max()
        if max_x - min_x > 0:
            X[:, 0] = (X[:, 0] - min_x) / (max_x - min_x)
        if max_y - min_y > 0:
            X[:, 1] = (X[:, 1] - min_y) / (max_y - min_y)
    
    return X, y

if __name__ == "__main__":
    pass
