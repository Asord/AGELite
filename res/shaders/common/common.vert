
const mat4 m_shadow_bias = mat4(
    0.5, 0.0, 0.0, 0.0,
    0.0, 0.5, 0.0, 0.0,
    0.0, 0.0, 0.5, 0.0,
    0.5, 0.5, 0.5, 1.0
);

mat3 build_TBN(mat4 model_matrix, vec3 tangent, vec3 bitangent, vec3 normal) {
    return mat3(
        normalize(vec3(model_matrix * vec4(tangent, 0.0))),
        normalize(vec3(model_matrix * vec4(bitangent, 0.0))),
        normalize(vec3(model_matrix * vec4(normal, 0.0)))
    );
}

mat3 build_smooth_TBN(vec3 tangent, vec3 bitangent, vec3 normal) {
        return mat3(
        normalize(tangent),
        normalize(bitangent),
        normalize(normal)
    );
}

vec3 get_model_center(mat4 model_matrix) {
    return vec3(model_matrix[3][0], model_matrix[3][1], model_matrix[3][2]);
}