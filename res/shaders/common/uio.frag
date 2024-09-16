// UNIFORMS INPUTS OUTPUTS 

const int CUBEMAP = 1;
const int ALBEDO = 2;
const int METALLIC = 4;
const int SPECULAR = 8;
const int ROUGHNESS = 16;
const int NORMAL = 32;
const int EMMISIVE = 64;
const int AO = 128;


out vec4 fragment_color;

in vec2 uv_0;
in vec3 vn_0;
in vec3 v3_fragment_position;
in vec4 v3_shadow_position;
in mat3 TBN;
in vec3 center;

uniform samplerCube map_cubemap;
uniform sampler2D  map_albedo;
uniform sampler2D  map_metallic;
uniform sampler2D  map_roughness;
uniform sampler2D  map_specular;
uniform sampler2D  map_normal;
uniform sampler2D  map_emissive;
uniform sampler2D  map_ao;
//uniform sampler2DShadow map_shadow;

uniform DirectionalLight directional_light;
//uniform PointLight[MAX_LIGHTS] point_lights;

uniform int enabled_maps; // enum_map
/*uniform bool has_cubemap;
uniform bool has_albedo;
uniform bool has_metallic;
uniform bool has_specular;
uniform bool has_roughness;
uniform bool has_normal;
uniform bool has_emissive;
uniform bool has_ao;*/

uniform vec3 v3_camera_position;
uniform vec2 v2_resolution;
uniform bool debug_show_normal;