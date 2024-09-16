#version 330 core

#include "common/common.frag" // ignore
#include "common/uio.frag"

#include "common/pbr.frag"

void main()
{		
    // material properties
    vec3  albedo = vec3(1.0);
    float metallic = 0.0;
    float roughness = 1.0;
    float ao = 1.0;

    if ((enabled_maps & ALBEDO) != 0) {
        albedo = pow(texture(map_albedo, uv_0).rgb, vec3(2.2));
    }
    if ((enabled_maps & METALLIC) != 0) {
        metallic = texture(map_metallic, uv_0).r;
    }    
    if ((enabled_maps & ROUGHNESS) != 0) {
        roughness = texture(map_roughness, uv_0).r;
    }
    if ((enabled_maps & AO) != 0) {
        ao = texture(map_ao, uv_0).r;
    }    

    // input lighting data
    vec3 N = normalize(vn_0);
    vec3 V = normalize(v3_camera_position - v3_fragment_position);
    vec3 R = reflect(-V, N);    
    
    if ((enabled_maps & NORMAL) != 0) {
        N = texture(map_normal, uv_0).rgb * 2.0 - 1.0;
        N = normalize(TBN * N);
    }

    // reflectance
    vec3 F0 = vec3(0.04);    
    
    if ((enabled_maps & CUBEMAP) != 0) {
        vec3 I = normalize(v3_fragment_position - v3_camera_position);
        vec3 R = reflect(I, N);
        F0 = pow(texture(map_cubemap, R).rgb, vec3(2.2));
    }

    F0 = mix(F0, albedo, metallic);

    // ========== reflection equation ====================
    vec3 Lo = vec3(0.0);

    vec3 L = normalize(-directional_light.direction); // or inverted ?
    vec3 H = normalize(V + L);
    const float distance = 10.0; // constant as using directional light without a position
    float attenuation = 1.0 / (distance * distance);
    vec3 radiance = (directional_light.light.Id + directional_light.light.Is) * attenuation; // maybe half light

    // Cook-Torrance BRDF
    float NDF = DistributionGGX(N, H, roughness);
    float G   = GeometrySmith(N, V, L, roughness);
    vec3  F   = fresnelSchlick(max(dot(H, V), 0.0), F0);

    vec3 numerator = NDF * G * F;
    float denominator = 4.0 * max(dot(N, V), 0.0) * max(dot(N, L), 0.0) + 0.0001;
    vec3 specular = numerator / denominator;

    if ((enabled_maps & SPECULAR) != 0) { 
        specular *= texture(map_specular, uv_0).r;
    }

    // Energy conservation clamping
    vec3 kS = F;
    vec3 kD = vec3(1.0) - kS;
    kD *= 1.0 - metallic;

    // scale light
    float NdotL = max(dot(N, L), 0.0);

    // outgoing radiance
    Lo = (kD * albedo / PI + specular) * radiance * NdotL;

    // ========== irradiance ========== 

    //vec3 reflectance = 
    vec3 diffuse = albedo * directional_light.light.Id;
    vec3 ambient = (kD * diffuse) * ao * directional_light.light.Ia;

    vec3 color = ambient + (Lo * directional_light.light.Is);

    // gamma correction
    color = color / (color + vec3(1.0));
    color = pow(color, vec3(1.0/2.2));

    if (debug_show_normal) {
        color = show_debug_normal(color, N);
    }

    fragment_color = vec4(color, 1.0);
}  