# 🏢 Consultor de CNPJ - Versão Streamlit

Aplicação moderna para consulta de CNPJs brasileiros usando Streamlit, com interface responsiva e recursos avançados.

## 📋 Índice

- [Características](#características)
- [Requisitos](#requisitos)
- [Instalação](#instalação)
- [Como Usar](#como-usar)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Deployment](#deployment)
- [Diferenças da Versão Tkinter](#diferenças-da-versão-tkinter)
- [Troubleshooting](#troubleshooting)

## ✨ Características

### Funcionalidades Principais

- **🔍 Consulta Individual**: Consulte CNPJs individualmente com resultados detalhados
- **📊 Processamento em Lote**: Processe múltiplos CNPJs de arquivos Excel ou CSV
- **⚙️ Configurações Personalizáveis**: Ajuste limites de API, proxy e outras configurações
- **📋 Sistema de Logs**: Acompanhe todas as operações em tempo real
- **💾 Cache Inteligente**: Resultados salvos para consultas futuras
- **📥 Exportação**: Baixe resultados em formato Excel

### Melhorias da Versão Streamlit

- ✅ Interface moderna e responsiva
- ✅ Funciona em qualquer navegador (desktop e mobile)
- ✅ Drag-and-drop para upload de arquivos
- ✅ Tabelas interativas para visualização de dados
- ✅ Temas claro/escuro nativos do Streamlit
- ✅ Sem necessidade de instalação de executável
- ✅ Fácil deployment na nuvem
- ✅ ~60% menos código que a versão Tkinter

## 📦 Requisitos

### Sistema

- Python 3.8 ou superior
- Conexão com internet
- Navegador web moderno

### Dependências

```
streamlit==1.31.0
openpyxl==3.1.2
requests==2.32.4
pandas==2.2.0
```

## 🚀 Instalação

### 1. Clone ou baixe o projeto

```bash
cd Consultor_cnpj_v3/codigos_v3
```

### 2. Crie um ambiente virtual (recomendado)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements_streamlit.txt
```

## 💻 Como Usar

### Executar Localmente

```bash
streamlit run app_streamlit.py
```

A aplicação abrirá automaticamente no navegador em `http://localhost:8501`

### Consulta Individual

1. Acesse a aba **"🔍 Consulta Individual"**
2. Digite o CNPJ (com ou sem formatação)
3. Clique em **"🔎 Consultar"**
4. Visualize os resultados completos
5. Veja as inscrições estaduais em tabela interativa

### Processamento em Lote

1. Acesse a aba **"📊 Processamento em Lote"**
2. Faça upload do arquivo Excel ou CSV
3. Informe o nome da coluna com CNPJs (padrão: "CNPJ")
4. Defina o nome do arquivo de saída
5. Clique em **"🚀 Processar Arquivo"**
6. Acompanhe o progresso em tempo real
7. Baixe os resultados usando o botão de download

### Configurações

Use a **barra lateral** para:

- Ajustar limites de requisições por minuto
- Configurar tempo de espera
- Definir proxy (se necessário)
- Limpar cache
- Limpar logs

## 📁 Estrutura do Projeto

```
codigos_v3/
├── app_streamlit.py           # Aplicação principal Streamlit
├── api_client.py              # Cliente da API CNPJ.WS
├── constants.py               # Constantes e configurações
├── requirements_streamlit.txt # Dependências Python
├── README_STREAMLIT.md        # Esta documentação
├── .streamlit/
│   └── config.toml           # Configurações do Streamlit
└── cnpj_cache.json           # Cache de consultas (gerado automaticamente)
```

## 🌐 Deployment

### Streamlit Cloud (Gratuito)

1. **Crie uma conta** em [streamlit.io](https://streamlit.io)

2. **Faça upload do projeto** para GitHub

3. **Configure o deployment:**
   - Conecte seu repositório GitHub
   - Selecione o branch
   - Defina o caminho: `Consultor_cnpj_v3/codigos_v3/app_streamlit.py`
   - Arquivo de requirements: `requirements_streamlit.txt`

4. **Deploy!** A aplicação estará disponível em uma URL pública

### Docker (Opcional)

Crie um `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements_streamlit.txt .
RUN pip install --no-cache-dir -r requirements_streamlit.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app_streamlit.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

Build e execute:

```bash
docker build -t consultor-cnpj .
docker run -p 8501:8501 consultor-cnpj
```

### Servidor Local (Produção)

Para executar em servidor:

```bash
streamlit run app_streamlit.py --server.port 8501 --server.address 0.0.0.0
```

Com PM2 (para manter rodando):

```bash
pm2 start "streamlit run app_streamlit.py" --name consultor-cnpj
```

## 🔄 Diferenças da Versão Tkinter

| Aspecto | Tkinter | Streamlit |
|---------|---------|-----------|
| **Interface** | Desktop nativa | Web responsiva |
| **Instalação** | Executável Windows | Navegador web |
| **Código** | ~550 linhas | ~670 linhas (mais funcionalidades) |
| **Threading** | Manual com Queue | Nativo do Streamlit |
| **Tabelas** | Text widget | DataFrame interativo |
| **Progresso** | ttk.Progressbar | st.progress() |
| **Logs** | Text widget | Expander colapsável |
| **Deployment** | Instalador .exe | Cloud/Docker/Local |
| **Mobile** | Não suportado | Totalmente responsivo |
| **Temas** | Fixo | Claro/Escuro automático |

## 🛠️ Troubleshooting

### Erro: "ModuleNotFoundError: No module named 'streamlit'"

**Solução:** Instale as dependências
```bash
pip install -r requirements_streamlit.txt
```

### Erro: "Address already in use"

**Solução:** Porta 8501 já está em uso. Use outra porta:
```bash
streamlit run app_streamlit.py --server.port 8502
```

### Erro de Rate Limit da API

**Solução:** 
1. Acesse as Configurações na barra lateral
2. Aumente o "Tempo de espera" para 90 segundos
3. Reduza "Requisições por minuto" para 2
4. Salve as configurações

### Arquivo não processa

**Solução:**
1. Verifique se o arquivo é Excel (.xlsx, .xls) ou CSV
2. Confirme que existe uma coluna com CNPJs
3. Verifique o nome exato da coluna (case-sensitive)
4. Certifique-se que os CNPJs estão no formato correto

### Proxy não funciona

**Solução:**
1. Verifique o formato: `http://proxy:porta` ou `https://proxy:porta`
2. Teste com e sem autenticação
3. Confirme que o proxy está acessível
4. Salve as configurações após preencher

## 📊 Formato dos Arquivos

### Arquivo de Entrada (Excel/CSV)

```
| CNPJ           | Outras Colunas |
|----------------|----------------|
| 00000000000191 | ...            |
| 12.345.678/0001-90 | ...        |
```

### Arquivo de Saída (Excel)

**Aba "CNPJs":**
- CNPJ, Razão Social, Nome Fantasia
- Natureza Jurídica
- Endereço completo
- Telefone, Email
- Situação cadastral
- IE Ativa (número, UF, situação)

**Aba "Histórico IEs":**
- Todas as inscrições estaduais
- Histórico completo por CNPJ

## 🔐 Segurança

- ✅ Não armazena senhas em texto plano
- ✅ Cache local (não compartilhado)
- ✅ Conexões HTTPS com a API
- ✅ Validação de entrada de dados
- ✅ Proteção XSRF habilitada

## 📝 Logs

Todos os eventos são registrados em:
- **Interface:** Expander "📋 Log de Atividades"
- **Arquivo:** `log_cnpj.txt` (no diretório da aplicação)

Tipos de log:
- ℹ️ Informação
- ✅ Sucesso
- ❌ Erro
- ⚠️ Aviso

## 🆘 Suporte

Para dúvidas ou problemas:
1. Consulte a aba **"❓ Ajuda"** na aplicação
2. Verifique os logs de atividades
3. Revise esta documentação
4. Entre em contato com o desenvolvedor

## 📄 Licença

Este projeto utiliza a API pública do CNPJ.WS (https://publica.cnpj.ws/)

---

**Versão:** 3.0 (Streamlit)  
**Última atualização:** 2026  
**Desenvolvido com:** Python + Streamlit