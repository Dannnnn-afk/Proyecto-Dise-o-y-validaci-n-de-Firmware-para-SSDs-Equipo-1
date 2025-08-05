cmake_minimum_required(VERSION 3.16)
project(NVMeTester VERSION 1.0.0 LANGUAGES CXX)

# Configuración del estándar C++
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Configuraciones de compilación
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -Wextra -Wpedantic")
set(CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_DEBUG} -g -O0 -DDEBUG")
set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -O3 -DNDEBUG")

# Directorios de inclusión
include_directories(include)

# Buscar dependencias necesarias
find_package(Threads REQUIRED)

# Subdirectorios
add_subdirectory(src)
add_subdirectory(tests)

# Crear el ejecutable principal
add_executable(nvme_tester
    src/main.cpp
    src/nvme_device.cpp
    src/test_manager.cpp
    src/performance_tests.cpp
    src/reliability_tests.cpp
    src/io_operations.cpp
    src/system_interface.cpp
    src/logger.cpp
    src/config_manager.cpp
    src/report_generator.cpp
)

# Enlazar librerías
target_link_libraries(nvme_tester
    Threads::Threads
    ${CMAKE_DL_LIBS}
)

# Configuración para instalación
install(TARGETS nvme_tester DESTINATION bin)
install(DIRECTORY config/ DESTINATION share/nvme_tester/config)
install(DIRECTORY docs/ DESTINATION share/nvme_tester/docs)
