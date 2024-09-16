#version 330 core

layout (location = 0) out vec4 fragColor;

in vec4 clipCoords;

uniform samplerCube cubemap;
uniform mat4 m_invProjView;

void main()
{
    // Inversely project from [clip-space] to [normalized world space]
    vec4 worldCoords = m_invProjView * clipCoords;
    vec3 texCubeCoord = normalize(worldCoords.xyz / worldCoords.w);
    
    fragColor = texture(cubemap, texCubeCoord);
}