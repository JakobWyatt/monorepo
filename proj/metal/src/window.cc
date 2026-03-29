#include "window.h"

GLFWContext::~GLFWContext()
{
    if (mOwning) {
        glfwTerminate();
    }
}

std::optional<GLFWContext> GLFWContext::Create()
{
    glfwSetErrorCallback(OnError);
    if (!glfwInit()) {
        return std::nullopt;
    }
    return GLFWContext();
}

void GLFWContext::OnError(int error, char const* description)
{
    std::println("GLFW Error: ({}) {}", error, description);
}

GLFWContext::GLFWContext(GLFWContext&& other) noexcept
    : mOwning(std::exchange(other.mOwning, false))
{
}

GLFWContext& GLFWContext::operator=(GLFWContext&& other) noexcept
{
    if (this != &other) {
        if (mOwning) {
            glfwTerminate();
        }
        mOwning = std::exchange(other.mOwning, false);
    }
    return *this;
}

std::optional<Window> Window::Create(GLFWContext const&)
{
    Window window;
    window.mWindow.reset(glfwCreateWindow(WIDTH, HEIGHT, TITLE.c_str(), nullptr, nullptr));
    if (!window.mWindow) {
        return std::nullopt;
    }
    return window;
}
