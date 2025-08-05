#ifndef LOGGER_H
#define LOGGER_H

#include <string>
#include <fstream>
#include <memory>
#include <mutex>
#include <chrono>

/**
 * @brief Sistema de logging para la aplicación de testing NVMe
 * 
 * Proporciona logging thread-safe con diferentes niveles de severidad
 * y capacidad de escritura a archivo y consola.
 */
class Logger {
public:
    enum class LogLevel {
        DEBUG = 0,
        INFO = 1,
        WARNING = 2,
        ERROR = 3,
        CRITICAL = 4
    };

    static Logger& getInstance();
    
    // Configuración
    void set_log_level(LogLevel level);
    void set_output_file(const std::string& filename);
    void enable_console_output(bool enable);
    void enable_timestamps(bool enable);
    void set_max_file_size(size_t max_size_mb);
    
    // Métodos de logging
    void debug(const std::string& message);
    void info(const std::string& message);
    void warning(const std::string& message);
    void error(const std::string& message);
    void critical(const std::string& message);
    
    // Logging formateado
    template<typename... Args>
    void debug(const std::string& format, Args... args);
    
    template<typename... Args>
    void info(const std::string& format, Args... args);
    
    template<typename... Args>
    void warning(const std::string& format, Args... args);
    
    template<typename... Args>
    void error(const std::string& format, Args... args);
    
    template<typename... Args>
    void critical(const std::string& format, Args... args);
    
    // Control de archivos
    void flush();
    void rotate_log_file();
    void close();

private:
    Logger();
    ~Logger();
    Logger(const Logger&) = delete;
    Logger& operator=(const Logger&) = delete;
    
    void log(LogLevel level, const std::string& message);
    std::string format_message(LogLevel level, const std::string& message);
    std::string get_timestamp();
    std::string level_to_string(LogLevel level);
    void check_file_rotation();
    
    LogLevel current_level_;
    std::unique_ptr<std::ofstream> file_stream_;
    std::string log_filename_;
    bool console_output_enabled_;
    bool timestamps_enabled_;
    size_t max_file_size_bytes_;
    size_t current_file_size_;
    std::mutex log_mutex_;
};

// Macros para facilitar el uso
#define LOG_DEBUG(msg) Logger::getInstance().debug(msg)
#define LOG_INFO(msg) Logger::getInstance().info(msg)
#define LOG_WARNING(msg) Logger::getInstance().warning(msg)
#define LOG_ERROR(msg) Logger::getInstance().error(msg)
#define LOG_CRITICAL(msg) Logger::getInstance().critical(msg)

#define LOG_DEBUG_F(fmt, ...) Logger::getInstance().debug(fmt, __VA_ARGS__)
#define LOG_INFO_F(fmt, ...) Logger::getInstance().info(fmt, __VA_ARGS__)
#define LOG_WARNING_F(fmt, ...) Logger::getInstance().warning(fmt, __VA_ARGS__)
#define LOG_ERROR_F(fmt, ...) Logger::getInstance().error(fmt, __VA_ARGS__)
#define LOG_CRITICAL_F(fmt, ...) Logger::getInstance().critical(fmt, __VA_ARGS__)

#endif // LOGGER_H
