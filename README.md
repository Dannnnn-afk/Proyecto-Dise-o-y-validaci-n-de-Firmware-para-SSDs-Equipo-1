# NVMe Tester - Aplicación para Testing de Memorias NVMe

Una aplicación profesional en C++ para realizar pruebas exhaustivas de rendimiento, confiabilidad y durabilidad en dispositivos de almacenamiento NVMe.

## Nombres de los integrantes:

## Características

### 🚀 Pruebas de Rendimiento
- **Throughput Secuencial**: Medición de velocidades de lectura y escritura secuencial
- **IOPS Aleatorios**: Evaluación de operaciones de entrada/salida por segundo
- **Latencia**: Análisis detallado de tiempos de respuesta
- **Escalabilidad**: Pruebas con diferentes tamaños de bloque y profundidades de cola

### 🔧 Pruebas de Confiabilidad
- **Integridad de Datos**: Verificación con múltiples patrones de datos
- **Resistencia a Fallos**: Simulación de condiciones adversas
- **Monitoreo SMART**: Seguimiento de atributos de salud del dispositivo
- **Pruebas de Resistencia**: Evaluación bajo carga continua

### 📊 Generación de Reportes
- **Formatos Múltiples**: HTML, JSON, CSV
- **Gráficos Interactivos**: Visualización de resultados
- **Análisis Comparativo**: Comparación entre dispositivos
- **Exportación de Datos**: Para análisis posterior

## Estructura del Proyecto

```
nvme-tester/
├── src/                    # Código fuente principal
│   ├── main.cpp           # Punto de entrada de la aplicación
│   ├── nvme_device.cpp    # Interfaz con dispositivos NVMe
│   ├── test_manager.cpp   # Gestor principal de pruebas
│   ├── performance_tests.cpp  # Implementación de pruebas de rendimiento
│   ├── reliability_tests.cpp  # Implementación de pruebas de confiabilidad
│   ├── io_operations.cpp  # Operaciones de E/S de bajo nivel
│   ├── system_interface.cpp  # Interfaz con el sistema operativo
│   ├── logger.cpp         # Sistema de logging
│   ├── config_manager.cpp # Gestor de configuración
│   └── report_generator.cpp  # Generador de reportes
├── include/               # Archivos de cabecera
│   ├── nvme_device.h      # Definiciones para dispositivos NVMe
│   ├── test_manager.h     # Gestor de pruebas
│   ├── performance_tests.h    # Pruebas de rendimiento
│   ├── reliability_tests.h    # Pruebas de confiabilidad
│   ├── logger.h           # Sistema de logging
│   ├── config_manager.h   # Gestor de configuración
│   └── report_generator.h # Generador de reportes
├── tests/                 # Pruebas unitarias e integración
│   ├── test_nvme_device.cpp
│   ├── test_performance_tests.cpp
│   ├── test_reliability_tests.cpp
│   └── integration_tests/
├── config/                # Archivos de configuración
│   └── default_config.json
├── docs/                  # Documentación
├── build/                 # Archivos de compilación
├── CMakeLists.txt         # Configuración de construcción
├── build.sh              # Script de construcción
└── README.md             # Este archivo
```

## Requisitos del Sistema

### Hardware
- **CPU**: x86_64 o ARM64
- **RAM**: Mínimo 4GB (8GB recomendado)
- **Almacenamiento**: 1GB libre para logs y reportes
- **Dispositivos NVMe**: Uno o más dispositivos compatibles

### Software
- **SO**: Linux (Ubuntu 20.04+, CentOS 8+, Debian 11+)
- **Compilador**: GCC 9+ o Clang 10+
- **CMake**: Versión 3.16 o superior
- **Dependencias**: pthread, libnvme (opcional)

## Instalación

### 1. Clonar el Repositorio
```bash
git clone https://github.com/tu-usuario/nvme-tester.git
cd nvme-tester
```

### 2. Instalar Dependencias (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install build-essential cmake libgtest-dev libnvme-dev
```

### 3. Compilar el Proyecto
```bash
# Compilación básica
./build.sh

# Compilación con tests
./build.sh --test

# Compilación en modo debug
./build.sh --debug --test
```

### 4. Instalación Sistema (Opcional)
```bash
./build.sh --install
```

## Uso

### Uso Básico
```bash
# Probar un dispositivo NVMe
sudo ./build/nvme_tester /dev/nvme0n1

# Probar múltiples dispositivos
sudo ./build/nvme_tester /dev/nvme0n1 /dev/nvme1n1
```

### Opciones Avanzadas
```bash
# Pruebas específicas de rendimiento por 5 minutos
sudo ./build/nvme_tester -t performance -d 300 /dev/nvme0n1

# Usar archivo de configuración personalizado
sudo ./build/nvme_tester -c my_config.json --output ./results /dev/nvme0n1

# Generar reporte en formato JSON
sudo ./build/nvme_tester -f json --verbose /dev/nvme0n1
```

### Parámetros de Línea de Comandos
- `-h, --help`: Mostrar ayuda
- `-v, --verbose`: Modo verboso
- `-c, --config FILE`: Archivo de configuración
- `-o, --output DIR`: Directorio de salida
- `-t, --test TYPE`: Tipo de prueba (performance, reliability, endurance, all)
- `-d, --duration SEC`: Duración de las pruebas
- `-f, --format FORMAT`: Formato del reporte (html, json, csv)
- `-l, --list-devices`: Listar dispositivos disponibles

## Configuración

El archivo `config/default_config.json` contiene todas las configuraciones por defecto. Puedes crear tu propio archivo de configuración basado en este template.

### Ejemplo de Configuración
```json
{
  "test_config": {
    "default_test_duration": 60,
    "default_block_size": 4096,
    "enable_data_verification": true
  },
  "performance_tests": {
    "sequential_read": {
      "enabled": true,
      "block_sizes": [4096, 8192, 16384, 65536],
      "duration_seconds": 30
    }
  }
}
```

## Tipos de Pruebas

### 1. Pruebas de Rendimiento
- **Lectura/Escritura Secuencial**: Mide el throughput máximo
- **Lectura/Escritura Aleatoria**: Evalúa el rendimiento en accesos aleatorios
- **Cargas de Trabajo Mixtas**: Simulan patrones de uso real
- **Escalabilidad de Queue Depth**: Optimización de paralelismo

### 2. Pruebas de Confiabilidad
- **Integridad de Datos**: Verificación con patrones conocidos
- **Pruebas de Estrés**: Operaciones continuas bajo carga
- **Simulación de Fallos**: Recuperación ante interrupciones
- **Monitoreo SMART**: Seguimiento de métricas de salud

### 3. Pruebas de Resistencia
- **Ciclos de Escritura**: Evaluación de desgaste
- **Retención de Datos**: Persistencia a largo plazo
- **Condiciones Térmicas**: Rendimiento bajo temperatura

## Interpretación de Resultados

### Métricas de Rendimiento
- **Throughput**: MB/s para operaciones secuenciales
- **IOPS**: Operaciones por segundo para accesos aleatorios
- **Latencia**: Tiempo de respuesta en microsegundos
- **Consistencia**: Variabilidad en el rendimiento

### Indicadores de Salud
- **Temperatura**: Rango operativo normal
- **Spare Disponible**: Reserva para reemplazo de bloques
- **Porcentaje de Uso**: Vida útil consumida
- **Errores de Media**: Problemas en el almacenamiento

## Solución de Problemas

### Problemas Comunes

1. **Error de Permisos**
   ```bash
   sudo ./nvme_tester /dev/nvme0n1
   ```

2. **Dispositivo No Encontrado**
   ```bash
   # Listar dispositivos disponibles
   ./nvme_tester --list-devices
   lsblk -d -o NAME,SIZE,MODEL | grep nvme
   ```

3. **Dependencias Faltantes**
   ```bash
   # Ubuntu/Debian
   sudo apt install libnvme-dev
   
   # CentOS/RHEL
   sudo yum install nvme-cli-devel
   ```

## Desarrollo

### Compilación para Desarrollo
```bash
./build.sh --debug --test
```

### Ejecutar Tests
```bash
cd build
make test
```

### Añadir Nuevas Pruebas
1. Crear el archivo de cabecera en `include/`
2. Implementar en `src/`
3. Añadir tests en `tests/`
4. Actualizar `CMakeLists.txt`

## Contribución

1. Fork del repositorio
2. Crear rama para feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit de cambios (`git commit -am 'Añadir nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## Contacto

Para preguntas, sugerencias o reportes de bugs, por favor crear un issue en GitHub o contactar a:

- **Equipo de Desarrollo**: [emails de los integrantes]
- **Repositorio**: https://github.com/tu-usuario/nvme-tester

## Agradecimientos

- Comunidad de desarrollo de NVMe
- Desarrolladores de herramientas de testing de almacenamiento
- Contribuidores de bibliotecas de código abierto utilizadas 
