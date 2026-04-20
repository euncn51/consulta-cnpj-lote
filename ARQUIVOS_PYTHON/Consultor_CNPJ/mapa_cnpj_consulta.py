import requests
import json

def get_type_name(value):
    """Retorna o nome do tipo do valor."""
    if value is None:
        return "null"
    elif isinstance(value, str):
        return "string"
    elif isinstance(value, bool):
        return "boolean"
    elif isinstance(value, int) or isinstance(value, float):
        return "number"
    elif isinstance(value, list):
        return "list"
    elif isinstance(value, dict):
        return "object"
    else:
        return type(value).__name__

def value_str(v):
    """Converte valores para string legível."""
    if v is None:
        return "null"
    return str(v)

def safe_get_inscricao_estadual(est, field):
    """Obtém campos de inscrições estaduais de forma segura."""
    inscricoes = est.get("inscricoes_estaduais", [])
    if inscricoes and len(inscricoes) > 0:
        return inscricoes[0].get(field)
    return None

def get_filtered_map(data):
    """Retorna apenas os campos filtrados no formato desejado."""
    est = data.get("estabelecimento", {})
    campos = [
        ("razao_social", data.get("razao_social")),
        ("estabelecimento.nome_fantasia", est.get("nome_fantasia")),
        ("estabelecimento.situacao_cadastral", est.get("situacao_cadastral")),
        ("estabelecimento.data_situacao_cadastral", est.get("data_situacao_cadastral")),
        ("estabelecimento.data_inicio_atividade", est.get("data_inicio_atividade")),
        ("estabelecimento.tipo_logradouro", est.get("tipo_logradouro")),
        ("estabelecimento.logradouro", est.get("logradouro")),
        ("estabelecimento.numero", est.get("numero")),
        ("estabelecimento.complemento", est.get("complemento")),
        ("estabelecimento.bairro", est.get("bairro")),
        ("estabelecimento.cep", est.get("cep")),
        ("estabelecimento.pais.id", est.get("pais", {}).get("id")),
        ("estabelecimento.pais.nome", est.get("pais", {}).get("nome")),
        ("estabelecimento.estado.nome", est.get("estado", {}).get("nome")),
        ("estabelecimento.estado.sigla", est.get("estado", {}).get("sigla")),
        ("estabelecimento.cidade.nome", est.get("cidade", {}).get("nome")),
        ("estabelecimento.cidade.ibge_id", est.get("cidade", {}).get("ibge_id")),
        ("estabelecimento.motivo_situacao_cadastral", est.get("motivo_situacao_cadastral")),
        ("estabelecimento.inscricoes_estaduais[0].inscricao_estadual", safe_get_inscricao_estadual(est, "inscricao_estadual")),
        ("estabelecimento.inscricoes_estaduais[0].ativo", safe_get_inscricao_estadual(est, "ativo")),
        ("estabelecimento.inscricoes_estaduais[0].atualizado_em", safe_get_inscricao_estadual(est, "atualizado_em")),
        ("estabelecimento.inscricoes_estaduais[0].estado.nome", safe_get_inscricao_estadual(est, {}).get("estado", {}).get("nome") if safe_get_inscricao_estadual(est, "estado") else None),
        ("estabelecimento.inscricoes_estaduais[0].estado.sigla", safe_get_inscricao_estadual(est, {}).get("estado", {}).get("sigla") if safe_get_inscricao_estadual(est, "estado") else None),
    ]

    linhas = []
    for chave, valor in campos:
        tipo = get_type_name(valor)
        linhas.append(f"{chave} ({tipo}): {value_str(valor)}")
    return linhas

def process_cnpj_filtered(cnpj):
    """Consulta a API e salva apenas o mapa filtrado."""
    cnpj_clean = ''.join(filter(str.isdigit, cnpj))
    url = f"https://publica.cnpj.ws/cnpj/{cnpj_clean}"

    try:
        print(f"\n🔍 Consultando CNPJ: {cnpj_clean}...")
        response = requests.get(url, headers={"Accept": "application/json"}, timeout=10)

        if response.status_code == 200:
            data = response.json()
            linhas = get_filtered_map(data)

            filename = f"empresa_{cnpj_clean}_mapa_filtrado.txt"
            with open(filename, "w", encoding="utf-8") as f:
                for linha in linhas:
                    f.write(linha + "\n")
            print(f"✅ Mapa filtrado salvo em: {filename}")

            # Também imprime no terminal
            print("\n=== MAPA FILTRADO ===")
            for linha in linhas:
                print(linha)

        elif response.status_code == 404:
            print("❌ CNPJ não encontrado.")
        else:
            print(f"❌ Erro na requisição: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"❌ Erro de conexão: {e}")
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")

if __name__ == "__main__":
    # Exemplo com o CNPJ desejado
    process_cnpj_filtered("00589841000186")