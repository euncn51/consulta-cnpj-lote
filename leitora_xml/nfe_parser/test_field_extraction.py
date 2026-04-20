"""
Script de Teste - Validação de Extração de Campos
Compara campos extraídos pelo streaming_parser.py com leito_nfe_xml_v7.py
"""

import sys
from pathlib import Path

# Adicionar diretório ao path
sys.path.insert(0, str(Path(__file__).parent))

from src.core.streaming_parser import StreamingNFeParser
from leito_nfe_xml_v7 import NFeParser
import pandas as pd


def compare_parsers(xml_file_path: str):
    """
    Compara resultados dos dois parsers
    
    Args:
        xml_file_path: Caminho do arquivo XML de teste
    """
    print("=" * 80)
    print("TESTE DE VALIDAÇÃO DE CAMPOS - NFe Parser")
    print("=" * 80)
    print()
    
    # Parser Original
    print("1️⃣  Executando Parser Original (leito_nfe_xml_v7.py)...")
    original_parser = NFeParser()
    
    with open(xml_file_path, 'r', encoding='utf-8') as f:
        xml_content = f.read()
    
    original_data = original_parser.parse_nfe_xml(xml_content)
    original_fields = set()
    
    if original_data:
        original_fields = set(original_data[0].keys())
        print(f"   ✓ Campos extraídos: {len(original_fields)}")
        print(f"   ✓ Itens processados: {len(original_data)}")
    else:
        print("   ✗ Nenhum dado extraído!")
        return
    
    print()
    
    # Parser Streaming
    print("2️⃣  Executando Parser Streaming (streaming_parser.py)...")
    streaming_parser = StreamingNFeParser()
    streaming_data = streaming_parser.parse_xml_stream(xml_file_path)
    streaming_fields = set()
    
    if streaming_data:
        streaming_fields = set(streaming_data[0].keys())
        print(f"   ✓ Campos extraídos: {len(streaming_fields)}")
        print(f"   ✓ Itens processados: {len(streaming_data)}")
    else:
        print("   ✗ Nenhum dado extraído!")
        return
    
    print()
    print("=" * 80)
    print("ANÁLISE COMPARATIVA")
    print("=" * 80)
    print()
    
    # Campos em comum
    common_fields = original_fields & streaming_fields
    print(f"✓ Campos em comum: {len(common_fields)}")
    
    # Campos faltantes no streaming
    missing_in_streaming = original_fields - streaming_fields
    if missing_in_streaming:
        print(f"\n⚠️  Campos FALTANTES no Streaming Parser: {len(missing_in_streaming)}")
        print("   Campos:")
        for field in sorted(missing_in_streaming):
            print(f"   - {field}")
    else:
        print("\n✓ Todos os campos do parser original estão presentes!")
    
    # Campos extras no streaming
    extra_in_streaming = streaming_fields - original_fields
    if extra_in_streaming:
        print(f"\n➕ Campos EXTRAS no Streaming Parser: {len(extra_in_streaming)}")
        print("   Campos:")
        for field in sorted(extra_in_streaming):
            print(f"   - {field}")
    
    print()
    print("=" * 80)
    print("GRUPOS DE CAMPOS")
    print("=" * 80)
    print()
    
    # Análise por grupos
    grupos = {
        'Identificação': ['Id', 'versao_nfe', 'cUF', 'cNF', 'natOp', 'mod', 'serie', 'nNF', 'dhEmi'],
        'Emitente': ['emit_CNPJ', 'emit_xNome', 'emit_IE', 'emit_xFant', 'emit_CRT'],
        'Destinatário': ['dest_CNPJ', 'dest_CPF', 'dest_xNome', 'dest_IE'],
        'Produto': ['cProd', 'xProd', 'NCM', 'CFOP', 'uCom', 'qCom', 'vUnCom', 'vProd', 'uTrib', 'qTrib', 'vUnTrib'],
        'ICMS': [f for f in streaming_fields if 'ICMS_' in f],
        'PIS': ['PIS_CST', 'PIS_vBC', 'PIS_pPIS', 'PIS_vPIS'],
        'COFINS': ['COFINS_CST', 'COFINS_vBC', 'COFINS_pCOFINS', 'COFINS_vCOFINS'],
        'IBS/CBS': [f for f in streaming_fields if 'ibscbs_' in f],
        'gTribRegular': [f for f in streaming_fields if 'gTribRegular_' in f],
        'Totais': [f for f in streaming_fields if 'total_' in f],
        'Transporte': ['transp_modFrete', 'transp_transporta_xNome', 'transp_transporta_IE'],
        'Pagamento': ['pag_detPag_tPag', 'pag_detPag_vPag']
    }
    
    for grupo, campos_esperados in grupos.items():
        campos_presentes = [c for c in campos_esperados if c in streaming_fields]
        if isinstance(campos_esperados, list) and campos_esperados and isinstance(campos_esperados[0], str):
            total = len(campos_esperados)
            presentes = len(campos_presentes)
            percentual = (presentes / total * 100) if total > 0 else 0
            
            status = "✓" if presentes == total else "⚠️"
            print(f"{status} {grupo}: {presentes}/{total} campos ({percentual:.0f}%)")
    
    print()
    print("=" * 80)
    print("RESUMO FINAL")
    print("=" * 80)
    print()
    
    cobertura = (len(common_fields) / len(original_fields) * 100) if original_fields else 0
    print(f"📊 Cobertura de Campos: {cobertura:.1f}%")
    print(f"📈 Total de Campos Originais: {len(original_fields)}")
    print(f"📈 Total de Campos Streaming: {len(streaming_fields)}")
    print(f"✓ Campos Implementados: {len(common_fields)}")
    
    if missing_in_streaming:
        print(f"⚠️  Campos Faltantes: {len(missing_in_streaming)}")
    else:
        print("✅ TODOS OS CAMPOS IMPLEMENTADOS COM SUCESSO!")
    
    print()
    
    # Salvar relatório
    print("💾 Salvando relatório detalhado...")
    
    relatorio = {
        'Campo': [],
        'Original': [],
        'Streaming': [],
        'Status': []
    }
    
    all_fields = original_fields | streaming_fields
    for field in sorted(all_fields):
        relatorio['Campo'].append(field)
        relatorio['Original'].append('✓' if field in original_fields else '✗')
        relatorio['Streaming'].append('✓' if field in streaming_fields else '✗')
        
        if field in common_fields:
            relatorio['Status'].append('OK')
        elif field in missing_in_streaming:
            relatorio['Status'].append('FALTANTE')
        else:
            relatorio['Status'].append('EXTRA')
    
    df_relatorio = pd.DataFrame(relatorio)
    df_relatorio.to_excel('relatorio_campos.xlsx', index=False)
    print("   ✓ Relatório salvo: relatorio_campos.xlsx")
    
    print()
    print("=" * 80)


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("Uso: python test_field_extraction.py <caminho_xml>")
        print()
        print("Exemplo:")
        print("  python test_field_extraction.py nota_fiscal.xml")
        sys.exit(1)
    
    xml_file = sys.argv[1]
    
    if not Path(xml_file).exists():
        print(f"❌ Erro: Arquivo não encontrado: {xml_file}")
        sys.exit(1)
    
    try:
        compare_parsers(xml_file)
    except Exception as e:
        print(f"❌ Erro durante o teste: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

# Made with Bob
