"""
GUI Desktop para NFe Parser usando tkinter

Interface gráfica completa com:
- Seleção de arquivos/pastas
- Barra de progresso
- Visualização de logs
- Configurações
- Exportação de resultados
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import queue
from pathlib import Path
import sys
import glob
from datetime import datetime

# Adicionar diretório pai ao path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.utils.logger import setup_logger, get_logger
from src.config import get_settings
from src.core.streaming_parser import StreamingNFeParser
from src.core.field_mapper import FieldMapper


class LogHandler:
    """Handler para capturar logs e exibir na GUI"""
    
    def __init__(self, text_widget):
        self.text_widget = text_widget
        self.queue = queue.Queue()
    
    def write(self, message):
        """Escreve mensagem na fila"""
        if message.strip():
            self.queue.put(message)
    
    def flush(self):
        """Flush (necessário para compatibilidade)"""
        pass
    
    def update_text_widget(self):
        """Atualiza widget de texto com mensagens da fila"""
        try:
            while True:
                message = self.queue.get_nowait()
                self.text_widget.insert(tk.END, message)
                self.text_widget.see(tk.END)
        except queue.Empty:
            pass


class NFeParserGUI:
    """
    Interface Gráfica Desktop para NFe Parser
    
    Funcionalidades:
    - Seleção de arquivos XML individuais ou pasta
    - Processamento com barra de progresso
    - Visualização de logs em tempo real
    - Configurações personalizáveis
    - Exportação de resultados
    """
    
    def __init__(self, root):
        """
        Inicializa a GUI
        
        Args:
            root: Janela raiz do tkinter
        """
        self.root = root
        self.root.title("NFe Parser - Análise de Notas Fiscais")
        self.root.geometry("1000x700")
        
        # Configurar logging
        setup_logger(log_level='INFO')
        self.logger = get_logger('gui')
        
        # Componentes
        self.settings = get_settings()
        self.parser = StreamingNFeParser()
        self.mapper = FieldMapper()
        
        # Variáveis
        self.selected_files = []
        self.processing = False
        self.results_data = []
        
        # Criar interface
        self._create_widgets()
        self._setup_layout()
        
        self.logger.info("GUI inicializada")
    
    def _create_widgets(self):
        """Cria todos os widgets da interface"""
        
        # Frame principal
        self.main_frame = ttk.Frame(self.root, padding="10")
        
        # === SEÇÃO 1: Seleção de Arquivos ===
        self.file_frame = ttk.LabelFrame(
            self.main_frame,
            text="1. Seleção de Arquivos",
            padding="10"
        )
        
        # Botões de seleção
        self.btn_select_files = ttk.Button(
            self.file_frame,
            text="Selecionar Arquivos XML",
            command=self.select_files
        )
        
        self.btn_select_folder = ttk.Button(
            self.file_frame,
            text="Selecionar Pasta",
            command=self.select_folder
        )
        
        # Label de arquivos selecionados
        self.lbl_files = ttk.Label(
            self.file_frame,
            text="Nenhum arquivo selecionado",
            foreground="gray"
        )
        
        # === SEÇÃO 2: Opções ===
        self.options_frame = ttk.LabelFrame(
            self.main_frame,
            text="2. Opções de Processamento",
            padding="10"
        )
        
        # Checkbox: Usar streaming
        self.var_streaming = tk.BooleanVar(value=True)
        self.chk_streaming = ttk.Checkbutton(
            self.options_frame,
            text="Usar processamento streaming (recomendado para arquivos grandes)",
            variable=self.var_streaming
        )
        
        # Checkbox: Validar schema
        self.var_validate = tk.BooleanVar(value=False)
        self.chk_validate = ttk.Checkbutton(
            self.options_frame,
            text="Validar schema XML",
            variable=self.var_validate
        )
        
        # Formato de exportação
        ttk.Label(self.options_frame, text="Formato de exportação:").grid(
            row=2, column=0, sticky=tk.W, pady=5
        )
        self.var_format = tk.StringVar(value="xlsx")
        formats = [("Excel (.xlsx)", "xlsx"), ("CSV (.csv)", "csv"), ("JSON (.json)", "json")]
        for i, (text, value) in enumerate(formats):
            ttk.Radiobutton(
                self.options_frame,
                text=text,
                variable=self.var_format,
                value=value
            ).grid(row=2, column=i+1, sticky=tk.W, padx=5)
        
        # === SEÇÃO 3: Progresso ===
        self.progress_frame = ttk.LabelFrame(
            self.main_frame,
            text="3. Progresso",
            padding="10"
        )
        
        # Barra de progresso
        self.progress_bar = ttk.Progressbar(
            self.progress_frame,
            mode='determinate',
            length=400
        )
        
        # Label de status
        self.lbl_status = ttk.Label(
            self.progress_frame,
            text="Aguardando...",
            foreground="blue"
        )
        
        # === SEÇÃO 4: Logs ===
        self.log_frame = ttk.LabelFrame(
            self.main_frame,
            text="4. Logs do Processamento",
            padding="10"
        )
        
        # Área de texto para logs
        self.txt_logs = scrolledtext.ScrolledText(
            self.log_frame,
            height=15,
            width=100,
            wrap=tk.WORD,
            font=("Consolas", 9)
        )
        
        # === SEÇÃO 5: Ações ===
        self.action_frame = ttk.Frame(self.main_frame, padding="10")
        
        # Botão processar
        self.btn_process = ttk.Button(
            self.action_frame,
            text="Iniciar Processamento",
            command=self.start_processing,
            style="Accent.TButton"
        )
        
        # Botão parar
        self.btn_stop = ttk.Button(
            self.action_frame,
            text="Parar",
            command=self.stop_processing,
            state=tk.DISABLED
        )
        
        # Botão limpar
        self.btn_clear = ttk.Button(
            self.action_frame,
            text="Limpar Logs",
            command=self.clear_logs
        )
        
        # Botão exportar
        self.btn_export = ttk.Button(
            self.action_frame,
            text="Exportar Resultados",
            command=self.export_results,
            state=tk.DISABLED
        )
    
    def _setup_layout(self):
        """Organiza o layout dos widgets"""
        
        # Frame principal
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Seção 1: Arquivos
        self.file_frame.pack(fill=tk.X, pady=5)
        self.btn_select_files.pack(side=tk.LEFT, padx=5)
        self.btn_select_folder.pack(side=tk.LEFT, padx=5)
        self.lbl_files.pack(side=tk.LEFT, padx=20)
        
        # Seção 2: Opções
        self.options_frame.pack(fill=tk.X, pady=5)
        self.chk_streaming.grid(row=0, column=0, columnspan=4, sticky=tk.W, pady=2)
        self.chk_validate.grid(row=1, column=0, columnspan=4, sticky=tk.W, pady=2)
        
        # Seção 3: Progresso
        self.progress_frame.pack(fill=tk.X, pady=5)
        self.progress_bar.pack(pady=5)
        self.lbl_status.pack()
        
        # Seção 4: Logs
        self.log_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        self.txt_logs.pack(fill=tk.BOTH, expand=True)
        
        # Seção 5: Ações
        self.action_frame.pack(fill=tk.X, pady=5)
        self.btn_process.pack(side=tk.LEFT, padx=5)
        self.btn_stop.pack(side=tk.LEFT, padx=5)
        self.btn_clear.pack(side=tk.LEFT, padx=5)
        self.btn_export.pack(side=tk.RIGHT, padx=5)
    
    def select_files(self):
        """Seleciona arquivos XML individuais"""
        files = filedialog.askopenfilenames(
            title="Selecionar arquivos XML",
            filetypes=[("Arquivos XML", "*.xml"), ("Todos os arquivos", "*.*")]
        )
        
        if files:
            self.selected_files = list(files)
            count = len(self.selected_files)
            self.lbl_files.config(
                text=f"{count} arquivo(s) selecionado(s)",
                foreground="green"
            )
            self.log(f"Selecionados {count} arquivos")
    
    def select_folder(self):
        """Seleciona pasta com arquivos XML"""
        folder = filedialog.askdirectory(title="Selecionar pasta com XMLs")
        
        if folder:
            xml_files = glob.glob(str(Path(folder) / "*.xml"))
            self.selected_files = xml_files
            count = len(self.selected_files)
            self.lbl_files.config(
                text=f"{count} arquivo(s) encontrado(s) em {Path(folder).name}",
                foreground="green"
            )
            self.log(f"Encontrados {count} arquivos em {folder}")
    
    def log(self, message):
        """Adiciona mensagem ao log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.txt_logs.insert(tk.END, f"[{timestamp}] {message}\n")
        self.txt_logs.see(tk.END)
    
    def clear_logs(self):
        """Limpa área de logs"""
        self.txt_logs.delete(1.0, tk.END)
    
    def update_progress(self, current, total):
        """Atualiza barra de progresso"""
        if total > 0:
            percent = (current / total) * 100
            self.progress_bar['value'] = percent
            self.lbl_status.config(
                text=f"Processando: {current}/{total} ({percent:.1f}%)"
            )
            self.root.update_idletasks()
    
    def start_processing(self):
        """Inicia processamento em thread separada"""
        if not self.selected_files:
            messagebox.showwarning(
                "Aviso",
                "Selecione arquivos XML primeiro!"
            )
            return
        
        # Desabilitar botões
        self.btn_process.config(state=tk.DISABLED)
        self.btn_stop.config(state=tk.NORMAL)
        self.btn_export.config(state=tk.DISABLED)
        
        self.processing = True
        self.results_data = []
        
        # Iniciar thread de processamento
        thread = threading.Thread(target=self._process_files, daemon=True)
        thread.start()
    
    def _process_files(self):
        """Processa arquivos (executado em thread separada)"""
        try:
            self.log("="*50)
            self.log("INICIANDO PROCESSAMENTO")
            self.log("="*50)
            
            total_files = len(self.selected_files)
            all_data = []
            
            for idx, file_path in enumerate(self.selected_files, 1):
                if not self.processing:
                    self.log("Processamento interrompido pelo usuário")
                    break
                
                filename = Path(file_path).name
                self.log(f"\nProcessando {idx}/{total_files}: {filename}")
                
                try:
                    # Processar arquivo
                    if self.var_streaming.get():
                        data = self.parser.parse_xml_stream(file_path)
                    else:
                        # Usar parser padrão (não implementado neste exemplo)
                        data = self.parser.parse_xml_stream(file_path)
                    
                    all_data.extend(data)
                    self.log(f"  ✓ {len(data)} itens extraídos")
                    
                except Exception as e:
                    self.log(f"  ✗ Erro: {str(e)}")
                    self.logger.error(f"Erro ao processar {filename}: {e}", exc_info=True)
                
                # Atualizar progresso
                self.root.after(0, self.update_progress, idx, total_files)
            
            # Salvar resultados
            self.results_data = all_data
            
            # Finalizar
            self.log("\n" + "="*50)
            self.log(f"PROCESSAMENTO CONCLUÍDO!")
            self.log(f"Total de registros: {len(all_data)}")
            self.log("="*50)
            
            # Habilitar exportação
            self.root.after(0, lambda: self.btn_export.config(state=tk.NORMAL))
            
            # Mostrar mensagem de sucesso
            self.root.after(0, lambda: messagebox.showinfo(
                "Sucesso",
                f"Processamento concluído!\n\n"
                f"Arquivos processados: {total_files}\n"
                f"Registros extraídos: {len(all_data)}"
            ))
            
        except Exception as e:
            self.log(f"\nERRO CRÍTICO: {str(e)}")
            self.logger.error(f"Erro crítico: {e}", exc_info=True)
            self.root.after(0, lambda: messagebox.showerror(
                "Erro",
                f"Erro durante processamento:\n{str(e)}"
            ))
        
        finally:
            # Reabilitar botões
            self.processing = False
            self.root.after(0, lambda: self.btn_process.config(state=tk.NORMAL))
            self.root.after(0, lambda: self.btn_stop.config(state=tk.DISABLED))
    
    def stop_processing(self):
        """Para o processamento"""
        self.processing = False
        self.log("\nParando processamento...")
    
    def export_results(self):
        """Exporta resultados para arquivo"""
        if not self.results_data:
            messagebox.showwarning("Aviso", "Nenhum dado para exportar!")
            return
        
        # Solicitar local de salvamento
        format_ext = self.var_format.get()
        filetypes = {
            'xlsx': [("Excel", "*.xlsx")],
            'csv': [("CSV", "*.csv")],
            'json': [("JSON", "*.json")]
        }
        
        filename = filedialog.asksaveasfilename(
            title="Salvar resultados",
            defaultextension=f".{format_ext}",
            filetypes=filetypes.get(format_ext, [("Todos", "*.*")])
        )
        
        if filename:
            try:
                import pandas as pd
                df = pd.DataFrame(self.results_data)
                
                if format_ext == 'xlsx':
                    df.to_excel(filename, index=False)
                elif format_ext == 'csv':
                    df.to_csv(filename, index=False, encoding='utf-8-sig')
                elif format_ext == 'json':
                    df.to_json(filename, orient='records', indent=2)
                
                self.log(f"\nResultados exportados: {filename}")
                messagebox.showinfo(
                    "Sucesso",
                    f"Resultados exportados com sucesso!\n\n{filename}"
                )
            
            except Exception as e:
                self.log(f"\nErro ao exportar: {str(e)}")
                messagebox.showerror("Erro", f"Erro ao exportar:\n{str(e)}")


def main():
    """Função principal para executar a GUI"""
    root = tk.Tk()
    app = NFeParserGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()

# Made with Bob
