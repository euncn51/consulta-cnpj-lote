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

def explore_json(data, prefix="", output_lines=None):
    """Percorre o JSON e armazena todas as chaves, valores e tipos."""
    if isinstance(data, dict):
        for key, value in data.items():
            new_prefix = f"{prefix}.{key}" if prefix else key
            explore_json(value, new_prefix, output_lines)
    elif isinstance(data, list):
        for idx, item in enumerate(data):
            new_prefix = f"{prefix}[{idx}]"
            explore_json(item, new_prefix, output_lines)
    else:
        line = f"{prefix} ({get_type_name(data)}): {value_str(data)}"
        output_lines.append(line)

def get_company_data(cnpj):
    """Consulta a API publica.cnpj.ws, salva JSON e mapa de campos com tipos."""
    cnpj_clean = ''.join(filter(str.isdigit, cnpj))
    url = f"https://publica.cnpj.ws/cnpj/{cnpj_clean}"

    try:
        print(f"Consultando CNPJ: {cnpj_clean}...")
        response = requests.get(url, headers={"Accept": "application/json"}, timeout=10)

        if response.status_code == 200:
            data = response.json()

            # 📂 Salva JSON bruto formatado
            json_filename = f"empresa_{cnpj_clean}.json"
            with open(json_filename, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            print(f"✅ JSON salvo em: {json_filename}")

            # 📂 Gera e salva o mapa de campos com tipos
            mapa_linhas = []
            explore_json(data, output_lines=mapa_linhas)

            mapa_filename = f"empresa_{cnpj_clean}_mapa.txt"
            with open(mapa_filename, "w", encoding="utf-8") as f:
                for linha in mapa_linhas:
                    f.write(linha + "\n")
            print(f"✅ Mapa de campos salvo em: {mapa_filename}")

            # 🖥️ Mostra no terminal
            print("\n=== MAPA DE CAMPOS COM TIPOS ===")
            for linha in mapa_linhas:
                print(linha)

        elif response.status_code == 404:
            print("❌ CNPJ não encontrado na base de dados.")
        else:
            print(f"❌ Erro na requisição: {response.status_code}")
            print(response.text)

    except requests.exceptions.RequestException as e:
        print(f"❌ Erro de conexão: {e}")

if __name__ == "__main__":
    # 🔹 CNPJ de exemplo
    get_company_data("04954351000192")
