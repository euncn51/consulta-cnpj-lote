"""
Script para executar a GUI Web do NFe Parser (Streamlit)

Execute este script para abrir a interface web no navegador.
"""

import subprocess
import sys
from pathlib import Path

def main():
    print("\n" + "="*60)
    print("NFe Parser - Interface Web (Streamlit)")
    print("="*60 + "\n")
    print("Iniciando servidor Streamlit...")
    print("A aplicação será aberta automaticamente no navegador.\n")
    print("Para parar o servidor, pressione Ctrl+C\n")
    print("="*60 + "\n")
    
    # Caminho para o app Streamlit
    app_path = Path(__file__).parent / "src" / "gui" / "streamlit_app.py"
    
    try:
        # Executar Streamlit
        subprocess.run([
            sys.executable,
            "-m",
            "streamlit",
            "run",
            str(app_path),
            "--server.port=8501",
            "--server.headless=false"
        ])
    except KeyboardInterrupt:
        print("\n\nServidor encerrado pelo usuário")
    except Exception as e:
        print(f"\nErro ao iniciar servidor: {e}")
        print("\nCertifique-se de que o Streamlit está instalado:")
        print("  pip install streamlit plotly")

if __name__ == '__main__':
    main()

# Made with Bob
