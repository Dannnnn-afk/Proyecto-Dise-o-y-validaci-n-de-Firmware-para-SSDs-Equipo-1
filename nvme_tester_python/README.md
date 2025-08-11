# NVMe Tester Python

Aplicación para testing de memorias NVMe desarrollada en Python. Este proyecto permite ejecutar pruebas de funcionalidad y rendimiento en dispositivos de almacenamiento NVMe.

## 📋 Requisitos del Sistema

### Herramientas del Sistema
- **Ubuntu 24.04.2 LTS** (o distribución compatible)
- **nvme-cli** - Herramientas de línea de comandos para NVMe
- **Python 3.12+** - Intérprete de Python

### Dependencias de Python
Las dependencias se encuentran listadas en `requirements.txt`:
- `pytest` - Framework de testing
- `pytest-html` - Generación de reportes HTML para pytest
- `colorama` - Colores en terminal multiplataforma
- `rich` - Salida formateada y rica en consola

## 🚀 Instalación

### 1. Instalar herramientas del sistema
```bash
sudo apt update
sudo apt install -y nvme-cli
```

### 2. Configurar entorno Python
```bash
# Crear entorno virtual (opcional pero recomendado)
python3 -m venv .venv
source .venv/bin/activate  # En Linux/Mac

# Instalar dependencias
pip install -r requirements.txt
```

### 3. Verificar instalación
```bash
# Verificar nvme-cli
nvme --version

# Verificar Python
python3 --version
```

## 📁 Estructura del Proyecto

```
nvme_tester_python/
├── main.py                    # Punto de entrada principal
├── requirements.txt           # Dependencias de Python
├── README.md                 # Este archivo
├── config/                   # Archivos de configuración
├── docs/                     # Documentación
├── logs/                     # Archivos de log de pruebas
├── src/                      # Código fuente principal
│   ├── admin_passthru_wrappper.py  # Wrapper para comandos admin-passthru
│   ├── error_report.py       # Manejo de reportes de errores
│   ├── logger.py            # Sistema de logging
│   ├── nvme_wrapper.py      # Wrapper para comandos NVMe
│   └── test_manager.py      # Gestor de pruebas
├── tests/                    # Casos de prueba
│   ├── test_id_control.py   # Pruebas de ID control
│   ├── test_smart_log.py    # Pruebas de SMART log
│   ├── test_smart_log_healt.py  # Pruebas de salud SMART
│   └── test_other.py        # Otras pruebas
└── utils/                    # Utilidades auxiliares
    ├── get_features_wrapper.py
    ├── get_ID_NS_.py
    └── get_smart_log.py
```

## 🧪 Ejecutar Pruebas

### Ejecutar prueba específica (SMART Log)
```bash
# Método 1: A través del TestManager (Recomendado)
python3 -c "from src.test_manager import TestManager; test = TestManager('PHA42142004Y1P2A', 'test_smart_log'); test.run() if test.test is not None else print('Test initialization failed')"

# Método 2: Con pytest
pytest tests/test_smart_log.py -v

# Método 3: Ejecutar directamente
python3 -m tests.test_smart_log
```

### Ejecutar todas las pruebas
```bash
pytest tests/ -v --html=reports/test_report.html
```

## 📊 Pruebas Disponibles

- **test_id_control** - Pruebas de identificación y control del dispositivo
- **test_smart_log** - Pruebas de registro SMART y temperatura
- **test_smart_log_healt** - Pruebas de salud del dispositivo

## 📝 Logs

Los archivos de log se generan automáticamente en el directorio `logs/` con timestamps:
- `nvme_smart_test_YYYYMMDD_HHMMSS.log`
- `quick_test_YYYYMMDD_HHMMSS.log`
- `test_con_errores_YYYYMMDD_HHMMSS.log`

## ⚙️ Configuración

El proyecto utiliza variables de configuración que pueden ajustarse en:
- Archivos en `config/`
- Variables en `src/test_manager.py`

## 🔧 Desarrollo

### Estructura de una prueba
```python
class NuevaPrueba:
    def __init__(self, nvme_wrapper, logger):
        self.nvme_wrapper = nvme_wrapper
        self.logger = logger
    
    def run(self):
        self.logger.log_test_start("nueva_prueba")
        # Lógica de la prueba
        self.logger.log_test_end("nueva_prueba", "PASS/FAIL")
        return resultado
```

### Agregar nueva prueba
1. Crear archivo en `tests/`
2. Implementar la clase de prueba
3. Agregar al `tests_pool` en `src/test_manager.py`

## 📞 Soporte

Para reportar problemas o solicitar funcionalidades, revisa los logs en el directorio `logs/` y proporciona la información relevante.

## 📄 Licencia

[Especificar licencia del proyecto]