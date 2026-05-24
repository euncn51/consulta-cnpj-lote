# 🚀 Quick Start - Consultor de CNPJ (Streamlit)

## Instalação Rápida (3 passos)

### 1️⃣ Instale as dependências

```bash
pip install -r requirements_streamlit.txt
```

### 2️⃣ Execute a aplicação

```bash
streamlit run app_streamlit.py
```

### 3️⃣ Acesse no navegador

A aplicação abrirá automaticamente em: **http://localhost:8501**

---

## 📖 Uso Básico

### Consulta Individual

1. Digite o CNPJ no campo
2. Clique em "Consultar"
3. Veja os resultados completos

### Processamento em Lote

1. Faça upload do arquivo Excel/CSV
2. Informe o nome da coluna com CNPJs
3. Clique em "Processar Arquivo"
4. Baixe os resultados

---

## ⚙️ Configurações Importantes

**Barra Lateral → Configurações:**

- **Requisições/min:** 3 (padrão)
- **Tempo de espera:** 65 segundos (padrão)

**Se receber erro de rate limit:**
- Aumente o tempo de espera para 90 segundos
- Reduza requisições/min para 2

---

## 📁 Arquivos Criados

- `app_streamlit.py` - Aplicação principal
- `requirements_streamlit.txt` - Dependências
- `.streamlit/config.toml` - Configurações de tema
- `README_STREAMLIT.md` - Documentação completa
- `cnpj_cache.json` - Cache (gerado automaticamente)
- `log_cnpj.txt` - Logs (gerado automaticamente)

---

## 🆘 Problemas Comuns

**Porta já em uso?**
```bash
streamlit run app_streamlit.py --server.port 8502
```

**Módulo não encontrado?**
```bash
pip install streamlit pandas openpyxl requests
```

**API retorna erro?**
- Verifique sua conexão com internet
- Ajuste os limites nas configurações
- Aguarde alguns minutos e tente novamente

---

## 📚 Documentação Completa

Veja `README_STREAMLIT.md` para:
- Deployment na nuvem
- Configuração de proxy
- Troubleshooting detalhado
- Exemplos de uso avançado

---

**Pronto para usar! 🎉**