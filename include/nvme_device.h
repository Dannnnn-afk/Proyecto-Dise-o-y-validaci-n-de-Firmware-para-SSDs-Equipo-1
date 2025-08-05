#ifndef NVME_DEVICE_H
#define NVME_DEVICE_H

#include <string>
#include <vector>
#include <memory>
#include <cstdint>

/**
 * @brief Clase para manejar dispositivos NVMe
 * 
 * Esta clase encapsula las operaciones básicas de un dispositivo NVMe,
 * incluyendo identificación, configuración y acceso de bajo nivel.
 */
class NVMeDevice {
public:
    struct DeviceInfo {
        std::string model;
        std::string serial;
        std::string firmware_version;
        uint64_t capacity_bytes;
        uint32_t block_size;
        uint32_t max_lba;
        bool smart_enabled;
    };

    struct SmartData {
        uint8_t critical_warning;
        uint16_t temperature;
        uint8_t available_spare;
        uint8_t available_spare_threshold;
        uint8_t percentage_used;
        uint64_t data_units_read[2];
        uint64_t data_units_written[2];
        uint64_t host_read_commands[2];
        uint64_t host_write_commands[2];
        uint64_t controller_busy_time[2];
        uint64_t power_cycles[2];
        uint64_t power_on_hours[2];
        uint64_t unsafe_shutdowns[2];
        uint64_t media_errors[2];
        uint64_t error_log_entries[2];
    };

    NVMeDevice(const std::string& device_path);
    ~NVMeDevice();

    // Operaciones básicas
    bool initialize();
    bool is_connected() const;
    void disconnect();

    // Información del dispositivo
    DeviceInfo get_device_info() const;
    SmartData get_smart_data() const;
    
    // Operaciones I/O
    bool read_blocks(uint64_t lba, uint32_t block_count, void* buffer);
    bool write_blocks(uint64_t lba, uint32_t block_count, const void* buffer);
    bool flush();
    
    // Control de energía
    bool set_power_state(uint8_t power_state);
    uint8_t get_power_state() const;
    
    // Utilidades
    std::string get_device_path() const { return device_path_; }
    bool perform_trim(uint64_t lba, uint32_t block_count);

private:
    std::string device_path_;
    int device_fd_;
    DeviceInfo device_info_;
    bool initialized_;
    
    bool send_admin_command(void* cmd, void* data = nullptr, size_t data_len = 0);
    bool send_io_command(void* cmd, void* data = nullptr, size_t data_len = 0);
};

#endif // NVME_DEVICE_H
