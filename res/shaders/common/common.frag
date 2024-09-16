#define MAX_LIGHTS 3

const float PI = 3.14159265359;

struct Light
{
    vec3 position;
    vec3 Ia;
    vec3 Id;
    vec3 Is;
};

struct DirectionalLight
{
    int shadowable;
    mat4 m_view_light;
    vec3 direction;
    Light light;
};

//struct PointLight
//{
//    int enabled;
//    float constant;
//    float linear;
//    float quadratic;
//    Light light;
//};


vec3 show_debug_normal(vec3 Kd, vec3 normal) {
    vec3 N = normalize(normal);
    vec3 iN = -N;
    vec3 iColor = vec3(0.0, 1.0, 1.0) * iN.x + vec3(1.0, 0.0, 1.0) * iN.y + vec3(1.0, 1.0, 0.0) * iN.z;
    return Kd * 0.85 + (N + iColor) * 0.15;
}