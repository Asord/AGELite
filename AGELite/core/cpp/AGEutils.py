import ctypes
from pathlib import Path
from typing import Callable

bake_tangants: Callable = None

class _globals:
    """ hold globals for AGEutils.dll wrapper """
    nb_floats_per_vertex_in = 8
    nb_flooats_per_vertex_out = 14
    nb_vertex_per_face = 3

    size_of_float = 4

    size_of_faces_in = size_of_float * nb_floats_per_vertex_in * nb_vertex_per_face
    size_of_faces_out = size_of_float * nb_flooats_per_vertex_out * nb_vertex_per_face

    dll_path = Path("AGELite/core/cpp/AGEutils.dll").resolve()

    try:
        if dll_path.exists():
            hllDll = ctypes.WinDLL(dll_path.__str__())
        else:
            print("\x1b[33mAGEutils.dll not found\x1b[0m")
            hllDll = None
    except Exception as e:
        # IMPORTANT: if the DLL did not load sucessfully, it might be because you don't have msvc143 installed in your computer. 
        hllDll = None
        print(f"\x1b[33mAGEutils.dll can't be initialized:\n{e}\x1b[0m")


def _dll_bake_tangants(buffer: bytes) -> bytes:
    """ AGEutils.dll wrapper for bake_tangants """

    assert type(buffer) == bytes
    assert _globals.hllDll.bake_tangants

    _size_of_buffer_in = len(buffer)

    assert _size_of_buffer_in % _globals.size_of_faces_in == 0 # buffer should be multiple of faces

    _nb_faces = _size_of_buffer_in // _globals.size_of_faces_in
    _size_of_buffer_out = _globals.size_of_faces_out * _nb_faces

    data = ctypes.create_string_buffer(buffer, _size_of_buffer_in)
    out = (ctypes.c_char_p * _size_of_buffer_out)()

    # void bake_tangants(const char* in, char* out, size_t in_nb_faces)
    _globals.hllDll.bake_tangants(ctypes.byref(data), ctypes.byref(out), _nb_faces)

    return bytes(out)

def _py_bake_tangants(buffer: bytes) -> bytes:
    """ legacy python implementation of bake_tangants if the dll can't be loaded """
    from io import BytesIO
    from struct import unpack, pack
    import glm

    # output buffer
    out = BytesIO() 

    # constants representing the size of all elements

    sF = 4              # float
    sP = 3*sF           # position
    sN = 3*sF           # normal
    sUV = 2*sF          # uv
    sV = sP + sN + sUV  # vertex
    sF = 3*sV           # face


    nb_faces = len(buffer)//sF

    # variable declarations (for optimization)
    edge1 = edge2 = tangent = bitangent = glm.vec3()
    deltaUV1 = deltaUV2 = glm.vec2()
    f = 0.0
    face: list[tuple[glm.vec3, glm.vec3, glm.vec2]] = []

    # for each face
    for i in range(0, len(buffer), sF):
        face.clear()

        # get each vertex data of the face
        for j in range(0, sF, sV): 
            u, v, nx, ny, nz, x, y, z  = unpack('2f 3f 3f', buffer[i+j:i+j+sV])
            face.append((glm.vec3(x, y, z), glm.vec3(nx, ny, nz), glm.vec2(u, v)))

        # compute tangent/bitangent
        edge1 = face[1][0] - face[0][0]
        edge2 = face[2][0] - face[0][0]

        deltaUV1 = face[1][2] - face[0][2]
        deltaUV2 = face[2][2] - face[0][2]

        f = (deltaUV1.x * deltaUV2.y - deltaUV2.x * deltaUV1.y)

        f = 1.0 / (deltaUV1.x * deltaUV2.y - deltaUV2.x * deltaUV1.y)

        tangent   = f * ( deltaUV2.y * edge1 - deltaUV1.y * edge2)
        bitangent = f * (-deltaUV2.x * edge1 + deltaUV1.x * edge2)

        # write the output
        for v in face:
            out.write(pack('2f 3f 3f 3f 3f', *v[2].to_tuple(), *bitangent.to_tuple(), *tangent.to_tuple(), *v[1].to_tuple(), *v[0].to_tuple()))

        # print progress
        if i//sF % (nb_faces//5) == 0: # every 20%
            p = i//sF
            print(f"   {p}/{nb_faces} ({ (p/(nb_faces)*100):.2f}%)                          ", end='\r')
    print("                                                                                 ", end='\r')
    
    # return the result
    out.seek(0)
    return out.read()


if _globals.hllDll is not None:
    bake_tangants = _dll_bake_tangants
else:
    bake_tangants = _py_bake_tangants
    print("\x1b[33mWARNING: AGEutils.dll not initialized, using Python implementation. Will be slower.\x1b[0m")
