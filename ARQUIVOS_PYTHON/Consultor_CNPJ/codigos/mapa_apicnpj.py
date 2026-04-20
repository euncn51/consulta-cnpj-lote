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
    print(f"\nCNPJ: {data.get('taxId')}")
    print(f"Nome Fantasia: {data.get('alias', 'N/A')}")
    print(f"Data de Fundação: {format_date(data.get('founded'))}")
    print(f"É matriz: {'Sim' if data.get('head') else 'Não'}")
    print(f"Situação: {data.get('status', {}).get('text', 'N/A')}")
    print(f"Data da Situação: {format_date(data.get('statusDate'))}")
    print(f"Última Atualização: {data.get('updated', 'N/A')}")
    
    # Dados da empresa matriz
    company = data.get('company', {})
    print("\n" + "-"*50)
    print(f"{'EMPRESA MATRIZ':^50}")
    print("-"*50)
    print(f"Nome: {company.get('name', 'N/A')}")
    print(f"ID: {company.get('id', 'N/A')}")
    print(f"Natureza Jurídica: {company.get('nature', {}).get('text', 'N/A')}")
    print(f"Porte: {company.get('size', {}).get('text', 'N/A')}")
    print(f"Capital Social: R$ {company.get('equity', 0):,.2f}")
    print(f"Optante pelo Simples: {'Sim' if company.get('simples', {}).get('optant') else 'Não'}")
    print(f"Optante pelo SIMPLES: {'Sim' if company.get('simei', {}).get('optant') else 'Não'}")
    
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
    print(f"País: {address.get('country', {}).get('name', 'N/A')}")
    
    # Atividades
    print("\n" + "-"*50)
    print(f"{'ATIVIDADES':^50}")
    print("-"*50)
    print(f"Principal: {data.get('mainActivity', {}).get('text', 'N/A')}")
    
    side_activities = data.get('sideActivities', [])
    if side_activities:
        print("\nAtividades Secundárias:")
        for activity in side_activities:
            print(f"- {activity.get('text', 'N/A')}")
    
    # Contatos
    print("\n" + "-"*50)
    print(f"{'CONTATOS':^50}")
    print("-"*50)
    
    phones = data.get('phones', [])
    if phones:
        print("Telefones:")
        for phone in phones:
            print(f"- ({phone.get('area')}) {phone.get('number')} ({phone.get('type')})")
    
    emails = data.get('emails', [])
    if emails:
        print("\nEmails:")
        for email in emails:
            print(f"- {email.get('address')} ({email.get('ownership')})")
    
    # Membros/Diretores
    members = company.get('members', [])
    if members:
        print("\n" + "-"*50)
        print(f"{'DIRETORES/SÓCIOS':^50}")
        print("-"*50)
        for member in members:
            person = member.get('person', {})
            print(f"\nNome: {person.get('name', 'N/A')}")
            print(f"CPF: {person.get('taxId', 'N/A')}")
            print(f"Tipo: {person.get('type', 'N/A')}")
            print(f"Faixa Etária: {person.get('age', 'N/A')}")
            print(f"Cargo: {member.get('role', {}).get('text', 'N/A')}")
            print(f"Desde: {format_date(member.get('since'))}")
    
    # Inscrições Estaduais
    registrations = data.get('registrations', [])
    if registrations:
        print("\n" + "-"*50)
        print(f"{'INSCRIÇÕES ESTADUAIS':^50}")
        print("-"*50)
        for reg in registrations:
            print(f"\nNúmero: {reg.get('number')}")
            print(f"Estado: {reg.get('state')}")
            print(f"Tipo: {reg.get('type', {}).get('text', 'N/A')}")
            print(f"Situação: {reg.get('status', {}).get('text', 'N/A')}")
            print(f"Data Situação: {format_date(reg.get('statusDate'))}")
            print(f"Ativa: {'Sim' if reg.get('enabled') else 'Não'}")
    
    # SUFRAMA
    suframa = data.get('suframa', [])
    if suframa:
        print("\n" + "-"*50)
        print(f"{'SUFRAMA':^50}")
        print("-"*50)
        for suf in suframa:
            print(f"\nNúmero: {suf.get('number')}")
            print(f"Desde: {format_date(suf.get('since'))}")
            print(f"Aprovado: {'Sim' if suf.get('approved') else 'Não'}")
            print(f"Data Aprovação: {format_date(suf.get('approvalDate'))}")
            print(f"Situação: {suf.get('status', {}).get('text', 'N/A')}")
            
            incentives = suf.get('incentives', [])
            if incentives:
                print("\nIncentivos Fiscais:")
                for inc in incentives:
                    print(f"- {inc.get('tribute')}: {inc.get('benefit')}")
                    print(f"  Finalidade: {inc.get('purpose')}")
                    print(f"  Base Legal: {inc.get('basis')}")

def get_company_data(cnpj):
    url = f"https://open.cnpja.com/office/{cnpj}"
    
    headers = {
        "Accept": "application/json",
        # "Authorization": "Bearer SEU_TOKEN_AQUI"  # Descomente se necessário
    }
    
    try:
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            display_company_data(data)
            
            # Salvar em arquivo JSON
            with open(f'empresa_{cnpj}.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"\nDados completos salvos em 'empresa_{cnpj}.json'")
        else:
            print(f"Erro na requisição: {response.status_code}")
            print(response.text)
    
    except requests.exceptions.RequestException as e:
        print(f"Erro de conexão: {e}")
    except json.JSONDecodeError as e:
        print(f"Erro ao decodificar JSON: {e}")

if __name__ == "__main__":
    cnpj = "04918912000106"  # CNPJ 
    get_company_data(cnpj)