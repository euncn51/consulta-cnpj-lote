# 📋 Guia do settings.yaml - NFe Parser v2.0

## 🎯 Visão Geral

O arquivo `config/settings.yaml` contém **todas as configurações** do sistema NFe Parser. Ele permite personalizar o comportamento do parser, GUI, exportação e muito mais **sem modificar código**.

---

## 📂 Estrutura do Arquivo

O `settings.yaml` está organizado em **10 seções principais**:

1. **Logging** - Configurações de registro de eventos
2. **Parser** - Configurações de processamento XML
3. **Fields** - Configurações de extração de campos
4. **Export** - Configurações de exportação
5. **GUI** - Configurações da interface gráfica
6. **Performance** - Otimizações de desempenho
7. **Validation** - Validações de dados
8. **Advanced** - Configurações avançadas
9. **Reforma Tributária** - Campos específicos da reforma
10. **Compatibility** - Compatibilidade com versões

---

## 🔧 Configurações Principais

### 1. Logging

```yaml
logging:
  level: INFO              # DEBUG, INFO, WARNING, ERROR
  file: "logs/nfe_parser.log"
  max_bytes: 10485760      # 10MB
  backup_count: 5
```

**Quando ajustar:**
- `level: DEBUG` - Para investigar problemas
- `level: ERROR` - Para produção (menos logs)
- `max_bytes` - Se logs crescem muito rápido

---

### 2. Parser

```yaml
parser:
  encoding: "utf-8"
  buffer_size: 8192        # 8KB
  timeout: 300             # 5 minutos
  continue_on_error: true
```

**Quando ajustar:**
- `encoding` - Se XMLs têm encoding diferente
- `timeout` - Para arquivos muito grandes
- `continue_on_error: false` - Para abortar em erros

---

### 3. Fields (Campos)

```yaml
fields:
  extract_all: true        # Extrair todos os 155+ campos
  include_empty: true      # Incluir campos vazios
  convert_numeric: true    # Converter para float
  decimal_places: 2
```

**Configuração Atual:**
- ✅ `extract_all: true` - **Extrai todos os 155+ campos**
- ✅ `include_empty: true` - Mantém campos vazios (útil para análise)

**Quando ajustar:**
- `extract_all: false` - Para extrair apenas grupos específicos
- `include_empty: false` - Para remover colunas vazias
- `decimal_places: 4` - Para mais precisão em valores

---

### 4. Export (Exportação)

```yaml
export:
  default_format: "excel"  # excel, csv, json
  output_dir: "output"
  create_date_folders: true
  
  csv:
    separator: ","
    encoding: "utf-8-sig"  # UTF-8 com BOM (Excel)
    
  excel:
    engine: "openpyxl"
    freeze_panes: true     # Congelar primeira linha
    auto_filter: true      # Filtro automático
    
  json:
    indent: 2
    ensure_ascii: false
```

**Quando ajustar:**
- `default_format: "csv"` - Para usar CSV por padrão
- `csv.separator: ";"` - Para Excel brasileiro
- `excel.freeze_panes: false` - Desabilitar congelamento
- `create_date_folders: false` - Não criar subpastas

---

### 5. GUI

```yaml
gui:
  window:
    width: 1200
    height: 800
    title: "NFe Parser v2.0"
    
  directories:
    default_output: "output"
    remember_last: true
    
  processing:
    show_progress: true
    show_logs: true
    max_log_lines: 1000
```

**Quando ajustar:**
- `window.width/height` - Ajustar tamanho da janela
- `remember_last: false` - Não lembrar último diretório
- `max_log_lines: 500` - Menos linhas de log na GUI

---

### 6. Performance

```yaml
performance:
  parallel_processing: true
  num_workers: 0           # 0 = automático
  chunk_size: 100
  enable_cache: false
```

**Quando ajustar:**
- `parallel_processing: false` - Desabilitar paralelismo
- `num_workers: 4` - Fixar número de workers
- `enable_cache: true` - Ativar cache (experimental)

---

### 7. Reforma Tributária

```yaml
reforma_tributaria:
  extract_ibscbs: true           # IBS/CBS
  extract_gtribregular: true     # gTribRegular
  extract_credito_presumido: true
  mark_not_applicable: true      # Marcar como "NA"
```

**Configuração Atual:**
- ✅ Todos os campos da Reforma Tributária habilitados
- ✅ Campos não aplicáveis marcados como "NA"

**Quando ajustar:**
- `extract_ibscbs: false` - Se não precisa IBS/CBS
- `mark_not_applicable: false` - Deixar vazio ao invés de "NA"

---

## 🎯 Casos de Uso Comuns

### Caso 1: Máximo Desempenho
```yaml
logging:
  level: ERROR
  console: false

parser:
  buffer_size: 16384
  continue_on_error: true

performance:
  parallel_processing: true
  num_workers: 0

export:
  create_date_folders: false
```

### Caso 2: Máximo Debug
```yaml
logging:
  level: DEBUG
  console: true

parser:
  validate_xml: true
  continue_on_error: false

advanced:
  debug_mode: true
  save_error_files: true
  generate_report: true
```

### Caso 3: Exportação Otimizada para Excel
```yaml
export:
  default_format: "excel"
  
  excel:
    freeze_panes: true
    auto_filter: true
    column_width: "auto"

fields:
  include_empty: false
  decimal_places: 2
```

### Caso 4: CSV para Importação
```yaml
export:
  default_format: "csv"
  
  csv:
    separator: ";"
    encoding: "utf-8-sig"
    decimal: ","

fields:
  include_empty: false
  convert_numeric: true
```

---

## 📝 Como Usar

### 1. Editar Configurações

Abra `config/settings.yaml` em qualquer editor de texto e modifique os valores:

```yaml
# Exemplo: Mudar nível de log
logging:
  level: DEBUG  # Era INFO, agora DEBUG
```

### 2. Salvar e Reiniciar

Após modificar, **salve o arquivo** e **reinicie a aplicação**:

```bash
# Fechar GUI se estiver aberta
# Depois executar novamente:
python run_gui.py
```

### 3. Verificar Logs

As configurações são carregadas no início. Verifique os logs:

```
2026-04-18 10:00:00 - settings - INFO - Configurações carregadas de config/settings.yaml
2026-04-18 10:00:00 - settings - INFO - Nível de log: DEBUG
```

---

## ⚠️ Avisos Importantes

### 1. Valores Padrão
Se o `settings.yaml` estiver vazio ou com erro, o sistema usa **valores padrão seguros**.

### 2. Validação
Valores inválidos são **ignorados** e substituídos por padrões:
```yaml
logging:
  level: INVALIDO  # ❌ Será ignorado, usará INFO
```

### 3. Sintaxe YAML
- Use **espaços**, não tabs
- Respeite a **indentação**
- Strings com caracteres especiais: use **aspas**
- Booleanos: `true` ou `false` (minúsculas)

### 4. Comentários
Linhas iniciadas com `#` são **comentários** e são ignoradas.

---

## 🔍 Verificar Configurações Ativas

Para ver quais configurações estão ativas:

```python
from src.config import get_settings

settings = get_settings()
print(settings.logging.level)        # INFO
print(settings.export.default_format) # excel
print(settings.fields.extract_all)   # True
```

---

## 📊 Configurações Recomendadas

### Para Uso Diário
```yaml
logging:
  level: INFO

fields:
  extract_all: true
  include_empty: true

export:
  default_format: "excel"
  create_date_folders: true

reforma_tributaria:
  extract_ibscbs: true
  extract_gtribregular: true
```

### Para Produção
```yaml
logging:
  level: WARNING
  console: false

parser:
  continue_on_error: true
  max_errors: 100

performance:
  parallel_processing: true

validation:
  strict_mode: false
```

### Para Desenvolvimento
```yaml
logging:
  level: DEBUG
  console: true

advanced:
  debug_mode: true
  save_error_files: true
  generate_report: true
  collect_statistics: true
```

---

## 🎯 Resumo

| Seção | Propósito | Ajustar Quando |
|-------|-----------|----------------|
| **Logging** | Controlar logs | Debugar ou reduzir logs |
| **Parser** | Processamento XML | Problemas de encoding/timeout |
| **Fields** | Campos extraídos | Personalizar saída |
| **Export** | Formato de saída | Mudar formato padrão |
| **GUI** | Interface | Ajustar aparência |
| **Performance** | Velocidade | Otimizar processamento |
| **Reforma Tributária** | IBS/CBS | Habilitar/desabilitar |

---

## ✅ Conclusão

O `settings.yaml` está **pronto para uso** com configurações otimizadas para:
- ✅ Extrair todos os 155+ campos
- ✅ Suporte completo à Reforma Tributária
- ✅ Exportação para Excel/CSV/JSON
- ✅ Logging adequado
- ✅ Performance balanceada

**Você pode usar o sistema sem modificar nada!** As configurações atuais são ideais para a maioria dos casos.

---

**Última atualização:** 2026-04-18  
**Versão:** 2.0