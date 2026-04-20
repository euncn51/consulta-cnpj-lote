"""
Gerenciador de Configurações do NFe Parser

Carrega e gerencia configurações a partir de arquivos YAML.
"""

import yaml
from pathlib import Path
from typing import Dict, Any, Optional
import sys

# Adicionar diretório pai ao path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.utils.logger import get_logger


class Settings:
    """
    Gerenciador de configurações do sistema
    
    Carrega configurações de arquivos YAML e fornece acesso fácil aos valores.
    Suporta valores padrão e validação básica.
    """
    
    _instance = None
    _initialized = False
    
    def __new__(cls):
        """Implementa padrão Singleton"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Inicializa o gerenciador de configurações"""
        if not self._initialized:
            self.logger = get_logger('settings')
            self._config = {}
            self._config_dir = Path('config')
            self._load_default_config()
            Settings._initialized = True
    
    def _load_default_config(self):
        """Carrega configuração padrão"""
        self._config = {
            'app': {
                'name': 'NFe Parser',
                'version': '2.0.0',
                'description': 'Sistema de análise de Notas Fiscais Eletrônicas'
            },
            'logging': {
                'level': 'INFO',
                'console_level': 'INFO',
                'file_level': 'DEBUG',
                'log_dir': 'logs',
                'max_bytes': 10485760,
                'backup_count': 5
            },
            'parser': {
                'use_streaming': True,
                'validate_schema': False,
                'encoding': 'utf-8',
                'batch_size': 100,
                'show_progress': True,
                'stop_on_error': False
            },
            'export': {
                'default_format': 'xlsx',
                'output_dir': 'output'
            }
        }
        self.logger.debug("Configuração padrão carregada")
    
    def load_from_file(self, config_file: str = 'settings.yaml'):
        """
        Carrega configurações de um arquivo YAML
        
        Args:
            config_file: Nome do arquivo de configuração
        """
        config_path = self._config_dir / config_file
        
        try:
            if config_path.exists():
                with open(config_path, 'r', encoding='utf-8') as f:
                    file_config = yaml.safe_load(f)
                    if file_config:
                        self._merge_config(file_config)
                        self.logger.info(f"Configuração carregada de {config_path}")
                    else:
                        self.logger.warning(f"Arquivo {config_path} está vazio")
            else:
                self.logger.warning(f"Arquivo de configuração não encontrado: {config_path}")
                self.logger.info("Usando configuração padrão")
        except Exception as e:
            self.logger.error(f"Erro ao carregar configuração: {e}", exc_info=True)
            self.logger.info("Usando configuração padrão")
    
    def _merge_config(self, new_config: Dict[str, Any]):
        """
        Mescla nova configuração com a existente
        
        Args:
            new_config: Nova configuração a ser mesclada
        """
        def merge_dict(base: dict, update: dict):
            """Mescla dicionários recursivamente"""
            for key, value in update.items():
                if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                    merge_dict(base[key], value)
                else:
                    base[key] = value
        
        merge_dict(self._config, new_config)
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Obtém valor de configuração usando notação de ponto
        
        Args:
            key: Chave da configuração (ex: 'logging.level')
            default: Valor padrão se chave não existir
            
        Returns:
            Valor da configuração ou default
            
        Example:
            >>> settings = Settings()
            >>> level = settings.get('logging.level')
            >>> output_dir = settings.get('export.output_dir', 'output')
        """
        keys = key.split('.')
        value = self._config
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            self.logger.debug(f"Chave não encontrada: {key}, usando default: {default}")
            return default
    
    def set(self, key: str, value: Any):
        """
        Define valor de configuração usando notação de ponto
        
        Args:
            key: Chave da configuração (ex: 'logging.level')
            value: Novo valor
            
        Example:
            >>> settings = Settings()
            >>> settings.set('logging.level', 'DEBUG')
        """
        keys = key.split('.')
        config = self._config
        
        # Navegar até o penúltimo nível
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        # Definir valor
        config[keys[-1]] = value
        self.logger.debug(f"Configuração atualizada: {key} = {value}")
    
    def get_all(self) -> Dict[str, Any]:
        """
        Retorna todas as configurações
        
        Returns:
            Dicionário com todas as configurações
        """
        return self._config.copy()
    
    def save_to_file(self, config_file: str = 'settings.yaml'):
        """
        Salva configurações atuais em arquivo YAML
        
        Args:
            config_file: Nome do arquivo de configuração
        """
        config_path = self._config_dir / config_file
        
        try:
            # Criar diretório se não existir
            config_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(config_path, 'w', encoding='utf-8') as f:
                yaml.dump(self._config, f, default_flow_style=False, allow_unicode=True)
            
            self.logger.info(f"Configuração salva em {config_path}")
        except Exception as e:
            self.logger.error(f"Erro ao salvar configuração: {e}", exc_info=True)
    
    def reload(self):
        """Recarrega configurações do arquivo"""
        self.logger.info("Recarregando configurações...")
        self._load_default_config()
        self.load_from_file()
    
    # Propriedades de conveniência para acesso rápido
    @property
    def app_name(self) -> str:
        """Nome da aplicação"""
        return self.get('app.name', 'NFe Parser')
    
    @property
    def app_version(self) -> str:
        """Versão da aplicação"""
        return self.get('app.version', '2.0.0')
    
    @property
    def log_level(self) -> str:
        """Nível de log"""
        return self.get('logging.level', 'INFO')
    
    @property
    def use_streaming(self) -> bool:
        """Usar processamento streaming"""
        return self.get('parser.use_streaming', True)
    
    @property
    def output_dir(self) -> str:
        """Diretório de saída"""
        return self.get('export.output_dir', 'output')
    
    @property
    def default_export_format(self) -> str:
        """Formato padrão de exportação"""
        return self.get('export.default_format', 'xlsx')
    
    def __repr__(self) -> str:
        """Representação em string"""
        return f"Settings(app={self.app_name}, version={self.app_version})"


# Instância global (Singleton)
_settings_instance: Optional[Settings] = None


def get_settings() -> Settings:
    """
    Obtém instância global de Settings
    
    Returns:
        Instância de Settings
        
    Example:
        >>> from src.config import get_settings
        >>> settings = get_settings()
        >>> print(settings.app_name)
    """
    global _settings_instance
    if _settings_instance is None:
        _settings_instance = Settings()
        # Tentar carregar do arquivo
        try:
            _settings_instance.load_from_file()
        except Exception:
            pass  # Usar configuração padrão
    return _settings_instance


# Exemplo de uso
if __name__ == '__main__':
    from src.utils.logger import setup_logger
    
    # Configurar logging
    setup_logger()
    
    # Obter settings
    settings = get_settings()
    
    print(f"\nConfiguração do {settings.app_name} v{settings.app_version}")
    print(f"Nível de log: {settings.log_level}")
    print(f"Usar streaming: {settings.use_streaming}")
    print(f"Diretório de saída: {settings.output_dir}")
    
    # Testar get/set
    print(f"\nValor atual de 'parser.batch_size': {settings.get('parser.batch_size')}")
    settings.set('parser.batch_size', 200)
    print(f"Novo valor de 'parser.batch_size': {settings.get('parser.batch_size')}")
    
    # Mostrar todas as configurações
    print("\nTodas as configurações:")
    import json
    print(json.dumps(settings.get_all(), indent=2))

# Made with Bob
