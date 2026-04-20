"""
Módulo para monitoramento e verificação do status das APIs
Versão 2.0 - Sistema de Health Check integrado
"""

import requests
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import threading
from queue import Queue
import json

class APIStatusMonitor:
    """
    Monitor de status das APIs com cache e verificação periódica
    """
    
    def __init__(self):
        self.api_status = {
            'cnpj': {
                'status': 'unknown',
                'last_check': None,
                'response_time': 0,
                'error_count': 0,
                'url': 'https://open.cnpja.com/office/00000000000191'
            },
            'ibge': {
                'status': 'unknown', 
                'last_check': None,
                'response_time': 0,
                'error_count': 0,
                'url': 'https://servicodados.ibge.gov.br/api/v1/localidades/estados/SP/municipios'
            }
        }
        self.check_interval = 300  # 5 minutos entre verificações
        self.timeout = 10
        self.last_check_time = None
        self.is_checking = False
        
    def check_api_status(self, api_type: str) -> Tuple[bool, float]:
        """
        Verifica o status de uma API específica
        
        Args:
            api_type: 'cnpj' ou 'ibge'
            
        Returns:
            Tuple[bool, float]: (status, tempo_resposta)
        """
        if api_type not in self.api_status:
            return False, 0
            
        api_config = self.api_status[api_type]
        
        try:
            start_time = time.time()
            
            if api_type == 'cnpj':
                # Para CNPJ, aceitamos 200, 404, 429 como "online"
                response = requests.get(api_config['url'], timeout=self.timeout)
                is_online = response.status_code in [200, 404, 429]
            else:
                # Para IBGE, só 200 é considerado online
                response = requests.get(api_config['url'], timeout=self.timeout)
                is_online = response.status_code == 200
                
            response_time = (time.time() - start_time) * 1000  # ms
            
            return is_online, response_time
            
        except (requests.exceptions.RequestException, Exception):
            return False, 0
    
    def check_all_apis(self) -> Dict[str, Dict]:
        """
        Verifica o status de todas as APIs
        
        Returns:
            Dict com status atualizado
        """
        self.is_checking = True
        results = {}
        
        for api_type in self.api_status:
            status, response_time = self.check_api_status(api_type)
            
            self.api_status[api_type]['status'] = 'online' if status else 'offline'
            self.api_status[api_type]['last_check'] = datetime.now()
            self.api_status[api_type]['response_time'] = response_time
            
            if not status:
                self.api_status[api_type]['error_count'] += 1
            else:
                self.api_status[api_type]['error_count'] = 0
                
            results[api_type] = self.api_status[api_type].copy()
        
        self.last_check_time = datetime.now()
        self.is_checking = False
        return results
    
    def get_status(self) -> Dict[str, Dict]:
        """
        Retorna o status atual das APIs
        """
        # Se nunca verificou ou precisa verificar novamente
        if (not self.last_check_time or 
            datetime.now() - self.last_check_time > timedelta(seconds=self.check_interval)):
            return self.check_all_apis()
        return self.api_status
    
    def get_api_status_emoji(self, api_type: str) -> str:
        """
        Retorna emoji representando o status da API
        """
        status = self.api_status.get(api_type, {}).get('status', 'unknown')
        if status == 'online':
            return '✅'
        elif status == 'offline':
            return '❌'
        else:
            return '❓'
    
    def get_api_status_text(self, api_type: str) -> str:
        """
        Retorna texto descritivo do status
        """
        api_data = self.api_status.get(api_type, {})
        status = api_data.get('status', 'unknown')
        last_check = api_data.get('last_check')
        response_time = api_data.get('response_time', 0)
        
        if status == 'online':
            return f"Online ({response_time:.0f}ms)"
        elif status == 'offline':
            if last_check:
                return f"Offline - Última verificação: {last_check.strftime('%H:%M:%S')}"
            return "Offline"
        else:
            return "Status desconhecido"

class BackgroundStatusChecker:
    """
    Verificador de status em background
    """
    
    def __init__(self, status_monitor: APIStatusMonitor, update_callback=None):
        self.monitor = status_monitor
        self.update_callback = update_callback
        self.running = False
        self.thread = None
        
    def start(self):
        """Inicia a verificação em background"""
        if self.running:
            return
            
        self.running = True
        self.thread = threading.Thread(target=self._check_loop, daemon=True)
        self.thread.start()
    
    def stop(self):
        """Para a verificação"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=2)
    
    def _check_loop(self):
        """Loop de verificação em background"""
        while self.running:
            try:
                results = self.monitor.check_all_apis()
                if self.update_callback:
                    self.update_callback(results)
            except Exception as e:
                print(f"Erro na verificação de status: {e}")
            
            # Espera 5 minutos entre verificações
            for _ in range(300):  # 300 segundos = 5 minutos
                if not self.running:
                    break
                time.sleep(1)