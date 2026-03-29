#include "window.h"

int main()
{
    auto ctx = GLFWContext::Create();
    if (!ctx) {
        std::abort();
    }
    auto window = Window::Create(*ctx);
}
