#define WIN32_LEAN_AND_MEAN
#include <windows.h>

#include "vec.h"
#include "globals.h"

BOOL APIENTRY DllMain(HMODULE hModule, DWORD  ul_reason_for_call, LPVOID lpReserved) {
    switch (ul_reason_for_call) {
        case DLL_PROCESS_ATTACH:
        case DLL_THREAD_ATTACH:
        case DLL_THREAD_DETACH:
        case DLL_PROCESS_DETACH:
            break;
    }
    return TRUE;
}

// Input vertex structure
struct VertIn {
    vec2 uv;
    vec3 normals;
    vec3 position;
};

// Input face structure
struct FaceIn {
    VertIn v0;
    VertIn v1;
    VertIn v2;
};

// Output vertex structure
struct VertOut {
    vec2 uv;
    vec3 bitangant;
    vec3 tangant;
    vec3 normals;
    vec3 position;
};

// Output face structure
struct FaceOut {
    VertOut v0;
    VertOut v1;
    VertOut v2;
};

inline void facein_t_faceout(const FaceIn& in, FaceOut* out) {
    // copy the input face data to the output face
    out->v0.position = in.v0.position;
    out->v1.position = in.v1.position;
    out->v2.position = in.v2.position;

    out->v0.normals = in.v0.normals;
    out->v1.normals = in.v1.normals;
    out->v2.normals = in.v2.normals;

    out->v0.uv = in.v0.uv;
    out->v1.uv = in.v1.uv;
    out->v2.uv = in.v2.uv;
}

inline void tanbit_t_faceout(const vec3& tangant, const vec3& bitangant, FaceOut* out) {
    // copy the tangant and bitangant to the output face
    out->v0.tangant = tangant;
    out->v1.tangant = tangant;
    out->v2.tangant = tangant;

    out->v0.bitangant = bitangant;
    out->v1.bitangant = bitangant;
    out->v2.bitangant = bitangant;
}

extern "C" __declspec(dllexport) void bake_tangants(const char* vertices_in, char* vertices_out, const size_t nb_faces_in) {
    // bake tangant and bitangent to the vertices data

    // variables
    vec3 edge1, edge2, tangant, bitangant;
    vec2 deltaUV1, deltaUV2;

    float f = 0.0f;
    FaceIn face_in;
    FaceOut face_out;
    
    // for each face
    for (size_t face_in_idx = 0; face_in_idx < nb_faces_in; face_in_idx++) {
        // get the input face data
        memcpy(&face_in, vertices_in + face_in_idx * size_of::inFace, size_of::inFace);

        // copy the data to the output face
        facein_t_faceout(face_in, &face_out);
        
        // compute tangant and bitangant
        edge1 = face_in.v1.position - face_in.v0.position;
        edge2 = face_in.v2.position - face_in.v0.position;

        deltaUV1 = face_in.v1.uv - face_in.v0.uv;
        deltaUV2 = face_in.v2.uv - face_in.v0.uv;

        f = 1.0f / (deltaUV1.x * deltaUV2.y - deltaUV2.x * deltaUV1.y);

        tangant = vec3(f * (deltaUV2.y * edge1 - deltaUV1.y * edge2)).normalize();
        bitangant = vec3(f * (-deltaUV2.x * edge1 + deltaUV1.x * edge2)).normalize();

        // copy the tangant and bitangant to the output face
        tanbit_t_faceout(tangant, bitangant, &face_out);

        // copy the output face data to the output data
        memcpy(vertices_out + face_in_idx * size_of::outFace, &face_out, size_of::outFace);
    }
}