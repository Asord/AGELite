#version 330 core

const vec3 light_direction = vec3(0.0, -1.0, 0.0);
const vec3 light_color     = vec3(1.0, 1.0, 1.0);

out vec4 fragment_color;

in vec3 vn_0;

uniform vec3 color;

void main() {
    vec3 color = (color*light_color) + (color*light_color*max(dot(normalize(vn_0), normalize(-light_direction)), 0.0f));
    fragment_color = vec4(color, 1.0);
}