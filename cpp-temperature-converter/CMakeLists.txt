cmake_minimum_required(VERSION 3.21)
project(temperature_converter LANGUAGES CXX)

include(FetchContent)
# Slint is built from source, which requires a Rust toolchain. This also makes the
# SLINT_FEATURE_SYSTEM_TESTING option available: the UI tests set it to ON when
# configuring, see tests/conftest.py.
FetchContent_Declare(
    Slint
    GIT_REPOSITORY https://github.com/slint-ui/slint.git
    GIT_TAG release/1
    GIT_SHALLOW TRUE
    SOURCE_SUBDIR api/cpp
)
FetchContent_MakeAvailable(Slint)

add_executable(temperature_converter main.cpp)
target_compile_features(temperature_converter PRIVATE cxx_std_20)
target_link_libraries(temperature_converter PRIVATE Slint::Slint)
slint_target_sources(temperature_converter ui/app-window.slint)

# On Windows, copy the Slint DLL next to the application binary so that it's found.
if (WIN32)
    add_custom_command(TARGET temperature_converter POST_BUILD
        COMMAND ${CMAKE_COMMAND} -E copy $<TARGET_RUNTIME_DLLS:temperature_converter> $<TARGET_FILE_DIR:temperature_converter>
        COMMAND_EXPAND_LISTS)
endif()
