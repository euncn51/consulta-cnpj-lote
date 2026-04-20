"""
Módulo da interface gráfica do Consultor de CNPJ

Implementa a interface usando Tkinter com:
- Abas para consulta individual e em lote
- Controle de progresso
- Exibição de logs
- Configurações do sistema
"""

import json
import os
import threading
from queue import Queue
from datetime import datetime
from tkinter import (
    Tk, Frame, Label, Entry, Button, Text, Scrollbar, END, 
    messagebox, filedialog
)
from tkinter import ttk

from constants import LANG
from api_client import CNPJConsultor

class CNPJConsultorGUI:
    """
    Classe principal da interface gráfica
    
    Atributos:
        root (Tk): Janela principal
        consultor (CNPJConsultor): Instância do consultor de CNPJ
        processing_thread (Thread): Thread de processamento
        progress_queue (Queue): Fila para comunicação com a thread
        log_file (str): Caminho do arquivo de log
    """
    def __init__(self, root):
        self.root = root
        self.root.title(LANG["title"])
        self.root.geometry("900x700")
        self.consultor = CNPJConsultor()
        self.processing_thread = None
        self.progress_queue = Queue()
        self.log_file = LANG["log_file"]

        # Ícones para status (apenas emojis)
        self.icon_success = "✅"
        self.icon_error = "❌"
        self.icon_info = "ℹ️"

        self._setup_ui()
        self._check_queue()
    
    def _setup_ui(self):
        """Configura todos os componentes da interface"""
        main_frame = Frame(self.root, padx=10, pady=10)
        main_frame.pack(fill="both", expand=True)
        
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill="both", expand=True)
        
        self._create_individual_tab()
        self._create_batch_tab()
        self._create_settings_tab()
        self._create_help_tab()
        
        self._create_log_area(main_frame)
    
    def _create_individual_tab(self):
        """Cria a aba de consulta individual"""
        tab = Frame(self.notebook)
        self.notebook.add(tab, text=LANG["individual_tab"])

        # Campo CNPJ
        Label(tab, text="CNPJ:", font=('Arial', 12, 'bold')).grid(
            row=0, column=0, padx=8, pady=8, sticky="e")
        self.cnpj_entry = Entry(tab, width=25, font=('Arial', 14))
        self.cnpj_entry.grid(row=0, column=1, padx=8, pady=8, sticky="w")
        self.cnpj_entry.bind('<Return>', lambda e: self._consultar_individual())
        self.cnpj_entry.focus_set()

        # Botões
        btn_process = Button(
            tab, text=LANG["process"], command=self._consultar_individual,
            width=15, bg="#4F81BD", fg="white", font=('Arial', 11, 'bold'))
        btn_process.grid(row=0, column=2, padx=8, pady=8)

        btn_clear = Button(
            tab, text="Limpar", command=lambda: self._limpar_individual(),
            width=10, bg="#e0e0e0", font=('Arial', 10))
        btn_clear.grid(row=0, column=3, padx=4, pady=8)

        # Área de resultados
        self.result_text = Text(
            tab, height=22, width=90, state="disabled", 
            font=('Courier', 10), bg="#f7faff", relief="groove", bd=2)
        self.result_text.grid(
            row=1, column=0, columnspan=4, padx=8, pady=8, sticky="nsew")

        scrollbar = Scrollbar(tab, command=self.result_text.yview)
        scrollbar.grid(row=1, column=4, sticky="ns")
        self.result_text.config(yscrollcommand=scrollbar.set)

        # Expansão automática
        tab.grid_rowconfigure(1, weight=1)
        tab.grid_columnconfigure(1, weight=1)

    def _limpar_individual(self):
        """Limpa os campos da aba individual"""
        self.cnpj_entry.delete(0, END)
        self.result_text.config(state="normal")
        self.result_text.delete(1.0, END)
        self.result_text.config(state="disabled")
        self.cnpj_entry.focus_set()
        self._set_status("info", LANG["ready"])

    def _create_batch_tab(self):
        """Cria a aba de processamento em lote"""
        tab = Frame(self.notebook, bg="#f7faff")
        self.notebook.add(tab, text=LANG["batch_tab"])
        
        # Arquivo de entrada
        Label(tab, text=LANG["input_file"], font=('Arial', 11, 'bold'), 
             bg="#f7faff").grid(row=0, column=0, padx=8, pady=8, sticky="e")
        self.input_entry = Entry(tab, width=50, font=('Arial', 11))
        self.input_entry.grid(row=0, column=1, padx=8, pady=8, sticky="w")

        btn_input = Button(
            tab, text=LANG["select"], command=self._select_input_file, 
            width=12, bg="#e0e0e0", font=('Arial', 10, 'bold'))
        btn_input.grid(row=0, column=2, padx=8, pady=8)

        # Arquivo de saída
        Label(tab, text=LANG["output_file"], font=('Arial', 11, 'bold'), 
             bg="#f7faff").grid(row=1, column=0, padx=8, pady=8, sticky="e")
        self.output_entry = Entry(tab, width=50, font=('Arial', 11))
        self.output_entry.grid(row=1, column=1, padx=8, pady=8, sticky="w")

        btn_output = Button(
            tab, text=LANG["select"], command=self._select_output_file, 
            width=12, bg="#e0e0e0", font=('Arial', 10, 'bold'))
        btn_output.grid(row=1, column=2, padx=8, pady=8)

        # Coluna CNPJ
        Label(tab, text=LANG["col_cnpj"], font=('Arial', 11, 'bold'), 
             bg="#f7faff").grid(row=2, column=0, padx=8, pady=8, sticky="e")
        self.col_entry = Entry(tab, width=20, font=('Arial', 11))
        self.col_entry.grid(row=2, column=1, padx=8, pady=8, sticky="w")
        self.col_entry.insert(0, "CNPJ")

        # Botões de processamento
        btn_frame = Frame(tab, bg="#f7faff")
        btn_frame.grid(row=3, column=0, columnspan=3, pady=12)
        
        self.process_btn = Button(
            btn_frame, text=LANG["process"], command=self._start_processing, 
            width=15, bg="#4F81BD", fg="white", font=('Arial', 11, 'bold'))
        self.process_btn.pack(side="left", padx=8)
        
        self.cancel_btn = Button(
            btn_frame, text=LANG["cancel"], command=self._cancel_processing, 
            state="disabled", width=15, bg="#e0e0e0", font=('Arial', 11))
        self.cancel_btn.pack(side="left", padx=8)

        # Barra de progresso
        self.progress_bar = ttk.Progressbar(
            tab, orient="horizontal", length=500, mode="determinate")
        self.progress_bar.grid(
            row=4, column=0, columnspan=3, pady=10, padx=8, sticky="ew")

        # Status
        self.status_label = Label(
            tab, text=LANG["ready"], relief="sunken", anchor="w", 
            bg="#e0e0e0", font=('Arial', 10))
        self.status_label.grid(
            row=5, column=0, columnspan=3, sticky="ew", padx=8, pady=8)

        # Expansão automática
        tab.grid_rowconfigure(4, weight=1)
        tab.grid_columnconfigure(1, weight=1)

    def _create_settings_tab(self):
        """Cria a aba de configurações"""
        tab = Frame(self.notebook, bg="#f7faff")
        self.notebook.add(tab, text=LANG["settings_tab"])

        # Limite de requisições
        Label(tab, text=LANG["limit_label"], font=('Arial', 11, 'bold'), 
             bg="#f7faff").grid(row=0, column=0, padx=8, pady=8, sticky="e")
        self.limit_entry = Entry(tab, width=8, font=('Arial', 11))
        self.limit_entry.grid(row=0, column=1, padx=8, pady=8, sticky="w")
        self.limit_entry.insert(0, str(self.consultor.limite_requisicoes))

        # Tempo de espera
        Label(tab, text=LANG["wait_label"], font=('Arial', 11, 'bold'), 
             bg="#f7faff").grid(row=1, column=0, padx=8, pady=8, sticky="e")
        self.wait_entry = Entry(tab, width=8, font=('Arial', 11))
        self.wait_entry.grid(row=1, column=1, padx=8, pady=8, sticky="w")
        self.wait_entry.insert(0, str(self.consultor.tempo_espera))

        # Configurações de Proxy
        Label(tab, text="Proxy HTTP:", font=('Arial', 11, 'bold'), 
             bg="#f7faff").grid(row=2, column=0, padx=8, pady=8, sticky="e")
        self.proxy_http_entry = Entry(tab, width=30, font=('Arial', 11))
        self.proxy_http_entry.grid(row=2, column=1, padx=8, pady=8, sticky="w")

        Label(tab, text="Proxy HTTPS:", font=('Arial', 11, 'bold'), 
             bg="#f7faff").grid(row=3, column=0, padx=8, pady=8, sticky="e")
        self.proxy_https_entry = Entry(tab, width=30, font=('Arial', 11))
        self.proxy_https_entry.grid(row=3, column=1, padx=8, pady=8, sticky="w")

        Label(tab, text="Usuário:", font=('Arial', 11, 'bold'), 
             bg="#f7faff").grid(row=4, column=0, padx=8, pady=8, sticky="e")
        self.proxy_user_entry = Entry(tab, width=20, font=('Arial', 11))
        self.proxy_user_entry.grid(row=4, column=1, padx=8, pady=8, sticky="w")

        Label(tab, text="Senha:", font=('Arial', 11, 'bold'), 
             bg="#f7faff").grid(row=5, column=0, padx=8, pady=8, sticky="e")
        self.proxy_pass_entry = Entry(tab, width=20, show="*", font=('Arial', 11))
        self.proxy_pass_entry.grid(row=5, column=1, padx=8, pady=8, sticky="w")

        # Botões
        btn_save = Button(
            tab, text=LANG["save_settings"], command=self._save_settings, 
            width=20, bg="#4F81BD", fg="white", font=('Arial', 11, 'bold'))
        btn_save.grid(row=6, column=0, columnspan=2, pady=14)

        btn_clear = Button(
            tab, text=LANG["clear_cache"], command=self._clear_cache, 
            width=20, bg="#ffcccc", font=('Arial', 11, 'bold'))
        btn_clear.grid(row=7, column=0, columnspan=2, pady=8)

        # Expansão automática
        tab.grid_rowconfigure(8, weight=1)
        tab.grid_columnconfigure(1, weight=1)

    def _create_help_tab(self):
        """Cria a aba de ajuda"""
        tab = Frame(self.notebook, bg="#f7faff")
        self.notebook.add(tab, text="Ajuda")

        help_text = (
            "Bem-vindo ao Consultor de CNPJ!\n\n"
            "• Consulta Individual:\n"
            "  - Digite o CNPJ e clique em 'Processar' ou pressione Enter.\n"
            "  - Use o botão 'Limpar' para apagar o campo e o resultado.\n\n"
            "• Processamento em Lote:\n"
            "  - Selecione um arquivo Excel ou CSV com uma coluna de CNPJs.\n"
            "  - Informe o nome da coluna (padrão: CNPJ).\n"
            "  - Escolha onde salvar o resultado.\n"
            "  - Clique em 'Processar' para iniciar.\n"
            "  - A barra de progresso mostrará o andamento.\n\n"
            "• Configurações:\n"
            "  - Limite de requisições/min: ajuste para evitar bloqueio da API.\n"
            "  - Tempo de espera: tempo de pausa ao atingir o limite.\n"
            "  - Proxy: preencha se sua rede exigir proxy.\n\n"
            "• Atalhos e Dicas:\n"
            "  - Enter: processa o CNPJ na aba individual.\n"
            "  - Esc: limpa o campo CNPJ.\n"
            "  - Ctrl+V: cola no campo CNPJ.\n"
            "  - O log abaixo mostra todas as ações e mensagens do sistema.\n\n"
            "• Dúvidas frequentes:\n"
            "  - O arquivo de saída será salvo em Excel, com abas para dados e histórico de IEs.\n"
            "  - CNPJs inválidos ou com erro serão destacados no resultado.\n"
            "  - Para suporte, consulte o desenvolvedor.\n"
        )

        text = Text(tab, wrap="word", font=("Arial", 11), 
                   bg="#f7faff", relief="flat", borderwidth=0)
        text.insert(END, help_text)
        text.config(state="disabled")
        text.pack(fill="both", expand=True, padx=8, pady=8)

        # Expansão automática
        tab.grid_rowconfigure(1, weight=1)
        tab.grid_columnconfigure(0, weight=1)

    def _create_log_area(self, parent):
        """Cria a área de log na parte inferior"""
        log_frame = Frame(parent)
        log_frame.pack(fill="both", expand=True)
        
        Label(log_frame, text=LANG["log_title"]).pack(anchor="w")
        
        self.log_text = Text(log_frame, height=8, width=100, state="disabled")
        self.log_text.pack(fill="both", expand=True, padx=5, pady=5)
        
        scrollbar = Scrollbar(log_frame, command=self.log_text.yview)
        scrollbar.pack(side="right", fill="y")
        self.log_text.config(yscrollcommand=scrollbar.set)

    def _select_input_file(self):
        """Abre diálogo para selecionar arquivo de entrada"""
        filename = filedialog.askopenfilename(
            title="Selecione o arquivo com CNPJs",
            filetypes=[("Excel", "*.xlsx *.xls"), ("CSV", "*.csv"), ("Todos", "*.*")]
        )
        if filename:
            self.input_entry.delete(0, END)
            self.input_entry.insert(0, filename)
    
    def _select_output_file(self):
        """Abre diálogo para selecionar arquivo de saída"""
        filename = filedialog.asksaveasfilename(
            title="Salvar resultados",
            defaultextension=".xlsx",
            filetypes=[("Excel", "*.xlsx"), ("Todos", "*.*")],
            initialfile="resultados_cnpj.xlsx"
        )
        if filename:
            self.output_entry.delete(0, END)
            self.output_entry.insert(0, filename)
    
    def _start_processing(self):
        """Inicia o processamento em lote em uma thread separada"""
        input_file = self.input_entry.get()
        output_file = self.output_entry.get()
        coluna = self.col_entry.get()
        
        if not input_file or not output_file:
            messagebox.showerror(LANG["error"], LANG["select_files"])
            self._set_status(LANG["error"], LANG["select_files"])
            return
        
        if os.path.exists(output_file):
            if not messagebox.askyesno(LANG["info"], LANG["overwrite"]):
                return
        
        self.process_btn.config(state="disabled")
        self.cancel_btn.config(state="normal")
        self.progress_bar["value"] = 0
        self._set_status(LANG["info"], LANG["start"])
        self._log_message(f"Iniciando processamento de {os.path.basename(input_file)}", "info")
        
        self.processing_thread = threading.Thread(
            target=self.consultor.processar_planilha,
            args=(input_file, output_file, coluna, self.progress_queue),
            daemon=True
        )
        self.processing_thread.start()

    def _set_status(self, status_type, message):
        """Atualiza a barra de status
        
        Args:
            status_type (str): Tipo de status ("success", "error", "info")
            message (str): Mensagem a ser exibida
        """
        color = {"success": "#d4edda", "error": "#f8d7da", "info": "#e0e0e0"}
        fg_color = {"success": "#155724", "error": "#721c24", "info": "#333"}
        icon = {
            "success": self.icon_success,
            "error": self.icon_error,
            "info": self.icon_info
        }
        self.status_label.config(
            text=f"{icon.get(status_type, '')} {message}",
            bg=color.get(status_type, "#e0e0e0"),
            fg=fg_color.get(status_type, "#333")
        )

    def _consultar_individual(self):
        """Realiza uma consulta individual de CNPJ"""
        cnpj = self.cnpj_entry.get().strip()
        if not cnpj:
            messagebox.showerror(LANG["error"], LANG["enter_cnpj"])
            self._set_status("error", LANG["enter_cnpj"])
            return
        
        cnpj_limpo = self.consultor.clean_cnpj(cnpj)
        if len(cnpj_limpo) != 14:
            messagebox.showerror(LANG["error"], LANG["invalid_cnpj"])
            self._set_status("error", LANG["invalid_cnpj"])
            return
        
        self._log_message(LANG["consulting"].format(cnpj=cnpj_limpo), "info")
        self._set_status("info", LANG["consulting"].format(cnpj=cnpj_limpo))
        
        dados = self.consultor.consultar_cnpj(cnpj_limpo)
        
        if dados:
            resultado = self.consultor.extrair_dados(dados)
            self._display_result(resultado)
            self._log_message(LANG["consult_success"], "success")
            self._set_status("success", LANG["consult_success"])
        else:
            self._log_message(LANG["consult_fail"].format(cnpj=cnpj_limpo), "error")
            self._set_status("error", LANG["consult_fail"].format(cnpj=cnpj_limpo))
            messagebox.showerror(LANG["error"], LANG["consult_fail"].format(cnpj=cnpj_limpo))

    def _display_result(self, resultado):
        """Exibe o resultado da consulta na área de texto
        
        Args:
            resultado (dict): Dados do CNPJ formatados
        """
        self.result_text.config(state="normal")
        self.result_text.delete(1.0, END)
        
        if not resultado:
            self.result_text.insert(END, LANG["no_result"])
            return
        
        for chave, valor in resultado.items():
            if chave != 'INSCRICOES_ESTADUAIS':
                self.result_text.insert(END, f"{chave:.<25}: {valor}\n")
        
        # Mostra detalhes das IEs
        if 'INSCRICOES_ESTADUAIS' in resultado:
            try:
                ies = json.loads(resultado['INSCRICOES_ESTADUAIS'])
                self.result_text.insert(END, f"\n{LANG['ies_title']}\n")
                for ie in ies:
                    self.result_text.insert(END, f"\nNúmero: {ie.get('NUMERO', '')}")
                    self.result_text.insert(END, f"\nUF: {ie.get('UF', '')}")
                    self.result_text.insert(END, f"\nTipo: {ie.get('TIPO', '')}")
                    self.result_text.insert(END, f"\nSituação: {ie.get('SITUACAO', '')}")
                    self.result_text.insert(END, f"\nData Situação: {ie.get('DATA_SITUACAO', '')}")
                    self.result_text.insert(END, f"\nAtiva: {ie.get('ATIVA', '')}")
                    self.result_text.insert(END, "\n" + "-"*50 + "\n")
            except:
                self.result_text.insert(END, f"\n{LANG['ies_error']}\n")
        
        self.result_text.config(state="disabled")

    def _log_message(self, message, level="info"):
        """Adiciona mensagem ao log
        
        Args:
            message (str): Mensagem a ser registrada
            level (str): Nível da mensagem ("info", "success", "error")
        """
        now = datetime.now().strftime('%H:%M:%S')
        prefix = {
            "info": f"{self.icon_info} ",
            "success": f"{self.icon_success} ",
            "error": f"{self.icon_error} "
        }.get(level, "")
        log_line = f"{now} - {prefix}{message}\n"

        self.log_text.config(state="normal")
        self.log_text.insert(END, log_line)
        self.log_text.see(END)
        self.log_text.config(state="disabled")

        # Salva log em arquivo
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(log_line)
        except Exception:
            pass

    def _check_queue(self):
        """Verifica a fila de progresso e atualiza a interface"""
        try:
            while not self.progress_queue.empty():
                msg_type, content = self.progress_queue.get_nowait()
                
                if msg_type == "progress":
                    current, total, cnpj = content
                    percent = (current / total) * 100
                    self.progress_bar["value"] = percent
                    status = f"Processando {current}/{total} ({percent:.1f}%) - CNPJ: {cnpj}"
                    self._set_status("info", status)
                    self.status_label.config(text=status)
                
                elif msg_type == "info":
                    self._log_message(content, "info")
                    self._set_status("info", content)
                
                elif msg_type == "error":
                    self._log_message(f"{LANG['error']}: {content}", "error")
                    self._set_status("error", content)
                    messagebox.showerror(LANG["error"], content)
                    self._reset_processing_ui()
                
                elif msg_type == "success":
                    self._log_message(content, "success")
                    self._set_status("success", content)
                    messagebox.showinfo(LANG["success"], content)
                    self._reset_processing_ui()
        
        except Exception as e:
            self._log_message(f"Erro ao processar fila: {str(e)}", "error")
        
        self.root.after(100, self._check_queue)

    def _reset_processing_ui(self):
        """Reinicia a UI após conclusão do processamento"""
        self.process_btn.config(state="normal")
        self.cancel_btn.config(state="disabled")
        self._set_status("info", LANG["ready"])

    def _save_settings(self):
        """Salva as configurações alteradas pelo usuário"""
        try:
            self.consultor.limite_requisicoes = int(self.limit_entry.get())
            self.consultor.tempo_espera = int(self.wait_entry.get())
            
            # Configurações de proxy
            proxies = {}
            if self.proxy_http_entry.get():
                proxies['http'] = self.proxy_http_entry.get()
            if self.proxy_https_entry.get():
                proxies['https'] = self.proxy_https_entry.get()
            auth = None
            if self.proxy_user_entry.get() and self.proxy_pass_entry.get():
                auth = (self.proxy_user_entry.get(), self.proxy_pass_entry.get())
            self.consultor.session.proxies = proxies
            self.consultor.session.auth = auth
            
            messagebox.showinfo(LANG["success"], LANG["settings_saved"])
            self._set_status("success", LANG["settings_saved"])
            self._log_message(LANG["settings_saved"], "success")
        except ValueError:
            messagebox.showerror(LANG["error"], LANG["invalid_values"])
            self._set_status("error", LANG["invalid_values"])
            self._log_message(LANG["invalid_values"], "error")

    def _clear_cache(self):
        """Limpa o cache de consultas"""
        self.consultor.cache = {}
        self.consultor._save_cache()
        messagebox.showinfo(LANG["info"], LANG["cache_cleared"])
        self._set_status("success", LANG["cache_cleared"])
        self._log_message(LANG["cache_cleared"], "success")

    def _cancel_processing(self):
        """Cancela o processamento em andamento"""
        self.consultor.stop_processing = True
        self._set_status("info", LANG["cancel_request"])
        self._log_message(LANG["cancel_request"], "info")
        self.cancel_btn.config(state="disabled")


def main():
    """Função principal para iniciar a aplicação"""
    root = Tk()
    app = CNPJConsultorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()