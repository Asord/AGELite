#version 330 core
#include "common/common.frag"
#include "common/uio.frag"

#include "common/phong.frag"

void main()
{

    vec3 normal = normalize(vn_0);
    
    vec3 Ka = vec3(1.0);
    vec3 Kd = vec3(0.8);
    vec3 Ks = vec3(0.4);
    float metalness = 0.0;

    if ((enabled_maps & ALBEDO) != 0) {
        Ka = texture(map_albedo, uv_0).rgb;
        Kd = Ka * texture(map_albedo, uv_0).a;
    }
    if ((enabled_maps & SPECULAR) != 0) {
        Ks = texture(map_specular, uv_0).rgb;
    }
    if ((enabled_maps & ROUGHNESS) != 0) {
        Ks = Ks * texture(map_roughness, uv_0).r;
    }
    if ((enabled_maps & METALLIC) != 0) {
        metalness = texture(map_metallic, uv_0).r;
    }
    if ((enabled_maps & AO) != 0) {
        Ka = Ka * texture(map_ao, uv_0).r;
    }        
    if ((enabled_maps & NORMAL) != 0) {
        normal = texture(map_normal, uv_0).rgb * 2.0 - 1.0;
        normal = normalize(TBN * normal);
    }
    if ((enabled_maps & CUBEMAP) != 0) {
        vec3 I = normalize(v3_fragment_position - v3_camera_position);
        vec3 R = reflect(I, normal);
        Ks += mix(Ks, texture(map_cubemap, R).rgb, metalness);
    }

    Ka = pow(Ka, vec3(gamma));

    // lighting
    vec3 color = calcDirectionalLight(Ka, Kd, Ks, Ns, normal);
    //color += calcPointLight(Ka, Kd, Ks, Ns, normal);

    // debug normals
    if (debug_show_normal) {
        color = show_debug_normal(color, normal);
    }
    // gamma correction
    color = pow(color, 1.0 / vec3(gamma));
    // output
    fragment_color = vec4(color, 1.0);
}