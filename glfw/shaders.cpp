#include <iostream>
#include <cmath>
#include "glad/glad.h"
#include <GLFW/glfw3.h>

void framebuffer_size_callback(GLFWwindow* window, int width, int height)
{
    glViewport(0, 0, width, height);
}
void processInput(GLFWwindow *window)
{
    if(glfwGetKey(window, GLFW_KEY_ESCAPE) == GLFW_PRESS)
        glfwSetWindowShouldClose(window, true);
}

int main()
{
    std::cout << "HELLO" << std::endl;
    glfwInit();
    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3);
    glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);
    // for mac:
    glfwWindowHint(GLFW_OPENGL_FORWARD_COMPAT, GLFW_TRUE);

        GLFWwindow* window = glfwCreateWindow(800, 600, "LearnOpenGL", NULL, NULL);
    if (window == NULL)
    {
        std::cout << "Failed to create GLFW window" << std::endl;
        glfwTerminate();
        return -1;
    }
    glfwMakeContextCurrent(window);

    glfwSetFramebufferSizeCallback(window, framebuffer_size_callback);
    if (!gladLoadGLLoader((GLADloadproc)glfwGetProcAddress))
    {
        std::cout << "Failed to initialize GLAD" << std::endl;
        return -1;
    }

    unsigned int vertexShader;
    vertexShader = glCreateShader(GL_VERTEX_SHADER);

    float cubeVertices[] = {
         0.8f,  0.8f, 0.8f,  // top right
         0.8f, -0.8f, 0.8f,  // bottom right
        -0.8f, -0.8f, 0.8f,  // bottom left
        -0.8f,  0.8f, 0.8f,   // top left

         0.8f,  0.8f, 0.8f,  // top right
         0.8f, -0.8f, 0.8f,  // bottom right
        -0.8f, -0.8f, 0.8f,  // bottom left
        -0.8f,  0.8f, 0.8f,   // top left
    };

    unsigned int rectIndices[] = {  // note that we start from 0!
        0, 1, 3,   // first triangle
        1, 2, 3    // second triangle
    };

    unsigned int cubeIndices[] = {  // note that we start from 0!
        0, 1, 3,   // first triangle
        1, 2, 3,    // second triangle
        4, 5, 7,   // first triangle
        5, 6, 7    // second triangle
    };

    unsigned int VBO;
    glGenBuffers(1, &VBO);

    unsigned int VAO;
    glGenVertexArrays(1, &VAO);

    glBindVertexArray(VAO);
    // 2. copy our vertices array in a buffer for OpenGL to use
    glBindBuffer(GL_ARRAY_BUFFER, VBO);
    glBufferData(GL_ARRAY_BUFFER, sizeof(cubeVertices), cubeVertices, GL_STATIC_DRAW);
    // glBufferData(GL_ARRAY_BUFFER, sizeof(rectVertices), rectVertices, GL_STATIC_DRAW);

    unsigned int EBO;
    glGenBuffers(1, &EBO);
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO);
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, sizeof(cubeIndices), cubeIndices, GL_STATIC_DRAW);

    // 3. then set our vertex attributes pointers
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * sizeof(float), (void*)0);
    glEnableVertexAttribArray(0);

    const char *vertexShaderSource = "#version 330 core\n"

        "layout (location = 0) in vec3 aPos;\n"

        "out vec4 vertexColor;\n "

        "float random (vec2 st) {"
        "    return fract(sin(dot(st.xy,"
        "        vec2(12.9898,78.233)))*"
        "        43758.5453123);"
        "}"
        "void main()\n"
        "{\n"
        "  gl_Position = vec4(aPos, 1.0f);\n"
        " vertexColor = vec4(aPos, 1.0f);\n"
        "}\n\0";

    const char *greenFragmentShaderSource = "#version 330 core\n"
        "uniform vec4 vertexColor;"
        "out vec4 FragColor;\n"
        "void main()\n"
        "{\n"
        "    FragColor = vertexColor;\n"
        "}\n\0";

    const char *whiteFragmentShaderSource = "#version 330 core\n"
        "in vec4 gl_FragCoord;"
        "in vec4 vertexColor;"
        "out vec4 FragColor;\n"
        "void main()\n"
        "{\n"
        "    FragColor = vertexColor;\n"
        "}\n\0";

    // "    FragColor = vec4(gl_FragCoord.x /800.0f, gl_FragCoord.y /600.0f, 0.0f, 1.0f);\n"
    glShaderSource(vertexShader, 1, &vertexShaderSource, NULL);
    glCompileShader(vertexShader);
    int  success;
    char infoLog[512];
    glGetShaderiv(vertexShader, GL_COMPILE_STATUS, &success);
    if(!success)
    {
        glGetShaderInfoLog(vertexShader, 512, NULL, infoLog);
        std::cout << "ERROR::SHADER::VERTEX::COMPILATION_FAILED\n" << infoLog << std::endl;
    }

    unsigned int greenFragmentShader;
    greenFragmentShader = glCreateShader(GL_FRAGMENT_SHADER);
    glShaderSource(greenFragmentShader, 1, &greenFragmentShaderSource, NULL);
    glCompileShader(greenFragmentShader);

    unsigned int whiteFragmentShader;
    whiteFragmentShader = glCreateShader(GL_FRAGMENT_SHADER);
    glShaderSource(whiteFragmentShader, 1, &whiteFragmentShaderSource, NULL);
    glCompileShader(whiteFragmentShader);

    glGetProgramiv(whiteFragmentShader, GL_LINK_STATUS, &success);
    if(!success) {
        glGetProgramInfoLog(whiteFragmentShader, 512, NULL, infoLog);
        std::cout << "ERROR::SHADER LINK FAILED\n" << infoLog << std::endl;

    }
    unsigned int greenShaderProgram;
    greenShaderProgram = glCreateProgram();
    glAttachShader(greenShaderProgram, vertexShader);
    glAttachShader(greenShaderProgram, greenFragmentShader);
    glLinkProgram(greenShaderProgram);

    unsigned int whiteShaderProgram;
    whiteShaderProgram = glCreateProgram();
    glAttachShader(whiteShaderProgram, vertexShader);
    glAttachShader(whiteShaderProgram, whiteFragmentShader);
    glLinkProgram(whiteShaderProgram);


    glGetProgramiv(whiteShaderProgram, GL_LINK_STATUS, &success);
    if(!success) {
        glGetProgramInfoLog(whiteShaderProgram, 512, NULL, infoLog);
        std::cout << "ERROR::SHADER LINK FAILED\n" << infoLog << std::endl;

    }

    glUseProgram(whiteShaderProgram);
    glDeleteShader(vertexShader);
    glDeleteShader(greenFragmentShader);
    glDeleteShader(whiteFragmentShader);


    int t = 0;
    while(!glfwWindowShouldClose(window))
    {
        t++;
        if (t % 50 == 0)
            std::cout << t << std::endl;
        processInput(window);

        float timeValue = glfwGetTime();
        float greenValue = (sin(timeValue) / 2.0f) + 0.5f;
        int vertexColorLocation = glGetUniformLocation(greenShaderProgram, "vertexColor");
        glUseProgram(greenShaderProgram);
        glUniform4f(vertexColorLocation, 0.0f, greenValue, 0.0f, 1.0f);

        // float r = (1 + std::sin(t/10.0f)) / 2.0f;
        // float g = (1 + std::cos(t/200.0f)+1) / 2.0f;
        // float b = (1 + std::sin(t/400.0f)+2) / 2.0f;
        float r = 0.0f; float g = 0.0f; float b = 0.0f;
        glClearColor(r, g, b, 1.0f);
        glClear(GL_COLOR_BUFFER_BIT);

        glUseProgram(greenShaderProgram);
        // glPolygonMode(GL_FRONT_AND_BACK, GL_LINE);
        // or fill: glPolygonMode(GL_FRONT_AND_BACK, GL_FILL);
        glBindVertexArray(VAO);
        glDrawArrays(GL_TRIANGLES, 0, 3);

        glUseProgram(whiteShaderProgram);
        // draw EBO object (Element Buffer Object)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO);
        glDrawElements(GL_TRIANGLES, 3, GL_UNSIGNED_INT, 0);


        glDrawElements(GL_TRIANGLES, 3, GL_UNSIGNED_INT, (void *)7);
        glBindVertexArray(0);

        glfwSwapBuffers(window);
        glfwPollEvents();
    }

    glfwTerminate();
    return 0;
}
