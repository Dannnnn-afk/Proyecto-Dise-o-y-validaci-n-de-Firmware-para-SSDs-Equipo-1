#ifndef REPORT_GENERATOR_H
#define REPORT_GENERATOR_H

#include <string>
#include <vector>
#include <memory>

/**
 * @brief Generador de reportes para resultados de testing NVMe
 * 
 * Crea reportes en múltiples formatos (HTML, JSON, CSV) con
 * gráficos y análisis detallado de los resultados.
 */
class ReportGenerator {
public:
    enum class ReportFormat {
        HTML,
        JSON,
        CSV,
        XML,
        PDF
    };

    struct TestData {
        std::string test_name;
        std::string test_type;
        std::string device_name;
        std::string timestamp;
        bool passed;
        double duration_seconds;
        std::map<std::string, double> metrics;
        std::vector<std::string> notes;
    };

    ReportGenerator();
    ~ReportGenerator();

    // Configuración
    void set_output_directory(const std::string& directory);
    void set_template_directory(const std::string& directory);
    void enable_charts(bool enable);
    void enable_raw_data_export(bool enable);

    // Generación de reportes
    bool generate_report(const std::vector<TestData>& test_data, 
                        ReportFormat format = ReportFormat::HTML);
    bool generate_html_report(const std::vector<TestData>& test_data);
    bool generate_json_report(const std::vector<TestData>& test_data);
    bool generate_csv_report(const std::vector<TestData>& test_data);

    // Utilidades
    std::string get_last_report_path() const;
    bool validate_output_directory() const;

private:
    std::string output_directory_;
    std::string template_directory_;
    std::string last_report_path_;
    bool charts_enabled_;
    bool raw_data_export_enabled_;

    // Generadores específicos
    std::string generate_html_content(const std::vector<TestData>& test_data);
    std::string generate_json_content(const std::vector<TestData>& test_data);
    std::string generate_csv_content(const std::vector<TestData>& test_data);
    
    // Utilidades de formato
    std::string format_timestamp(const std::string& timestamp);
    std::string format_duration(double seconds);
    std::string format_metric_value(double value, const std::string& unit);
    
    // Generación de gráficos
    bool generate_performance_charts(const std::vector<TestData>& test_data);
    bool generate_comparison_charts(const std::vector<TestData>& test_data);
};

#endif // REPORT_GENERATOR_H
