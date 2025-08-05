
#include "/workspaces/Proyecto-Dise-o-y-validaci-n-de-Firmware-para-SSDs-Equipo-1./include/logger.h"
#include <iostream>
#include <vector>
#include <string>
#include <getopt.h>
#include "/workspaces/Proyecto-Dise-o-y-validaci-n-de-Firmware-para-SSDs-Equipo-1./include/test_manager.h"

void print_usage(const char* program_name) {
    std::cout << "Uso: " << program_name << " [OPCIONES] [DISPOSITIVOS]\n\n";
    std::cout << "Opciones:\n";
    std::cout << "  -h, --help              Mostrar esta ayuda\n";
    std::cout << "  -v, --verbose           Modo verboso\n";
    std::cout << "  -c, --config FILE       Archivo de configuración\n";
    std::cout << "  -o, --output DIR        Directorio de salida\n";
    std::cout << "  -t, --test TYPE         Tipo de prueba (performance, reliability, endurance, power, all)\n";
    std::cout << "  -d, --duration SEC      Duración de las pruebas en segundos\n";
    std::cout << "  -f, --format FORMAT     Formato del reporte (html, json, csv)\n";
    std::cout << "  -l, --list-devices      Listar dispositivos NVMe disponibles\n";
    std::cout << "\nEjemplos:\n";
    std::cout << "  " << program_name << " /dev/nvme0n1\n";
    std::cout << "  " << program_name << " -t performance -d 300 /dev/nvme0n1\n";
    std::cout << "  " << program_name << " --config tests.conf --output results /dev/nvme0n1 /dev/nvme1n1\n";
}

void list_nvme_devices() {
    // TODO: Implementar detección automática de dispositivos NVMe
    std::cout << "Dispositivos NVMe detectados:\n";
    std::cout << "  /dev/nvme0n1 - Samsung SSD 980 PRO 1TB\n";
    std::cout << "  /dev/nvme1n1 - WD Black SN850 2TB\n";
}

TestManager::TestType parse_test_type(const std::string& type_str) {
    if (type_str == "performance") return TestManager::TestType::PERFORMANCE;
    if (type_str == "reliability") return TestManager::TestType::RELIABILITY;
    if (type_str == "endurance") return TestManager::TestType::ENDURANCE;
    if (type_str == "power") return TestManager::TestType::POWER;
    if (type_str == "compatibility") return TestManager::TestType::COMPATIBILITY;
    if (type_str == "all") return TestManager::TestType::ALL;
    
    std::cerr << "Tipo de prueba desconocido: " << type_str << std::endl;
    return TestManager::TestType::ALL;
}

int main(int argc, char* argv[]) {
    // Configuración por defecto
    std::string config_file;
    std::string output_dir = "./results";
    std::string test_type_str = "all";
    std::string report_format = "html";
    int test_duration = 60;
    bool verbose = false;
    bool list_devices = false;
    
    // Opciones de línea de comandos
    static struct option long_options[] = {
        {"help",         no_argument,       0, 'h'},
        {"verbose",      no_argument,       0, 'v'},
        {"config",       required_argument, 0, 'c'},
        {"output",       required_argument, 0, 'o'},
        {"test",         required_argument, 0, 't'},
        {"duration",     required_argument, 0, 'd'},
        {"format",       required_argument, 0, 'f'},
        {"list-devices", no_argument,       0, 'l'},
        {0, 0, 0, 0}
    };
    
    int option_index = 0;
    int c;
    
    while ((c = getopt_long(argc, argv, "hvc:o:t:d:f:l", long_options, &option_index)) != -1) {
        switch (c) {
            case 'h':
                print_usage(argv[0]);
                return 0;
            case 'v':
                verbose = true;
                break;
            case 'c':
                config_file = optarg;
                break;
            case 'o':
                output_dir = optarg;
                break;
            case 't':
                test_type_str = optarg;
                break;
            case 'd':
                test_duration = std::atoi(optarg);
                break;
            case 'f':
                report_format = optarg;
                break;
            case 'l':
                list_devices = true;
                break;
            case '?':
                print_usage(argv[0]);
                return 1;
            default:
                break;
        }
    }
    
    if (list_devices) {
        list_nvme_devices();
        return 0;
    }
    
    // Verificar que se especificaron dispositivos
    if (optind >= argc) {
        std::cerr << "Error: Debe especificar al menos un dispositivo NVMe\n";
        print_usage(argv[0]);
        return 1;
    }
    
    // Configurar logger
    Logger& logger = Logger::getInstance();
    logger.set_log_level(verbose ? Logger::LogLevel::DEBUG : Logger::LogLevel::INFO);
    logger.enable_console_output(true);
    logger.enable_timestamps(true);
    
    try {
        // Crear el gestor de pruebas
        TestManager test_manager;
        
        // Inicializar con archivo de configuración si se especificó
        if (!test_manager.initialize(config_file)) {
            LOG_ERROR("Error al inicializar el gestor de pruebas");
            return 1;
        }
        
        // Configurar parámetros
        test_manager.set_output_directory(output_dir);
        test_manager.set_test_duration(test_duration);
        test_manager.set_verbose_mode(verbose);
        
        // Agregar dispositivos
        for (int i = optind; i < argc; i++) {
            std::string device_path = argv[i];
            LOG_INFO_F("Agregando dispositivo: %s", device_path.c_str());
            
            if (!test_manager.add_device(device_path)) {
                LOG_ERROR_F("Error al agregar dispositivo: %s", device_path.c_str());
                return 1;
            }
        }
        
        // Ejecutar pruebas
        TestManager::TestType test_type = parse_test_type(test_type_str);
        LOG_INFO_F("Iniciando pruebas de tipo: %s", test_type_str.c_str());
        
        if (!test_manager.run_tests(test_type)) {
            LOG_ERROR("Error durante la ejecución de las pruebas");
            return 1;
        }
        
        // Generar reporte
        LOG_INFO("Generando reporte de resultados...");
        if (!test_manager.generate_report(report_format)) {
            LOG_WARNING("Error al generar el reporte");
        }
        
        // Mostrar resumen
        test_manager.print_summary();
        
        LOG_INFO("Pruebas completadas exitosamente");
        return 0;
        
    } catch (const std::exception& e) {
        LOG_CRITICAL_F("Excepción no manejada: %s", e.what());
        return 1;
    } catch (...) {
        LOG_CRITICAL("Excepción desconocida");
        return 1;
    }
}
