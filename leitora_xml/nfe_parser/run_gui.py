"""
Script para executar a GUI Desktop do NFe Parser

Execute este script para abrir a interface gráfica.
"""

import sys
from pathlib import Path

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent))

from src.gui.tkinter_app import main

if __name__ == '__main__':
    print("\n" + "="*60)
    print("NFe Parser - Interface Gráfica Desktop")
    print("="*60 + "\n")
    print("Iniciando aplicação...")
    print("Aguarde a janela abrir...\n")
    
    try:
        main()
    except KeyboardInterrupt:
        print("\nAplicação encerrada pelo usuário")
    except Exception as e:
        print(f"\nErro ao iniciar aplicação: {e}")
        import traceback
        traceback.print_exc()

# Made with Bob
