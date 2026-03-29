#include "window.h"

#include "shim.h"

void Window::OnError(int error, char const* description)
{
    std::println("GLFW Error: ({}) {}", error, description);
}

std::unique_ptr<Window> Window::Create()
{
    if (!sGlfwInitialised) {
        glfwSetErrorCallback(OnError);
        if (!glfwInit()) {
            return nullptr;
        }
        sGlfwInitialised = true;
    }
    glfwWindowHint(GLFW_CLIENT_API, GLFW_NO_API);
    auto* glfwWindow = glfwCreateWindow(WIDTH, HEIGHT, TITLE.c_str(), nullptr, nullptr);
    if (!glfwWindow) {
        glfwTerminate();
        sGlfwInitialised = false;
        return nullptr;
    }
    return std::make_unique<Window>(glfwWindow);
}

Window::Window(GLFWwindow* window)
{
    mWindow.reset(window);
    mDevice = NS::TransferPtr(MTL::CreateSystemDefaultDevice());
    mLayer = NS::TransferPtr(CA::MetalLayer::layer());
    mLayer->setDevice(mDevice.get());
    mLayer->setPixelFormat(MTL::PixelFormatBGRA8Unorm);
    mMetalWindow = glfwGetCocoaWindow(mWindow.get());
    ConfigureMetalWindow(mMetalWindow, mLayer.get());
}

Window::~Window()
{
    mWindow.reset();
    if (sGlfwInitialised) {
        glfwTerminate();
        sGlfwInitialised = false;
    }
}

void Window::Run()
{
    while (!glfwWindowShouldClose(mWindow.get())) {
        glfwPollEvents();
    }
}
