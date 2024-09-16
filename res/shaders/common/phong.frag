//float getSoftShadowX16()
//{
//    if (directional_light.shadowable != 1) return 1.0;
//
//    vec2 pixelOffset = 1.0 / v2_resolution;
//
//    float shadow;
//    float swidth = 1.0;
//    float endp = swidth * 1.5;
//    for (float y = -endp; y <= endp; y += swidth)
//    {
//        for (float x = -endp; x <= endp; x += swidth) 
//        {
//            shadow += textureProj(map_shadow, v3_shadow_position + vec4(vec2(x, y) * pixelOffset * v3_shadow_position.ww, 0.0, 0.0));
//        }
//    }
//    return shadow / 16;
//}

//vec3 calcPointLight(vec3 Ka, vec3 Kd, vec3 Ks, float Ns, vec3 normal)
//{
//    vec3 result = vec3(0.0, 0.0, 0.0);
//
//    for (int i = 0; i < MAX_LIGHTS; i++)
//    {
//        if (point_lights[i].enabled != 1) continue;
//        PointLight pl = point_lights[i];
//
//        vec3 N = normalize(normal);
//        vec3 L = normalize(pl.light.position - v3_fragment_position);
//        vec3 V = normalize(v3_camera_position - v3_fragment_position);
//        vec3 H = normalize(V + L);
//
//        float Ld = max(dot(N, L), 0.0);
//        float NdotH = max(dot(N, H), 0.0);
//        
//        float Ls =  (Ns + 2.0) * pow(NdotH, Ns) / (2.0 * 3.1415);
//
//        float dist = length(pl.light.position - v3_fragment_position);
//        float attenuation = 1.0 / (pl.constant + pl.linear *dist + pl.quadratic *dist*dist);
//
//        vec3 ambiant = pl.light.Ia * Ka;
//        vec3 diffuse = pl.light.Id * Kd * Ld;
//        vec3 specular = pl.light.Is * Ks * Ls;
//
//        result += (ambiant + diffuse + specular) * attenuation;
//    }
//    return result;
//}


vec3 calcDirectionalLight(vec3 Ka, vec3 Kd, vec3 Ks, float Ns, vec3 normal) {
	// diffuse lighting
	vec3 N = normalize(normal);
    vec3 L = normalize(-directional_light.direction);
	float diffuse = max(dot(N, L), 0.0f);


	// specular lighting
    vec3 V = normalize(v3_camera_position - v3_fragment_position);
    vec3 R = reflect(-L, N);
    //vec3 halfwayVec = normalize(viewDirection + L);
    float spec = pow(max(dot(V, R), 0.0f), Ns);

    vec3 a = Ka * directional_light.light.Ia;
    vec3 d = Kd * directional_light.light.Id * diffuse;
    vec3 s = Ks * directional_light.light.Is * spec;
    float shadow = 1.0; //getSoftShadowX16();

	return (a + (d + s) + (shadow * 0.001));
}


const float Ns = 10.0;
const float gamma = 2.2;