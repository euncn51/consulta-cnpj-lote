# 🚀 Guia Rápido - Streaming Parser v2.0

## 📋 Visão Geral

O **Streaming Parser v2.0** agora extrai **TODOS os 155+ campos** das NF-e, incluindo:
- ✅ Todos os campos do cabeçalho (identificação, emitente, destinatário, totais)
- ✅ Todos os campos de produto (18 campos)
- ✅ ICMS completo com Partilha DIFAL (30+ campos)
- ✅ PIS e COFINS (8 campos)
- ✅ IBS/CBS e gTribRegular - Reforma Tributária (20+ campos)
- ✅ Transporte e Pagamento (5 campos)

---

## 🎯 Uso Básico

### 1. Importar o Parser
```python
from src.core.streaming_parser import StreamingNFeParser
import pandas as pd

# Criar instância
parser = StreamingNFeParser()
```

### 2. Processar um Arquivo XML
```python
# Parse de arquivo único
data = parser.parse_xml_stream('nota_fiscal.xml')

# Verificar campos extraídos
print(f"Total de campos: {len(data[0])}")
print(f"Total de itens: {len(data)}")
```

### 3. Exportar para Excel
```python
# Converter para DataFrame
df = pd.DataFrame(data)

# Exportar para Excel
df.to_excel('resultado_completo.xlsx', index=False)
print(f"✓ Exportado {len(df)} itens com {len(df.columns)} campos")
```

### 4. Exportar para CSV
```python
# Exportar para CSV
df.to_csv('resultado_completo.csv', index=False, encoding='utf-8-sig')
print("✓ CSV exportado com sucesso")
```

### 5. Exportar para JSON
```python
# Exportar para JSON
df.to_json('resultado_completo.json', orient='records', indent=2, force_ascii=False)
print("✓ JSON exportado com sucesso")
```

---

## 📊 Campos Disponíveis

### Cabeçalho (55 campos)

#### Identificação (23 campos)
```python
item['Id']                  # ID da NF-e
item['versao_nfe']          # Versão do schema
item['cUF']                 # Código UF
item['cNF']                 # Código numérico
item['natOp']               # Natureza da operação
item['mod']                 # Modelo do documento
item['serie']               # Série
item['nNF']                 # Número da NF-e
item['dhEmi']               # Data/hora de emissão
item['dhSaiEnt']            # Data/hora de saída/entrada
item['tpNF']                # Tipo de NF-e (0=entrada, 1=saída)
item['idDest']              # Destino da operação
item['cMunFG']              # Município de ocorrência
item['tpImp']               # Formato de impressão
item['tpEmis']              # Tipo de emissão
item['cDV']                 # Dígito verificador
item['tpAmb']               # Ambiente (1=produção, 2=homologação)
item['finNFe']              # Finalidade de emissão
item['indFinal']            # Consumidor final
item['indPres']             # Indicador de presença
item['procEmi']             # Processo de emissão
item['verProc']             # Versão do processo
item['cMunFGIBS']           # Município IBS (Reforma Tributária)
item['tpNFDebito']          # Tipo NF débito (Reforma Tributária)
item['tpNFCredito']         # Tipo NF crédito (Reforma Tributária)
```

#### Emitente (16 campos)
```python
item['emit_CNPJ']           # CNPJ do emitente
item['emit_CPF']            # CPF do emitente
item['emit_xNome']          # Razão social
item['emit_xFant']          # Nome fantasia
item['emit_IE']             # Inscrição estadual
item['emit_IEST']           # IE do substituto tributário
item['emit_IM']             # Inscrição municipal
item['emit_CNAE']           # CNAE fiscal
item['emit_CRT']            # Código de regime tributário
item['emit_ender_xLgr']     # Logradouro
item['emit_ender_nro']      # Número
item['emit_ender_xBairro']  # Bairro
item['emit_ender_cMun']     # Código município
item['emit_ender_xMun']     # Nome município
item['emit_ender_UF']       # UF
item['emit_ender_CEP']      # CEP
```

#### Destinatário (16 campos)
```python
item['dest_CNPJ']           # CNPJ do destinatário
item['dest_CPF']            # CPF do destinatário
item['dest_idEstrangeiro']  # ID estrangeiro
item['dest_xNome']          # Razão social
item['dest_indIEDest']      # Indicador IE
item['dest_IE']             # Inscrição estadual
item['dest_ISUF']           # Inscrição SUFRAMA
item['dest_IM']             # Inscrição municipal
item['dest_email']          # Email
item['dest_ender_xLgr']     # Logradouro
item['dest_ender_nro']      # Número
item['dest_ender_xBairro']  # Bairro
item['dest_ender_cMun']     # Código município
item['dest_ender_xMun']     # Nome município
item['dest_ender_UF']       # UF
item['dest_ender_CEP']      # CEP
```

#### Totais (35+ campos)
```python
# ICMSTot (20 campos)
item['total_vBC']           # Base de cálculo ICMS
item['total_vICMS']         # Valor ICMS
item['total_vICMSDeson']    # Valor ICMS desonerado
item['total_vFCPUFDest']    # Valor FCP UF destino
item['total_vICMSUFDest']   # Valor ICMS UF destino
item['total_vICMSUFRemet']  # Valor ICMS UF remetente
item['total_vFCP']          # Valor FCP
item['total_vBCST']         # Base de cálculo ST
item['total_vST']           # Valor ST
item['total_vProd']         # Valor produtos
item['total_vFrete']        # Valor frete
item['total_vSeg']          # Valor seguro
item['total_vDesc']         # Valor desconto
item['total_vII']           # Valor II
item['total_vIPI']          # Valor IPI
item['total_vPIS']          # Valor PIS
item['total_vCOFINS']       # Valor COFINS
item['total_vOutro']        # Outras despesas
item['total_vNF']           # Valor total da NF-e
item['total_vTotTrib']      # Valor total tributos

# IBSCBSTot (15+ campos - Reforma Tributária)
item['total_vBCIBSCBS']     # Base de cálculo IBS/CBS
item['total_gIBS_vIBS']     # Valor IBS
item['total_gIBS_vCredPres'] # Crédito presumido IBS
item['total_gCBS_vCBS']     # Valor CBS
item['total_gCBS_vCredPres'] # Crédito presumido CBS
# ... e mais campos de subgrupos

item['vNFTot']              # Valor total final
```

#### Transporte e Pagamento (5 campos)
```python
item['transp_modFrete']              # Modalidade frete
item['transp_transporta_xNome']      # Nome transportadora
item['transp_transporta_IE']         # IE transportadora
item['pag_detPag_tPag']              # Tipo pagamento
item['pag_detPag_vPag']              # Valor pagamento
```

---

### Item (100+ campos)

#### Produto (18 campos)
```python
item['nItem']               # Número do item
item['cProd']               # Código do produto
item['cEAN']                # Código EAN
item['xProd']               # Descrição do produto
item['NCM']                 # Código NCM
item['CFOP']                # CFOP
item['uCom']                # Unidade comercial
item['qCom']                # Quantidade comercial
item['vUnCom']              # Valor unitário comercial
item['vProd']               # Valor total do produto
item['uTrib']               # Unidade tributável
item['qTrib']               # Quantidade tributável
item['vUnTrib']             # Valor unitário tributável
item['vFrete']              # Valor frete
item['vSeg']                # Valor seguro
item['vDesc']               # Valor desconto
item['vOutro']              # Outras despesas
item['indTot']              # Indicador de total
item['vItem']               # Valor do item
```

#### ICMS (30+ campos por tipo)
```python
# Exemplo para ICMS00
item['ICMS_ICMS00_CST']     # CST
item['ICMS_ICMS00_orig']    # Origem
item['ICMS_ICMS00_vBC']     # Base de cálculo
item['ICMS_ICMS00_pICMS']   # Alíquota
item['ICMS_ICMS00_vICMS']   # Valor ICMS
item['ICMS_ICMS00_pFCP']    # Alíquota FCP
item['ICMS_ICMS00_vFCP']    # Valor FCP

# Desoneração
item['ICMS_ICMS00_vICMSDeson']  # Valor desonerado
item['ICMS_ICMS00_motDesICMS']  # Motivo desoneração

# Partilha DIFAL (8 campos)
item['ICMS_ICMS00_Partilha_vBCUFDest']
item['ICMS_ICMS00_Partilha_pICMSUFDest']
item['ICMS_ICMS00_Partilha_vICMSUFDest']
# ... e mais campos de partilha
```

#### PIS e COFINS (8 campos)
```python
item['PIS_CST']             # CST PIS
item['PIS_vBC']             # Base de cálculo PIS
item['PIS_pPIS']            # Alíquota PIS
item['PIS_vPIS']            # Valor PIS

item['COFINS_CST']          # CST COFINS
item['COFINS_vBC']          # Base de cálculo COFINS
item['COFINS_pCOFINS']      # Alíquota COFINS
item['COFINS_vCOFINS']      # Valor COFINS
```

#### IBS/CBS - Reforma Tributária (20+ campos)
```python
item['ibscbs_CST']          # CST IBS/CBS
item['ibscbs_cClassTrib']   # Classificação tributária
item['ibscbs_vBC']          # Base de cálculo
item['ibscbs_vIBS']         # Valor IBS

# gIBSUF
item['ibscbs_gIBSUF_pIBSUF']  # Alíquota IBS UF
item['ibscbs_gIBSUF_vIBSUF']  # Valor IBS UF

# gIBSMun
item['ibscbs_gIBSMun_pIBSMun']  # Alíquota IBS Municipal
item['ibscbs_gIBSMun_vIBSMun']  # Valor IBS Municipal

# gCBS
item['ibscbs_gCBS_pCBS']    # Alíquota CBS
item['ibscbs_gCBS_vCBS']    # Valor CBS

# gTribRegular (8 campos)
item['gTribRegular_CSTReg']
item['gTribRegular_cClassTribReg']
item['gTribRegular_pAliqEfetRegIBSUF']
item['gTribRegular_vTribRegIBSUF']
# ... e mais campos
```

#### Crédito Presumido (3 campos)
```python
item['gCred_cCredPresumido']   # Código crédito presumido
item['gCred_pCredPresumido']   # Percentual
item['gCred_vCredPresumido']   # Valor
```

---

## 🧪 Validação e Testes

### Testar Extração de Campos
```bash
# Executar script de teste
python test_field_extraction.py nota_fiscal.xml
```

**O script irá:**
1. ✅ Comparar com parser original
2. ✅ Listar campos faltantes (se houver)
3. ✅ Gerar relatório Excel (`relatorio_campos.xlsx`)
4. ✅ Mostrar cobertura de campos

### Verificar Campos Específicos
```python
# Carregar dados
data = parser.parse_xml_stream('nota_fiscal.xml')
item = data[0]

# Verificar campos
print(f"Total de campos: {len(item)}")
print(f"Campos disponíveis: {list(item.keys())}")

# Verificar campo específico
if 'ICMS_ICMS00_vICMS' in item:
    print(f"ICMS encontrado: {item['ICMS_ICMS00_vICMS']}")
```

---

## 📈 Exemplos Práticos

### Exemplo 1: Análise de Impostos
```python
from src.core.streaming_parser import StreamingNFeParser
import pandas as pd

parser = StreamingNFeParser()
data = parser.parse_xml_stream('nota_fiscal.xml')
df = pd.DataFrame(data)

# Análise de ICMS
icms_cols = [col for col in df.columns if 'ICMS_' in col]
print(f"Campos ICMS: {len(icms_cols)}")

# Soma de valores
total_icms = df['ICMS_ICMS00_vICMS'].sum()
print(f"Total ICMS: R$ {total_icms:,.2f}")
```

### Exemplo 2: Exportação Filtrada
```python
# Selecionar apenas campos importantes
campos_importantes = [
    'nNF', 'serie', 'dhEmi',
    'emit_xNome', 'dest_xNome',
    'cProd', 'xProd', 'vProd',
    'ICMS_ICMS00_vICMS', 'PIS_vPIS', 'COFINS_vCOFINS'
]

df_filtrado = df[campos_importantes]
df_filtrado.to_excel('resumo.xlsx', index=False)
```

### Exemplo 3: Múltiplos Arquivos
```python
import glob

# Processar todos os XMLs de uma pasta
xml_files = glob.glob('notas/*.xml')
all_data = parser.parse_multiple_files(xml_files)

# Exportar consolidado
df_consolidado = pd.DataFrame(all_data)
df_consolidado.to_excel('consolidado.xlsx', index=False)
print(f"✓ Processados {len(xml_files)} arquivos")
print(f"✓ Total de itens: {len(df_consolidado)}")
```

---

## 🎯 Dicas e Boas Práticas

### 1. Verificar Campos Antes de Usar
```python
# Sempre verificar se campo existe
valor = item.get('campo_opcional', 'N/A')
```

### 2. Tratar Valores None
```python
# Substituir None por 0 em campos numéricos
df.fillna(0, inplace=True)
```

### 3. Filtrar Campos Relevantes
```python
# Remover campos vazios
df_limpo = df.dropna(axis=1, how='all')
```

### 4. Usar Logging
```python
from src.utils.logger import setup_logger

# Ativar logs detalhados
setup_logger(log_level='DEBUG')
```

---

## 🐛 Solução de Problemas

### Problema: Campos com valor None
**Causa:** Campo não existe no XML  
**Solução:** Normal para campos opcionais

### Problema: Erro ao exportar Excel
**Causa:** Muitos campos (limite Excel: 16.384 colunas)  
**Solução:** Filtrar campos ou usar CSV

### Problema: Encoding incorreto
**Causa:** Arquivo XML com encoding diferente  
**Solução:** Verificar encoding do arquivo

---

## 📞 Suporte

- 📖 Documentação completa: `CHANGELOG_STREAMING_PARSER.md`
- 🧪 Script de teste: `test_field_extraction.py`
- 📊 Logs: `logs/streaming_parser.log`

---

**Versão:** 2.0  
**Última atualização:** 2026-04-17