# Arquitectura del NVMe Tester

## Resumen de la Arquitectura

El NVMe Tester está diseñado con una arquitectura modular y escalable que separa claramente las responsabilidades y permite fácil mantenimiento y extensión.

## Componentes Principales

### 1. **Capa de Aplicación (`main.cpp`)**
- Punto de entrada de la aplicación
- Procesamiento de argumentos de línea de comandos
- Inicialización y coordinación de componentes
- Manejo de excepciones de alto nivel

### 2. **Gestor de Pruebas (`TestManager`)**
- **Responsabilidad**: Coordinación general de todas las pruebas
- **Funcionalidades**:
  - Gestión del ciclo de vida de las pruebas
  - Coordinación entre diferentes tipos de test
  - Control de progreso y cancelación
  - Generación de reportes finales

### 3. **Capa de Dispositivo (`NVMeDevice`)**
- **Responsabilidad**: Abstracción del hardware NVMe
- **Funcionalidades**:
  - Inicialización y configuración de dispositivos
  - Operaciones básicas de I/O
  - Acceso a información SMART
  - Control de energía

### 4. **Módulos de Pruebas**

#### 4.1 **Pruebas de Rendimiento (`PerformanceTests`)**
- Tests de throughput secuencial y aleatorio
- Medición de latencia y IOPS
- Pruebas de escalabilidad
- Análisis de patrones de acceso

#### 4.2 **Pruebas de Confiabilidad (`ReliabilityTests`)**
- Verificación de integridad de datos
- Simulación de condiciones adversas
- Pruebas de resistencia
- Monitoreo SMART

### 5. **Capa de E/S (`IOOperations`)**
- **Responsabilidad**: Operaciones de bajo nivel
- **Funcionalidades**:
  - E/O síncrona y asíncrona
  - Gestión de colas
  - Estadísticas de rendimiento
  - Control de alineación de memoria

### 6. **Interfaz del Sistema (`SystemInterface`)**
- **Responsabilidad**: Interacción con el SO
- **Funcionalidades**:
  - Detección automática de dispositivos
  - Verificación de permisos
  - Configuración del sistema
  - Monitoreo de recursos

### 7. **Servicios de Apoyo**

#### 7.1 **Logger**
- Sistema de logging thread-safe
- Múltiples niveles de severidad
- Rotación automática de archivos
- Salida a consola y archivo

#### 7.2 **ConfigManager**
- Gestión de configuración flexible
- Soporte para JSON/YAML
- Validación de configuración
- Configuración por defecto

#### 7.3 **ReportGenerator**
- Generación de reportes en múltiples formatos
- Creación de gráficos y visualizaciones
- Exportación de datos brutos
- Templates personalizables

## Flujo de Ejecución

```
1. Inicialización de la aplicación
   ├── Procesamiento de argumentos
   ├── Configuración del logger
   └── Carga de configuración

2. Preparación de dispositivos
   ├── Detección automática (opcional)
   ├── Validación de permisos
   ├── Inicialización de dispositivos
   └── Verificación de compatibilidad

3. Ejecución de pruebas
   ├── Configuración de parámetros
   ├── Ejecución secuencial/paralela
   ├── Monitoreo de progreso
   └── Recolección de resultados

4. Generación de reportes
   ├── Agregación de datos
   ├── Análisis estadístico
   ├── Creación de visualizaciones
   └── Exportación en formato deseado

5. Limpieza y finalización
   ├── Liberación de recursos
   ├── Resumen en consola
   └── Logging final
```

## Principios de Diseño

### 1. **Separación de Responsabilidades**
- Cada clase tiene una responsabilidad específica y bien definida
- Interfaces claras entre componentes
- Bajo acoplamiento entre módulos

### 2. **Escalabilidad**
- Fácil adición de nuevos tipos de pruebas
- Soporte para múltiples dispositivos simultáneos
- Configuración flexible

### 3. **Robustez**
- Manejo exhaustivo de errores
- Logging detallado para debugging
- Validación de entrada
- Recovery automático cuando sea posible

### 4. **Rendimiento**
- E/O asíncrona para máximo throughput
- Uso eficiente de memoria
- Paralelización donde sea apropiado
- Caching inteligente

### 5. **Mantenibilidad**
- Código autodocumentado
- Tests unitarios e integración
- Documentación completa
- Estándares de codificación consistentes

## Patrones de Diseño Utilizados

### 1. **Singleton** (Logger)
- Garantiza una instancia única del logger
- Acceso global thread-safe

### 2. **Strategy** (Tipos de Pruebas)
- Permite intercambiar algoritmos de testing
- Fácil extensión con nuevos tipos

### 3. **Factory** (Creación de Dispositivos)
- Encapsula la lógica de creación
- Soporte para diferentes tipos de dispositivo

### 4. **Observer** (Progress Callbacks)
- Notificación de progreso
- Desacoplamiento entre pruebas y UI

### 5. **Template Method** (Estructura de Pruebas)
- Define el esqueleto de ejecución
- Permite personalización específica

## Consideraciones de Threading

### Thread Safety
- Logger es completamente thread-safe
- IOOperations maneja concurrencia internamente
- ConfigManager es read-only después de inicialización
- Estadísticas protegidas con mutex

### Paralelización
- Pruebas pueden ejecutarse en paralelo (opcional)
- E/O asíncrona para máximo rendimiento
- Worker threads para tareas CPU-intensivas

## Extensibilidad

### Agregar Nuevos Tipos de Pruebas
1. Crear nueva clase heredando de base común
2. Implementar interfaz estándar
3. Registrar en TestManager
4. Añadir configuración correspondiente

### Soporte para Nuevos Formatos de Reporte
1. Extender ReportGenerator
2. Implementar nuevo formato
3. Añadir a enumeración de formatos
4. Actualizar configuración

### Nuevos Tipos de Dispositivo
1. Extender o especializar NVMeDevice
2. Implementar interfaz específica
3. Registrar en factory
4. Añadir detección automática

## Métricas y Monitoreo

### Logging
- Eventos de sistema
- Errores y warnings
- Métricas de rendimiento
- Progreso de pruebas

### Estadísticas
- Contadores de operaciones
- Tiempos de ejecución
- Uso de recursos
- Resultados de pruebas

### Alertas
- Condiciones de error
- Umbrales de rendimiento
- Estado de dispositivos
- Problemas de sistema
