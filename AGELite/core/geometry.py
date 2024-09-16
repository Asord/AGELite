from pathlib import Path

import numpy as np 
import glm

from .cpp.AGEutils import bake_tangants

def triangulate(vertices: list[tuple[int]], indices: list[tuple[int]]) -> list[tuple[int]]:
    """ triangulate a list of vertices and indices """
    return [vertices[ind] for triangle in indices for ind in triangle]

def get_normals(vertices: list[tuple[int]] | np.ndarray) -> np.ndarray:
    """ get the normals of a list of vertices """
    normals = []
    for ti in range(0, len(vertices), 3):
        triangle_vertices = [glm.vec3(data) for data in vertices[ti:ti+3]]
        tn = glm.normalize(glm.cross(triangle_vertices[1] - triangle_vertices[0], triangle_vertices[2] - triangle_vertices[0]))
        normals += [tn, tn, tn]
    normals = np.array(normals, dtype='f4')
    return normals


def primitive_triangle(boundary_square: tuple[tuple[int, int]] = ((-1, -1), (1, 1))) -> list[tuple[int, int]]:
    """ create a triangle within a boundary square """
    (xm, ym), (Xm, Ym) = boundary_square
    return [(xm, ym), (Xm, ym), (xm, Ym)]

def primitive_square(boundary_square: tuple[tuple[int, int]] = ((-1, -1), (1, 1)))-> list[tuple[int, int]]:
    """ create a square within a boundary square """
    (xm, ym), (Xm, Ym) = boundary_square
    return [(xm, ym), (Xm, ym), (Xm, Ym), (xm, ym), (Xm, Ym), (xm, Ym)]

def primitive_quad(boundary_square: tuple[tuple[int, int]] = ((-1, -1), (1, 1)))-> list[tuple[int, int]]:
    """ create a quad within a boundary square """
    (xm, ym), (Xm, Ym) = boundary_square
    return [(xm, ym), (Xm, ym), (Xm, Ym), (xm, Ym)]

def primitive_cube(boundary_box: tuple[tuple[int]] = ((-1, -1, -1), (1, 1, 1))) -> list[tuple[int]]:
    """ create a cube within a boundary box """
    (xm, ym, zm), (Xm, Ym, Zm) = boundary_box
    vertices = [(xm, ym, Zm), (Xm, ym, Zm), (Xm, Ym, Zm), (xm, Ym, Zm), (xm, Ym, zm), (xm, ym, zm), (Xm, ym, zm), (Xm, Ym, zm)]
    indices = [(0, 2, 3), (0, 1, 2), (1, 7, 2), (1, 6, 7), (6, 5, 4), (4, 7, 6), (3, 4, 5), (3, 5, 0), (3, 7, 4), (3, 2, 7), (0, 6, 1), (0, 5, 6)]
    return triangulate(vertices, indices)

def new_sphere() -> np.ndarray:
    """ load the sphere model """
    # format of data within the mdl file: (v2f uv,v3f normal,v3f position) * number of vertices
    # calls bake_tangants() to add tangant and bitangent to the vertices
    # output format: (v2f uv, v3f tangent, v3f bitangent,v3f normal,v3f position) * number of vertices
    return np.fromstring(bake_tangants(Path("./res/mdl/sphere.mdl").read_bytes()), dtype='f4').reshape(-1, 14)

def new_arrow() -> np.ndarray:
    """ load the arrow model """
    # format of data within the mdl file: (v2f uv,v3f normal,v3f position) * number of vertices
    # calls bake_tangants() to add tangant and bitangent to the vertices
    # output format: (v2f uv, v3f tangent, v3f bitangent,v3f normal,v3f position) * number of vertices
    return np.fromstring(bake_tangants(Path("./res/mdl/arrow.mdl").read_bytes()), dtype='f4').reshape(-1, 14)

def new_cube() -> np.ndarray:
    """ create a cube model """
    tex_coord_vertices = [(0, 0), (1, 0), (1, 1), (0, 1)]
    tex_coord_indices = [(0, 2, 3), (0, 1, 2), (0, 2, 3), (0, 1, 2), (0, 1, 2), (2, 3, 0), (2, 3, 0), (2, 0, 1), (0, 2, 3), (0, 1, 2), (3, 1, 2), (3, 0, 1)]
    tex_coord_data = np.array(triangulate(tex_coord_vertices, tex_coord_indices), dtype='f4')

    normals = np.array([
        ( 0, 0, 1) * 6,
        ( 1, 0, 0) * 6,
        ( 0, 0,-1) * 6,
        (-1, 0, 0) * 6,
        ( 0, 1, 0) * 6,
        ( 0,-1, 0) * 6
    ], dtype='f4').reshape(36, 3)

    vertex_data = np.array(primitive_cube(), dtype='f4')
    vertex_data = np.hstack([normals, vertex_data])
    vertex_data = np.hstack([tex_coord_data, vertex_data])
    return np.fromstring(bake_tangants(vertex_data.tobytes()), dtype='f4').reshape(-1, 14)

def new_triangle_screen() -> np.ndarray:
    """ create a triangle that covers the entire screen """
    primitive = np.array(primitive_triangle(((-1, -1), (3, 3))), dtype='f4')
    primitive_back = np.array([(px, py, 0.9999) for px, py in primitive], dtype='f4')
    return primitive_back
