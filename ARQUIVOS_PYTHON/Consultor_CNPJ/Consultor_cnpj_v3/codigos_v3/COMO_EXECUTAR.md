# ⚠️ IMPORTANTE: Como Executar a Aplicação Streamlit

## ❌ ERRO COMUM

**NÃO execute assim:**
```bash
python app_streamlit.py
```

Isso causará o erro: `missing ScriptRunContext`

---

## ✅ FORMA CORRETA

### Opção 1: Comando Streamlit (RECOMENDADO)

```bash
streamlit run app_streamlit.py
```

### Opção 2: Usando o Script de Inicialização

**Windows:**
```bash
.\run_streamlit.bat
```

**Linux/Mac:**
```bash
./run_streamlit.sh
```

---

## 📋 Passo a Passo Completo

### 1. Abra o PowerShell ou Terminal

Navegue até a pasta do projeto:
```bash
cd C:\Users\08748D631\.vscode\ARQUIVOS_PYTHON\Consultor_CNPJ\Consultor_cnpj_v3\codigos_v3
```

### 2. Instale as Dependências (primeira vez)

```bash
pip install -r requirements_streamlit.txt
```

### 3. Execute a Aplicação

```bash
streamlit run app_streamlit.py
```

### 4. Acesse no Navegador

A aplicação abrirá automaticamente em:
```
http://localhost:8501
```

Se não abrir automaticamente, copie e cole o endereço no navegador.

---

## 🔧 Solução de Problemas

### Erro: "streamlit não é reconhecido"

**Solução:**
```bash
pip install streamlit
```

### Erro: "Porta 8501 já está em uso"

**Solução:** Use outra porta
```bash
streamlit run app_streamlit.py --server.port 8502
```

### Erro: "ModuleNotFoundError"

**Solução:** Instale todas as dependências
```bash
pip install -r requirements_streamlit.txt
```

---

## 💡 Dicas

- **Parar a aplicação:** Pressione `Ctrl+C` no terminal
- **Recarregar:** A aplicação recarrega automaticamente ao salvar alterações
- **Limpar cache:** Pressione `C` no terminal ou use o menu da aplicação

---

## 📞 Precisa de Ajuda?

Consulte os arquivos de documentação:
- `QUICKSTART_STREAMLIT.md` - Início rápido
- `README_STREAMLIT.md` - Documentação completa
- `MIGRATION_SUMMARY.md` - Resumo da migração