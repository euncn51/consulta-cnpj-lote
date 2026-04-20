#!/usr/bin/env python3
"""
Script para testar o status da API Open CNPJ e API do IBGE
"""

import requests
import time
from datetime import datetime
import sys

def test_api_cnpj():
    """Testa o status da API Open CNPJ"""
    
    # Configurações
    base_url = "https://open.cnpja.com/office/"
    timeout = 10
    test_cnpj = "04954351000192"  # CNPJ da União (sempre existe)
    
    print("🔍 Testando status da API Open CNPJ...")
    print(f"📋 URL base: {base_url}")
    print(f"⏱️  Timeout: {timeout}s")
    print("-" * 50)
    
    # Cria sessão
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json'
    })
    
    # Teste 1: Requisição HEAD (mais rápida)
    print("1. Testando requisição HEAD...")
    try:
        start_time = time.time()
        response = session.head(base_url, timeout=5)
        end_time = time.time()
        
        print(f"   ✅ Status: {response.status_code}")
        print(f"   ⚡ Tempo resposta: {(end_time - start_time)*1000:.2f}ms")
        
    except requests.exceptions.Timeout:
        print("   ❌ TIMEOUT - API não respondeu em 5 segundos")
        return False
    except requests.exceptions.ConnectionError as e:
        print(f"   ❌ ERRO DE CONEXÃO: {e}")
        return False
    except Exception as e:
        print(f"   ⚠️  ERRO: {e}")
    
    # Teste 2: Consulta real de CNPJ
    print("\n2. Testando consulta de CNPJ...")
    try:
        start_time = time.time()
        response = session.get(base_url + test_cnpj, timeout=timeout)
        end_time = time.time()
        
        print(f"   ✅ Status: {response.status_code}")
        print(f"   ⚡ Tempo resposta: {(end_time - start_time)*1000:.2f}ms")
        
        if response.status_code == 200:
            print("   🎉 CONSULTA BEM-SUCEDIDA!")
            data = response.json()
            print(f"   📛 Razão Social: {data.get('company', {}).get('name', 'N/A')}")
            return True
        elif response.status_code == 404:
            print("   ❌ CNPJ não encontrado (mas API respondeu)")
            return True
        elif response.status_code == 429:
            print("   ⚠️  RATE LIMIT - Muitas requisições")
            return True
        else:
            print(f"   ❌ Status inesperado: {response.status_code}")
            return False
            
    except requests.exceptions.Timeout:
        print("   ❌ TIMEOUT - Consulta não completou em 10 segundos")
        return False
    except requests.exceptions.ConnectionError as e:
        print(f"   ❌ ERRO DE CONEXÃO: {e}")
        return False
    except requests.exceptions.JSONDecodeError:
        print("   ❌ ERRO - Resposta não é JSON válido")
        return False
    except Exception as e:
        print(f"   ⚠️  ERRO INESPERADO: {e}")
        return False

def test_api_ibge():
    """Testa o status da API do IBGE"""
    
    print("\n" + "="*60)
    print("🌎 Testando status da API do IBGE...")
    print(f"📋 URL base: https://servicodados.ibge.gov.br/api/v1/localidades/estados/SP/municipios")
    print("-" * 60)
    
    # Teste com estado SP (São Paulo)
    ibge_url = "https://servicodados.ibge.gov.br/api/v1/localidades/estados/SP/municipios"
    
    try:
        start_time = time.time()
        response = requests.get(ibge_url, timeout=10)
        end_time = time.time()
        
        response_time = (end_time - start_time) * 1000
        print(f"   ✅ Status: {response.status_code}")
        print(f"   ⚡ Tempo resposta: {response_time:.2f}ms")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   🎯 Municípios retornados: {len(data)}")
            if data:
                print(f"   📍 Exemplo: {data[0]['nome']} (ID: {data[0]['id']})")
            return True
        else:
            print(f"   ❌ Status inesperado: {response.status_code}")
            return False
            
    except requests.exceptions.Timeout:
        print("   ❌ TIMEOUT - API do IBGE não respondeu em 10 segundos")
        return False
    except requests.exceptions.ConnectionError as e:
        print(f"   ❌ ERRO DE CONEXÃO: {e}")
        return False
    except requests.exceptions.JSONDecodeError:
        print("   ❌ ERRO - Resposta não é JSON válido")
        return False
    except Exception as e:
        print(f"   ⚠️  ERRO INESPERADO: {e}")
        return False

def test_ibge_multiple_states():
    """Testa a API do IBGE com múltiplos estados"""
    
    print("\n" + "="*60)
    print("🧪 Testando API do IBGE com diferentes estados...")
    print("-" * 60)
    
    estados = ["SP", "RJ", "MG", "RS"]  # Alguns estados para teste
    results = {}
    
    for uf in estados:
        ibge_url = f"https://servicodados.ibge.gov.br/api/v1/localidades/estados/{uf}/municipios"
        
        try:
            start_time = time.time()
            response = requests.get(ibge_url, timeout=8)
            end_time = time.time()
            
            response_time = (end_time - start_time) * 1000
            
            if response.status_code == 200:
                data = response.json()
                results[uf] = {
                    "status": "✅ ONLINE",
                    "time": f"{response_time:.0f}ms",
                    "municipios": len(data)
                }
                print(f"   {uf}: ✅ {len(data)} municípios ({response_time:.0f}ms)")
            else:
                results[uf] = {
                    "status": f"❌ ERRO {response.status_code}",
                    "time": f"{response_time:.0f}ms",
                    "municipios": 0
                }
                print(f"   {uf}: ❌ Erro {response.status_code}")
                
        except Exception as e:
            results[uf] = {
                "status": f"❌ EXCEÇÃO",
                "time": "N/A",
                "municipios": 0
            }
            print(f"   {uf}: ❌ Exceção: {str(e)[:50]}...")
    
    return results

def detailed_api_test():
    """Teste detalhado das APIs"""
    
    endpoints_to_test = [
        {"name": "API CNPJ - URL Base", "url": "https://open.cnpja.com/office/", "method": "HEAD"},
        {"name": "API CNPJ - CNPJ Válido", "url": "https://open.cnpja.com/office/00000000000191", "method": "GET"},
        {"name": "API IBGE - SP", "url": "https://servicodados.ibge.gov.br/api/v1/localidades/estados/SP/municipios", "method": "GET"},
        {"name": "API IBGE - RJ", "url": "https://servicodados.ibge.gov.br/api/v1/localidades/estados/RJ/municipios", "method": "GET"},
    ]
    
    print("🔍 TESTE DETALHADO DAS APIS")
    print("=" * 60)
    
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'API-Tester/1.0',
        'Accept': 'application/json'
    })
    
    all_ok = True
    results = {}
    
    for endpoint in endpoints_to_test:
        print(f"\n📡 Testando: {endpoint['name']}")
        print(f"   🌐 URL: {endpoint['url']}")
        print(f"   📤 Método: {endpoint['method']}")
        
        try:
            start_time = time.time()
            
            if endpoint['method'] == 'HEAD':
                response = session.head(endpoint['url'], timeout=8)
            else:
                response = session.get(endpoint['url'], timeout=8)
                
            end_time = time.time()
            
            response_time = (end_time - start_time) * 1000
            
            # Critérios de sucesso diferentes para cada API
            if "CNPJ" in endpoint['name']:
                is_success = response.status_code in [200, 404, 429, 400]
            else:  # API IBGE
                is_success = response.status_code == 200
                
            status_emoji = "✅" if is_success else "❌"
            
            print(f"   {status_emoji} Status: {response.status_code}")
            print(f"   ⚡ Tempo: {response_time:.2f}ms")
            
            if "GET" in endpoint['method'] and response.status_code == 200:
                try:
                    data = response.json()
                    if "IBGE" in endpoint['name']:
                        print(f"   📊 Municípios: {len(data)}")
                    elif "CNPJ" in endpoint['name']:
                        company_name = data.get('company', {}).get('name', 'N/A')
                        print(f"   📛 Empresa: {company_name}")
                except:
                    print(f"   📊 Dados: {len(response.content)} bytes")
            
            if not is_success:
                all_ok = False
                print(f"   💀 ERRO: Status inesperado")
                
            # Guarda resultado
            results[endpoint['name']] = {
                "status": response.status_code,
                "time": response_time,
                "success": is_success
            }
                
        except requests.exceptions.Timeout:
            print("   ❌ TIMEOUT - Não respondeu em 8 segundos")
            all_ok = False
            results[endpoint['name']] = {"status": "TIMEOUT", "time": None, "success": False}
        except requests.exceptions.ConnectionError as e:
            print(f"   ❌ CONEXÃO RECUSADA: {e}")
            all_ok = False
            results[endpoint['name']] = {"status": "CONNECTION_ERROR", "time": None, "success": False}
        except Exception as e:
            print(f"   ⚠️  ERRO: {e}")
            all_ok = False
            results[endpoint['name']] = {"status": "EXCEPTION", "time": None, "success": False}
    
    return all_ok, results

def main():
    """Função principal"""
    print("🤖 TESTADOR DAS APIS (CNPJ + IBGE)")
    print("=" * 50)
    print(f"⏰ Início: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print()
    
    # Opções de teste
    if len(sys.argv) > 1:
        test_type = sys.argv[1].lower()
    else:
        test_type = "quick"
    
    success = True
    
    if test_type == "detailed":
        success, results = detailed_api_test()
    elif test_type == "ibge":
        success = test_api_ibge()
        success = success and test_ibge_multiple_states()
    elif test_type == "full":
        success = test_api_cnpj()
        success = success and test_api_ibge()
    else:
        success = test_api_cnpj()
        success = success and test_api_ibge()
    
    print("\n" + "=" * 60)
    print("📊 RESULTADO FINAL:")
    
    if success:
        print("🎉 TODAS AS APIS ESTÃO FUNCIONANDO CORRETAMENTE!")
        print("\n💡 APIs testadas:")
        print("   • ✅ API Open CNPJ")
        print("   • ✅ API IBGE (Serviço de Dados)")
    else:
        print("❌ ALGUMA API ESTÁ COM PROBLEMAS!")
        print("\n💡 Possíveis soluções:")
        print("   • Verifique sua conexão com a internet")
        print("   • As APIs podem estar temporariamente offline")
        print("   • Verifique se há bloqueio de firewall/proxy")
        print("   • Tente novamente em alguns minutos")
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()