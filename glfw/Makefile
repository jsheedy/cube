triangle: triangle.cpp
	g++ `pkg-config --cflags glfw3` -o triangle triangle.cpp glad.c  `pkg-config --static --libs glfw3` -I .

hello-shaders: hello-shaders.cpp
	g++ `pkg-config --cflags glfw3` -o hello-shaders hello-shaders.cpp glad.c  `pkg-config --static --libs glfw3` -I .

hello-textures: hello-textures.cpp shaders/hello.vs shaders/hello.fs
	g++ `pkg-config --cflags glfw3` -o hello-textures hello-textures.cpp glad.c  `pkg-config --static --libs glfw3` -I .

hello-transformations: hello-transformations.cpp shaders/hello.vs shaders/hello.fs
	g++ `pkg-config --cflags glfw3` -o hello-transformations hello-transformations.cpp glad.c  `pkg-config --static --libs glfw3` -I .

hello-coordinate-systems: hello-coordinate-systems.cpp shaders/hello.vs shaders/hello.fs
	g++ `pkg-config --cflags glfw3` -o hello-coordinate-systems hello-coordinate-systems.cpp glad.c  `pkg-config --static --libs glfw3` -I .

hello-camera: hello-camera.cpp shaders/hello.vs shaders/hello.fs
	g++ `pkg-config --cflags glfw3` -o hello-camera hello-camera.cpp glad.c  `pkg-config --static --libs glfw3` -I .

the-cube: the-cube.cpp shaders/hello.vs shaders/hello.fs
	g++ `pkg-config --cflags glfw3` -o the-cube the-cube.cpp glad.c  `pkg-config --static --libs glfw3` -I .

hello-colors: hello-colors.cpp shaders/hello-colors.vs shaders/hello-colors.fs
	g++ `pkg-config --cflags glfw3` -o hello-colors hello-colors.cpp glad.c  `pkg-config --static --libs glfw3` -I .