#ifndef RELIABILITY_TESTS_H
#define RELIABILITY_TESTS_H


#include "nvme_device.h"
#include <memory>
#include <vector>
#include <string>

/**
 * @brief Clase para pruebas de confiabilidad y integridad de datos
 * 
 * Implementa pruebas para verificar la integridad de los datos,
 * resistencia a fallos y comportamiento bajo condiciones adversas.
 */
class ReliabilityTests {
public:
    struct ReliabilityResult {
        bool passed;
        std::string test_name;
        std::string description;
        size_t errors_detected;
        size_t data_corruptions;
        double error_rate;
        std::vector<std::string> error_details;
    };

    ReliabilityTests(std::shared_ptr<NVMeDevice> device);
    ~ReliabilityTests();

    // Pruebas de integridad de datos
    ReliabilityResult test_data_integrity_simple();
    ReliabilityResult test_data_integrity_complex_patterns();
    ReliabilityResult test_data_persistence();
    ReliabilityResult test_write_read_verify_cycles(size_t cycle_count = 1000);

    // Pruebas de resistencia
    ReliabilityResult test_power_loss_simulation();
    ReliabilityResult test_unexpected_disconnection();
    ReliabilityResult test_thermal_stress();

    // Pruebas de límites
    ReliabilityResult test_boundary_conditions();
    ReliabilityResult test_maximum_lba_access();
    ReliabilityResult test_concurrent_access();

    // Pruebas de recuperación
    ReliabilityResult test_error_recovery();
    ReliabilityResult test_bad_block_handling();
    ReliabilityResult test_wear_leveling_verification();

    // Pruebas de SMART
    ReliabilityResult test_smart_attributes();
    ReliabilityResult test_smart_thresholds();
    ReliabilityResult test_smart_error_log();

    // Utilidades
    void set_progress_callback(std::function<void(double)> callback);
    void stop_current_test();

private:
    std::shared_ptr<NVMeDevice> device_;
    std::function<void(double)> progress_callback_;
    bool stop_requested_;
    
    // Patrones de datos para pruebas
    std::vector<uint8_t> create_walking_ones_pattern(size_t size);
    std::vector<uint8_t> create_walking_zeros_pattern(size_t size);
    std::vector<uint8_t> create_checkerboard_pattern(size_t size);
    std::vector<uint8_t> create_random_pattern(size_t size, uint32_t seed);
    std::vector<uint8_t> create_address_pattern(size_t size, uint64_t base_address);
    
    // Verificación de patrones
    bool verify_pattern(const std::vector<uint8_t>& data, const std::vector<uint8_t>& expected);
    
    // Simulación de condiciones adversas
    bool simulate_power_interruption();
    bool simulate_thermal_condition(int temperature_celsius);
    
    // Análisis de errores
    void analyze_data_corruption(const std::vector<uint8_t>& expected, 
                                const std::vector<uint8_t>& actual,
                                ReliabilityResult& result);
    
    // Estadísticas de errores
    struct ErrorStatistics {
        size_t bit_errors;
        size_t byte_errors;
        size_t block_errors;
        std::vector<size_t> error_positions;
        
        void add_bit_error(size_t position);
        void add_byte_error(size_t position);
        void add_block_error(size_t position);
        void reset();
    };
};

#endif // RELIABILITY_TESTS_H
