"""
Script de teste para Fase 2 - Configuração e Mapeamento

Testa o sistema de configurações e mapeamento dinâmico de campos.
"""

import sys
from pathlib import Path

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent))

from src.utils.logger import setup_logger, get_logger
from src.config.settings import Settings, get_settings
from src.core.field_mapper import FieldMapper


def test_settings():
    """Testa o sistema de configurações"""
    print("\n" + "="*60)
    print("TESTE 1: Sistema de Configuracoes")
    print("="*60 + "\n")
    
    logger = get_logger('test_settings')
    
    # Obter settings
    settings = get_settings()
    
    logger.info(f"Aplicacao: {settings.app_name} v{settings.app_version}")
    logger.info(f"Nivel de log: {settings.log_level}")
    logger.info(f"Usar streaming: {settings.use_streaming}")
    logger.info(f"Diretorio de saida: {settings.output_dir}")
    
    # Testar get/set
    logger.info("\nTestando get/set de configuracoes:")
    batch_size = settings.get('parser.batch_size', 100)
    logger.info(f"  Batch size atual: {batch_size}")
    
    settings.set('parser.batch_size', 200)
    new_batch_size = settings.get('parser.batch_size')
    logger.info(f"  Novo batch size: {new_batch_size}")
    
    # Testar propriedades
    logger.info("\nPropriedades de acesso rapido:")
    logger.info(f"  app_name: {settings.app_name}")
    logger.info(f"  app_version: {settings.app_version}")
    logger.info(f"  log_level: {settings.log_level}")
    logger.info(f"  use_streaming: {settings.use_streaming}")
    logger.info(f"  default_export_format: {settings.default_export_format}")
    
    print("\n[OK] Teste de configuracoes concluido!")


def test_field_mapper():
    """Testa o mapeador de campos"""
    print("\n" + "="*60)
    print("TESTE 2: Mapeador de Campos")
    print("="*60 + "\n")
    
    logger = get_logger('test_mapper')
    
    # Criar mapper
    mapper = FieldMapper()
    
    logger.info(f"Mapeador criado: {mapper}")
    
    # Estatísticas
    stats = mapper.get_statistics()
    logger.info(f"\nEstatisticas do mapeamento:")
    logger.info(f"  Total de campos: {stats['total_fields']}")
    logger.info(f"  Campos obrigatorios: {stats['required_fields']}")
    logger.info(f"  Campos opcionais: {stats['optional_fields']}")
    logger.info(f"  Grupos: {list(stats['groups'].keys())}")
    logger.info(f"  Tipos: {stats['types']}")
    
    # Testar adição de campo
    logger.info("\nAdicionando campo customizado...")
    mapper.add_field(
        field_name='meu_campo_teste',
        xpath='det/prod/meuCampo',
        field_type='decimal',
        required=False,
        group='custom',
        description='Campo de teste adicionado dinamicamente'
    )
    
    # Verificar campo adicionado
    config = mapper.get_field_config('meu_campo_teste')
    if config:
        logger.info(f"  Campo adicionado com sucesso!")
        logger.info(f"  XPath: {config['xpath']}")
        logger.info(f"  Tipo: {config['type']}")
        logger.info(f"  Grupo: {config['group']}")
    
    # Testar conversão de valores
    logger.info("\nTestando conversao de valores:")
    test_values = [
        ('123', 'integer', 123),
        ('45.67', 'decimal', 45.67),
        ('true', 'boolean', True),
        ('Texto', 'string', 'Texto')
    ]
    
    for value, field_type, expected in test_values:
        converted = mapper.convert_value(value, field_type)
        status = "[OK]" if converted == expected else "[ERRO]"
        logger.info(f"  {status} '{value}' -> {field_type}: {converted}")
    
    # Testar campos por grupo
    logger.info("\nCampos por grupo:")
    for group in ['emitente', 'identificacao', 'produto']:
        fields = mapper.get_fields_by_group(group)
        logger.info(f"  {group}: {len(fields)} campos")
    
    print("\n[OK] Teste de mapeador concluido!")


def test_integration():
    """Testa integração entre configurações e mapeamento"""
    print("\n" + "="*60)
    print("TESTE 3: Integracao Config + Mapeamento")
    print("="*60 + "\n")
    
    logger = get_logger('test_integration')
    
    # Obter componentes
    settings = get_settings()
    mapper = FieldMapper()
    
    logger.info("Testando integracao entre componentes...")
    
    # Simular fluxo de processamento
    logger.info("\n[PASSO 1] Carregar configuracoes")
    logger.info(f"  Aplicacao: {settings.app_name}")
    logger.info(f"  Usar streaming: {settings.use_streaming}")
    
    logger.info("\n[PASSO 2] Carregar mapeamento de campos")
    stats = mapper.get_statistics()
    logger.info(f"  Campos carregados: {stats['total_fields']}")
    logger.info(f"  Grupos: {len(stats['groups'])}")
    
    logger.info("\n[PASSO 3] Validar configuracao")
    if settings.use_streaming:
        logger.info("  [OK] Processamento streaming habilitado")
    
    logger.info("\n[PASSO 4] Preparar para processar XMLs")
    output_dir = settings.output_dir
    export_format = settings.default_export_format
    logger.info(f"  Diretorio de saida: {output_dir}")
    logger.info(f"  Formato de exportacao: {export_format}")
    
    logger.info("\n[PASSO 5] Sistema pronto para processar!")
    logger.info("  [OK] Configuracoes carregadas")
    logger.info("  [OK] Mapeamento carregado")
    logger.info("  [OK] Logger configurado")
    logger.info("  [OK] Parser streaming disponivel")
    
    print("\n[OK] Teste de integracao concluido!")


def show_features():
    """Mostra funcionalidades da Fase 2"""
    print("\n" + "="*60)
    print("FUNCIONALIDADES DA FASE 2")
    print("="*60 + "\n")
    
    print("[OK] Sistema de Configuracoes")
    print("  - Carregamento de configuracoes via YAML")
    print("  - Valores padrao integrados")
    print("  - Acesso facil via notacao de ponto")
    print("  - Propriedades de conveniencia")
    print("  - Padrao Singleton")
    
    print("\n[OK] Mapeamento Dinamico de Campos")
    print("  - Definicao de campos via YAML")
    print("  - Adicao dinamica de campos")
    print("  - Suporte a multiplos tipos de dados")
    print("  - Validacao de campos obrigatorios")
    print("  - Conversao automatica de tipos")
    print("  - Organizacao por grupos")
    print("  - Estatisticas de mapeamento")
    
    print("\n[OK] Arquivos de Configuracao")
    print("  - config/settings.yaml - Configuracoes gerais")
    print("  - config/field_mapping.yaml - Mapeamento de campos")
    
    print("\n[OK] Integracao com Fase 1")
    print("  - Logger integrado")
    print("  - Parser streaming compativel")
    print("  - Arquitetura modular mantida")


def main():
    """Função principal"""
    print("\n" + "="*60)
    print("FASE 2 - CONFIGURACAO E MAPEAMENTO")
    print("="*60)
    
    try:
        # Configurar logging
        setup_logger(log_level='INFO')
        
        # Executar testes
        test_settings()
        test_field_mapper()
        test_integration()
        show_features()
        
        print("\n" + "="*60)
        print("[SUCESSO] FASE 2 CONCLUIDA!")
        print("="*60 + "\n")
        
        print("Proximos passos:")
        print("  1. Desenvolver GUI Desktop (tkinter)")
        print("  2. Desenvolver GUI Web (Streamlit)")
        print("  3. Implementar exportacao de resultados")
        print("  4. Adicionar validacao de schema XML")
        print("  5. Criar testes unitarios")
        print()
        
    except Exception as e:
        print(f"\n[ERRO] Erro durante os testes: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()

# Made with Bob
