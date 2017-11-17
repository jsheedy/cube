hello-models: hello-models.cpp shaders/models.vs shaders/models.fs
	g++ `pkg-config --cflags glfw3` -o hello-models hello-models.cpp glad.c -lassimp `pkg-config --static --libs glfw3` -I .