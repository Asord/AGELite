#version 330 core

layout (location = 2) in vec3 in_normal;
layout (location = 3) in vec3 in_vertex;

out vec3 vn_0;

uniform mat4 m_proj;
uniform mat4 m_view;
uniform mat4 m_model;

void main()
{
    vec3 v3_fragment_position = vec3(m_model * vec4(in_vertex, 1.0));
    vn_0 = mat3(transpose(inverse(m_model))) * in_normal;
    gl_Position = m_proj * m_view * vec4(v3_fragment_position, 1.0);
}