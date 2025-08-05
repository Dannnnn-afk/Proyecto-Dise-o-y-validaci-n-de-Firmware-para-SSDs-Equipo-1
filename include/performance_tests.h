#ifndef PERFORMANCE_TESTS_H
#define PERFORMANCE_TESTS_H

#include "nvme_device.h"
#include <memory>
#include <vector>
#include <chrono>

/**
 * @brief Clase para pruebas de rendimiento de dispositivos NVMe
 * 
 * Implementa diferentes tipos de pruebas de rendimiento incluyendo
 * throughput, latencia, IOPS, y patrones de acceso variados.
 */
class PerformanceTests {
public:
    struct PerformanceResult {
        double read_throughput_mbps;
        double write_throughput_mbps;
        double read_iops;
        double write_iops;
        double avg_read_latency_us;
        double avg_write_latency_us;
        double max_read_latency_us;
        double max_write_latency_us;
        double min_read_latency_us;
        double min_write_latency_us;
    };

    struct TestConfig {
        size_t block_size = 4096;
        size_t queue_depth = 32;
        size_t test_duration_seconds = 60;
        size_t data_size_mb = 1024;
        bool use_direct_io = true;
        bool verify_data = false;
    };

    PerformanceTests(std::shared_ptr<NVMeDevice> device);
    ~PerformanceTests();

    // Pruebas de throughput
    PerformanceResult test_sequential_read(const TestConfig& config);
    PerformanceResult test_sequential_write(const TestConfig& config);
    PerformanceResult test_random_read(const TestConfig& config);
    PerformanceResult test_random_write(const TestConfig& config);
    PerformanceResult test_mixed_workload(const TestConfig& config, double read_percentage = 70.0);

    // Pruebas de latencia
    PerformanceResult test_read_latency(size_t block_size = 4096, size_t sample_count = 10000);
    PerformanceResult test_write_latency(size_t block_size = 4096, size_t sample_count = 10000);

    // Pruebas de IOPS
    PerformanceResult test_4k_random_read_iops(int duration_seconds = 30);
    PerformanceResult test_4k_random_write_iops(int duration_seconds = 30);

    // Pruebas de escalabilidad
    std::vector<PerformanceResult> test_queue_depth_scaling(const std::vector<size_t>& queue_depths);
    std::vector<PerformanceResult> test_block_size_scaling(const std::vector<size_t>& block_sizes);

    // Utilidades
    void set_progress_callback(std::function<void(double)> callback);
    void stop_current_test();

private:
    std::shared_ptr<NVMeDevice> device_;
    std::function<void(double)> progress_callback_;
    bool stop_requested_;
    
    std::vector<uint8_t> generate_test_pattern(size_t size, uint32_t seed = 0x12345678);
    bool verify_test_pattern(const std::vector<uint8_t>& data, uint32_t seed = 0x12345678);
    double measure_latency(std::function<bool()> operation);
    
    // Estadísticas
    class LatencyStats {
    public:
        void add_sample(double latency_us);
        double get_average() const;
        double get_min() const;
        double get_max() const;
        double get_percentile(double percentile) const;
        size_t get_sample_count() const;
        void reset();
        
    private:
        std::vector<double> samples_;
        double sum_;
        double min_;
        double max_;
    };
};

#endif // PERFORMANCE_TESTS_H
