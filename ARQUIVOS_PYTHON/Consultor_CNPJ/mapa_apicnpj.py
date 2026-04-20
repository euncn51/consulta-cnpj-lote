import requests
import json
from datetime import datetime

def format_date(date_str):
    if not date_str:
        return "N/A"
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        return date_obj.strftime("%d/%m/%Y")
    except:
        return date_str

def display_company_data(data):
    print("\n" + "="*50)
    print(f"{'DADOS DA EMPRESA':^50}")
    print("="*50)
    
    # Informações básicas
    print(f"\nCNPJ: {data.get('cnpj')}")
    print(f"Nome Fantasia: {data.get('alias', 'N/A')}")
    print(f"Razão Social: {data.get('name', 'N/A')}")
    print(f"Data de Abertura: {format_date(data.get('opened'))}")
    print(f"Situação: {data.get('status', {}).get('text', 'N/A')}")
    print(f"Data da Situação: {format_date(data.get('statusDate'))}")
    print(f"Última Atualização: {format_date(data.get('updated'))}")
    
    # Natureza Jurídica e Porte
    print(f"\nNatureza Jurídica: {data.get('nature', {}).get('text', 'N/A')}")
    print(f"Porte: {data.get('size', {}).get('text', 'N/A')}")
    print(f"Capital Social: R$ {data.get('equity', 0):,.2f}")
    
    # Regimes tributários
    simples = data.get('simples', {})
    print(f"\nOptante pelo Simples Nacional: {'Sim' if simples.get('optant') else 'Não'}")
    if simples.get('optant'):
        print(f"Data de Opção: {format_date(simples.get('since'))}")
    
    # Endereço
    address = data.get('address', {})
    print("\n" + "-"*50)
    print(f"{'ENDEREÇO':^50}")
    print("-"*50)
    print(f"Logradouro: {address.get('street', 'N/A')}, {address.get('number', 'N/A')}")
    print(f"Complemento: {address.get('details', 'N/A')}")
    print(f"Bairro: {address.get('district', 'N/A')}")
    print(f"Cidade: {address.get('city', 'N/A')} - {address.get('state', 'N/A')}")
    print(f"CEP: {address.get('zip', 'N/A')}")
    
    # Contatos
    print("\n" + "-"*50)
    print(f"{'CONTATOS':^50}")
    print("-"*50)
    
    phones = data.get('phones', [])
    if phones:
        print("Telefones:")
        for phone in phones:
            print(f"- ({phone.get('area')}) {phone.get('number')}")
    
    emails = data.get('emails', [])
    if emails:
        print("\nEmails:")
        for email in emails:
            print(f"- {email}")
    
    # Atividades Econômicas
    print("\n" + "-"*50)
    print(f"{'ATIVIDADES ECONÔMICAS':^50}")
    print("-"*50)
    
    primary_activity = data.get('primaryActivity', {})
    if primary_activity:
        print(f"Atividade Principal:")
        print(f"Código: {primary_activity.get('code')}")
        print(f"Descrição: {primary_activity.get('text')}")
    
    secondary_activities = data.get('secondaryActivities', [])
    if secondary_activities:
        print(f"\nAtividades Secundárias ({len(secondary_activities)}):")
        for i, activity in enumerate(secondary_activities, 1):
            print(f"{i}. Código: {activity.get('code')} - {activity.get('text')}")
    
    # Sócios/Quadro Societário
    print("\n" + "-"*50)
    print(f"{'QUADRO SOCIETÁRIO':^50}")
    print("-"*50)
    
    partners = data.get('partners', [])
    if partners:
        for partner in partners:
            print(f"\nNome: {partner.get('name', 'N/A')}")
            print(f"Tipo: {partner.get('type', 'N/A')}")
            if partner.get('taxId'):
                print(f"CPF/CNPJ: {partner.get('taxId')}")
            print(f"Participação: {partner.get('stake', 'N/A')}%")
            print(f"Data de Entrada: {format_date(partner.get('since'))}")
    else:
        print("Nenhum sócio encontrado ou informação não disponível")

def get_company_data(cnpj):
    # Remove caracteres não numéricos do CNPJ
    cnpj_clean = ''.join(filter(str.isdigit, cnpj))
    
    # URL correta da API CNPJA
    url = f"https://api.cnpja.com/office/{cnpj_clean}"
    
    headers = {
        "Accept": "application/json",
        # "Authorization": "SEU_TOKEN_AQUI"  # Descomente se tiver token
    }
    
    try:
        print(f"Consultando CNPJ: {cnpj_clean}")
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            display_company_data(data)
            
            # Salvar em arquivo JSON
            filename = f'empresa_{cnpj_clean}.json'
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"\nDados completos salvos em '{filename}'")
            
        elif response.status_code == 404:
            print("CNPJ não encontrado na base de dados")
        elif response.status_code == 401:
            print("Erro de autenticação. Token inválido ou não fornecido.")
        elif response.status_code == 429:
            print("Limite de requisições excedido. Tente novamente mais tarde.")
        else:
            print(f"Erro na requisição: {response.status_code}")
            print(f"Resposta: {response.text}")
    
    except requests.exceptions.RequestException as e:
        print(f"Erro de conexão: {e}")
    except json.JSONDecodeError as e:
        print(f"Erro ao decodificar JSON: {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")

if __name__ == "__main__":
    # CNPJ de exemplo (substitua por um CNPJ válido)
    cnpj = "04954351000192"  
    
    # Ou para usar input do usuário:
    # cnpj = input("Digite o CNPJ: ").strip()
    
    get_company_data(cnpj)
    