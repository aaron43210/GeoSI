cmake_minimum_required(VERSION 3.18)
project(geosi_chunker VERSION 1.0.0 LANGUAGES CXX)

# ── C++17 required for std::string_view ──────────────────────────────────────
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# ── Aggressive optimisation ───────────────────────────────────────────────────
if(NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE Release)
endif()

add_compile_options(
    -O3           # Maximum optimisation
    -march=native # Use all CPU features available on the build machine
    -Wall
    -Wextra
    -Wpedantic
)

# ── pybind11 ─────────────────────────────────────────────────────────────────
# Find pybind11 via pip-installed package first, then system install
find_package(pybind11 CONFIG QUIET)
if(NOT pybind11_FOUND)
    execute_process(
        COMMAND "${Python_EXECUTABLE}" -m pybind11 --cmakedir
        OUTPUT_VARIABLE PYBIND11_CMAKE_DIR
        OUTPUT_STRIP_TRAILING_WHITESPACE
    )
    find_package(pybind11 CONFIG REQUIRED HINTS "${PYBIND11_CMAKE_DIR}")
endif()

# ── Extension module ─────────────────────────────────────────────────────────
pybind11_add_module(
    geosi_chunker
    THIN_LTO          # Link-time optimisation for smaller binary
    geosi_rag/chunker_ext.cpp
)

# Strip debug symbols in release builds to reduce .so size
if(CMAKE_BUILD_TYPE STREQUAL "Release")
    if(APPLE)
        target_link_options(geosi_chunker PRIVATE -Wl,-x)
    elseif(UNIX)
        target_link_options(geosi_chunker PRIVATE -Wl,--strip-all)
    endif()
endif()

# Install into geosi_rag/ so Python can import it as geosi_rag.geosi_chunker
install(TARGETS geosi_chunker DESTINATION geosi_rag)
