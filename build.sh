# Script de construcción para el proyecto NVMe Tester
#!/bin/bash

set -e  # Salir en caso de error

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para imprimir mensajes con color
print_message() {
    echo -e "${BLUE}[BUILD]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Verificar dependencias
check_dependencies() {
    print_message "Verificando dependencias..."
    
    # Verificar CMake
    if ! command -v cmake &> /dev/null; then
        print_error "CMake no está instalado"
        exit 1
    fi
    
    # Verificar compilador C++
    if ! command -v g++ &> /dev/null && ! command -v clang++ &> /dev/null; then
        print_error "No se encontró compilador C++"
        exit 1
    fi
    
    # Verificar make
    if ! command -v make &> /dev/null; then
        print_error "Make no está instalado"
        exit 1
    fi
    
    print_success "Todas las dependencias están disponibles"
}

# Función de limpieza
clean_build() {
    print_message "Limpiando archivos de compilación..."
    if [ -d "build" ]; then
        rm -rf build/*
        print_success "Directorio build limpiado"
    fi
}

# Función de configuración
configure_build() {
    print_message "Configurando el proyecto..."
    
    mkdir -p build
    cd build
    
    cmake .. \
        -DCMAKE_BUILD_TYPE=${BUILD_TYPE:-Release} \
        -DCMAKE_INSTALL_PREFIX=${INSTALL_PREFIX:-/usr/local} \
        -DENABLE_TESTING=${ENABLE_TESTING:-ON}
    
    cd ..
    print_success "Configuración completada"
}

# Función de compilación
build_project() {
    print_message "Compilando el proyecto..."
    
    cd build
    make -j$(nproc)
    cd ..
    
    print_success "Compilación completada"
}

# Función para ejecutar tests
run_tests() {
    print_message "Ejecutando tests..."
    
    cd build
    if make test; then
        print_success "Todos los tests pasaron"
    else
        print_warning "Algunos tests fallaron"
    fi
    cd ..
}

# Función de instalación
install_project() {
    print_message "Instalando el proyecto..."
    
    cd build
    sudo make install
    cd ..
    
    print_success "Instalación completada"
}

# Función para mostrar ayuda
show_help() {
    echo "Script de construcción para NVMe Tester"
    echo ""
    echo "Uso: $0 [OPCIONES]"
    echo ""
    echo "Opciones:"
    echo "  -h, --help           Mostrar esta ayuda"
    echo "  -c, --clean          Limpiar archivos de compilación"
    echo "  -d, --debug          Compilar en modo debug"
    echo "  -r, --release        Compilar en modo release (por defecto)"
    echo "  -t, --test           Ejecutar tests después de compilar"
    echo "  -i, --install        Instalar después de compilar"
    echo "  --no-tests           Deshabilitar compilación de tests"
    echo ""
    echo "Variables de entorno:"
    echo "  BUILD_TYPE           Tipo de compilación (Debug/Release)"
    echo "  INSTALL_PREFIX       Prefijo de instalación"
    echo "  ENABLE_TESTING       Habilitar tests (ON/OFF)"
}

# Procesar argumentos de línea de comandos
CLEAN=false
RUN_TESTS=false
INSTALL=false
BUILD_TYPE="Release"
ENABLE_TESTING="ON"

while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            show_help
            exit 0
            ;;
        -c|--clean)
            CLEAN=true
            shift
            ;;
        -d|--debug)
            BUILD_TYPE="Debug"
            shift
            ;;
        -r|--release)
            BUILD_TYPE="Release"
            shift
            ;;
        -t|--test)
            RUN_TESTS=true
            shift
            ;;
        -i|--install)
            INSTALL=true
            shift
            ;;
        --no-tests)
            ENABLE_TESTING="OFF"
            shift
            ;;
        *)
            print_error "Opción desconocida: $1"
            show_help
            exit 1
            ;;
    esac
done

# Ejecutar construcción
print_message "Iniciando construcción del proyecto NVMe Tester"
print_message "Tipo de compilación: $BUILD_TYPE"

check_dependencies

if [ "$CLEAN" = true ]; then
    clean_build
fi

configure_build
build_project

if [ "$RUN_TESTS" = true ] && [ "$ENABLE_TESTING" = "ON" ]; then
    run_tests
fi

if [ "$INSTALL" = true ]; then
    install_project
fi

print_success "Construcción completada exitosamente"
print_message "Ejecutable disponible en: build/nvme_tester"
