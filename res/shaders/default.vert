#version 330 core

#include "common/common.vert"
#include "common/uio.vert"

void main()
{
    uv_0 = in_uv;

    v3_fragment_position = vec3(m_model * vec4(in_vertex, 1.0));
    gl_Position = m_proj * m_view * vec4(v3_fragment_position, 1.0);

    center = vec3(0, 0, 0); //get_model_center(m_model);
    
    if (smooth_normals) {
        vn_0 =  normalize(in_vertex - center);
        TBN = build_smooth_TBN(in_tangent, in_bitangent, vn_0);
    }
    else {
        vn_0 = vec3(m_model * vec4(in_normal, 0.0)); 
        TBN = build_TBN(m_model, in_tangent, in_bitangent, in_normal);
    }

    mat4 shadowMVP = m_proj * m_view_light * m_model;
    v3_shadow_position = m_shadow_bias * shadowMVP * vec4(in_vertex, 1.0);
    v3_shadow_position.z -= 0.0005;
}