#ifndef TEST_MANAGER_H
#define TEST_MANAGER_H

#include "nvme_device.h"
#include "performance_tests.h"
#include "reliability_tests.h"
#include "logger.h"
#include "config_manager.h"
#include "report_generator.h"
#include <memory>
#include <vector>
#include <string>

/**
 * @brief Gestor principal de pruebas para dispositivos NVMe
 * 
 * Esta clase coordina la ejecución de diferentes tipos de pruebas
 * y gestiona el flujo general de testing.
 */
class TestManager {
public:
    enum class TestType {
        PERFORMANCE,
        RELIABILITY,
        ENDURANCE,
        POWER,
        COMPATIBILITY,
        ALL
    };

    enum class TestResult {
        PASSED,
        FAILED,
        WARNING,
        SKIPPED
    };

    struct TestSummary {
        std::string test_name;
        TestType type;
        TestResult result;
        std::string description;
        double duration_seconds;
        std::vector<std::string> details;
    };

    TestManager();
    ~TestManager();

    // Configuración
    bool initialize(const std::string& config_file = "");
    bool add_device(const std::string& device_path);
    void set_output_directory(const std::string& output_dir);
    void set_test_duration(int seconds);
    void set_verbose_mode(bool verbose);

    // Ejecución de pruebas
    bool run_tests(TestType test_type = TestType::ALL);
    bool run_specific_test(const std::string& test_name);
    
    // Pruebas individuales
    bool run_performance_tests();
    bool run_reliability_tests();
    bool run_endurance_tests();
    bool run_power_tests();
    bool run_compatibility_tests();

    // Resultados
    std::vector<TestSummary> get_test_results() const;
    bool generate_report(const std::string& format = "html");
    void print_summary() const;

    // Control de ejecución
    void stop_tests();
    bool is_running() const;
    double get_progress() const;

private:
    std::vector<std::shared_ptr<NVMeDevice>> devices_;
    std::unique_ptr<PerformanceTests> performance_tests_;
    std::unique_ptr<ReliabilityTests> reliability_tests_;
    std::unique_ptr<Logger> logger_;
    std::unique_ptr<ConfigManager> config_manager_;
    std::unique_ptr<ReportGenerator> report_generator_;
    
    std::vector<TestSummary> test_results_;
    std::string output_directory_;
    int test_duration_seconds_;
    bool verbose_mode_;
    bool running_;
    bool stop_requested_;
    
    void setup_logger();
    bool validate_devices();
    void cleanup();
};

#endif // TEST_MANAGER_H
