#pragma once

#include <memory>
#include <print>
#include <string>

#define GLFW_INCLUDE_NONE
#include <GLFW/glfw3.h>
#define GLFW_EXPOSE_NATIVE_COCOA
#include <GLFW/glfw3native.h>

#include <Foundation/Foundation.hpp>
#include <Metal/Metal.hpp>
#include <QuartzCore/QuartzCore.hpp>

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
    NS::SharedPtr<CA::MetalLayer> mLayer;
    id mMetalWindow = nullptr;
};
