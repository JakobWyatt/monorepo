#include "window.h"

void Window::OnError(int error, char const* description)
{
    std::println("GLFW Error: ({}) {}", error, description);
    std::abort();
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
    mDevice = TransferPtr(MTL::CreateSystemDefaultDevice());
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
