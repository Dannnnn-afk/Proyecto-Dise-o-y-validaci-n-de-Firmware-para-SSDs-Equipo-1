#ifndef CONFIG_MANAGER_H
#define CONFIG_MANAGER_H

#include <string>
#include <map>
#include <vector>
#include <variant>

/**
 * @brief Gestor de configuración para la aplicación de testing NVMe
 * 
 * Maneja la carga y guardado de configuraciones desde archivos JSON/YAML
 * y proporciona acceso type-safe a los parámetros de configuración.
 */
class ConfigManager {
public:
    using ConfigValue = std::variant<std::string, int, double, bool>;
    
    ConfigManager();
    ~ConfigManager();
    
    // Carga y guardado
    bool load_from_file(const std::string& filename);
    bool save_to_file(const std::string& filename);
    bool load_default_config();
    
    // Acceso a configuración
    template<typename T>
    T get(const std::string& key, const T& default_value = T{}) const;
    
    void set(const std::string& key, const ConfigValue& value);
    bool has_key(const std::string& key) const;
    void remove_key(const std::string& key);
    
    // Configuraciones específicas de testing
    struct TestConfig {
        int default_test_duration;
        size_t default_block_size;
        size_t default_queue_depth;
        bool enable_data_verification;
        bool enable_smart_monitoring;
        std::string output_directory;
        std::string log_level;
    };
    
    struct DeviceConfig {
        std::vector<std::string> device_paths;
        bool auto_detect_devices;
        int device_timeout_seconds;
        bool enable_trim_support;
    };
    
    struct ReportConfig {
        std::string default_format;
        bool include_charts;
        bool include_raw_data;
        std::string template_path;
    };
    
    TestConfig get_test_config() const;
    DeviceConfig get_device_config() const;
    ReportConfig get_report_config() const;
    
    void set_test_config(const TestConfig& config);
    void set_device_config(const DeviceConfig& config);
    void set_report_config(const ReportConfig& config);
    
    // Validación
    bool validate_config() const;
    std::vector<std::string> get_validation_errors() const;
    
    // Utilidades
    void print_config() const;
    std::vector<std::string> get_all_keys() const;

private:
    std::map<std::string, ConfigValue> config_data_;
    std::string config_filename_;
    mutable std::vector<std::string> validation_errors_;
    
    void set_default_values();
    bool parse_json_file(const std::string& filename);
    bool parse_yaml_file(const std::string& filename);
    bool write_json_file(const std::string& filename);
    bool write_yaml_file(const std::string& filename);
    
    std::string get_file_extension(const std::string& filename) const;
    void validate_test_config() const;
    void validate_device_config() const;
    void validate_report_config() const;
};

#endif // CONFIG_MANAGER_H
