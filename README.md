# NFe Parser - Sistema de Análise de Notas Fiscais Eletrônicas

Sistema completo para parsing e análise de arquivos XML de NF-e (Nota Fiscal Eletrônica) com suporte à Reforma Tributária.

## 🚀 Funcionalidades Implementadas

### ✅ Sistema de Logging Estruturado
- Múltiplos níveis de log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- Rotação automática de arquivos (10MB, 5 backups)
- Formatação colorida no console
- Logs detalhados salvos em arquivo
- Thread-safe e modular

### ✅ Processamento Streaming
- Parsing incremental usando `xml.etree.ElementTree.iterparse()`
- Baixo uso de memória (ideal para arquivos grandes)
- Suporta arquivos XML de qualquer tamanho
- Callbacks de progresso em tempo real
- Liberação automática de memória após processar cada elemento

### ✅ Arquitetura Modular
- Separação clara de responsabilidades
- Fácil manutenção e extensão
- Imports organizados
- Documentação completa em código

## 📁 Estrutura do Projeto

```
nfe_parser/
├── src/
│   ├── core/
│   │   ├── __init__.py
│   │   └── streaming_parser.py    # Parser com streaming
│   ├── utils/
│   │   ├── __init__.py
│   │   └── logger.py               # Sistema de logging
│   └── __init__.py
├── logs/                            # Logs gerados automaticamente
├── docs/
│   ├── analise_nfe_parser.md       # Análise completa do código
│   └── plano_melhorias_nfe_parser.md  # Plano de melhorias
├── leito_nfe_xml_v7.py             # Parser original
├── test_streaming_logger_simple.py # Script de teste
└── README.md
```

## 🔧 Instalação

### Requisitos
- Python 3.8+
- Dependências básicas (incluídas no Python):
  - xml.etree.ElementTree
  - logging
  - pathlib

### Instalação de Dependências Adicionais (para versão completa)
```bash
pip install pandas numpy openpyxl pyyaml
```

## 📖 Uso Básico

### 1. Sistema de Logging

```python
from src.utils.logger import setup_logger, get_logger

# Configurar logging
setup_logger(
    log_dir='logs',
    log_level='INFO',
    console_level='INFO',
    file_level='DEBUG'
)

# Obter logger para seu módulo
logger = get_logger('meu_modulo')

# Usar logger
logger.info("Processando arquivo XML")
logger.warning("Atenção: campo opcional não encontrado")
logger.error("Erro ao processar", exc_info=True)
```

### 2. Parser com Streaming

```python
from src.core.streaming_parser import StreamingNFeParser
from src.utils.logger import setup_logger

# Configurar logging
setup_logger()

# Criar parser
parser = StreamingNFeParser()

# Callback de progresso (opcional)
def on_progress(current, total):
    percent = (current / total) * 100
    print(f"Progresso: {current}/{total} ({percent:.1f}%)")

# Processar arquivo XML
data = parser.parse_xml_stream(
    'caminho/para/nota.xml',
    progress_callback=on_progress
)

# Processar múltiplos arquivos
file_paths = ['nota1.xml', 'nota2.xml', 'nota3.xml']
all_data = parser.parse_multiple_files(file_paths)

# Converter para DataFrame (requer pandas)
import pandas as pd
df = pd.DataFrame(all_data)
```

### 3. Executar Testes

```bash
# Teste completo do sistema
python test_streaming_logger_simple.py
```

## 📊 Dados Extraídos

O parser extrai os seguintes grupos de dados da NF-e:

### Cabeçalho (Header)
- **Emitente**: CNPJ, Nome, IE, Endereço
- **Identificação**: Número, Série, Data de Emissão, Natureza da Operação
- **Destinatário**: CNPJ/CPF, Nome
- **Totais**: Valor total da NF-e

### Itens (Detalhes)
- **Produto**: Código, Descrição, NCM, CFOP, Quantidade, Valor
- **Impostos**:
  - ICMS (CST, Base de Cálculo, Alíquota, Valor)
  - PIS (CST, Base de Cálculo, Alíquota, Valor)
  - COFINS (CST, Base de Cálculo, Alíquota, Valor)
  - IBS/CBS (Reforma Tributária)

## 🎯 Exemplos de Uso

### Exemplo 1: Processar um único arquivo

```python
from src.core.streaming_parser import StreamingNFeParser
from src.utils.logger import setup_logger, get_logger

# Setup
setup_logger(log_level='INFO')
logger = get_logger('exemplo1')
parser = StreamingNFeParser()

# Processar
logger.info("Iniciando processamento...")
data = parser.parse_xml_stream('nota_fiscal.xml')
logger.info(f"Extraídos {len(data)} itens")

# Exibir primeiro item
if data:
    print("\nPrimeiro item:")
    for key, value in data[0].items():
        print(f"  {key}: {value}")
```

### Exemplo 2: Processar pasta com múltiplos XMLs

```python
from src.core.streaming_parser import StreamingNFeParser
from src.utils.logger import setup_logger, get_logger
import glob
import pandas as pd

# Setup
setup_logger()
logger = get_logger('exemplo2')
parser = StreamingNFeParser()

# Buscar arquivos
xml_files = glob.glob('pasta_xmls/*.xml')
logger.info(f"Encontrados {len(xml_files)} arquivos XML")

# Processar com callback
def on_file_progress(current, total, filename):
    logger.info(f"Processando {current}/{total}: {filename}")

all_data = parser.parse_multiple_files(xml_files, on_file_progress)

# Converter para DataFrame e salvar
df = pd.DataFrame(all_data)
df.to_excel('resultado.xlsx', index=False)
logger.info(f"Resultado salvo: {len(df)} registros")
```

### Exemplo 3: Monitorar uso de memória

```python
from src.core.streaming_parser import StreamingNFeParser
from src.utils.logger import setup_logger, get_logger
import psutil
import os

setup_logger()
logger = get_logger('exemplo3')
parser = StreamingNFeParser()

# Memória inicial
process = psutil.Process(os.getpid())
mem_before = process.memory_info().rss / 1024 / 1024  # MB

logger.info(f"Memória inicial: {mem_before:.2f} MB")

# Processar arquivo grande
data = parser.parse_xml_stream('arquivo_grande.xml')

# Memória final
mem_after = process.memory_info().rss / 1024 / 1024  # MB
logger.info(f"Memória final: {mem_after:.2f} MB")
logger.info(f"Diferença: {mem_after - mem_before:.2f} MB")
```

## 📝 Logs

Os logs são salvos automaticamente em:
- **Diretório**: `logs/`
- **Formato**: `nfe_parser_YYYYMMDD.log`
- **Rotação**: Automática quando atingir 10MB
- **Backups**: Mantém 5 arquivos anteriores

### Níveis de Log

- **DEBUG**: Detalhes técnicos (apenas em arquivo)
- **INFO**: Informações gerais (console e arquivo)
- **WARNING**: Avisos (console e arquivo)
- **ERROR**: Erros (console e arquivo)
- **CRITICAL**: Erros críticos (console e arquivo)

## 🔜 Próximas Funcionalidades

1. ⏳ Sistema de mapeamento dinâmico de campos XML
2. ⏳ GUI Desktop (tkinter)
3. ⏳ GUI Web (Streamlit)
4. ⏳ Exportação para múltiplos formatos (Excel, CSV, JSON)
5. ⏳ Validação de schema XML
6. ⏳ Testes unitários completos

## 📚 Documentação Adicional

- **[Análise Completa](analise_nfe_parser.md)**: Análise detalhada do código original
- **[Plano de Melhorias](plano_melhorias_nfe_parser.md)**: Roadmap completo de melhorias

## 🤝 Contribuindo

Para adicionar novos campos ao parser:

1. Edite `src/core/streaming_parser.py`
2. Adicione o campo no método `_extract_item_data()` ou `_extract_header_data()`
3. Use os métodos auxiliares: `find_element()`, `find_element_text()`, `_to_float()`
4. Teste com `test_streaming_logger_simple.py`

## 📄 Licença

Este projeto é de código aberto e está disponível para uso livre.

## 🐛 Reportar Problemas

Para reportar bugs ou sugerir melhorias, verifique os logs em `logs/` e inclua:
- Versão do Python
- Sistema operacional
- Arquivo de log relevante
- Descrição do problema

## 🎓 Suporte

Para dúvidas sobre o uso:
1. Consulte a documentação em `docs/`
2. Execute os testes de exemplo
3. Verifique os logs para mensagens de erro detalhadas

---

**Versão**: 2.0.0  
**Última Atualização**: 2026-04-17  
**Status**: ✅ Logging e Streaming implementados
