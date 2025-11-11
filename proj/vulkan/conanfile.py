from conan import ConanFile
from conan.tools.cmake import CMake, cmake_layout, CMakeDeps, CMakeToolchain


class VulkanAppConan(ConanFile):
    name = "vulkan-app"
    version = "0.0.0"
    settings = "os", "compiler", "build_type", "arch"

    def layout(self):
        cmake_layout(self)

    def requirements(self):
        self.requires("glfw/3.4")
        self.requires("vulkan-loader/1.4.313.0")

    def build_requirements(self):
        self.tool_requires("cmake/4.1.2")
        self.tool_requires("ninja/1.13.1")

    def generate(self):
        deps = CMakeDeps(self)
        deps.set_property("vulkan-loader", "cmake_file_name", "Vulkan")
        deps.set_property("vulkan-loader", "cmake_target_name", "Vulkan::Vulkan")
        deps.generate()

        tc = CMakeToolchain(self)
        tc.user_presets_path = False
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()
