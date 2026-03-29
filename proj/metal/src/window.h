#pragma once

#include <memory>
#include <optional>
#include <print>
#include <string>

#include <GLFW/glfw3.h>

constexpr int WIDTH = 640;
constexpr int HEIGHT = 480;
constexpr std::string TITLE = "Metal";

class GLFWContext {
public:
    ~GLFWContext();

    static std::optional<GLFWContext> Create();

    GLFWContext(GLFWContext const&) = delete;
    GLFWContext& operator=(GLFWContext const&) = delete;

    GLFWContext(GLFWContext&&) noexcept;
    GLFWContext& operator=(GLFWContext&&) noexcept;

private:
    GLFWContext() = default;
    static void OnError(int, char const*);

    bool mOwning = true;
};

class Window {
public:
    static std::optional<Window> Create(GLFWContext const&);

private:
    std::unique_ptr<GLFWwindow, decltype(&glfwDestroyWindow)> mWindow { nullptr, glfwDestroyWindow };
};
