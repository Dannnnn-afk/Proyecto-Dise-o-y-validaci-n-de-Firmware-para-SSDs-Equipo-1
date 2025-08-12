"""
Aplicación principal para testing de memorias NVMe.

Punto de entrada de la aplicación con procesamiento de argumentos
y coordinación de componentes principales.
"""

import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.test_manager import TestManager



if __name__ == "__main__":
    main()
