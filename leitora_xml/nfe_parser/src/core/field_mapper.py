"""
Sistema de Mapeamento Dinâmico de Campos XML

Permite adicionar e gerenciar campos do XML de forma fácil e configurável.
"""

import yaml
from pathlib import Path
from typing import Dict, List, Any, Optional
from decimal import Decimal
from datetime import datetime
import sys

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.utils.logger import get_logger


class FieldMapper:
    """
    Gerenciador de mapeamento de campos XML
    
    Carrega definições de campos de arquivo YAML e fornece métodos
    para extrair valores do XML de forma dinâmica.
    
    Características:
    - Mapeamento configurável via YAML
    - Suporte a múltiplos tipos de dados
    - Validação de campos obrigatórios
    - Fácil adição de novos campos
    """
    
    def __init__(self, mapping_file: str = 'config/field_mapping.yaml'):
        """
        Inicializa o mapeador de campos
        
        Args:
            mapping_file: Caminho para arquivo de mapeamento YAML
        """
        self.logger = get_logger('field_mapper')
        self.mapping_file = Path(mapping_file)
        self.field_definitions = {}
        self._load_mapping()
    
    def _load_mapping(self):
        """Carrega mapeamento de campos do arquivo YAML"""
        try:
            if self.mapping_file.exists():
                with open(self.mapping_file, 'r', encoding='utf-8') as f:
                    raw_mapping = yaml.safe_load(f)
                    if raw_mapping:
                        self._process_mapping(raw_mapping)
                        self.logger.info(f"Mapeamento carregado: {len(self.field_definitions)} campos")
                    else:
                        self.logger.warning(f"Arquivo de mapeamento vazio: {self.mapping_file}")
            else:
                self.logger.warning(f"Arquivo de mapeamento não encontrado: {self.mapping_file}")
                self._load_default_mapping()
        except Exception as e:
            self.logger.error(f"Erro ao carregar mapeamento: {e}", exc_info=True)
            self._load_default_mapping()
    
    def _process_mapping(self, raw_mapping: Dict[str, Any]):
        """
        Processa mapeamento bruto do YAML
        
        Args:
            raw_mapping: Dicionário com mapeamento do YAML
        """
        for group_name, fields in raw_mapping.items():
            if isinstance(fields, dict):
                for field_name, field_config in fields.items():
                    if isinstance(field_config, dict):
                        self.field_definitions[field_name] = {
                            'group': group_name,
                            'xpath': field_config.get('xpath', ''),
                            'type': field_config.get('type', 'string'),
                            'required': field_config.get('required', False),
                            'format': field_config.get('format'),
                            'default': field_config.get('default'),
                            'description': field_config.get('description', '')
                        }
    
    def _load_default_mapping(self):
        """Carrega mapeamento padrão mínimo"""
        self.field_definitions = {
            'nNF': {
                'group': 'identificacao',
                'xpath': 'ide/nNF',
                'type': 'integer',
                'required': True,
                'description': 'Número da NF-e'
            },
            'emit_xNome': {
                'group': 'emitente',
                'xpath': 'emit/xNome',
                'type': 'string',
                'required': True,
                'description': 'Nome do emitente'
            }
        }
        self.logger.info("Mapeamento padrão carregado")
    
    def add_field(self, 
                  field_name: str,
                  xpath: str,
                  field_type: str = 'string',
                  required: bool = False,
                  group: str = 'custom',
                  description: str = '',
                  format_str: Optional[str] = None,
                  default: Any = None):
        """
        Adiciona novo campo ao mapeamento dinamicamente
        
        Args:
            field_name: Nome do campo no DataFrame
            xpath: Caminho XPath no XML
            field_type: Tipo do campo (string, integer, decimal, datetime, boolean)
            required: Se o campo é obrigatório
            group: Grupo do campo
            description: Descrição do campo
            format_str: Formato para conversão (ex: data)
            default: Valor padrão se campo não existir
            
        Example:
            >>> mapper = FieldMapper()
            >>> mapper.add_field(
            ...     'meu_campo',
            ...     'det/prod/meuCampo',
            ...     field_type='decimal',
            ...     required=False
            ... )
        """
        self.field_definitions[field_name] = {
            'group': group,
            'xpath': xpath,
            'type': field_type,
            'required': required,
            'format': format_str,
            'default': default,
            'description': description
        }
        self.logger.info(f"Campo adicionado: {field_name}")
    
    def remove_field(self, field_name: str):
        """
        Remove campo do mapeamento
        
        Args:
            field_name: Nome do campo a remover
        """
        if field_name in self.field_definitions:
            del self.field_definitions[field_name]
            self.logger.info(f"Campo removido: {field_name}")
        else:
            self.logger.warning(f"Campo não encontrado: {field_name}")
    
    def get_field_config(self, field_name: str) -> Optional[Dict[str, Any]]:
        """
        Obtém configuração de um campo
        
        Args:
            field_name: Nome do campo
            
        Returns:
            Dicionário com configuração do campo ou None
        """
        return self.field_definitions.get(field_name)
    
    def get_fields_by_group(self, group: str) -> Dict[str, Dict[str, Any]]:
        """
        Obtém todos os campos de um grupo
        
        Args:
            group: Nome do grupo
            
        Returns:
            Dicionário com campos do grupo
        """
        return {
            name: config
            for name, config in self.field_definitions.items()
            if config['group'] == group
        }
    
    def get_all_fields(self) -> Dict[str, Dict[str, Any]]:
        """
        Obtém todos os campos definidos
        
        Returns:
            Dicionário com todos os campos
        """
        return self.field_definitions.copy()
    
    def get_required_fields(self) -> List[str]:
        """
        Obtém lista de campos obrigatórios
        
        Returns:
            Lista com nomes dos campos obrigatórios
        """
        return [
            name for name, config in self.field_definitions.items()
            if config['required']
        ]
    
    def convert_value(self, value: Any, field_type: str, format_str: Optional[str] = None) -> Any:
        """
        Converte valor para o tipo especificado
        
        Args:
            value: Valor a converter
            field_type: Tipo alvo
            format_str: Formato para conversão (opcional)
            
        Returns:
            Valor convertido ou None
        """
        if value is None or value == '':
            return None
        
        try:
            if field_type == 'string':
                return str(value)
            
            elif field_type == 'integer':
                return int(float(value))
            
            elif field_type == 'decimal':
                return float(value)
            
            elif field_type == 'boolean':
                if isinstance(value, str):
                    return value.lower() in ('true', '1', 'yes', 'sim')
                return bool(value)
            
            elif field_type == 'datetime':
                if format_str:
                    return datetime.strptime(value, format_str)
                else:
                    # Tentar formatos comuns
                    for fmt in ['%Y-%m-%dT%H:%M:%S%z', '%Y-%m-%d', '%d/%m/%Y']:
                        try:
                            return datetime.strptime(value, fmt)
                        except ValueError:
                            continue
                    return value
            
            else:
                self.logger.warning(f"Tipo desconhecido: {field_type}, retornando string")
                return str(value)
        
        except Exception as e:
            self.logger.debug(f"Erro ao converter valor '{value}' para {field_type}: {e}")
            return None
    
    def validate_required_fields(self, data: Dict[str, Any]) -> tuple[bool, List[str]]:
        """
        Valida se todos os campos obrigatórios estão presentes
        
        Args:
            data: Dicionário com dados extraídos
            
        Returns:
            Tupla (válido, lista_de_campos_faltantes)
        """
        missing_fields = []
        
        for field_name in self.get_required_fields():
            if field_name not in data or data[field_name] is None:
                missing_fields.append(field_name)
        
        is_valid = len(missing_fields) == 0
        
        if not is_valid:
            self.logger.warning(f"Campos obrigatórios faltantes: {missing_fields}")
        
        return is_valid, missing_fields
    
    def save_mapping(self, output_file: Optional[str] = None):
        """
        Salva mapeamento atual em arquivo YAML
        
        Args:
            output_file: Caminho do arquivo de saída (opcional)
        """
        if output_file is None:
            output_file = self.mapping_file
        else:
            output_file = Path(output_file)
        
        try:
            # Organizar por grupos
            grouped_mapping = {}
            for field_name, config in self.field_definitions.items():
                group = config['group']
                if group not in grouped_mapping:
                    grouped_mapping[group] = {}
                
                grouped_mapping[group][field_name] = {
                    'xpath': config['xpath'],
                    'type': config['type'],
                    'required': config['required'],
                    'description': config['description']
                }
                
                if config.get('format'):
                    grouped_mapping[group][field_name]['format'] = config['format']
                if config.get('default') is not None:
                    grouped_mapping[group][field_name]['default'] = config['default']
            
            # Salvar
            output_file.parent.mkdir(parents=True, exist_ok=True)
            with open(output_file, 'w', encoding='utf-8') as f:
                yaml.dump(grouped_mapping, f, default_flow_style=False, allow_unicode=True)
            
            self.logger.info(f"Mapeamento salvo em {output_file}")
        
        except Exception as e:
            self.logger.error(f"Erro ao salvar mapeamento: {e}", exc_info=True)
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Obtém estatísticas sobre o mapeamento
        
        Returns:
            Dicionário com estatísticas
        """
        groups = {}
        types = {}
        
        for field_name, config in self.field_definitions.items():
            # Contar por grupo
            group = config['group']
            groups[group] = groups.get(group, 0) + 1
            
            # Contar por tipo
            field_type = config['type']
            types[field_type] = types.get(field_type, 0) + 1
        
        return {
            'total_fields': len(self.field_definitions),
            'required_fields': len(self.get_required_fields()),
            'optional_fields': len(self.field_definitions) - len(self.get_required_fields()),
            'groups': groups,
            'types': types
        }
    
    def __repr__(self) -> str:
        """Representação em string"""
        stats = self.get_statistics()
        return f"FieldMapper(fields={stats['total_fields']}, groups={len(stats['groups'])})"


# Exemplo de uso
if __name__ == '__main__':
    from src.utils.logger import setup_logger
    
    # Configurar logging
    setup_logger(log_level='DEBUG')
    
    # Criar mapper
    mapper = FieldMapper()
    
    print(f"\n{mapper}")
    print(f"\nTotal de campos: {len(mapper.get_all_fields())}")
    print(f"Campos obrigatórios: {len(mapper.get_required_fields())}")
    
    # Adicionar campo customizado
    print("\nAdicionando campo customizado...")
    mapper.add_field(
        'meu_campo_teste',
        'det/prod/meuCampo',
        field_type='decimal',
        required=False,
        description='Campo de teste'
    )
    
    # Mostrar estatísticas
    print("\nEstatísticas:")
    stats = mapper.get_statistics()
    print(f"  Total de campos: {stats['total_fields']}")
    print(f"  Campos obrigatórios: {stats['required_fields']}")
    print(f"  Campos opcionais: {stats['optional_fields']}")
    print(f"  Grupos: {list(stats['groups'].keys())}")
    print(f"  Tipos: {stats['types']}")

# Made with Bob
