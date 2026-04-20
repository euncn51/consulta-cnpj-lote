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
    "ies_none": "Nenhuma inscrição estadual encontrada",
    "cancel_request": "Solicitação de cancelamento enviada...",
    "log_file": "log_cnpj.txt"
}

# Configurações da API - ATUALIZADO PARA CNPJ WS
API_CONFIG = {
    "base_url": "https://publica.cnpj.ws/cnpj/",
    "default_rate_limit": 3,  # requisições por minuto
    "default_wait_time": 65,  # segundos
    "timeout": 30,  # aumentado para 30 segundos
    "cache_file": "cnpj_cache.json",
    "ibge_timeout": 5  # segundos para timeout da API do IBGE
}

# Configurações de estilo para Excel - ATUALIZADO com NATUREZA_JURIDICA
EXCEL_STYLES = {
    "header_font": {"bold": True, "color": "FFFFFF"},
    "header_fill": {"patternType": "solid", "fgColor": "4F81BD"},
    "column_widths": {
        "main": {
            'A': 18,  # CNPJ
            'B': 40,  # RAZAO_SOCIAL
            'C': 30,  # NOME_FANTASIA
            'D': 25,  # NATUREZA_JURIDICA (NOVA COLUNA)
            'E': 30,  # ENDERECO
            'F': 10,  # NUMERO
            'G': 20,  # COMPLEMENTO
            'H': 20,  # BAIRRO
            'I': 10,  # CEP
            'J': 20,  # MUNICIPIO
            'K': 10,  # COD_IBGE
            'L': 5,   # UF
            'M': 15,  # TELEFONE
            'N': 30,  # EMAIL
            'O': 15,  # SITUACAO
            'P': 20,  # DATA_SITUACAO_CADASTRAL
            'Q': 20,  # DATA_CONSULTA
            'R': 20,  # IE_ATIVA_NUMERO
            'S': 15,  # IE_ATIVA_UF
            'T': 15,  # IE_ATIVA_SITUACAO
            'U': 15   # IE_ATIVA_DATA
        },
        "history": {
            'A': 18, 'B': 40, 'C': 20, 'D': 5, 'E': 15,
            'F': 20, 'G': 15, 'H': 10
        }
    }
}