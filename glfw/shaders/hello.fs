#version 330 core
in vec4 gl_FragCoord;
in vec2 TexCoord;
in vec3 vertexColor;

uniform sampler2D texture1;
uniform sampler2D texture2;

uniform float mixValue;

out vec4 FragColor;

void main()
{
    //float alpha = 1.0;
    //FragColor = vec4(vertexColor, alpha);
    //FragColor = vec4(vec3(alpha*4, alpha*2, alpha), alpha);
    //FragColor = texture(texture1, TexCoord);

    float XX = TexCoord.x;
    float YY = TexCoord.y;
    if (mixValue > 0.5) {
        XX = (1-TexCoord.x) / 5;
        YY = (1-TexCoord.y) / 5;
    }
    FragColor = texture(texture1, TexCoord);
    //FragColor = mix(texture(texture1, TexCoord), texture(texture2, vec2(XX, YY)), mixValue);
}