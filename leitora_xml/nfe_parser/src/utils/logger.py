"""
Sistema de Logging Estruturado para NFe Parser

Fornece logging com múltiplos níveis, rotação de arquivos e formatação colorida.
"""

import logging
import logging.handlers
import sys
from pathlib import Path
from typing import Optional
from datetime import datetime


class ColoredFormatter(logging.Formatter):
    """Formatter com cores para console"""
    
    # Códigos de cores ANSI
    COLORS = {
        'DEBUG': '\033[36m',      # Ciano
        'INFO': '\033[32m',       # Verde
        'WARNING': '\033[33m',    # Amarelo
        'ERROR': '\033[31m',      # Vermelho
        'CRITICAL': '\033[35m',   # Magenta
        'RESET': '\033[0m'        # Reset
    }
    
    def format(self, record):
        """Formata o log com cores"""
        if sys.stdout.isatty():  # Apenas colorir se for terminal
            levelname = record.levelname
            if levelname in self.COLORS:
                record.levelname = f"{self.COLORS[levelname]}{levelname}{self.COLORS['RESET']}"
        return super().format(record)


class NFeLogger:
    """
    Gerenciador de logging para NFe Parser
    
    Características:
    - Múltiplos níveis de log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    - Rotação automática de arquivos
    - Formatação colorida no console
    - Logs separados por módulo
    - Thread-safe
    """
    
    _loggers = {}
    _initialized = False
    
    @classmethod
    def setup(cls, 
              log_dir: str = 'logs',
              log_level: str = 'INFO',
              console_level: str = 'INFO',
              file_level: str = 'DEBUG',
              max_bytes: int = 10 * 1024 * 1024,  # 10MB
              backup_count: int = 5):
        """
        Configura o sistema de logging
        
        Args:
            log_dir: Diretório para arquivos de log
            log_level: Nível geral de log
            console_level: Nível de log para console
            file_level: Nível de log para arquivo
            max_bytes: Tamanho máximo do arquivo de log
            backup_count: Número de backups a manter
        """
        if cls._initialized:
            return
        
        # Criar diretório de logs
        log_path = Path(log_dir)
        log_path.mkdir(exist_ok=True)
        
        # Configurar logger raiz
        root_logger = logging.getLogger('nfe_parser')
        root_logger.setLevel(getattr(logging, log_level.upper()))
        
        # Remover handlers existentes
        root_logger.handlers.clear()
        
        # Handler para console com cores
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(getattr(logging, console_level.upper()))
        console_formatter = ColoredFormatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        console_handler.setFormatter(console_formatter)
        root_logger.addHandler(console_handler)
        
        # Handler para arquivo com rotação
        log_file = log_path / f'nfe_parser_{datetime.now().strftime("%Y%m%d")}.log'
        file_handler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding='utf-8'
        )
        file_handler.setLevel(getattr(logging, file_level.upper()))
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(file_formatter)
        root_logger.addHandler(file_handler)
        
        cls._initialized = True
        root_logger.info("Sistema de logging inicializado")
    
    @classmethod
    def get_logger(cls, name: str) -> logging.Logger:
        """
        Obtém um logger para um módulo específico
        
        Args:
            name: Nome do módulo
            
        Returns:
            Logger configurado
        """
        if not cls._initialized:
            cls.setup()
        
        if name not in cls._loggers:
            logger = logging.getLogger(f'nfe_parser.{name}')
            cls._loggers[name] = logger
        
        return cls._loggers[name]


# Funções de conveniência
def setup_logger(log_dir: str = 'logs',
                log_level: str = 'INFO',
                console_level: str = 'INFO',
                file_level: str = 'DEBUG',
                max_bytes: int = 10 * 1024 * 1024,
                backup_count: int = 5):
    """
    Configura o sistema de logging (função de conveniência)
    
    Args:
        log_dir: Diretório para arquivos de log
        log_level: Nível geral de log
        console_level: Nível de log para console
        file_level: Nível de log para arquivo
        max_bytes: Tamanho máximo do arquivo de log
        backup_count: Número de backups a manter
    """
    NFeLogger.setup(
        log_dir=log_dir,
        log_level=log_level,
        console_level=console_level,
        file_level=file_level,
        max_bytes=max_bytes,
        backup_count=backup_count
    )


def get_logger(name: str) -> logging.Logger:
    """
    Obtém um logger para um módulo (função de conveniência)
    
    Args:
        name: Nome do módulo
        
    Returns:
        Logger configurado
        
    Example:
        >>> from src.utils.logger import get_logger
        >>> logger = get_logger('parser')
        >>> logger.info("Processando arquivo XML")
        >>> logger.error("Erro ao processar", exc_info=True)
    """
    return NFeLogger.get_logger(name)


# Exemplo de uso
if __name__ == '__main__':
    # Configurar logging
    setup_logger(log_level='DEBUG')
    
    # Obter logger
    logger = get_logger('test')
    
    # Testar diferentes níveis
    logger.debug("Mensagem de debug")
    logger.info("Mensagem informativa")
    logger.warning("Mensagem de aviso")
    logger.error("Mensagem de erro")
    logger.critical("Mensagem crítica")
    
    # Testar com exceção
    try:
        1 / 0
    except Exception as e:
        logger.error("Erro capturado", exc_info=True)

# Made with Bob
