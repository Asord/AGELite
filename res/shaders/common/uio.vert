in vec3 in_vertex;
in vec3 in_normal;
in vec3 in_tangent;
in vec3 in_bitangent;
in vec2 in_uv;

out vec2 uv_0;
out vec3 vn_0;
out vec3 v3_fragment_position;
out vec4 v3_shadow_position;
out mat3 TBN;
out vec3 center;

uniform mat4 m_proj;
uniform mat4 m_view;
uniform mat4 m_view_light;
uniform mat4 m_model;

uniform bool smooth_normals;