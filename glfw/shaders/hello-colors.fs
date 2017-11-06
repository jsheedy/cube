#version 330 core
struct Material {
    vec3 ambient;
    //vec3 diffuse;
    sampler2D diffuse;
    sampler2D specular;
    sampler2D emission;
    float shininess;
};

struct Light {
    vec3 position;
    vec3 direction;
    vec3 ambient;
    vec3 diffuse;
    vec3 specular;

    float constant;
    float linear;
    float quadratic;

    float cutOff;
    float outerCutOff;
};

uniform Light light;
uniform Material material;
uniform vec3 objectColor;
uniform vec3 viewPos;

in vec2 TexCoords;
in vec3 normal;
in vec3 fragPos;

out vec4 FragColor;

void main()
{
    //vec3 ambient = material.ambient;
    vec3 ambient = light.ambient * material.ambient;

    vec3 norm = normalize(normal);
    // directional
    //vec3 lightDir = normalize(-light.direction); //normalize(light.position - fragPos);

    vec3 lightDir = normalize(light.position - fragPos);

    float distance    = length(light.position - fragPos);
    float attenuation = 1.0 / (light.constant + light.linear * distance +
                    light.quadratic * (distance * distance));


    float diff = max(dot(norm, lightDir), 0.0);
    //vec3 diffuse = light.diffuse * material.diffuse * diff;
    vec3 diffuse = light.diffuse * diff * vec3(texture(material.diffuse, TexCoords));

    vec3 viewDir = normalize(viewPos - fragPos);
    vec3 reflectDir = reflect(-lightDir, norm);

    float spec = pow(max(dot(viewDir, reflectDir), 0.0), material.shininess);
    vec3 specular = light.specular * vec3(texture(material.specular, TexCoords)) * spec;

    vec3 emission = vec3(texture(material.emission, TexCoords));

    ambient  *= attenuation;
    diffuse  *= attenuation;
    specular *= attenuation;

    float theta = dot(lightDir, normalize(-light.direction));
    float epsilon   = light.cutOff - light.outerCutOff;
    float intensity = clamp((theta - light.outerCutOff) / epsilon, 0.0, 1.0);

    diffuse *= intensity;
    specular *= intensity;
    vec3 result = ambient + diffuse + specular + emission;

      //color = vec4(light.ambient * vec3(texture(material.diffuse, TexCoords)), 1.0);

    FragColor = vec4(result, 1.0);
}
