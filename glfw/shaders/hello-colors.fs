#version 330 core
out vec4 FragColor;

uniform vec3 objectColor;
uniform vec3 lightColor;
uniform vec3 lightPos;
uniform vec3 viewPos;

in vec3 normal;
in vec3 fragPos;

void main()
{
    float ambientStrength = 0.5;
    float specularStrength = 0.9;
    float diffStrength = 0.3;

    vec3 ambient = ambientStrength * lightColor;

    vec3 norm = normalize(normal);
    vec3 lightDir = normalize(lightPos - fragPos);

    float diff = max(dot(norm, lightDir), 0.0);
    vec3 diffuse = diffStrength * diff * lightColor;

    vec3 viewDir = normalize(viewPos - fragPos);
    vec3 reflectDir = reflect(-lightDir, norm);

    float spec = pow(max(dot(viewDir, reflectDir), 0.0), 64);
    vec3 specular = specularStrength * spec * lightColor;

    vec3 result = (ambient + diff + specular) * objectColor;
    FragColor = vec4(result, 1.0);
    //FragColor = vec4(lightColor * objectColor, 1.0);
}