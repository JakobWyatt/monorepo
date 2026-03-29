#pragma once

#include <memory>
#include <print>
#include <string>

#include <GLFW/glfw3.h>

#include <Foundation/Foundation.hpp>
#include <Metal/Metal.hpp>

constexpr int WIDTH = 640;
constexpr int HEIGHT = 480;
constexpr std::string TITLE = "Metal";

class Window {
public:
    static std::unique_ptr<Window> Create();

    Window(GLFWwindow*);
    ~Window();

    void Run();

private:
    static void OnError(int error, char const*);

    static inline bool sGlfwInitialised = false;
    std::unique_ptr<GLFWwindow, decltype(&glfwDestroyWindow)> mWindow { nullptr, glfwDestroyWindow };
    NS::SharedPtr<MTL::Device> mDevice;
};
