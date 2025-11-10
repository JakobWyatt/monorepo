cmake_minimum_required(VERSION 4.1.2)

project(vulkan CXX)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

set(CMAKE_CXX_STANDARD 23)

find_package(glfw3 CONFIG REQUIRED)
find_package(Vulkan CONFIG REQUIRED)

add_executable(vulkan src/main.cc)

target_link_libraries(vulkan PRIVATE
	glfw
	Vulkan::Vulkan
)
