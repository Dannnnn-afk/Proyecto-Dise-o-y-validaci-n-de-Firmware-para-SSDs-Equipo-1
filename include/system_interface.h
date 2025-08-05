#ifndef SYSTEM_INTERFACE_H
#define SYSTEM_INTERFACE_H

#include <string>
#include <vector>
#include <map>

/**
 * @brief Interfaz con el sistema operativo para operaciones NVMe
 * 
 * Proporciona funciones para interactuar con el kernel de Linux
 * y acceder a información específica de dispositivos NVMe.
 */
class SystemInterface {
public:
    struct SystemInfo {
        std::string kernel_version;
        std::string distribution;
        std::string architecture;
        uint64_t total_memory_kb;
        uint64_t available_memory_kb;
        std::vector<std::string> loaded_modules;
    };

    struct DeviceInfo {
        std::string device_path;
        std::string driver_name;
        std::string driver_version;
        std::string subsystem;
        std::string vendor_id;
        std::string device_id;
        std::string numa_node;
        std::map<std::string, std::string> sysfs_attributes;
    };

    SystemInterface();
    ~SystemInterface();

    // Información del sistema
    SystemInfo get_system_info();
    bool check_nvme_support();
    bool check_required_modules();
    std::vector<std::string> get_loaded_nvme_modules();

    // Detección de dispositivos
    std::vector<std::string> discover_nvme_devices();
    std::vector<DeviceInfo> get_all_nvme_devices_info();
    DeviceInfo get_device_info(const std::string& device_path);

    // Permisos y acceso
    bool check_device_permissions(const std::string& device_path);
    bool is_device_mounted(const std::string& device_path);
    std::vector<std::string> get_mount_points(const std::string& device_path);

    // Configuración del sistema
    bool disable_power_management(const std::string& device_path);
    bool enable_power_management(const std::string& device_path);
    bool set_io_scheduler(const std::string& device_path, const std::string& scheduler);
    std::string get_io_scheduler(const std::string& device_path);

    // Monitoreo de recursos
    double get_cpu_usage();
    double get_memory_usage();
    double get_io_wait_percentage();
    std::map<std::string, uint64_t> get_device_io_stats(const std::string& device_path);

    // Utilidades de logging del kernel
    std::vector<std::string> get_kernel_messages(const std::string& filter = "nvme");
    bool monitor_kernel_messages(const std::string& filter, 
                                std::function<void(const std::string&)> callback);

    // Control de procesos
    bool kill_competing_processes();
    std::vector<std::string> get_processes_using_device(const std::string& device_path);

private:
    bool read_file(const std::string& path, std::string& content);
    bool write_file(const std::string& path, const std::string& content);
    std::vector<std::string> list_directory(const std::string& path);
    bool file_exists(const std::string& path);
    bool is_directory(const std::string& path);
    
    std::string get_sysfs_path(const std::string& device_path);
    std::string get_proc_path(const std::string& device_path);
    
    // Cache de información del sistema
    SystemInfo cached_system_info_;
    bool system_info_cached_;
    std::chrono::steady_clock::time_point last_cache_update_;
    
    void update_system_info_cache();
    bool is_cache_valid();
};

#endif // SYSTEM_INTERFACE_H
