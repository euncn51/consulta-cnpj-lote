"""
Módulo da interface gráfica do Consultor de CNPJ v2.0 - Versão Completa

Implementa a interface usando Tkinter com organização mais lógica:
- Abas para consulta individual e em lote
- Configurações e ferramentas integradas em uma única aba
- Log de status visível para o usuário
- Controle de progresso
- Exibição de logs
- Monitoramento de status das APIs em tempo real
"""

import json
import os
import threading
from queue import Queue
from datetime import datetime
from tkinter import (
    LabelFrame, Tk, Frame, Label, Entry, Button, Text, Scrollbar, END, 
    messagebox, filedialog, Toplevel, Menu, StringVar
)
from tkinter import ttk
import webbrowser

from constants_v2 import LANG, SYSTEM_INFO, HELP_MESSAGES
from api_client_v2 import CNPJConsultor
from api_status import APIStatusMonitor, BackgroundStatusChecker

class StatusDetailDialog:
    """Diálogo para mostrar status detalhado das APIs"""
    
    def __init__(self, parent, status_data):
        self.top = Toplevel(parent)
        self.top.title("Status Detalhado das APIs")
        self.top.geometry("600x400")
        self.top.resizable(True, True)
        self.top.configure(bg="#f7faff")
        
        # Centralizar na tela
        self.top.transient(parent)
        self.top.grab_set()
        
        self._create_widgets(status_data)
    
    def _create_widgets(self, status_data):
        """Cria os widgets do diálogo"""
        main_frame = Frame(self.top, padx=20, pady=20, bg="#f7faff")
        main_frame.pack(fill="both", expand=True)
        
        # Título
        Label(main_frame, text="Status Detalhado das APIs", 
              font=('Arial', 16, 'bold'), bg="#f7faff", fg="#2c3e50").pack(pady=(0, 20))
        
        # Frame para cada API
        for api_type, api_data in status_data.items():
            frame = Frame(main_frame, relief="groove", bd=2, padx=15, pady=15, bg="#ffffff")
            frame.pack(fill="x", pady=8)
            
            api_name = "API CNPJ" if api_type == "cnpj" else "API IBGE"
            status = api_data.get('status', 'unknown')
            emoji = '✅' if status == 'online' else '❌'
            status_color = "green" if status == 'online' else "red"
            
            # Header
            header_frame = Frame(frame, bg="#ffffff")
            header_frame.pack(fill="x", pady=(0, 10))
            
            Label(header_frame, text=f"{api_name}", 
                  font=('Arial', 12, 'bold'), bg="#ffffff").pack(side="left")
            
            Label(header_frame, text=f"{emoji} {status.upper()}", 
                  fg=status_color, font=('Arial', 11, 'bold'), bg="#ffffff").pack(side="right")
            
            # Detalhes
            details_frame = Frame(frame, bg="#ffffff")
            details_frame.pack(fill="x")
            
            # Grid para detalhes
            row = 0
            if api_data.get('last_check'):
                Label(details_frame, text="Última verificação:", 
                      font=('Arial', 9, 'bold'), bg="#ffffff").grid(row=row, column=0, sticky="w", padx=(0, 5))
                Label(details_frame, text=api_data['last_check'].strftime('%d/%m/%Y %H:%M:%S'),
                      font=('Arial', 9), bg="#ffffff").grid(row=row, column=1, sticky="w")
                row += 1
            
            Label(details_frame, text="Tempo de resposta:", 
                  font=('Arial', 9, 'bold'), bg="#ffffff").grid(row=row, column=0, sticky="w", padx=(0, 5))
            Label(details_frame, text=f"{api_data.get('response_time', 0):.0f} ms",
                      font=('Arial', 9), bg="#ffffff").grid(row=row, column=1, sticky="w")
            row += 1
            
            Label(details_frame, text="Erros consecutivos:", 
                  font=('Arial', 9, 'bold'), bg="#ffffff").grid(row=row, column=0, sticky="w", padx=(0, 5))
            Label(details_frame, text=str(api_data.get('error_count', 0)),
                      font=('Arial', 9), bg="#ffffff").grid(row=row, column=1, sticky="w")
            row += 1
            
            Label(details_frame, text="URL:", 
                  font=('Arial', 9, 'bold'), bg="#ffffff").grid(row=row, column=0, sticky="w", padx=(0, 5))
            url_label = Label(details_frame, text=api_data.get('url', 'N/A'),
                             font=('Arial', 8), fg="blue", bg="#ffffff", cursor="hand2")
            url_label.grid(row=row, column=1, sticky="w")
            url_label.bind("<Button-1>", lambda e, url=api_data.get('url', ''): webbrowser.open(url))
            row += 1
            
            # Avaliação de performance
            response_time = api_data.get('response_time', 0)
            if response_time > 0:
                Label(details_frame, text="Performance:", 
                      font=('Arial', 9, 'bold'), bg="#ffffff").grid(row=row, column=0, sticky="w", padx=(0, 5))
                
                if response_time < 500:
                    perf_text = "Ótima ⭐"
                    perf_color = "green"
                elif response_time < 1000:
                    perf_text = "Boa 👍"
                    perf_color = "darkgreen"
                elif response_time < 2000:
                    perf_text = "Aceitável ✅"
                    perf_color = "orange"
                else:
                    perf_text = "Lenta ⚠️"
                    perf_color = "red"
                
                Label(details_frame, text=perf_text, fg=perf_color,
                      font=('Arial', 9, 'bold'), bg="#ffffff").grid(row=row, column=1, sticky="w")
        
        # Botões
        btn_frame = Frame(main_frame, bg="#f7faff")
        btn_frame.pack(pady=20)
        
        Button(btn_frame, text="🔄 Verificar Agora", command=self._check_now,
               width=15, bg="#3498db", fg="white", font=('Arial', 10, 'bold')).pack(side="left", padx=5)
        
        Button(btn_frame, text="Fechar", command=self.top.destroy,
               width=15, bg="#95a5a6", fg="white", font=('Arial', 10)).pack(side="left", padx=5)
    
    def _check_now(self):
        """Força verificação imediata"""
        # Esta funcionalidade seria implementada com callback para a main app
        messagebox.showinfo("Verificar", "Verificação manual seria implementada aqui")

class CNPJConsultorGUI:
    """
    Classe principal da interface gráfica v2.0 - Versão Completa
    
    Atributos:
        root (Tk): Janela principal
        consultor (CNPJConsultor): Instância do consultor de CNPJ
        processing_thread (Thread): Thread de processamento
        progress_queue (Queue): Fila para comunicação com a thread
        log_file (str): Caminho do arquivo de log
        status_checker (BackgroundStatusChecker): Verificador de status em background
    """
    
    def __init__(self, root):
        self.root = root
        self.root.title(f"{LANG['title']} {SYSTEM_INFO['version']}")
        self.root.geometry("1000x800")
        self.root.minsize(900, 700)
        
        # Configurar ícone (se disponível)
        try:
            self.root.iconbitmap("icon.ico")
        except:
            pass
        
        # Inicializar o consultor com callback para log
        self.consultor = CNPJConsultor(log_callback=self._log_message)
        self.processing_thread = None
        self.progress_queue = Queue()
        self.log_file = LANG["log_file"]
        
        # Sistema de monitoramento de APIs v2.0
        self.status_checker = BackgroundStatusChecker(
            self.consultor.status_monitor, 
            self._update_status_display
        )
        
        # Ícones para status (apenas emojis)
        self.icon_success = "✅"
        self.icon_error = "❌"
        self.icon_info = "ℹ️"
        self.icon_warning = "⚠️"

        # Variável para status atual
        self.current_status = StringVar()
        self.current_status.set(LANG["ready"])

        self._setup_ui()
        self._check_queue()
        self._start_background_monitoring()
        
        # Bind global de teclado
        self._setup_keyboard_bindings()
    
    def _setup_ui(self):
        """Configura todos os componentes da interface"""
        # Configurar estilo
        self._configure_styles()
        
        main_frame = Frame(self.root, padx=10, pady=10, bg="#f7faff")
        main_frame.pack(fill="both", expand=True)
        
        # Criar menu superior simplificado (apenas Ajuda)
        self._create_menu_bar()
        
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill="both", expand=True, pady=(0, 5))
        
        self._create_individual_tab()
        self._create_batch_tab()
        self._create_settings_tools_tab()  # Aba unificada de Configurações e Ferramentas
        self._create_help_tab()
        
        self._create_log_area(main_frame)
        self._create_status_bar(main_frame)
        self._create_api_status_bar(main_frame)
        
        # Status inicial
        self._update_status_display(self.consultor.get_api_status())
    
    def _configure_styles(self):
        """Configura estilos para os widgets"""
        style = ttk.Style()
        style.configure('TNotebook', background='#f7faff')
        style.configure('TNotebook.Tab', font=('Arial', 10, 'bold'))
        style.configure('TFrame', background='#f7faff')
        
        # Configurar cores
        self.colors = {
            'primary': '#3498db',
            'success': '#27ae60',
            'danger': '#e74c3c',
            'warning': '#f39c12',
            'info': '#95a5a6',
            'light': '#ecf0f1',
            'dark': '#2c3e50'
        }
    
    def _create_menu_bar(self):
        """Cria a barra de menu superior simplificada (apenas Ajuda)"""
        menubar = Menu(self.root)
        self.root.config(menu=menubar)
        
        # Menu Ajuda apenas
        help_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ajuda", menu=help_menu)
        help_menu.add_command(label="Documentação", command=self._show_docs)
        help_menu.add_command(label="Sobre", command=self._show_about)
    
    def _create_individual_tab(self):
        """Cria a aba de consulta individual"""
        tab = Frame(self.notebook, bg="#f7faff")
        self.notebook.add(tab, text=LANG["individual_tab"])

        # Frame de entrada
        input_frame = Frame(tab, bg="#f7faff", pady=10)
        input_frame.pack(fill="x", padx=10, pady=5)

        # Campo CNPJ
        Label(input_frame, text="CNPJ:", font=('Arial', 12, 'bold'), bg="#f7faff").grid(
            row=0, column=0, padx=8, pady=8, sticky="e")
        
        self.cnpj_entry = Entry(input_frame, width=25, font=('Arial', 14))
        self.cnpj_entry.grid(row=0, column=1, padx=8, pady=8, sticky="we")
        self.cnpj_entry.bind('<Return>', lambda e: self._consultar_individual())
        self.cnpj_entry.focus_set()

        # Botões
        btn_frame = Frame(input_frame, bg="#f7faff")
        btn_frame.grid(row=0, column=2, columnspan=2, padx=8, pady=8)

        btn_process = Button(
            btn_frame, text=LANG["process"], command=self._consultar_individual,
            width=12, bg=self.colors['primary'], fg="white", 
            font=('Arial', 11, 'bold'), cursor="hand2")
        btn_process.pack(side="left", padx=4)

        btn_clear = Button(
            btn_frame, text="Limpar", command=self._limpar_individual,
            width=10, bg=self.colors['info'], fg="white", 
            font=('Arial', 10), cursor="hand2")
        btn_clear.pack(side="left", padx=4)

        # Dica rápida
        tip_label = Label(input_frame, text=HELP_MESSAGES["cnpj_input"], 
                         font=('Arial', 9), fg="gray", bg="#f7faff")
        tip_label.grid(row=1, column=0, columnspan=4, pady=(0, 10))

        # Área de resultados
        result_frame = Frame(tab, bg="#f7faff")
        result_frame.pack(fill="both", expand=True, padx=10, pady=5)

        Label(result_frame, text="Resultado:", font=('Arial', 11, 'bold'), 
              bg="#f7faff").pack(anchor="w", pady=(0, 5))

        self.result_text = Text(
            result_frame, height=20, width=90, state="disabled", 
            font=('Consolas', 10), bg="#ffffff", relief="sunken", bd=2,
            wrap="word")
        
        text_scrollbar = Scrollbar(result_frame, command=self.result_text.yview)
        self.result_text.config(yscrollcommand=text_scrollbar.set)

        self.result_text.pack(side="left", fill="both", expand=True)
        text_scrollbar.pack(side="right", fill="y")

        # Expansão automática
        input_frame.columnconfigure(1, weight=1)
        tab.columnconfigure(0, weight=1)
        tab.rowconfigure(1, weight=1)

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
        
        # Frame principal
        main_frame = Frame(tab, bg="#f7faff", padx=20, pady=20)
        main_frame.pack(fill="both", expand=True)
        
        # Arquivo de entrada
        input_frame = Frame(main_frame, bg="#f7faff")
        input_frame.pack(fill="x", pady=8)
        
        Label(input_frame, text=LANG["input_file"], font=('Arial', 11, 'bold'), 
             bg="#f7faff").grid(row=0, column=0, padx=8, pady=8, sticky="e")
        
        self.input_entry = Entry(input_frame, font=('Arial', 11))
        self.input_entry.grid(row=0, column=1, padx=8, pady=8, sticky="we")
        
        btn_input = Button(
            input_frame, text=LANG["select"], command=self._select_input_file, 
            width=12, bg=self.colors['info'], fg="white", 
            font=('Arial', 10, 'bold'), cursor="hand2")
        btn_input.grid(row=0, column=2, padx=8, pady=8)
        
        # Arquivo de saída
        output_frame = Frame(main_frame, bg="#f7faff")
        output_frame.pack(fill="x", pady=8)
        
        Label(output_frame, text=LANG["output_file"], font=('Arial', 11, 'bold'), 
             bg="#f7faff").grid(row=0, column=0, padx=8, pady=8, sticky="e")
        
        self.output_entry = Entry(output_frame, font=('Arial', 11))
        self.output_entry.grid(row=0, column=1, padx=8, pady=8, sticky="we")
        
        btn_output = Button(
            output_frame, text=LANG["select"], command=self._select_output_file, 
            width=12, bg=self.colors['info'], fg="white", 
            font=('Arial', 10, 'bold'), cursor="hand2")
        btn_output.grid(row=0, column=2, padx=8, pady=8)
        
        # Coluna CNPJ
        col_frame = Frame(main_frame, bg="#f7faff")
        col_frame.pack(fill="x", pady=8)
        
        Label(col_frame, text=LANG["col_cnpj"], font=('Arial', 11, 'bold'), 
             bg="#f7faff").grid(row=0, column=0, padx=8, pady=8, sticky="e")
        
        self.col_entry = Entry(col_frame, width=20, font=('Arial', 11))
        self.col_entry.grid(row=0, column=1, padx=8, pady=8, sticky="w")
        self.col_entry.insert(0, "CNPJ")
        
        # Dica
        tip_label = Label(main_frame, text=HELP_MESSAGES["batch_processing"], 
                         font=('Arial', 9), fg="gray", bg="#f7faff")
        tip_label.pack(pady=(0, 20))
        
        # Botões de processamento
        btn_frame = Frame(main_frame, bg="#f7faff")
        btn_frame.pack(pady=20)
        
        self.process_btn = Button(
            btn_frame, text=LANG["process"], command=self._start_processing, 
            width=15, bg=self.colors['primary'], fg="white", 
            font=('Arial', 11, 'bold'), cursor="hand2")
        self.process_btn.pack(side="left", padx=8)
        
        self.cancel_btn = Button(
            btn_frame, text=LANG["cancel"], command=self._cancel_processing, 
            state="disabled", width=15, bg=self.colors['danger'], fg="white", 
            font=('Arial', 11), cursor="hand2")
        self.cancel_btn.pack(side="left", padx=8)
        
        # Barra de progresso
        progress_frame = Frame(main_frame, bg="#f7faff")
        progress_frame.pack(fill="x", pady=10)
        
        Label(progress_frame, text="Progresso:", font=('Arial', 10, 'bold'), 
              bg="#f7faff").pack(anchor="w")
        
        self.progress_bar = ttk.Progressbar(
            progress_frame, orient="horizontal", length=500, mode="determinate")
        self.progress_bar.pack(fill="x", pady=5)
        
        self.progress_label = Label(progress_frame, text="0%", 
                                   font=('Arial', 9), bg="#f7faff")
        self.progress_label.pack(anchor="e")
        
        # Expansão automática
        input_frame.columnconfigure(1, weight=1)
        output_frame.columnconfigure(1, weight=1)
        main_frame.columnconfigure(0, weight=1)

    def _create_settings_tools_tab(self):
        """Cria a aba unificada de configurações e ferramentas"""
        tab = Frame(self.notebook, bg="#f7faff")
        self.notebook.add(tab, text="Configurações e Ferramentas")
        
        main_frame = Frame(tab, bg="#f7faff", padx=20, pady=20)
        main_frame.pack(fill="both", expand=True)
        
        # Frame de configurações da API
        api_frame = LabelFrame(main_frame, text="Configurações da API", 
                              font=('Arial', 12, 'bold'), bg="#f7faff", padx=10, pady=10)
        api_frame.pack(fill="x", pady=10)
        
        # Limite de requisições
        Label(api_frame, text=LANG["limit_label"], font=('Arial', 10), 
             bg="#f7faff").grid(row=0, column=0, padx=8, pady=8, sticky="e")
        
        self.limit_entry = Entry(api_frame, width=8, font=('Arial', 10))
        self.limit_entry.grid(row=0, column=1, padx=8, pady=8, sticky="w")
        self.limit_entry.insert(0, str(self.consultor.limite_requisicoes))
        
        # Tempo de espera
        Label(api_frame, text=LANG["wait_label"], font=('Arial', 10), 
             bg="#f7faff").grid(row=1, column=0, padx=8, pady=8, sticky="e")
        
        self.wait_entry = Entry(api_frame, width=8, font=('Arial', 10))
        self.wait_entry.grid(row=1, column=1, padx=8, pady=8, sticky="w")
        self.wait_entry.insert(0, str(self.consultor.tempo_espera))
        
        # Frame de Ferramentas
        tools_frame = LabelFrame(main_frame, text="Ferramentas", 
                               font=('Arial', 12, 'bold'), bg="#f7faff", padx=10, pady=10)
        tools_frame.pack(fill="x", pady=10)
        
        # Botões de ferramentas
        tools_btn_frame = Frame(tools_frame, bg="#f7faff")
        tools_btn_frame.pack(pady=10)
        
        Button(tools_btn_frame, text="🔄 Verificar Status APIs", 
               command=self._manual_status_check, width=20,
               bg="#3498db", fg="white", font=('Arial', 10, 'bold')).pack(pady=5)
        
        Button(tools_btn_frame, text="🗑️ Limpar Cache", 
               command=self._clear_cache, width=20,
               bg="#e74c3c", fg="white", font=('Arial', 10, 'bold')).pack(pady=5)
        
        Button(tools_btn_frame, text="📊 Estatísticas", 
               command=self._show_stats, width=20,
               bg="#27ae60", fg="white", font=('Arial', 10, 'bold')).pack(pady=5)
        
        # Frame de Proxy
        proxy_frame = LabelFrame(main_frame, text="Configurações de Proxy", 
                               font=('Arial', 12, 'bold'), bg="#f7faff", padx=10, pady=10)
        proxy_frame.pack(fill="x", pady=10)
        
        Label(proxy_frame, text="Proxy HTTP:", font=('Arial', 10), 
             bg="#f7faff").grid(row=0, column=0, padx=8, pady=8, sticky="e")
        
        self.proxy_http_entry = Entry(proxy_frame, width=30, font=('Arial', 10))
        self.proxy_http_entry.grid(row=0, column=1, padx=8, pady=8, sticky="w")
        
        Label(proxy_frame, text="Proxy HTTPS:", font=('Arial', 10), 
             bg="#f7faff").grid(row=1, column=0, padx=8, pady=8, sticky="e")
        
        self.proxy_https_entry = Entry(proxy_frame, width=30, font=('Arial', 10))
        self.proxy_https_entry.grid(row=1, column=1, padx=8, pady=8, sticky="w")
        
        Label(proxy_frame, text="Usuário:", font=('Arial', 10), 
             bg="#f7faff").grid(row=2, column=0, padx=8, pady=8, sticky="e")
        
        self.proxy_user_entry = Entry(proxy_frame, width=20, font=('Arial', 10))
        self.proxy_user_entry.grid(row=2, column=1, padx=8, pady=8, sticky="w")
        
        Label(proxy_frame, text="Senha:", font=('Arial', 10), 
             bg="#f7faff").grid(row=3, column=0, padx=8, pady=8, sticky="e")
        
        self.proxy_pass_entry = Entry(proxy_frame, width=20, show="*", font=('Arial', 10))
        self.proxy_pass_entry.grid(row=3, column=1, padx=8, pady=8, sticky="w")
        
        # Botão salvar
        btn_frame = Frame(main_frame, bg="#f7faff")
        btn_frame.pack(pady=20)
        
        Button(btn_frame, text="💾 Salvar Configurações", command=self._save_settings, 
               width=20, bg="#2c3e50", fg="white", font=('Arial', 11, 'bold')).pack(pady=8)
        
        # Expansão automática
        api_frame.columnconfigure(1, weight=1)
        proxy_frame.columnconfigure(1, weight=1)

    def _create_help_tab(self):
        """Cria a aba de ajuda"""
        tab = Frame(self.notebook, bg="#f7faff")
        self.notebook.add(tab, text="Ajuda")
        
        main_frame = Frame(tab, bg="#f7faff")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Texto de ajuda atualizado
        help_text = (
            f"Bem-vindo ao {SYSTEM_INFO['name']} v{SYSTEM_INFO['version']}!\n\n"
            "• 📋 Consulta Individual:\n"
            "  - Digite o CNPJ e clique em 'Processar' ou pressione Enter.\n"
            "  - Use o botão 'Limpar' para apagar o campo e o resultado.\n"
            "  - Suporta CNPJ com ou sem formatação (14 dígitos).\n\n"
            "• 📊 Processamento em Lote:\n"
            "  - Selecione um arquivo Excel ou CSV com uma coluna de CNPJs.\n"
            "  - Informe o nome da coluna (padrão: CNPJ).\n"
            "  - Escolha onde salvar o resultado.\n"
            "  - Clique em 'Processar' para iniciar.\n"
            "  - A barra de progresso mostrará o andamento.\n\n"
            "• ⚙️ Configurações e Ferramentas:\n"
            "  - Limite de requisições/min: ajuste para evitar bloqueio da API.\n"
            "  - Tempo de espera: tempo de pausa ao atingir o limite.\n"
            "  - Proxy: preencha se sua rede exigir proxy.\n"
            "  - Ferramentas: Verificar APIs, Limpar Cache, Estatísticas.\n\n"
            "• 📡 Status das APIs:\n"
            "  - Verificação automática do status a cada 5 minutos.\n"
            "  - Ícones coloridos indicam status das APIs.\n"
            "  - Clique nos status para detalhes completos.\n\n"
            "• 🚨 Tratamento de Erros:\n"
            "  - Cache inteligente para consultas repetidas.\n"
            "  - Rate limit automático para evitar bloqueios.\n"
            "  - Log detalhado de todas as operações.\n\n"
            "• 📝 Log de Atividades:\n"
            "  - Todas as ações do sistema são registradas.\n"
            "  - Útil para diagnóstico de problemas.\n\n"
            "• 💡 Dicas Rápidas:\n"
            "  - Enter: processa o CNPJ na aba individual.\n"
            "  - Esc: limpa o campo CNPJ.\n"
            "  - Ctrl+V: cola no campo CNPJ.\n"
            "  - F5: verifica status das APIs manualmente.\n\n"
            f"• 🔧 Sistema: {SYSTEM_INFO['name']} v{SYSTEM_INFO['version']}\n"
            f"• 📦 Desenvolvido por: {SYSTEM_INFO['author']}\n"
            f"• 📄 Licença: {SYSTEM_INFO['license']}\n"
        )
        
        text_widget = Text(main_frame, wrap="word", font=("Arial", 11), 
                          bg="#ffffff", relief="flat", borderwidth=2, padx=10, pady=10)
        
        text_scrollbar = Scrollbar(main_frame, command=text_widget.yview)
        text_widget.config(yscrollcommand=text_scrollbar.set)
        
        text_widget.insert(END, help_text)
        text_widget.config(state="disabled")
        
        text_widget.pack(side="left", fill="both", expand=True)
        text_scrollbar.pack(side="right", fill="y")

    def _create_log_area(self, parent):
        """Cria a área de log na parte inferior"""
        log_frame = Frame(parent, bg="#f7faff")
        log_frame.pack(fill="both", expand=True, pady=(5, 0))
        
        Label(log_frame, text=LANG["log_title"], font=('Arial', 10, 'bold'), 
              bg="#f7faff").pack(anchor="w", padx=5)
        
        log_container = Frame(log_frame, bg="#f7faff")
        log_container.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.log_text = Text(log_container, height=8, state="disabled", 
                            font=('Consolas', 9), bg="#2c3e50", fg="#ecf0f1",
                            relief="sunken", bd=2)
        
        log_scrollbar = Scrollbar(log_container, command=self.log_text.yview)
        self.log_text.config(yscrollcommand=log_scrollbar.set)
        
        self.log_text.pack(side="left", fill="both", expand=True)
        log_scrollbar.pack(side="right", fill="y")
        
        # Menu de contexto para o log
        self._create_log_context_menu()

    def _create_status_bar(self, parent):
        """Cria a barra de status na parte inferior"""
        status_frame = Frame(parent, bg="#e0e0e0", relief="sunken", bd=1, height=30)
        status_frame.pack(fill="x", pady=(5, 0))
        status_frame.pack_propagate(False)  # Manter altura fixa
        
        # Status atual
        self.status_label = Label(status_frame, textvariable=self.current_status, 
                                relief="sunken", anchor="w", bg="#e0e0e0", 
                                font=('Arial', 10), padx=10, pady=8)
        self.status_label.pack(fill="x", padx=2, pady=2)

    def _create_api_status_bar(self, parent):
        """Cria a barra de status das APIs na parte inferior"""
        status_frame = Frame(parent, bg="#34495e", relief="sunken", bd=1, height=30)
        status_frame.pack(fill="x", pady=(5, 0))
        status_frame.pack_propagate(False)  # Manter altura fixa
        
        # Título
        Label(status_frame, text=LANG["api_status_title"] + ":", 
              font=('Arial', 9, 'bold'), bg="#34495e", fg="white").pack(side="left", padx=(10, 5))
        
        # Status API CNPJ (clicável)
        self.cnpj_status_label = Label(status_frame, text="CNPJ: ❓", 
                                      font=('Arial', 9), bg="#34495e", fg="white", 
                                      cursor="hand2", padx=5)
        self.cnpj_status_label.pack(side="left", padx=5)
        self.cnpj_status_label.bind("<Button-1>", lambda e: self._show_detailed_status())
        
        # Separador
        Label(status_frame, text="|", font=('Arial', 9), bg="#34495e", fg="white").pack(side="left", padx=5)
        
        # Status API IBGE (clicável)
        self.ibge_status_label = Label(status_frame, text="IBGE: ❓", 
                                     font=('Arial', 9), bg="#34495e", fg="white", 
                                     cursor="hand2", padx=5)
        self.ibge_status_label.pack(side="left", padx=5)
        self.ibge_status_label.bind("<Button-1>", lambda e: self._show_detailed_status())
        
        # Separador
        Label(status_frame, text="|", font=('Arial', 9), bg="#34495e", fg="white").pack(side="left", padx=5)
        
        # Botões à direita
        btn_frame = Frame(status_frame, bg="#34495e")
        btn_frame.pack(side="right", padx=10, pady=2)
        
        btn_check = Button(btn_frame, text="🔄 Verificar", 
                          command=self._manual_status_check,
                          font=('Arial', 8), bg="#3498db", fg="white",
                          cursor="hand2")
        btn_check.pack(side="left", padx=2)
        
        btn_details = Button(btn_frame, text="📊 Detalhes", 
                            command=self._show_detailed_status,
                            font=('Arial', 8), bg="#2c3e50", fg="white",
                            cursor="hand2")
        btn_details.pack(side="left", padx=2)

    def _create_log_context_menu(self):
        """Cria menu de contexto para a área de log"""
        self.log_menu = Menu(self.root, tearoff=0)
        self.log_menu.add_command(label="Copiar", command=self._copy_log)
        self.log_menu.add_command(label="Limpar Log", command=self._clear_log)
        self.log_menu.add_separator()
        self.log_menu.add_command(label="Salvar Log", command=self._save_log)
        self.log_menu.add_command(label="Abrir Pasta de Logs", command=self._open_log_folder)
        
        self.log_text.bind("<Button-3>", self._show_log_context_menu)

    def _setup_keyboard_bindings(self):
        """Configura atalhos de teclado"""
        self.root.bind('<F1>', lambda e: self.notebook.select(3))  # Ajuda
        self.root.bind('<F5>', lambda e: self._manual_status_check())
        self.root.bind('<Escape>', lambda e: self._limpar_individual())
        self.root.bind('<Control-s>', lambda e: self._save_settings())
        self.root.bind('<Control-l>', lambda e: self._clear_log())

    def _start_background_monitoring(self):
        """Inicia o monitoramento em background"""
        self.status_checker.start()
        self._log_message("Monitoramento de APIs iniciado", "info")

    def _select_input_file(self):
        """Abre diálogo para selecionar arquivo de entrada"""
        filename = filedialog.askopenfilename(
            title="Selecione o arquivo com CNPJs",
            filetypes=[
                ("Excel", "*.xlsx *.xls"),
                ("CSV", "*.csv"),
                ("Todos os arquivos", "*.*")
            ]
        )
        if filename:
            self.input_entry.delete(0, END)
            self.input_entry.insert(0, filename)
            self._log_message(f"Arquivo de entrada selecionado: {os.path.basename(filename)}", "info")

    def _select_output_file(self):
        """Abre diálogo para selecionar arquivo de saída"""
        filename = filedialog.asksaveasfilename(
            title="Salvar resultados",
            defaultextension=".xlsx",
            filetypes=[
                ("Excel", "*.xlsx"),
                ("CSV", "*.csv"),
                ("Todos os arquivos", "*.*")
            ],
            initialfile="resultados_cnpj.xlsx"
        )
        if filename:
            self.output_entry.delete(0, END)
            self.output_entry.insert(0, filename)
            self._log_message(f"Arquivo de saída selecionado: {os.path.basename(filename)}", "info")

    def _start_processing(self):
        """Inicia o processamento em lote em uma thread separada"""
        input_file = self.input_entry.get()
        output_file = self.output_entry.get()
        coluna = self.col_entry.get()
        
        if not input_file or not output_file:
            messagebox.showerror(LANG["error"], LANG["select_files"])
            self._set_status("error", LANG["select_files"])
            return
        
        if not os.path.exists(input_file):
            messagebox.showerror(LANG["error"], f"Arquivo não encontrado: {input_file}")
            self._set_status("error", "Arquivo não encontrado")
            return
        
        if os.path.exists(output_file):
            if not messagebox.askyesno(LANG["info"], LANG["overwrite"]):
                return
        
        # Verificar status da API antes de iniciar
        api_status = self.consultor.get_api_status()
        if api_status.get('cnpj', {}).get('status') != 'online':
            messagebox.showwarning("API Offline", 
                                 "A API CNPJ está offline. O processamento pode falhar.")
        
        self.process_btn.config(state="disabled")
        self.cancel_btn.config(state="normal")
        self.progress_bar["value"] = 0
        self.progress_label.config(text="0%")
        self._set_status("info", LANG["start"])
        self._log_message(f"Iniciando processamento de {os.path.basename(input_file)}", "info")
        
        self.processing_thread = threading.Thread(
            target=self.consultor.processar_planilha,
            args=(input_file, output_file, coluna, self.progress_queue),
            daemon=True
        )
        self.processing_thread.start()

    def _cancel_processing(self):
        """Cancela o processamento em andamento"""
        self.consultor.stop_processing = True
        self._set_status("info", LANG["cancel_request"])
        self._log_message(LANG["cancel_request"], "info")
        self.cancel_btn.config(state="disabled")

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
        
        # Verificar status da API antes de consultar
        if not self.consultor.is_api_online('cnpj'):
            messagebox.showwarning("API Offline", 
                                 "A API CNPJ está offline. A consulta pode falhar.")
        
        dados = self.consultor.consultar_cnpj(cnpj_limpo)
        
        if dados and 'ERRO' not in dados:
            resultado = self.consultor.extrair_dados(dados)
            self._display_result(resultado)
            self._log_message(LANG["consult_success"], "success")
            self._set_status("success", LANG["consult_success"])
        else:
            error_msg = dados.get('ERRO', 'Falha na consulta') if dados else 'Falha na consulta'
            self._log_message(f"{LANG['consult_fail'].format(cnpj=cnpj_limpo)}: {error_msg}", "error")
            self._set_status("error", LANG["consult_fail"].format(cnpj=cnpj_limpo))
            messagebox.showerror(LANG["error"], f"{LANG['consult_fail'].format(cnpj=cnpj_limpo)}\nErro: {error_msg}")

    def _display_result(self, resultado):
        """Exibe o resultado da consulta na área de texto"""
        self.result_text.config(state="normal")
        self.result_text.delete(1.0, END)
        
        if not resultado or 'ERRO' in resultado:
            self.result_text.insert(END, LANG["no_result"])
            if resultado and 'ERRO' in resultado:
                self.result_text.insert(END, f"\nErro: {resultado['ERRO']}")
            return
        
        # Dados principais
        campos_principais = [
            'CNPJ', 'RAZAO_SOCIAL', 'NOME_FANTASIA', 'ENDERECO', 'NUMERO',
            'COMPLEMENTO', 'BAIRRO', 'CEP', 'MUNICIPIO', 'COD_IBGE', 'UF',
            'TELEFONE', 'EMAIL', 'SITUACAO', 'DATA_CONSULTA'
        ]
        
        for campo in campos_principais:
            if campo in resultado:
                valor = resultado[campo] if resultado[campo] is not None else "N/A"
                self.result_text.insert(END, f"{campo:.<20}: {valor}\n")
        
        # IE Ativa
        self.result_text.insert(END, f"\n{'IE ATIVA':.<20}:\n")
        ie_campos = ['IE_ATIVA_NUMERO', 'IE_ATIVA_UF', 'IE_ATIVA_SITUACAO', 'IE_ATIVA_DATA']
        for campo in ie_campos:
            if campo in resultado:
                valor = resultado[campo] if resultado[campo] is not None else "N/A"
                nome_campo = campo.replace('IE_ATIVA_', '').title()
                self.result_text.insert(END, f"  {nome_campo:.<18}: {valor}\n")
        
        # Detalhes das IEs
        if 'INSCRICOES_ESTADUAIS' in resultado and resultado['INSCRICOES_ESTADUAIS']:
            try:
                ies = json.loads(resultado['INSCRICOES_ESTADUAIS'])
                self.result_text.insert(END, f"\n{LANG['ies_title']}\n")
                self.result_text.insert(END, "=" * 50 + "\n")
                
                for i, ie in enumerate(ies, 1):
                    self.result_text.insert(END, f"\nInscrição {i}:\n")
                    self.result_text.insert(END, f"  Número:....... {ie.get('NUMERO', 'N/A')}\n")
                    self.result_text.insert(END, f"  UF:........... {ie.get('UF', 'N/A')}\n")
                    self.result_text.insert(END, f"  Tipo:......... {ie.get('TIPO', 'N/A')}\n")
                    self.result_text.insert(END, f"  Situação:..... {ie.get('SITUACAO', 'N/A')}\n")
                    self.result_text.insert(END, f"  Data Situação: {ie.get('DATA_SITUACAO', 'N/A')}\n")
                    self.result_text.insert(END, f"  Ativa:........ {ie.get('ATIVA', 'N/A')}\n")
                    self.result_text.insert(END, "-" * 50 + "\n")
                    
            except json.JSONDecodeError:
                self.result_text.insert(END, f"\n{LANG['ies_error']}\n")
        
        self.result_text.config(state="disabled")

    def _log_message(self, message, level="info"):
        """Adiciona mensagem ao log"""
        now = datetime.now().strftime('%H:%M:%S')
        prefix = {
            "info": f"{self.icon_info} ",
            "success": f"{self.icon_success} ",
            "error": f"{self.icon_error} ",
            "warning": f"{self.icon_warning} "
        }.get(level, "")
        
        log_line = f"{now} - {prefix}{message}\n"
        
        self.log_text.config(state="normal")
        self.log_text.insert(END, log_line)
        self.log_text.see(END)
        self.log_text.config(state="disabled")
        
        # Atualizar status na barra de status
        self.current_status.set(message)
        
        # Salvar log em arquivo
        try:
            with open(self.log_file, "a", encoding="utf-8") as f:
                f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {message}\n")
        except Exception as e:
            print(f"Erro ao salvar log: {e}")

    def _check_queue(self):
        """Verifica a fila de progresso e atualiza a interface"""
        try:
            while not self.progress_queue.empty():
                msg_type, content = self.progress_queue.get_nowait()
                
                if msg_type == "progress":
                    current, total, cnpj = content
                    percent = (current / total) * 100
                    self.progress_bar["value"] = percent
                    self.progress_label.config(text=f"{percent:.1f}%")
                    status = f"Processando {current}/{total} ({percent:.1f}%) - CNPJ: {cnpj}"
                    self._set_status("info", status)
                
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
        self.progress_bar["value"] = 0
        self.progress_label.config(text="0%")
        self.consultor.stop_processing = False
        self._set_status("info", LANG["ready"])

    def _set_status(self, status_type, message):
        """Atualiza a barra de status"""
        color_map = {
            "success": "#d4edda",
            "error": "#f8d7da", 
            "info": "#e0e0e0",
            "warning": "#fff3cd"
        }
        fg_color_map = {
            "success": "#155724",
            "error": "#721c24",
            "info": "#333",
            "warning": "#856404"
        }
        icon_map = {
            "success": self.icon_success,
            "error": self.icon_error,
            "info": self.icon_info,
            "warning": self.icon_warning
        }
        
        # Atualizar a barra de status
        self.status_label.config(
            text=f"{icon_map.get(status_type, '')} {message}",
            bg=color_map.get(status_type, "#e0e0e0"),
            fg=fg_color_map.get(status_type, "#333")
        )
        
        # Atualizar também a variável de status
        self.current_status.set(f"{icon_map.get(status_type, '')} {message}")

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
        if messagebox.askyesno("Confirmar", "Tem certeza que deseja limpar o cache?"):
            self.consultor.clear_cache()
            messagebox.showinfo(LANG["info"], LANG["cache_cleared"])
            self._set_status("success", LANG["cache_cleared"])
            self._log_message(LANG["cache_cleared"], "success")

    def _manual_status_check(self):
        """Verificação manual do status das APIs"""
        self._log_message("Verificando status das APIs manualmente...", "info")
        self._set_status("info", LANG["checking_status"])
        
        def check():
            try:
                status = self.consultor.check_api_status()
                self._update_status_display(status)
                self._log_message("Status das APIs verificado", "success")
                self._set_status("success", "Status atualizado")
            except Exception as e:
                self._log_message(f"Erro ao verificar status: {e}", "error")
                self._set_status("error", "Erro na verificação")
        
        threading.Thread(target=check, daemon=True).start()

    def _update_status_display(self, status_data):
        """Atualiza a exibição do status das APIs"""
        def update():
            cnpj_status = status_data.get('cnpj', {})
            ibge_status = status_data.get('ibge', {})
            
            # API CNPJ
            cnpj_emoji = '✅' if cnpj_status.get('status') == 'online' else '❌'
            cnpj_time = cnpj_status.get('response_time', 0)
            cnpj_text = f"CNPJ: {cnpj_emoji} {cnpj_time:.0f}ms"
            cnpj_color = "green" if cnpj_status.get('status') == 'online' else "red"
            
            # API IBGE
            ibge_emoji = '✅' if ibge_status.get('status') == 'online' else '❌'
            ibge_time = ibge_status.get('response_time', 0)
            ibge_text = f"IBGE: {ibge_emoji} {ibge_time:.0f}ms"
            ibge_color = "green" if ibge_status.get('status') == 'online' else "red"
            
            self.cnpj_status_label.config(text=cnpj_text, fg=cnpj_color)
            self.ibge_status_label.config(text=ibge_text, fg=ibge_color)
            
            # Tooltips
            self._set_tooltip(self.cnpj_status_label, self._get_status_tooltip(cnpj_status, 'CNPJ'))
            self._set_tooltip(self.ibge_status_label, self._get_status_tooltip(ibge_status, 'IBGE'))
        
        self.root.after(0, update)

    def _get_status_tooltip(self, status_data, api_name):
        """Gera texto para tooltip do status"""
        last_check = status_data.get('last_check')
        error_count = status_data.get('error_count', 0)
        status = status_data.get('status', 'unknown')
        response_time = status_data.get('response_time', 0)
        
        tooltip = f"{api_name}\n"
        tooltip += f"Status: {status.upper()}\n"
        
        if last_check:
            tooltip += f"Última verificação: {last_check.strftime('%d/%m/%Y %H:%M:%S')}\n"
        
        tooltip += f"Tempo resposta: {response_time:.0f}ms\n"
        tooltip += f"Erros consecutivos: {error_count}"
        
        return tooltip

    def _set_tooltip(self, widget, text):
        """Configura tooltip para um widget"""
        def enter(event):
            self.tooltip = Toplevel()
            self.tooltip.wm_overrideredirect(True)
            self.tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
            label = Label(self.tooltip, text=text, justify='left',
                         background="#ffffe0", relief='solid', borderwidth=1,
                         font=("tahoma", "8", "normal"))
            label.pack()
        
        def leave(event):
            if hasattr(self, 'tooltip'):
                self.tooltip.destroy()
        
        widget.bind('<Enter>', enter)
        widget.bind('<Leave>', leave)

    def _show_detailed_status(self):
        """Mostra diálogo com status detalhado"""
        StatusDetailDialog(self.root, self.consultor.get_api_status())

    def _show_log_context_menu(self, event):
        """Mostra menu de contexto para o log"""
        try:
            self.log_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.log_menu.grab_release()

    def _copy_log(self):
        """Copia o conteúdo do log para a área de transferência"""
        self.root.clipboard_clear()
        self.root.clipboard_append(self.log_text.get(1.0, END))
        self._log_message("Log copiado para a área de transferência", "info")

    def _clear_log(self):
        """Limpa o conteúdo do log"""
        self.log_text.config(state="normal")
        self.log_text.delete(1.0, END)
        self.log_text.config(state="disabled")
        self._log_message("Log limpo", "info")

    def _save_log(self):
        """Salva o log em um arquivo"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Arquivos de texto", "*.txt"), ("Todos os arquivos", "*.*")],
            initialfile=f"log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        )
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(self.log_text.get(1.0, END))
                self._log_message(f"Log salvo em {filename}", "success")
            except Exception as e:
                self._log_message(f"Erro ao salvar log: {e}", "error")

    def _open_log_folder(self):
        """Abre a pasta de logs"""
        try:
            folder = os.path.dirname(os.path.abspath(self.log_file))
            if os.path.exists(folder):
                os.startfile(folder)
            else:
                os.startfile(os.getcwd())
        except Exception as e:
            self._log_message(f"Erro ao abrir pasta: {e}", "error")

    def _show_stats(self):
        """Mostra estatísticas do sistema"""
        cache_stats = self.consultor.get_cache_stats()
        rate_limit = self.consultor.get_rate_limit_info()
        
        stats_text = f"""Estatísticas do Sistema:

📊 Cache:
  - Entradas totais: {cache_stats['total_entries']}
  - Entradas regulares: {cache_stats['regular_entries']}
  - Entradas IBGE: {cache_stats['ibge_entries']}
  - Tamanho do arquivo: {cache_stats['cache_file_size'] / 1024:.1f} KB

⚡ Rate Limit:
  - Requisições atuais: {rate_limit['current_requests']}
  - Limite máximo: {rate_limit['max_requests']}/min
  - Tempo de espera: {rate_limit['wait_time']}s
  - Tempo para reset: {rate_limit['time_to_reset']:.1f}s

🌐 Status APIs:
  - API CNPJ: {self.consultor.get_api_status_text('cnpj')}
  - API IBGE: {self.consultor.get_api_status_text('ibge')}
"""
        messagebox.showinfo("Estatísticas do Sistema", stats_text)

    def _show_docs(self):
        """Mostra documentação"""
        webbrowser.open(SYSTEM_INFO['repository'])

    def _show_about(self):
        """Mostra informações sobre o software"""
        about_text = f"""{SYSTEM_INFO['name']} v{SYSTEM_INFO['version']}

{SYSTEM_INFO['description']}

Desenvolvido por: {SYSTEM_INFO['author']}
Licença: {SYSTEM_INFO['license']}
Repositório: {SYSTEM_INFO['repository']}

Funcionalidades:
- Consulta individual de CNPJ
- Processamento em lote de arquivos
- Monitoramento de status das APIs
- Cache inteligente de consultas
- Interface gráfica moderna
"""
        messagebox.showinfo("Sobre", about_text)

    def __del__(self):
        """Destruidor - para a verificação em background"""
        if hasattr(self, 'status_checker'):
            self.status_checker.stop()

def main():
    """Função principal para iniciar a aplicação"""
    root = Tk()
    app = CNPJConsultorGUI(root)
    
    # Configurar tratamento de exceções
    def show_error(*args):
        import traceback
        error = traceback.format_exception(*args)
        error_msg = f"Erro não tratado: {''.join(error)}"
        print(error_msg)
        app._log_message(error_msg, "error")
        messagebox.showerror("Erro", "Ocorreu um erro inesperado. Verifique o log para detalhes.")
    
    root.report_callback_exception = show_error
    
    root.mainloop()

if __name__ == "__main__":
    main()