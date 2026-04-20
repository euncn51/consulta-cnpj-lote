"""
GUI Web para NFe Parser usando Streamlit

Interface web moderna com:
- Upload de múltiplos arquivos
- Processamento em tempo real
- Visualizações interativas
- Dashboard de análise
- Download de resultados
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import sys
from datetime import datetime
import io

# Adicionar diretório pai ao path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.utils.logger import setup_logger, get_logger
from src.config import get_settings
from src.core.streaming_parser import StreamingNFeParser
from src.core.field_mapper import FieldMapper


# Configuração da página
st.set_page_config(
    page_title="NFe Parser - Análise de Notas Fiscais",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inicializar componentes
@st.cache_resource
def init_components():
    """Inicializa componentes do sistema"""
    setup_logger(log_level='INFO')
    logger = get_logger('streamlit_app')
    settings = get_settings()
    parser = StreamingNFeParser()
    mapper = FieldMapper()
    logger.info("Componentes inicializados")
    return logger, settings, parser, mapper

logger, settings, parser, mapper = init_components()


def main():
    """Função principal da aplicação"""
    
    # Título e descrição
    st.title("📊 NFe Parser - Análise de Notas Fiscais Eletrônicas")
    st.markdown("""
    Sistema completo para análise de arquivos XML de NF-e com:
    - ✅ Processamento streaming (arquivos grandes)
    - ✅ Visualizações interativas
    - ✅ Dashboard de análise
    - ✅ Exportação em múltiplos formatos
    """)
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Configurações")
        
        # Informações do sistema
        st.info(f"""
        **{settings.app_name}**  
        Versão: {settings.app_version}
        """)
        
        # Opções de processamento
        st.subheader("Opções")
        use_streaming = st.checkbox(
            "Usar processamento streaming",
            value=True,
            help="Recomendado para arquivos grandes"
        )
        
        validate_schema = st.checkbox(
            "Validar schema XML",
            value=False,
            help="Validação completa do XML"
        )
        
        # Formato de exportação
        st.subheader("Exportação")
        export_format = st.selectbox(
            "Formato",
            ["Excel (.xlsx)", "CSV (.csv)", "JSON (.json)"],
            index=0
        )
        
        # Estatísticas do mapeamento
        st.subheader("📋 Mapeamento")
        stats = mapper.get_statistics()
        st.metric("Total de Campos", stats['total_fields'])
        st.metric("Campos Obrigatórios", stats['required_fields'])
        st.metric("Grupos", len(stats['groups']))
    
    # Tabs principais
    tab1, tab2, tab3, tab4 = st.tabs([
        "📁 Upload & Processamento",
        "📊 Dashboard",
        "📈 Análise Detalhada",
        "ℹ️ Sobre"
    ])
    
    # TAB 1: Upload e Processamento
    with tab1:
        st.header("Upload de Arquivos XML")
        
        uploaded_files = st.file_uploader(
            "Selecione arquivos XML de NF-e",
            type=['xml'],
            accept_multiple_files=True,
            help="Você pode selecionar múltiplos arquivos"
        )
        
        if uploaded_files:
            st.success(f"✅ {len(uploaded_files)} arquivo(s) selecionado(s)")
            
            # Mostrar lista de arquivos
            with st.expander("📄 Arquivos Selecionados"):
                for file in uploaded_files:
                    st.text(f"• {file.name} ({file.size / 1024:.1f} KB)")
            
            # Botão processar
            if st.button("🚀 Processar Arquivos", type="primary", width='stretch'):
                process_files(uploaded_files, use_streaming)
        else:
            st.info("👆 Faça upload de arquivos XML para começar")
    
    # TAB 2: Dashboard
    with tab2:
        if 'df' in st.session_state and st.session_state.df is not None:
            show_dashboard(st.session_state.df)
        else:
            st.info("📊 Processe arquivos XML para ver o dashboard")
    
    # TAB 3: Análise Detalhada
    with tab3:
        if 'df' in st.session_state and st.session_state.df is not None:
            show_detailed_analysis(st.session_state.df)
        else:
            st.info("📈 Processe arquivos XML para ver análises detalhadas")
    
    # TAB 4: Sobre
    with tab4:
        show_about()


def process_files(uploaded_files, use_streaming):
    """Processa arquivos XML"""
    
    st.subheader("⚙️ Processamento")
    
    # Barra de progresso
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    all_data = []
    total_files = len(uploaded_files)
    
    for idx, uploaded_file in enumerate(uploaded_files, 1):
        # Atualizar status
        status_text.text(f"Processando {idx}/{total_files}: {uploaded_file.name}")
        progress_bar.progress(idx / total_files)
        
        try:
            # Ler conteúdo do arquivo
            xml_content = uploaded_file.read().decode('utf-8')
            
            # Salvar temporariamente
            temp_path = Path(f"temp_{uploaded_file.name}")
            with open(temp_path, 'w', encoding='utf-8') as f:
                f.write(xml_content)
            
            # Processar
            if use_streaming:
                data = parser.parse_xml_stream(str(temp_path))
            else:
                data = parser.parse_xml_stream(str(temp_path))
            
            all_data.extend(data)
            
            # Remover arquivo temporário
            temp_path.unlink()
            
        except Exception as e:
            st.error(f"❌ Erro ao processar {uploaded_file.name}: {str(e)}")
            logger.error(f"Erro: {e}", exc_info=True)
    
    # Finalizar
    progress_bar.progress(1.0)
    status_text.text("✅ Processamento concluído!")
    
    if all_data:
        # Criar DataFrame
        df = pd.DataFrame(all_data)
        st.session_state.df = df
        
        # Mostrar resumo
        st.success(f"""
        ✅ **Processamento Concluído!**
        - Arquivos processados: {total_files}
        - Registros extraídos: {len(df)}
        - Colunas: {len(df.columns)}
        """)
        
        # Botão para download
        show_download_button(df)
        
        # Preview dos dados
        with st.expander("👁️ Preview dos Dados"):
            st.dataframe(df.head(10), width='stretch')
    else:
        st.warning("⚠️ Nenhum dado foi extraído dos arquivos")


def show_download_button(df):
    """Mostra botão de download"""
    st.subheader("💾 Download dos Resultados")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Excel
        buffer = io.BytesIO()
        df.to_excel(buffer, index=False, engine='openpyxl')
        st.download_button(
            label="📥 Download Excel",
            data=buffer.getvalue(),
            file_name=f"nfe_resultados_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    
    with col2:
        # CSV
        csv = df.to_csv(index=False, encoding='utf-8-sig')
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name=f"nfe_resultados_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
    
    with col3:
        # JSON
        json_str = df.to_json(orient='records', indent=2)
        st.download_button(
            label="📥 Download JSON",
            data=json_str,
            file_name=f"nfe_resultados_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )


def show_dashboard(df):
    """Mostra dashboard com visualizações"""
    st.header("📊 Dashboard de Análise")
    
    # Métricas principais
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total de NF-es", df['nNF'].nunique() if 'nNF' in df.columns else 0)
    
    with col2:
        st.metric("Total de Itens", len(df))
    
    with col3:
        if 'total_vNF' in df.columns:
            total_value = df['total_vNF'].sum()
            st.metric("Valor Total", f"R$ {total_value:,.2f}")
        else:
            st.metric("Valor Total", "N/A")
    
    with col4:
        st.metric("Emitentes", df['emit_xNome'].nunique() if 'emit_xNome' in df.columns else 0)
    
    st.divider()
    
    # Gráficos
    col1, col2 = st.columns(2)
    
    with col1:
        # Gráfico de NF-es por emitente
        if 'emit_xNome' in df.columns:
            st.subheader("NF-es por Emitente")
            nfe_por_emitente = df.groupby('emit_xNome')['nNF'].nunique().sort_values(ascending=False).head(10)
            fig = px.bar(
                x=nfe_por_emitente.values,
                y=nfe_por_emitente.index,
                orientation='h',
                labels={'x': 'Quantidade', 'y': 'Emitente'},
                title="Top 10 Emitentes"
            )
            st.plotly_chart(fig, width='stretch')
    
    with col2:
        # Gráfico de valores
        if 'vProd' in df.columns:
            st.subheader("Distribuição de Valores")
            fig = px.histogram(
                df,
                x='vProd',
                nbins=50,
                labels={'vProd': 'Valor do Produto'},
                title="Distribuição de Valores dos Produtos"
            )
            st.plotly_chart(fig, width='stretch')
    
    # Tabela de resumo
    st.subheader("📋 Resumo por NF-e")
    if 'nNF' in df.columns:
        resumo = df.groupby('nNF').agg({
            'emit_xNome': 'first',
            'dest_xNome': 'first',
            'vProd': 'sum',
            'nItem': 'count'
        }).reset_index()
        resumo.columns = ['Número NF-e', 'Emitente', 'Destinatário', 'Valor Total', 'Qtd Itens']
        st.dataframe(resumo, width='stretch')


def show_detailed_analysis(df):
    """Mostra análise detalhada"""
    st.header("📈 Análise Detalhada")
    
    # Seletor de análise
    analysis_type = st.selectbox(
        "Selecione o tipo de análise",
        [
            "Produtos Mais Vendidos",
            "Análise por CFOP",
            "Análise de Impostos",
            "Análise Temporal",
            "Dados Completos"
        ]
    )
    
    if analysis_type == "Produtos Mais Vendidos":
        if 'xProd' in df.columns and 'qCom' in df.columns:
            st.subheader("🏆 Top 20 Produtos")
            produtos = df.groupby('xProd').agg({
                'qCom': 'sum',
                'vProd': 'sum'
            }).sort_values('qCom', ascending=False).head(20)
            
            fig = px.bar(
                produtos,
                x=produtos.index,
                y='qCom',
                title="Produtos Mais Vendidos (Quantidade)",
                labels={'qCom': 'Quantidade', 'xProd': 'Produto'}
            )
            fig.update_xaxes(tickangle=45)
            st.plotly_chart(fig, width='stretch')
            
            st.dataframe(produtos, width='stretch')
    
    elif analysis_type == "Análise por CFOP":
        if 'CFOP' in df.columns:
            st.subheader("📊 Análise por CFOP")
            cfop_analysis = df.groupby('CFOP').agg({
                'nItem': 'count',
                'vProd': 'sum'
            }).reset_index()
            cfop_analysis.columns = ['CFOP', 'Quantidade', 'Valor Total']
            
            fig = px.pie(
                cfop_analysis,
                values='Quantidade',
                names='CFOP',
                title="Distribuição por CFOP"
            )
            st.plotly_chart(fig, width='stretch')
            
            st.dataframe(cfop_analysis, width='stretch')
    
    elif analysis_type == "Análise de Impostos":
        st.subheader("💰 Análise de Impostos")
        
        impostos_cols = [col for col in df.columns if any(x in col for x in ['icms_v', 'pis_v', 'cofins_v'])]
        if impostos_cols:
            impostos_data = df[impostos_cols].sum()
            
            fig = px.bar(
                x=impostos_data.index,
                y=impostos_data.values,
                title="Total de Impostos",
                labels={'x': 'Tipo de Imposto', 'y': 'Valor (R$)'}
            )
            st.plotly_chart(fig, width='stretch')
    
    elif analysis_type == "Dados Completos":
        st.subheader("📋 Dados Completos")
        st.dataframe(df, width='stretch')
        
        # Informações sobre o DataFrame
        st.info(f"""
        **Informações do Dataset:**
        - Linhas: {len(df)}
        - Colunas: {len(df.columns)}
        - Memória: {df.memory_usage(deep=True).sum() / 1024 / 1024:.2f} MB
        """)


def show_about():
    """Mostra informações sobre o sistema"""
    st.header("ℹ️ Sobre o NFe Parser")
    
    st.markdown(f"""
    ### {settings.app_name}
    **Versão:** {settings.app_version}
    
    Sistema completo para análise de Notas Fiscais Eletrônicas (NF-e) com interface web moderna.
    
    #### 🚀 Funcionalidades
    
    - ✅ **Processamento Streaming**: Suporte a arquivos grandes
    - ✅ **Mapeamento Dinâmico**: 48+ campos configuráveis
    - ✅ **Visualizações Interativas**: Gráficos e dashboards
    - ✅ **Múltiplos Formatos**: Excel, CSV, JSON
    - ✅ **Análise em Tempo Real**: Processamento rápido
    
    #### 📊 Estatísticas do Mapeamento
    """)
    
    stats = mapper.get_statistics()
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total de Campos", stats['total_fields'])
    with col2:
        st.metric("Campos Obrigatórios", stats['required_fields'])
    with col3:
        st.metric("Grupos", len(stats['groups']))
    
    st.markdown("""
    #### 🛠️ Tecnologias
    
    - **Python 3.8+**
    - **Streamlit** - Interface web
    - **Pandas** - Manipulação de dados
    - **Plotly** - Visualizações interativas
    - **PyYAML** - Configurações
    
    #### 📚 Documentação
    
    Para mais informações, consulte:
    - README.md
    - analise_nfe_parser.md
    - plano_melhorias_nfe_parser.md
    """)


if __name__ == '__main__':
    main()

# Made with Bob
