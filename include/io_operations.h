#ifndef IO_OPERATIONS_H
#define IO_OPERATIONS_H

#include <cstdint>
#include <vector>
#include <memory>
#include <chrono>

/**
 * @brief Operaciones de E/S de bajo nivel para dispositivos NVMe
 * 
 * Proporciona una interfaz unificada para operaciones de lectura/escritura
 * con control preciso de timing y parámetros de acceso.
 */
class IOOperations {
public:
    struct IORequest {
        uint64_t lba;           // Logical Block Address
        uint32_t block_count;   // Número de bloques
        void* buffer;           // Buffer de datos
        size_t buffer_size;     // Tamaño del buffer
        bool is_write;          // true para escritura, false para lectura
        uint32_t queue_id;      // ID de la cola (para async I/O)
    };

    struct IOResult {
        bool success;
        uint64_t bytes_transferred;
        std::chrono::microseconds latency;
        uint32_t error_code;
        std::string error_message;
    };

    struct IOStats {
        uint64_t total_operations;
        uint64_t successful_operations;
        uint64_t failed_operations;
        uint64_t total_bytes;
        std::chrono::microseconds total_time;
        std::chrono::microseconds min_latency;
        std::chrono::microseconds max_latency;
        std::chrono::microseconds avg_latency;
    };

    IOOperations(int device_fd);
    ~IOOperations();

    // Operaciones síncronas
    IOResult sync_read(uint64_t lba, uint32_t block_count, void* buffer);
    IOResult sync_write(uint64_t lba, uint32_t block_count, const void* buffer);
    IOResult sync_flush();
    IOResult sync_trim(uint64_t lba, uint32_t block_count);

    // Operaciones asíncronas
    bool async_read(const IORequest& request);
    bool async_write(const IORequest& request);
    std::vector<IOResult> wait_for_completions(uint32_t max_completions = 0);
    bool cancel_pending_operations();

    // Operaciones por lotes
    std::vector<IOResult> batch_read(const std::vector<IORequest>& requests);
    std::vector<IOResult> batch_write(const std::vector<IORequest>& requests);

    // Configuración
    void set_queue_depth(uint32_t depth);
    void set_timeout_ms(uint32_t timeout);
    void enable_direct_io(bool enable);
    void enable_sync_io(bool enable);

    // Estadísticas
    IOStats get_statistics() const;
    void reset_statistics();
    void enable_statistics(bool enable);

    // Utilidades
    bool is_aligned(const void* buffer, size_t alignment = 512);
    void* allocate_aligned_buffer(size_t size, size_t alignment = 512);
    void free_aligned_buffer(void* buffer);

private:
    int device_fd_;
    uint32_t queue_depth_;
    uint32_t timeout_ms_;
    bool direct_io_enabled_;
    bool sync_io_enabled_;
    bool statistics_enabled_;
    
    IOStats statistics_;
    std::mutex stats_mutex_;
    
    // Gestión de E/O asíncrona
    struct AsyncContext;
    std::unique_ptr<AsyncContext> async_context_;
    
    void update_statistics(const IOResult& result);
    IOResult execute_sync_io(const IORequest& request);
    bool submit_async_io(const IORequest& request);
    
    // Utilidades de sistema
    bool setup_async_context();
    void cleanup_async_context();
    bool configure_device_settings();
};

#endif // IO_OPERATIONS_H
