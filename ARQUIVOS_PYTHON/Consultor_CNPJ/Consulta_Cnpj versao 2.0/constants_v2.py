"""
Módulo de constantes e configurações do Consultor de CNPJ v2.0

Contém todos os textos, URLs e configurações padrão do sistema.
Inclui sistema de monitoramento de status das APIs.
"""

# Dicionário de textos para internacionalização
LANG = {
    "title": "Consultor de CNPJ v2.0",
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
    "log_file": "log_cnpj.txt",
    
    # Novos textos para sistema de status da API v2.0
    "api_status_title": "Status das APIs",
    "api_cnpj_status": "API CNPJ:",
    "api_ibge_status": "API IBGE:",
    "status_online": "Online",
    "status_offline": "Offline",
    "status_unknown": "Desconhecido",
    "last_check": "Última verificação:",
    "response_time": "Tempo resposta:",
    "checking_status": "Verificando status...",
    "auto_check_enabled": "Verificação automática ativada",
    "auto_check_disabled": "Verificação automática desativada",
    "api_check_success": "Status das APIs verificado",
    "api_check_error": "Erro ao verificar status das APIs",
    "api_cnpj_online": "API CNPJ está online",
    "api_cnpj_offline": "API CNPJ está offline",
    "api_ibge_online": "API IBGE está online", 
    "api_ibge_offline": "API IBGE está offline",
    "api_connection_timeout": "Timeout na conexão com API",
    "api_connection_error": "Erro de conexão com API",
    "api_rate_limit": "Rate limit atingido - aguarde",
    "api_unexpected_error": "Erro inesperado na API",
    "api_retrying": "Tentando reconexão...",
    "api_max_retries": "Máximo de tentativas atingido",
    "api_health_check": "Verificação de saúde das APIs",
    "api_status_unknown": "Status da API desconhecido",
    "api_test_success": "Teste de API bem-sucedido",
    "api_test_failure": "Teste de API falhou",
    "api_monitoring_started": "Monitoramento de APIs iniciado",
    "api_monitoring_stopped": "Monitoramento de APIs parado",
    "api_status_change": "Mudança de status detectada",
    "api_all_online": "Todas as APIs estão online",
    "api_some_offline": "Algumas APIs estão offline",
    "api_all_offline": "Todas as APIs estão offline",
    "api_recovery": "API recuperada - voltou ao online",
    "api_degradation": "Degradação de performance detectada",
    "api_high_latency": "Alta latência na API",
    "api_normal_latency": "Latência normal na API",
    "api_optimal_performance": "Performance ótima da API",
    "api_acceptable_performance": "Performance aceitável da API",
    "api_poor_performance": "Performance ruim da API",
    "api_unacceptable_performance": "Performance inaceitável da API"
}

# Configurações da API
API_CONFIG = {
    "base_url": "https://open.cnpja.com/office/",
    "default_rate_limit": 3,  # requisições por minuto
    "default_wait_time": 65,  # segundos
    "timeout": 10,  # segundos para timeout da requisição
    "cache_file": "cnpj_cache.json",
    "ibge_timeout": 5,  # segundos para timeout da API do IBGE
    "max_retries": 3,  # máximo de tentativas de reconexão
    "retry_delay": 2,  # segundos entre tentativas
}

# Configurações de Status da API v2.0
API_STATUS = {
    "check_interval": 300,  # 5 minutos entre verificações
    "timeout": 10,  # timeout para verificação de status
    "status_online": "online",
    "status_offline": "offline", 
    "status_unknown": "unknown",
    "response_time_thresholds": {
        "optimal": 500,  # ms - performance ótima
        "good": 1000,    # ms - performance boa
        "acceptable": 2000,  # ms - performance aceitável
        "poor": 3000,    # ms - performance ruim
        "unacceptable": 5000  # ms - performance inaceitável
    },
    "error_threshold": 3,  # máximo de erros consecutivos antes de marcar como offline
    "recovery_threshold": 2,  # verificações bem-sucedidas consecutivas para marcar como online
    "urls": {
        "cnpj": "https://open.cnpja.com/office/00000000000191",
        "ibge": "https://servicodados.ibge.gov.br/api/v1/localidades/estados/SP/municipios"
    },
    "user_agents": [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
        "CNPJ-Consultor/2.0 (Health-Check)"
    ]
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
    },
    "status_colors": {
        "online": "00FF00",  # Verde
        "offline": "FF0000",  # Vermelho
        "unknown": "FFFF00",  # Amarelo
        "degraded": "FFA500",  # Laranja
        "high_latency": "FFCC00",  # Âmbar
    }
}

# Códigos de erro e mensagens
ERROR_CODES = {
    # Erros de API
    "API_001": "Timeout na conexão com a API",
    "API_002": "Erro de conexão com a API",
    "API_003": "Rate limit excedido",
    "API_004": "API indisponível",
    "API_005": "Resposta inválida da API",
    "API_006": "Erro de autenticação na API",
    
    # Erros de CNPJ
    "CNPJ_001": "CNPJ inválido",
    "CNPJ_002": "CNPJ não encontrado",
    "CNPJ_003": "CNPJ com formato incorreto",
    
    # Erros de arquivo
    "FILE_001": "Arquivo não encontrado",
    "FILE_002": "Formato de arquivo não suportado",
    "FILE_003": "Erro de permissão de arquivo",
    "FILE_004": "Arquivo corrompido",
    
    # Erros de sistema
    "SYS_001": "Memória insuficiente",
    "SYS_002": "Espaço em disco insuficiente",
    "SYS_003": "Erro de rede",
    "SYS_004": "Erro inesperado do sistema",
}

# Estados brasileiros para validação
BRAZILIAN_STATES = [
    "AC", "AL", "AM", "AP", "BA", "CE", "DF", "ES", "GO",
    "MA", "MG", "MS", "MT", "PA", "PB", "PE", "PI", "PR",
    "RJ", "RN", "RO", "RR", "RS", "SC", "SE", "SP", "TO"
]

# Configurações de proxy padrão
PROXY_CONFIG = {
    "http": None,
    "https": None,
    "auth": None,
    "enabled": False,
    "timeout": 30,
}

# Configurações de cache
CACHE_CONFIG = {
    "max_size": 1000,  # máximo de entradas no cache
    "ttl": 86400,  # 24 horas em segundos
    "cleanup_interval": 3600,  # 1 hora em segundos
    "compression": True,
    "backup_count": 3,
}

# Configurações de logging
LOG_CONFIG = {
    "level": "INFO",
    "format": "%(asctime)s - %(levelname)s - %(message)s",
    "date_format": "%Y-%m-%d %H:%M:%S",
    "max_file_size": 10485760,  # 10MB
    "backup_count": 5,
    "console_output": True,
    "file_output": True,
}

# Versão do sistema
SYSTEM_INFO = {
    "version": "2.0.0",
    "name": "Consultor de CNPJ",
    "description": "Sistema de consulta e processamento de CNPJs com monitoramento de APIs",
    "author": "Seu Nome",
    "license": "MIT",
    "repository": "https://github.com/seuusuario/cnpj-consultor",
    "requirements": [
        "requests>=2.28.0",
        "openpyxl>=3.0.0",
        "python>=3.8"
    ]
}

# Mensagens de ajuda e tooltips
HELP_MESSAGES = {
    "cnpj_input": "Digite o CNPJ com ou sem formatação (14 dígitos)",
    "batch_processing": "Selecione um arquivo Excel ou CSV com uma coluna de CNPJs",
    "api_status": "Verifica o status atual das APIs utilizadas pelo sistema",
    "rate_limit": "Número máximo de requisições por minuto para evitar bloqueio",
    "cache_info": "Os resultados são armazenados em cache para consultas futuras",
    "proxy_settings": "Configure proxy se sua rede exigir acesso através de servidor proxy",
    "log_info": "Todas as atividades do sistema são registradas no log",
    "status_indicators": "✅ Online | ❌ Offline | ⚠️ Degradado | 🔄 Verificando",
}

# Limites e validações
VALIDATION_RULES = {
    "cnpj_length": 14,
    "cnpj_regex": r"^\d{14}$",
    "email_regex": r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
    "phone_regex": r"^(\+\d{1,3})?[\s-]?\(?\d{2}\)?[\s-]?\d{4,5}[\s-]?\d{4}$",
    "cep_regex": r"^\d{5}-?\d{3}$",
    "max_file_size": 52428800,  # 50MB
    "allowed_extensions": [".xlsx", ".xls", ".csv"],
}

# Textos para relatórios e exportação
REPORT_TEXTS = {
    "export_success": "Exportação concluída com sucesso",
    "export_failed": "Falha na exportação",
    "report_title": "Relatório de Consultas CNPJ",
    "generated_on": "Gerado em",
    "total_records": "Total de registros",
    "successful_queries": "Consultas bem-sucedidas",
    "failed_queries": "Consultas com erro",
    "processing_time": "Tempo de processamento",
    "api_usage": "Uso de API",
    "cache_hits": "Acertos no cache",
    "cache_misses": "Perdas no cache",
}