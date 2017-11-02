#version 330 core
in vec4 gl_FragCoord;
uniform float alpha;
out vec4 FragColor;
void main()
{
    FragColor = vec4(vec3(alpha*4, alpha*2, alpha), alpha);
}