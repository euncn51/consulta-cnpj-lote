"""
Consultor de CNPJ - Versão Streamlit
Aplicação moderna para consulta de CNPJs usando Streamlit

Características:
- Interface responsiva e moderna
- Consulta individual e em lote
- Configurações personalizáveis
- Sistema de logging integrado
- Exportação de resultados
"""

import streamlit as st
import json
import os
from datetime import datetime
from io import BytesIO
import pandas as pd

from api_client import CNPJConsultor
from constants import LANG, API_CONFIG

# Configuração da página
st.set_page_config(
    page_title="Consultor de CNPJ",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado para melhorar a aparência
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #4F81BD;
        text-align: center;
        margin-bottom: 2rem;
    }
    .success-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
    }
    .error-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
    }
    .info-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
        color: #0c5460;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    .stTabs [data-baseweb="tab"] {
        height: 3rem;
        padding: 0 2rem;
    }
</style>
""", unsafe_allow_html=True)

# Inicialização do session state
def init_session_state():
    """Inicializa todas as variáveis de estado da sessão"""
    if 'consultor' not in st.session_state:
        st.session_state.consultor = CNPJConsultor()
    
    if 'logs' not in st.session_state:
        st.session_state.logs = []
    
    if 'processing' not in st.session_state:
        st.session_state.processing = False
    
    if 'last_result' not in st.session_state:
        st.session_state.last_result = None
    
    if 'batch_results' not in st.session_state:
        st.session_state.batch_results = None

def add_log(message: str, level: str = "info"):
    """Adiciona uma mensagem ao log"""
    timestamp = datetime.now().strftime('%H:%M:%S')
    icon = {"info": "ℹ️", "success": "✅", "error": "❌", "warning": "⚠️"}.get(level, "ℹ️")
    log_entry = f"{timestamp} - {icon} {message}"
    st.session_state.logs.append(log_entry)
    
    # Salva no arquivo de log
    try:
        with open(LANG["log_file"], "a", encoding="utf-8") as f:
            f.write(log_entry + "\n")
    except Exception:
        pass

def display_logs():
    """Exibe os logs em um expander"""
    with st.expander("📋 Log de Atividades", expanded=False):
        if st.session_state.logs:
            for log in reversed(st.session_state.logs[-50:]):  # Últimos 50 logs
                st.text(log)
        else:
            st.info("Nenhuma atividade registrada ainda.")

def sidebar_settings():
    """Cria a barra lateral com configurações"""
    st.sidebar.title("⚙️ Configurações")
    
    # Configurações de API
    st.sidebar.subheader("Limites de API")
    
    limite = st.sidebar.number_input(
        "Requisições por minuto:",
        min_value=1,
        max_value=10,
        value=st.session_state.consultor.limite_requisicoes,
        help="Número máximo de requisições por minuto"
    )
    
    tempo_espera = st.sidebar.number_input(
        "Tempo de espera (segundos):",
        min_value=10,
        max_value=120,
        value=st.session_state.consultor.tempo_espera,
        help="Tempo de espera ao atingir o limite"
    )
    
    # Configurações de Proxy
    st.sidebar.subheader("Configurações de Proxy")
    
    proxy_http = st.sidebar.text_input(
        "Proxy HTTP:",
        placeholder="http://proxy:porta"
    )
    
    proxy_https = st.sidebar.text_input(
        "Proxy HTTPS:",
        placeholder="https://proxy:porta"
    )
    
    with st.sidebar.expander("Autenticação do Proxy"):
        proxy_user = st.text_input("Usuário:", key="proxy_user")
        proxy_pass = st.text_input("Senha:", type="password", key="proxy_pass")
    
    # Botão para salvar configurações
    if st.sidebar.button("💾 Salvar Configurações", use_container_width=True):
        st.session_state.consultor.limite_requisicoes = limite
        st.session_state.consultor.tempo_espera = tempo_espera
        
        # Configurar proxy
        proxies = {}
        if proxy_http:
            proxies['http'] = proxy_http
        if proxy_https:
            proxies['https'] = proxy_https
        
        if proxies:
            st.session_state.consultor.session.proxies = proxies
        
        if proxy_user and proxy_pass:
            st.session_state.consultor.session.auth = (proxy_user, proxy_pass)
        
        st.sidebar.success("✅ Configurações salvas!")
        add_log("Configurações atualizadas", "success")
    
    # Gerenciamento de Cache
    st.sidebar.subheader("Gerenciamento")
    
    col1, col2 = st.sidebar.columns(2)
    
    with col1:
        if st.button("🗑️ Limpar Cache", use_container_width=True):
            st.session_state.consultor.cache = {}
            st.session_state.consultor._save_cache()
            st.sidebar.success("Cache limpo!")
            add_log("Cache limpo com sucesso", "success")
    
    with col2:
        if st.button("📝 Limpar Logs", use_container_width=True):
            st.session_state.logs = []
            st.sidebar.success("Logs limpos!")
    
    # Informações
    st.sidebar.divider()
    st.sidebar.info(f"📦 Cache: {len(st.session_state.consultor.cache)} CNPJs")
    st.sidebar.info(f"📊 Logs: {len(st.session_state.logs)} entradas")

def tab_individual():
    """Aba de consulta individual"""
    st.header("🔍 Consulta Individual de CNPJ")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        cnpj_input = st.text_input(
            "Digite o CNPJ:",
            placeholder="00.000.000/0000-00",
            help="Digite apenas os números ou com formatação",
            key="cnpj_input"
        )
    
    with col2:
        st.write("")  # Espaçamento
        st.write("")  # Espaçamento
        consultar_btn = st.button("🔎 Consultar", type="primary", use_container_width=True)
    
    if consultar_btn and cnpj_input:
        cnpj_limpo = st.session_state.consultor.clean_cnpj(cnpj_input)
        
        if len(cnpj_limpo) != 14:
            st.error("❌ CNPJ inválido! Deve conter 14 dígitos.")
            add_log(f"Tentativa de consulta com CNPJ inválido: {cnpj_input}", "error")
        else:
            with st.spinner(f"Consultando CNPJ {cnpj_limpo}..."):
                add_log(f"Consultando CNPJ: {cnpj_limpo}", "info")
                dados = st.session_state.consultor.consultar_cnpj(cnpj_limpo)
                
                if dados:
                    resultado = st.session_state.consultor.extrair_dados(dados)
                    st.session_state.last_result = resultado
                    add_log(f"Consulta realizada com sucesso: {cnpj_limpo}", "success")
                else:
                    st.error(f"❌ Falha na consulta do CNPJ {cnpj_limpo}")
                    add_log(f"Falha na consulta: {cnpj_limpo}", "error")
    
    # Exibir resultado
    if st.session_state.last_result:
        resultado = st.session_state.last_result
        
        if 'ERRO' in resultado:
            st.error(f"❌ Erro: {resultado['ERRO']}")
        else:
            st.success("✅ Consulta realizada com sucesso!")
            
            # Informações principais em cards
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("CNPJ", resultado.get('CNPJ', 'N/A'))
            with col2:
                st.metric("Situação", resultado.get('SITUACAO', 'N/A'))
            with col3:
                st.metric("UF", resultado.get('UF', 'N/A'))
            
            # Dados da empresa
            st.subheader("📋 Dados da Empresa")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.text_input("Razão Social:", value=resultado.get('RAZAO_SOCIAL', ''), disabled=True)
                st.text_input("Nome Fantasia:", value=resultado.get('NOME_FANTASIA', ''), disabled=True)
                st.text_input("Natureza Jurídica:", value=resultado.get('NATUREZA_JURIDICA', ''), disabled=True)
                st.text_input("Telefone:", value=resultado.get('TELEFONE', ''), disabled=True)
                st.text_input("Email:", value=resultado.get('EMAIL', ''), disabled=True)
            
            with col2:
                st.text_input("Endereço:", value=resultado.get('ENDERECO', ''), disabled=True)
                st.text_input("Número:", value=resultado.get('NUMERO', ''), disabled=True)
                st.text_input("Complemento:", value=resultado.get('COMPLEMENTO', ''), disabled=True)
                st.text_input("Bairro:", value=resultado.get('BAIRRO', ''), disabled=True)
                st.text_input("CEP:", value=resultado.get('CEP', ''), disabled=True)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.text_input("Município:", value=resultado.get('MUNICIPIO', ''), disabled=True)
            with col2:
                st.text_input("Código IBGE:", value=resultado.get('COD_IBGE', ''), disabled=True)
            with col3:
                st.text_input("Data Situação:", value=resultado.get('DATA_SITUACAO_CADASTRAL', ''), disabled=True)
            
            # Inscrições Estaduais
            st.subheader("📄 Inscrições Estaduais")
            
            if resultado.get('INSCRICOES_ESTADUAIS') and resultado['INSCRICOES_ESTADUAIS'] != '[]':
                try:
                    ies = json.loads(resultado['INSCRICOES_ESTADUAIS'])
                    if ies:
                        # Criar DataFrame para exibição
                        df_ies = pd.DataFrame(ies)
                        st.dataframe(df_ies, use_container_width=True, hide_index=True)
                    else:
                        st.info("ℹ️ Nenhuma inscrição estadual encontrada")
                except json.JSONDecodeError:
                    st.warning("⚠️ Erro ao processar inscrições estaduais")
            else:
                st.info("ℹ️ Nenhuma inscrição estadual encontrada")
            
            # Botões de ação
            col1, col2 = st.columns(2)
            
            with col1:
                # Botão para exportar resultado individual
                if st.button("📥 Exportar para Excel", use_container_width=True):
                    try:
                        # Criar arquivo Excel com o resultado
                        output_file = f"consulta_{resultado.get('CNPJ', 'cnpj')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
                        st.session_state.consultor._salvar_resultados([resultado], output_file)
                        
                        # Oferecer download
                        with open(output_file, "rb") as f:
                            st.download_button(
                                label="📥 Download Excel",
                                data=f.read(),
                                file_name=output_file,
                                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                use_container_width=True
                            )
                        
                        # Remover arquivo temporário
                        try:
                            os.remove(output_file)
                        except:
                            pass
                        
                        st.success("✅ Arquivo Excel gerado com sucesso!")
                        add_log(f"Exportação individual para Excel: {resultado.get('CNPJ', 'N/A')}", "success")
                    except Exception as e:
                        st.error(f"❌ Erro ao exportar: {str(e)}")
                        add_log(f"Erro na exportação: {str(e)}", "error")
            
            with col2:
                # Botão para limpar resultado
                if st.button("🗑️ Limpar Resultado", use_container_width=True):
                    st.session_state.last_result = None
                    st.rerun()

def tab_batch():
    """Aba de processamento em lote"""
    st.header("📊 Processamento em Lote")
    
    # Escolher método de entrada
    metodo = st.radio(
        "Escolha o método de entrada:",
        ["📁 Upload de Arquivo", "📋 Colar Lista de CNPJs"],
        horizontal=True
    )
    
    if metodo == "📁 Upload de Arquivo":
        st.info("💡 Faça upload de um arquivo Excel (.xlsx, .xls) ou CSV com uma coluna contendo CNPJs")
        
        # Upload do arquivo
        uploaded_file = st.file_uploader(
            "Selecione o arquivo com CNPJs:",
            type=['xlsx', 'xls', 'csv'],
            help="Arquivo deve conter uma coluna com CNPJs"
        )
        
        if uploaded_file:
            _processar_arquivo(uploaded_file)
    
    else:  # Colar Lista de CNPJs
        st.info("💡 Cole os CNPJs abaixo (um por linha ou separados por vírgula, ponto-e-vírgula ou espaço)")
        
        # Área de texto para colar CNPJs
        cnpjs_text = st.text_area(
            "Cole os CNPJs aqui:",
            height=200,
            placeholder="00000000000191\n12345678000190\n98765432000100\n...",
            help="Cole os CNPJs separados por linha, vírgula, ponto-e-vírgula ou espaço"
        )
        
        if cnpjs_text:
            _processar_lista_cnpjs(cnpjs_text)

def _processar_arquivo(uploaded_file):
    """Processa CNPJs de um arquivo"""
    if uploaded_file:
        # Nome da coluna CNPJ
        col_cnpj = st.text_input(
            "Nome da coluna com CNPJs:",
            value="CNPJ",
            help="Nome exato da coluna que contém os CNPJs"
        )
        
        # Nome do arquivo de saída
        output_name = st.text_input(
            "Nome do arquivo de saída:",
            value="resultados_cnpj.xlsx",
            help="Nome do arquivo Excel que será gerado"
        )
        
        if st.button("🚀 Processar Arquivo", type="primary", use_container_width=True):
            if not col_cnpj:
                st.error("❌ Informe o nome da coluna com CNPJs!")
            else:
                # Salvar arquivo temporariamente
                temp_input = f"temp_input_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{uploaded_file.name.split('.')[-1]}"
                with open(temp_input, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                
                try:
                    # Ler arquivo para contar CNPJs
                    df_input = st.session_state.consultor._ler_arquivo(temp_input)
                    
                    if not df_input or col_cnpj not in df_input[0]:
                        st.error(f"❌ Coluna '{col_cnpj}' não encontrada no arquivo!")
                        add_log(f"Coluna '{col_cnpj}' não encontrada", "error")
                    else:
                        total_cnpjs = len(df_input)
                        st.info(f"📊 Total de CNPJs a processar: {total_cnpjs}")
                        
                        # Criar containers para progresso
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        
                        # Processar
                        resultados = []
                        st.session_state.consultor.stop_processing = False
                        
                        for index, row in enumerate(df_input, 1):
                            if st.session_state.consultor.stop_processing:
                                st.warning("⚠️ Processamento cancelado!")
                                break
                            
                            cnpj = row.get(col_cnpj, "")
                            cnpj_limpo = st.session_state.consultor.clean_cnpj(str(cnpj))
                            
                            # Atualizar progresso
                            progress = index / total_cnpjs
                            progress_bar.progress(progress)
                            status_text.text(f"Processando {index}/{total_cnpjs} - CNPJ: {cnpj_limpo}")
                            
                            if len(cnpj_limpo) != 14:
                                resultados.append({'CNPJ': cnpj, 'ERRO': 'CNPJ inválido'})
                                continue
                            
                            dados = st.session_state.consultor.consultar_cnpj(cnpj_limpo)
                            if dados and 'estabelecimento' in dados:
                                resultados.append(st.session_state.consultor.extrair_dados(dados))
                            else:
                                resultados.append({'CNPJ': cnpj_limpo, 'ERRO': 'Falha na consulta'})
                        
                        # Salvar resultados
                        st.session_state.consultor._salvar_resultados(resultados, output_name)
                        st.session_state.batch_results = resultados
                        
                        progress_bar.progress(1.0)
                        status_text.empty()
                        
                        st.success(f"✅ Processamento concluído! {len(resultados)} CNPJs processados.")
                        add_log(f"Processamento em lote concluído: {len(resultados)} CNPJs", "success")
                        
                        # Botão de download
                        with open(output_name, "rb") as f:
                            st.download_button(
                                label="📥 Download Resultados",
                                data=f.read(),
                                file_name=output_name,
                                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                use_container_width=True
                            )
                        
                        # Exibir preview dos resultados
                        st.subheader("📋 Preview dos Resultados")
                        df_results = pd.DataFrame(resultados)
                        
                        # Formatar CNPJ para evitar notação científica
                        if 'CNPJ' in df_results.columns:
                            df_results['CNPJ'] = df_results['CNPJ'].astype(str)
                        

def _processar_lista_cnpjs(cnpjs_text):
    """Processa CNPJs colados diretamente"""
    # Nome do arquivo de saída
    output_name = st.text_input(
        "Nome do arquivo de saída:",
        value="resultados_cnpj.xlsx",
        help="Nome do arquivo Excel que será gerado",
        key="output_lista"
    )
    
    if st.button("🚀 Processar CNPJs", type="primary", use_container_width=True):
        try:
            # Extrair CNPJs do texto
            import re
            # Separar por linha, vírgula, ponto-e-vírgula ou espaço
            cnpjs_raw = re.split(r'[\n,;\s]+', cnpjs_text.strip())
            # Limpar e filtrar CNPJs vazios
            cnpjs_list = [cnpj.strip() for cnpj in cnpjs_raw if cnpj.strip()]
            
            if not cnpjs_list:
                st.error("❌ Nenhum CNPJ encontrado no texto!")
                return
            
            total_cnpjs = len(cnpjs_list)
            st.info(f"📊 Total de CNPJs encontrados: {total_cnpjs}")
            
            # Criar containers para progresso
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Processar
            resultados = []
            st.session_state.consultor.stop_processing = False
            
            for index, cnpj in enumerate(cnpjs_list, 1):
                if st.session_state.consultor.stop_processing:
                    st.warning("⚠️ Processamento cancelado!")
                    break
                
                cnpj_limpo = st.session_state.consultor.clean_cnpj(str(cnpj))
                
                # Atualizar progresso
                progress = index / total_cnpjs
                progress_bar.progress(progress)
                status_text.text(f"Processando {index}/{total_cnpjs} - CNPJ: {cnpj_limpo}")
                
                if len(cnpj_limpo) != 14:
                    resultados.append({'CNPJ': cnpj, 'ERRO': 'CNPJ inválido'})
                    add_log(f"CNPJ inválido: {cnpj}", "warning")
                    continue
                
                dados = st.session_state.consultor.consultar_cnpj(cnpj_limpo)
                if dados and 'estabelecimento' in dados:
                    resultados.append(st.session_state.consultor.extrair_dados(dados))
                else:
                    resultados.append({'CNPJ': cnpj_limpo, 'ERRO': 'Falha na consulta'})
            
            # Salvar resultados
            st.session_state.consultor._salvar_resultados(resultados, output_name)
            st.session_state.batch_results = resultados
            
            progress_bar.progress(1.0)
            status_text.empty()
            
            st.success(f"✅ Processamento concluído! {len(resultados)} CNPJs processados.")
            add_log(f"Processamento em lote (lista) concluído: {len(resultados)} CNPJs", "success")
            
            # Botão de download
            with open(output_name, "rb") as f:
                st.download_button(
                    label="📥 Download Resultados",
                    data=f.read(),
                    file_name=output_name,
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
            
            # Exibir preview dos resultados
            st.subheader("📋 Preview dos Resultados")
            df_results = pd.DataFrame(resultados)
            
            # Formatar CNPJ para evitar notação científica
            if 'CNPJ' in df_results.columns:
                df_results['CNPJ'] = df_results['CNPJ'].astype(str)
            
            # Remover coluna INSCRICOES_ESTADUAIS do preview
            cols_to_show = [col for col in df_results.columns if col != 'INSCRICOES_ESTADUAIS']
            df_preview = df_results[cols_to_show].head(20)
            
            st.dataframe(df_preview, use_container_width=True)
            
            # Mostrar estatísticas
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Processados", len(resultados))
            with col2:
                erros = len([r for r in resultados if 'ERRO' in r and r['ERRO']])
                st.metric("Com Erro", erros)
            with col3:
                sucesso = len(resultados) - erros
                st.metric("Sucesso", sucesso)
            
        except Exception as e:
            st.error(f"❌ Erro ao processar CNPJs: {str(e)}")
            add_log(f"Erro no processamento em lote (lista): {str(e)}", "error")

                        # Remover coluna INSCRICOES_ESTADUAIS do preview (muito grande)
                        cols_to_show = [col for col in df_results.columns if col != 'INSCRICOES_ESTADUAIS']
                        df_preview = df_results[cols_to_show].head(20)
                        
                        st.dataframe(df_preview, use_container_width=True)
                        
                        # Mostrar estatísticas
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Total Processados", len(resultados))
                        with col2:
                            erros = len([r for r in resultados if 'ERRO' in r and r['ERRO']])
                            st.metric("Com Erro", erros)
                        with col3:
                            sucesso = len(resultados) - erros
                            st.metric("Sucesso", sucesso)
                        
                except Exception as e:
                    st.error(f"❌ Erro ao processar arquivo: {str(e)}")
                    add_log(f"Erro no processamento em lote: {str(e)}", "error")
                finally:
                    # Limpar arquivo temporário com tratamento de erro
                    try:
                        if os.path.exists(temp_input):
                            import time
                            time.sleep(0.5)  # Aguarda um pouco antes de tentar remover
                            os.remove(temp_input)
                    except PermissionError:
                        # Se não conseguir remover, apenas registra no log
                        add_log(f"Arquivo temporário {temp_input} será removido posteriormente", "warning")
                    except Exception:
                        pass

def tab_help():
    """Aba de ajuda"""
    st.header("❓ Ajuda e Documentação")
    
    with st.expander("🔍 Consulta Individual", expanded=True):
        st.markdown("""
        ### Como usar a Consulta Individual
        
        1. **Digite o CNPJ** no campo de entrada (com ou sem formatação)
        2. **Clique em Consultar** ou pressione Enter
        3. **Visualize os resultados** com todos os dados da empresa
        4. **Inscrições Estaduais** são exibidas em uma tabela interativa
        
        **Dicas:**
        - Você pode digitar o CNPJ com ou sem pontuação
        - Os resultados são salvos em cache para consultas futuras
        - Use o botão "Limpar Resultado" para fazer uma nova consulta
        """)
    
    with st.expander("📊 Processamento em Lote"):
        st.markdown("""
        ### Como usar o Processamento em Lote
        
        1. **Prepare seu arquivo:**
           - Formato: Excel (.xlsx, .xls) ou CSV
           - Deve conter uma coluna com CNPJs
           - Pode ter outras colunas (serão ignoradas)
        
        2. **Faça o upload** do arquivo usando o botão de upload
        
        3. **Informe o nome da coluna** que contém os CNPJs (padrão: "CNPJ")
        
        4. **Defina o nome do arquivo de saída** (padrão: "resultados_cnpj.xlsx")
        
        5. **Clique em Processar** e aguarde
        
        6. **Baixe os resultados** usando o botão de download
        
        **O arquivo de saída contém:**
        - Aba "CNPJs": Dados completos de cada empresa
        - Aba "Histórico IEs": Todas as inscrições estaduais
        
        **Observações:**
        - O processamento respeita os limites de API configurados
        - CNPJs inválidos são marcados com erro
        - O progresso é exibido em tempo real
        """)
    
    with st.expander("⚙️ Configurações"):
        st.markdown("""
        ### Configurações Disponíveis
        
        **Limites de API:**
        - **Requisições por minuto:** Número máximo de consultas por minuto (padrão: 3)
        - **Tempo de espera:** Tempo de pausa ao atingir o limite (padrão: 65 segundos)
        
        **Proxy:**
        - Configure se sua rede exigir proxy
        - Suporta autenticação com usuário e senha
        - Formatos: `http://proxy:porta` ou `https://proxy:porta`
        
        **Gerenciamento:**
        - **Limpar Cache:** Remove todos os CNPJs salvos em cache
        - **Limpar Logs:** Limpa o histórico de atividades
        
        💡 **Dica:** Ajuste os limites de API se estiver recebendo erros de rate limit
        """)
    
    with st.expander("📋 Logs e Monitoramento"):
        st.markdown("""
        ### Sistema de Logs
        
        - Todos os eventos são registrados no log de atividades
        - Logs são salvos no arquivo `log_cnpj.txt`
        - Ícones indicam o tipo de evento:
          - ℹ️ Informação
          - ✅ Sucesso
          - ❌ Erro
          - ⚠️ Aviso
        
        **Visualização:**
        - Expanda o "Log de Atividades" na parte inferior
        - Mostra os últimos 50 eventos
        - Ordem cronológica reversa (mais recentes primeiro)
        """)
    
    with st.expander("🚀 Dicas e Atalhos"):
        st.markdown("""
        ### Dicas de Uso
        
        - **Cache inteligente:** CNPJs já consultados são recuperados instantaneamente
        - **Validação automática:** CNPJs inválidos são detectados antes da consulta
        - **Exportação completa:** Resultados incluem todas as inscrições estaduais
        - **Código IBGE:** Obtido automaticamente para cada município
        
        ### Solução de Problemas
        
        **Erro de rate limit:**
        - Aumente o tempo de espera nas configurações
        - Reduza o número de requisições por minuto
        
        **CNPJ não encontrado:**
        - Verifique se o CNPJ está correto
        - Alguns CNPJs podem não estar disponíveis na base pública
        
        **Erro de conexão:**
        - Verifique sua conexão com a internet
        - Configure o proxy se necessário
        """)
    
    st.divider()
    
    st.info("""
    **📞 Suporte**
    
    Para dúvidas ou problemas, consulte o desenvolvedor.
    
    **Versão:** 3.0 (Streamlit)  
    **API:** CNPJ.WS (https://publica.cnpj.ws/)
    """)

def main():
    """Função principal da aplicação"""
    # Inicializar session state
    init_session_state()
    
    # Título principal
    st.markdown('<h1 class="main-header">🏢 Consultor de CNPJ</h1>', unsafe_allow_html=True)
    
    # Sidebar com configurações
    sidebar_settings()
    
    # Tabs principais
    tab1, tab2, tab3 = st.tabs(["🔍 Consulta Individual", "📊 Processamento em Lote", "❓ Ajuda"])
    
    with tab1:
        tab_individual()
    
    with tab2:
        tab_batch()
    
    with tab3:
        tab_help()
    
    # Logs na parte inferior
    st.divider()
    display_logs()
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: gray;'>"
        "Consultor de CNPJ v3.0 | Desenvolvido com Streamlit"
        "</div>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()

# Made with Bob
