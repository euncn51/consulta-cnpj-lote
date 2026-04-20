"""
Módulo de constantes e configurações do Consultor de CNPJ

Contém todos os textos, URLs e configurações padrão do sistema.
"""

# Dicionário de textos para internacionalização
LANG = {
    "title": "Consultor de CNPJ",
    "individual_tab": "Consulta Individual",
    "batch_tab": "Processamento em Lote",
    "settings_tab": "Configurações",
    "log_title": "Log de Atividades:",
    "input_file": "Arquivo de Entrada:",
    "output_file": "Arquivo de Saída:",
    "select": "Selecionar",
    "col_cnpj": "Coluna CNPJ:",
    "process": "Processar",
    "cancel": "Cancelar",
    "ready": "Pronto",
    "start": "Iniciando...",
    "success": "Sucesso",
    "error": "Erro",
    "info": "Info",
    "save_settings": "Salvar Configurações",
    "clear_cache": "Limpar Cache",
    "limit_label": "Limite de requisições/min:",
    "wait_label": "Tempo de espera (seg):",
    "overwrite": "Arquivo de saída já existe. Sobrescrever?",
    "select_files": "Selecione os arquivos de entrada e saída!",
    "processing_cancelled": "Processamento cancelado",
    "processing_done": "Processamento concluído",
    "cache_cleared": "Cache limpo com sucesso!",
    "settings_saved": "Configurações salvas com sucesso!",
    "invalid_values": "Valores inválidos! Use números inteiros.",
    "enter_cnpj": "Digite um CNPJ para consultar!",
    "invalid_cnpj": "CNPJ inválido! Deve conter 14 dígitos.",
    "consulting": "Consultando CNPJ: {cnpj}",
    "consult_success": "Consulta realizada com sucesso!",
    "consult_fail": "Falha na consulta do CNPJ {cnpj}",
    "no_result": "Nenhum resultado encontrado.",
    "ies_title": "INSCRIÇÕES ESTADUAIS:",
    "ies_error": "Erro ao processar inscrições estaduais",
    "cancel_request": "Solicitação de cancelamento enviada...",
    "log_file": "log_cnpj.txt"
}

# Configurações da API
API_CONFIG = {
    "base_url": "https://open.cnpja.com/office/",
    "default_rate_limit": 3,  # requisições por minuto
    "default_wait_time": 65,  # segundos
    "timeout": 10,  # segundos para timeout da requisição
    "cache_file": "cnpj_cache.json",
    "ibge_timeout": 5  # segundos para timeout da API do IBGE
}

# Configurações de estilo para Excel
EXCEL_STYLES = {
    "header_font": {"bold": True, "color": "FFFFFF"},
    "header_fill": {"patternType": "solid", "fgColor": "4F81BD"},
    "column_widths": {
        "main": {
            'A': 18, 'B': 40, 'C': 30, 'D': 30, 'E': 10, 'F': 20,
            'G': 20, 'H': 10, 'I': 20, 'J': 10, 'K': 5, 'L': 15,
            'M': 30, 'N': 15, 'O': 20, 'P': 20, 'Q': 5, 'R': 20, 'S': 15
        },
        "history": {
            'A': 18, 'B': 40, 'C': 20, 'D': 5, 'E': 15,
            'F': 20, 'G': 15, 'H': 10
        }
    }
}