cmake_minimum_required(VERSION 4.1.2)

project(metal CXX)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

set(CMAKE_CXX_STANDARD 23)

find_package(glfw3 CONFIG REQUIRED)
find_package(metal-cpp CONFIG REQUIRED)

file(GLOB_RECURSE SOURCES "src/*.cc")
add_executable(metal ${SOURCES} src/shim.mm)

set_source_files_properties(src/shim.mm
    PROPERTIES COMPILE_FLAGS "-x objective-c++"
)

target_link_libraries(metal PRIVATE
	glfw
	metal-cpp::metal-cpp
)
