# -*- coding: utf-8 -*-
"""
Aplicación principal para testing de memorias NVMe.

Punto de entrada de la aplicación con procesamiento de argumentos
y coordinación de componentes principales.
"""

import sys
import os
import time
from datetime import datetime

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.test_manager import TestManager

class NVMeTestUI:
    """Interfaz de usuario para el sistema de testing NVMe"""
    
    def __init__(self):
        self.test_cases = {
            "1": {
                "name": "test_smart_log",
                "description": "Pruebas de registro SMART y temperatura",
                "duration": "~5-10 minutos",
                "details": "Verifica datos SMART, temperatura, porcentaje de uso y ejecuta comandos read/write"
            },
            "2": {
                "name": "test_id_control",
                "description": "Pruebas de identificación y control del dispositivo",
                "duration": "~2-5 minutos",
                "details": "Valida información de identificación del controlador contra valores esperados"
            },
            "3": {
                "name": "test_smart_log_healt",
                "description": "Pruebas de salud del dispositivo",
                "duration": "~10-15 minutos",
                "details": "Verifica salud del dispositivo, formatea namespaces y ejecuta pruebas de escritura"
            }
        }
        self.serial_number = None
        self.device_path = None  # Agregar para almacenar la ruta del dispositivo
    
    def show_banner(self):
        """Muestra el banner principal de la aplicación"""
        print("\n" + "="*80)
        print("           NVME TESTER FRAMEWORK - Sistema de Pruebas para SSDs NVMe")
        print("="*80)
        print("        Desarrollado para validación de firmware y hardware NVMe")
        print("        Universidad - Proyecto de Diseño y Validación de Firmware")
        print("="*80)
    
    def get_serial_number(self):
        """Obtiene automáticamente el número de serie del dispositivo o permite ingreso manual"""
        print("\nCONFIGURACION INICIAL")
        print("-" * 50)
        
        # Intentar detección automática
        print("Detectando dispositivos NVMe automáticamente...")
        auto_devices = self.auto_detect_nvme_devices()
        
        if auto_devices:
            print(f"\nDispositivos NVMe detectados: {len(auto_devices)}")
            print("-" * 40)
            
            for i, device in enumerate(auto_devices, 1):
                print(f"{i}. Dispositivo: {device['path']}")
                print(f"   Número de serie: {device['serial']}")
                print(f"   Modelo: {device['model']}")
                print(f"   Firmware: {device['firmware']}")
                print()
            
            # Opciones de selección
            print(f"{len(auto_devices) + 1}. Ingresar número de serie manualmente")
            print("0. Salir")
            print("-" * 40)
            
            while True:
                try:
                    choice = input("Seleccione un dispositivo: ").strip()
                    
                    if choice == "0":
                        print("Saliendo...")
                        sys.exit(0)
                    
                    elif choice == str(len(auto_devices) + 1):
                        # Ingreso manual
                        return self.manual_serial_input()
                    
                    else:
                        device_index = int(choice) - 1
                        if 0 <= device_index < len(auto_devices):
                            selected_device = auto_devices[device_index]
                            self.serial_number = selected_device['serial']
                            self.device_path = selected_device['path']
                            
                            print(f"\nDispositivo seleccionado:")
                            print(f"   Ruta: {self.device_path}")
                            print(f"   Número de serie: {self.serial_number}")
                            print(f"   Modelo: {selected_device['model']}")
                            
                            confirm = input("\n¿Confirmar selección? (s/n): ").lower()
                            if confirm == 's':
                                return self.serial_number
                            else:
                                continue
                        else:
                            print("Opción inválida. Intente nuevamente.")
                            
                except ValueError:
                    print("Por favor ingrese un número válido.")
                except KeyboardInterrupt:
                    print("\nOperación cancelada.")
                    sys.exit(0)
        else:
            print("No se detectaron dispositivos NVMe automáticamente.")
            print("Procediendo con ingreso manual...")
            return self.manual_serial_input()

    def auto_detect_nvme_devices(self):
        """Detecta automáticamente dispositivos NVMe y obtiene sus números de serie"""
        devices = []
        
        try:
            # Importar aquí para evitar problemas de inicialización
            from src.nvme_wrapper import NvmeCommands
            from src.logger import TestLogger
            
            # Crear logger temporal para la detección
            temp_logger = TestLogger("auto_detection")
            
            # Buscar dispositivos NVMe en el sistema
            nvme_paths = self.find_nvme_devices()
            
            if not nvme_paths:
                print("No se encontraron dispositivos NVMe en /dev/")
                return []
            
            print(f"Escaneando {len(nvme_paths)} dispositivo(s) NVMe...")
            
            for device_path in nvme_paths:
                try:
                    print(f"   Consultando {device_path}...")
                    
                    # Crear instancia temporal del wrapper para este dispositivo
                    nvme_wrapper = NvmeCommands(temp_logger, device=device_path)
                    
                    # Obtener información del controlador
                    id_ctrl_result = nvme_wrapper.idctrol(json_output=True)
                    
                    if id_ctrl_result and isinstance(id_ctrl_result, dict):
                        serial = id_ctrl_result.get('sn', '').strip()
                        model = id_ctrl_result.get('mn', 'Unknown').strip()
                        firmware = id_ctrl_result.get('fr', 'Unknown').strip()
                        
                        if serial:  # Solo agregar si tiene número de serie válido
                            device_info = {
                                'path': device_path,
                                'serial': serial,
                                'model': model,
                                'firmware': firmware,
                                'raw_data': id_ctrl_result
                            }
                            devices.append(device_info)
                            print(f"      ✓ Detectado: {serial}")
                        else:
                            print(f"      ✗ Sin número de serie válido")
                    else:
                        print(f"      ✗ No se pudo obtener información")
                        
                except Exception as e:
                    print(f"      ✗ Error consultando {device_path}: {str(e)}")
                    continue
        
        except Exception as e:
            print(f"Error durante la detección automática: {str(e)}")
            return []
        
        return devices

    def find_nvme_devices(self):
        """Busca dispositivos NVMe en el sistema"""
        nvme_devices = []
        
        try:
            import glob
            
            # Buscar dispositivos NVMe principales (nvme0, nvme1, etc.)
            nvme_pattern = "/dev/nvme[0-9]*"
            potential_devices = glob.glob(nvme_pattern)
            
            # Filtrar solo dispositivos principales (no particiones)
            for device in potential_devices:
                # Solo dispositivos principales como /dev/nvme0, no /dev/nvme0n1
                if device.endswith(('n1', 'n2', 'n3', 'n4', 'p1', 'p2', 'p3', 'p4')):
                    continue
                nvme_devices.append(device)
            
            # Si no encontramos dispositivos principales, buscar namespaces
            if not nvme_devices:
                namespace_pattern = "/dev/nvme[0-9]*n[0-9]*"
                namespace_devices = glob.glob(namespace_pattern)
                
                # Tomar solo el primer namespace de cada dispositivo
                seen_controllers = set()
                for device in sorted(namespace_devices):
                    # Extraer número de controlador (ej: nvme0 de nvme0n1)
                    import re
                    match = re.match(r'/dev/(nvme\d+)', device)
                    if match:
                        controller = match.group(1)
                        if controller not in seen_controllers:
                            nvme_devices.append(device)
                            seen_controllers.add(controller)
        
            return sorted(nvme_devices)
            
        except Exception as e:
            print(f"Error buscando dispositivos NVMe: {str(e)}")
            return []

    def manual_serial_input(self):
        """Permite ingreso manual del número de serie"""
        print("\nINGRESO MANUAL DE NUMERO DE SERIE")
        print("-" * 40)
        
        while True:
            serial = input("Ingrese el número de serie del dispositivo NVMe: ").strip()
            
            if not serial:
                print("ERROR: El número de serie no puede estar vacío")
                continue
            
            if len(serial) < 8:
                print("ADVERTENCIA: El número de serie parece demasiado corto")
                retry = input("¿Continuar de todos modos? (s/n): ").lower()
                if retry != 's':
                    continue
            
            # Confirmar número de serie
            print(f"\nNúmero de serie ingresado: {serial}")
            confirm = input("¿Es correcto? (s/n): ").lower()
            
            if confirm == 's':
                self.serial_number = serial
                self.device_path = None  # Se determinará más tarde
                return serial
            
            print("Reingrese el número de serie...")
    
    def show_main_menu(self):
        """Muestra el menú principal"""
        print("\nMENU PRINCIPAL - SELECCION DE PRUEBAS")
        print("-" * 60)
        print(f"Dispositivo: {self.serial_number}")
        if hasattr(self, 'device_path') and self.device_path:
            print(f"Ruta: {self.device_path}")
        print(f"Fecha/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("-" * 60)
        
        for key, test in self.test_cases.items():
            print(f"{key}. {test['description']}")
            print(f"   Nombre: {test['name']}")
            print(f"   Duración: {test['duration']}")
            print(f"   Detalles: {test['details']}")
            print()
        
        print("4. Ver información detallada de un test")
        print("5. Cambiar número de serie")
        print("6. Ejecutar todos los tests (secuencial)")
        print("7. Re-escanear dispositivos")
        print("0. Salir")
        print("-" * 60)
    
    def show_test_details(self):
        """Muestra información detallada de un test específico"""
        while True:
            print("\nINFORMACION DETALLADA DE TESTS")
            print("-" * 40)
            
            # Mostrar menú de tests disponibles
            for key, test in self.test_cases.items():
                print(f"{key}. {test['description']}")
            print("0. Volver al menú principal")
            print("-" * 40)
            
            try:
                choice = input("Seleccione un test para ver detalles: ").strip()
                
                # Switch case usando diccionario
                if choice == "0":
                    break
                elif choice in self.test_cases:
                    test = self.test_cases[choice]
                    self.display_test_info(test)
                    input("\nPresione Enter para continuar...")
                else:
                    print("Opción inválida. Seleccione un número del menú.")
                    time.sleep(1)
                    
            except KeyboardInterrupt:
                print("\nVolviendo al menú principal...")
                break
            except Exception as e:
                print(f"Error: {e}")
                time.sleep(1)
    
    def display_test_info(self, test):
        """Muestra información detallada de un test"""
        print(f"\nDETALLES DEL TEST: {test['name'].upper()}")
        print("="*70)
        print(f"Descripción: {test['description']}")
        print(f"Duración estimada: {test['duration']}")
        print(f"Funcionalidades: {test['details']}")
        
        # Información adicional específica por test
        if test['name'] == 'test_smart_log':
            print("\nPasos específicos:")
            print("   - Toma snapshot inicial con SMART-LOG")
            print("   - Verifica temperatura < 85°C")
            print("   - Verifica porcentaje de uso < 100%")
            print("   - Ejecuta comandos read/write (1-200 veces)")
            print("   - Toma snapshot final y compara")
            
        elif test['name'] == 'test_id_control':
            print("\nPasos específicos:")
            print("   - Ejecuta comando nvme id-ctrl")
            print("   - Compara con valores esperados en JSON")
            print("   - Ignora campos: sn, fguid, unvmcap, subnqn")
            print("   - Valida coincidencias en todos los demás campos")
            
        elif test['name'] == 'test_smart_log_healt':
            print("\nPasos específicos:")
            print("   - Toma snapshot inicial con ID-NS")
            print("   - Verifica block size, nuse, nsize, ncap, etc.")
            print("   - Elimina todos los namespaces")
            print("   - Crea y adjunta nuevo namespace")
            print("   - Formatea con block size 4096")
            print("   - Ejecuta comando write")
            print("   - Toma snapshot final")
    
    def confirm_test_execution(self, test_name, test_info):
        """Confirma la ejecución de un test"""
        print(f"\nCONFIRMACION DE EJECUCION")
        print("-" * 50)
        print(f"Test: {test_info['description']}")
        print(f"Dispositivo: {self.serial_number}")
        print(f"Duración estimada: {test_info['duration']}")
        print(f"Detalles: {test_info['details']}")
        
        print("\nADVERTENCIAS:")
        if test_name == 'test_smart_log_healt':
            print("   - Este test ELIMINARA todos los namespaces")
            print("   - Se FORMATEARA el dispositivo")
            print("   - Se PERDERAN todos los datos")
        else:
            print("   - Este test realizará operaciones de lectura/escritura")
            print("   - El dispositivo debe estar disponible")
        
        print("\n" + "="*60)
        confirm = input("¿Desea continuar con la ejecución? (s/n): ").lower()
        return confirm == 's'
    
    def execute_test(self, test_name):
        """Ejecuta un test específico"""
        test_info = None
        for test in self.test_cases.values():
            if test['name'] == test_name:
                test_info = test
                break
        
        if not test_info:
            print(f"ERROR: Test {test_name} no encontrado")
            return False
        
        # Confirmar ejecución
        if not self.confirm_test_execution(test_name, test_info):
            print("Ejecución cancelada por el usuario")
            return False
        
        print(f"\nINICIANDO EJECUCION DEL TEST: {test_name.upper()}")
        print("="*70)
        print(f"Hora de inicio: {datetime.now().strftime('%H:%M:%S')}")
        
        # Mostrar barra de progreso simulada
        print("\nPreparando ejecución...")
        self.show_progress_bar("Inicializando", 3)
        
        try:
            # Crear y ejecutar el test
            test_manager = TestManager(self.serial_number, test_name)
            
            if test_manager.test is None:
                print(f"ERROR: No se pudo inicializar el test {test_name}")
                return False
            
            print(f"\nTest manager inicializado correctamente")
            print(f"Ejecutando: {test_info['description']}")
            
            # Ejecutar el test
            start_time = time.time()
            result = test_manager.run()
            end_time = time.time()
            
            duration = end_time - start_time
            
            # Mostrar resultados
            print(f"\nEJECUCION COMPLETADA")
            print("="*60)
            print(f"Duración real: {duration:.2f} segundos")
            print(f"Hora de finalización: {datetime.now().strftime('%H:%M:%S')}")
            
            if result is not None:
                print(f"Estado: EXITO")
                
            else:
                print(f"Estado: FALLO")
                print(f"Revise los logs para más detalles")
            
            return result is not None
            
        except Exception as e:
            print(f"\nERROR DURANTE LA EJECUCION")
            print(f"Error: {str(e)}")
            print(f"Hora del error: {datetime.now().strftime('%H:%M:%S')}")
            return False
    
    def execute_all_tests(self):
        """Ejecuta todos los tests secuencialmente"""
        print(f"\nEJECUCION SECUENCIAL DE TODOS LOS TESTS")
        print("="*70)
        print(f"Dispositivo: {self.serial_number}")
        print(f"Total de tests: {len(self.test_cases)}")
        
        # Confirmar ejecución de todos los tests
        print("\nADVERTENCIA: Se ejecutarán TODOS los tests")
        print("   - Algunos tests pueden formatear el dispositivo")
        print("   - La duración total puede ser de 20-30 minutos")
        
        confirm = input("\n¿Desea continuar? (s/n): ").lower()
        if confirm != 's':
            print("Ejecución cancelada")
            return
        
        results = {}
        total_start = time.time()
        
        for i, (key, test) in enumerate(self.test_cases.items(), 1):
            print(f"\nEJECUTANDO TEST {i}/{len(self.test_cases)}: {test['name']}")
            print("-" * 60)
            
            try:
                result = self.execute_test(test['name'])
                results[test['name']] = result
                
                if result:
                    print(f"Test {test['name']} completado exitosamente")
                else:
                    print(f"Test {test['name']} falló")
                    
                # Pausa entre tests
                if i < len(self.test_cases):
                    print("\nPausa entre tests...")
                    time.sleep(2)
                    
            except Exception as e:
                print(f"Error en test {test['name']}: {e}")
                results[test['name']] = False
        
        total_end = time.time()
        total_duration = total_end - total_start
        
        # Mostrar resumen final
        self.show_execution_summary(results, total_duration)
    
    def show_execution_summary(self, results, total_duration):
        """Muestra el resumen de ejecución de todos los tests"""
        print(f"\nRESUMEN FINAL DE EJECUCION")
        print("="*70)
        print(f"Duración total: {total_duration:.2f} segundos ({total_duration/60:.1f} minutos)")
        print(f"Dispositivo: {self.serial_number}")
        print(f"Finalizado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        passed = sum(1 for result in results.values() if result)
        failed = len(results) - passed
        
        print(f"\nESTADISTICAS:")
        print(f"   Tests exitosos: {passed}")
        print(f"   Tests fallidos: {failed}")
        print(f"   Tasa de éxito: {passed/len(results)*100:.1f}%")
        
        print(f"\nDETALLE POR TEST:")
        for test_name, result in results.items():
            status = "PASS" if result else "FAIL"
            print(f"   {test_name}: [{status}]")
        
        if failed == 0:
            print(f"\nTODOS LOS TESTS PASARON EXITOSAMENTE")
        else:
            print(f"\n{failed} test(s) fallaron. Revise los logs para más detalles.")
    
    def show_progress_bar(self, task_name, duration):
        """Muestra una barra de progreso simulada"""
        print(f"Procesando {task_name}...")
        for i in range(duration):
            time.sleep(1)
            progress = "█" * (i + 1) + "░" * (duration - i - 1)
            print(f"\r   [{progress}] {((i+1)/duration)*100:.0f}%", end="", flush=True)
        print(" [COMPLETADO]")
    
    def run(self):
        """Ejecuta la interfaz de usuario principal"""
        self.show_banner()
        
        # Obtener número de serie automáticamente
        self.get_serial_number()
        
        while True:
            self.show_main_menu()
            
            try:
                choice = input("Seleccione una opción: ").strip()
                
                if choice == "0":
                    print("\nGracias por usar NVMe Tester Framework")
                    print("Saliendo del sistema...")
                    break
                
                elif choice in self.test_cases:
                    test_name = self.test_cases[choice]['name']
                    print(f"\nEjecutando: {test_name}")
                    result = self.execute_test(test_name)
                    input("\nPresione Enter para continuar...")
                
                elif choice == "4":
                    self.show_test_details()
                
                elif choice == "5":
                    print("\nCambiando número de serie...")
                    self.get_serial_number()
                
                elif choice == "6":
                    self.execute_all_tests()
                    input("\nPresione Enter para continuar...")
                
                elif choice == "7":
                    print("\nRe-escaneando dispositivos...")
                    self.get_serial_number()
                
                else:
                    print("Opción inválida. Seleccione una opción del menú.")
                    time.sleep(2)
                    
            except KeyboardInterrupt:
                print("\n\nInterrupción detectada (Ctrl+C)")
                confirm = input("¿Desea salir? (s/n): ").lower()
                if confirm == 's':
                    break
            except Exception as e:
                print(f"\nError inesperado: {e}")
                input("Presione Enter para continuar...")

def main():
    """Función principal"""
    try:
        ui = NVMeTestUI()
        ui.run()
    except Exception as e:
        print(f"Error crítico en la aplicación: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
