"""
Parser de NF-e com Processamento Streaming

Implementa parsing incremental de XMLs usando iterparse para economizar memória
e permitir processamento de arquivos muito grandes.
"""

import xml.etree.ElementTree as ET
from typing import Dict, List, Optional, Callable, Any
from pathlib import Path
import sys
import os

# Adicionar diretório pai ao path para imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.utils.logger import get_logger


class StreamingNFeParser:
    """
    Parser de NF-e com processamento streaming
    
    Usa xml.etree.ElementTree.iterparse() para processar XMLs incrementalmente,
    liberando memória após processar cada elemento. Ideal para arquivos grandes.
    
    Características:
    - Baixo uso de memória (processa elementos incrementalmente)
    - Suporta arquivos de qualquer tamanho
    - Callbacks para progresso em tempo real
    - Logging detalhado de cada etapa
    """
    
    def __init__(self):
        """Inicializa o parser streaming"""
        self.logger = get_logger('streaming_parser')
        self.namespaces = {
            'nfe': 'http://www.portalfiscal.inf.br/nfe',
            'ds': 'http://www.w3.org/2000/09/xmldsig#'
        }
        self.logger.info("StreamingNFeParser inicializado")
    
    def find_element(self, parent, tag_name: str):
        """
        Busca elemento com namespace
        
        Args:
            parent: Elemento pai
            tag_name: Nome da tag a buscar
            
        Returns:
            Elemento encontrado ou None
        """
        if parent is None:
            return None
        elem = parent.find(f'nfe:{tag_name}', self.namespaces)
        if elem is None:
            elem = parent.find(tag_name)
        return elem
    
    def find_element_text(self, parent, tag_name: str) -> Optional[str]:
        """
        Busca texto do elemento
        
        Args:
            parent: Elemento pai
            tag_name: Nome da tag
            
        Returns:
            Texto do elemento ou None
        """
        elem = self.find_element(parent, tag_name)
        return elem.text if elem is not None else None
    
    def find_all_elements(self, parent, tag_name: str) -> List:
        """
        Busca todos os elementos
        
        Args:
            parent: Elemento pai
            tag_name: Nome da tag
            
        Returns:
            Lista de elementos encontrados
        """
        if parent is None:
            return []
        elems = parent.findall(f'nfe:{tag_name}', self.namespaces)
        if not elems:
            elems = parent.findall(tag_name)
        return elems
    
    def _to_float(self, value: Any) -> Optional[float]:
        """
        Converte string para float seguro
        
        Args:
            value: Valor a converter
            
        Returns:
            Float ou None
        """
        try:
            return float(value) if value else None
        except (ValueError, TypeError):
            return None
    
    def _parse_emitente(self, inf_nfe, header_data):
        """Parse completo do grupo do emitente (16 campos)"""
        try:
            emit = self.find_element(inf_nfe, 'emit')
            if emit is not None:
                emitente_fields = {
                    'emit_CNPJ': 'CNPJ',
                    'emit_CPF': 'CPF',
                    'emit_xNome': 'xNome',
                    'emit_xFant': 'xFant',
                    'emit_IE': 'IE',
                    'emit_IEST': 'IEST',
                    'emit_IM': 'IM',
                    'emit_CNAE': 'CNAE',
                    'emit_CRT': 'CRT'
                }
                
                for field_key, xml_tag in emitente_fields.items():
                    value = self.find_element_text(emit, xml_tag)
                    if value:
                        header_data[field_key] = value
                
                # Endereço do emitente
                ender_emit = self.find_element(emit, 'enderEmit')
                if ender_emit is not None:
                    endereco_fields = {
                        'emit_ender_xLgr': 'xLgr',
                        'emit_ender_nro': 'nro',
                        'emit_ender_xBairro': 'xBairro',
                        'emit_ender_cMun': 'cMun',
                        'emit_ender_xMun': 'xMun',
                        'emit_ender_UF': 'UF',
                        'emit_ender_CEP': 'CEP'
                    }
                    
                    for field_key, xml_tag in endereco_fields.items():
                        value = self.find_element_text(ender_emit, xml_tag)
                        if value:
                            header_data[field_key] = value
                            
        except Exception as e:
            self.logger.error(f"Erro ao parsear emitente: {e}", exc_info=True)
    
    def _parse_identificacao(self, inf_nfe, header_data):
        """Parse completo do grupo de identificação da NF-e (23 campos)"""
        try:
            ide = self.find_element(inf_nfe, 'ide')
            if ide is not None:
                identificacao_fields = {
                    'cUF': 'cUF',
                    'cNF': 'cNF',
                    'natOp': 'natOp',
                    'mod': 'mod',
                    'serie': 'serie',
                    'nNF': 'nNF',
                    'dhEmi': 'dhEmi',
                    'dhSaiEnt': 'dhSaiEnt',
                    'tpNF': 'tpNF',
                    'idDest': 'idDest',
                    'cMunFG': 'cMunFG',
                    'tpImp': 'tpImp',
                    'tpEmis': 'tpEmis',
                    'cDV': 'cDV',
                    'tpAmb': 'tpAmb',
                    'finNFe': 'finNFe',
                    'indFinal': 'indFinal',
                    'indPres': 'indPres',
                    'procEmi': 'procEmi',
                    'verProc': 'verProc',
                    'cMunFGIBS': 'cMunFGIBS',
                    'tpNFDebito': 'tpNFDebito',
                    'tpNFCredito': 'tpNFCredito'
                }
                
                for field_key, xml_tag in identificacao_fields.items():
                    value = self.find_element_text(ide, xml_tag)
                    if value:
                        header_data[field_key] = value
                        
        except Exception as e:
            self.logger.error(f"Erro ao parsear identificação: {e}", exc_info=True)
    
    def _parse_destinatario(self, inf_nfe, header_data):
        """Parse completo do grupo do destinatário (16 campos)"""
        try:
            dest = self.find_element(inf_nfe, 'dest')
            if dest is not None:
                destinatario_fields = {
                    'dest_CNPJ': 'CNPJ',
                    'dest_CPF': 'CPF',
                    'dest_idEstrangeiro': 'idEstrangeiro',
                    'dest_xNome': 'xNome',
                    'dest_indIEDest': 'indIEDest',
                    'dest_IE': 'IE',
                    'dest_ISUF': 'ISUF',
                    'dest_IM': 'IM',
                    'dest_email': 'email'
                }
                
                for field_key, xml_tag in destinatario_fields.items():
                    value = self.find_element_text(dest, xml_tag)
                    if value:
                        header_data[field_key] = value
                
                # Endereço do destinatário
                ender_dest = self.find_element(dest, 'enderDest')
                if ender_dest is not None:
                    endereco_fields = {
                        'dest_ender_xLgr': 'xLgr',
                        'dest_ender_nro': 'nro',
                        'dest_ender_xBairro': 'xBairro',
                        'dest_ender_cMun': 'cMun',
                        'dest_ender_xMun': 'xMun',
                        'dest_ender_UF': 'UF',
                        'dest_ender_CEP': 'CEP'
                    }
                    
                    for field_key, xml_tag in endereco_fields.items():
                        value = self.find_element_text(ender_dest, xml_tag)
                        if value:
                            header_data[field_key] = value
                            
        except Exception as e:
            self.logger.error(f"Erro ao parsear destinatário: {e}", exc_info=True)
    
    def _parse_totais(self, inf_nfe, header_data):
        """Parse completo do grupo de totais da NF-e (35+ campos)"""
        try:
            total = self.find_element(inf_nfe, 'total')
            if total is not None:
                self._parse_icms_tot(total, header_data)
                self._parse_ibscbs_tot(total, header_data)
                self._parse_vnftot(total, header_data)
                
        except Exception as e:
            self.logger.error(f"Erro ao parsear totais: {e}", exc_info=True)
    
    def _parse_icms_tot(self, total, header_data):
        """Parse do grupo ICMSTot (20 campos)"""
        try:
            ICMSTot = self.find_element(total, 'ICMSTot')
            if ICMSTot is not None:
                icms_tot_fields = {
                    'total_vBC': 'vBC',
                    'total_vICMS': 'vICMS',
                    'total_vICMSDeson': 'vICMSDeson',
                    'total_vFCPUFDest': 'vFCPUFDest',
                    'total_vICMSUFDest': 'vICMSUFDest',
                    'total_vICMSUFRemet': 'vICMSUFRemet',
                    'total_vFCP': 'vFCP',
                    'total_vBCST': 'vBCST',
                    'total_vST': 'vST',
                    'total_vProd': 'vProd',
                    'total_vFrete': 'vFrete',
                    'total_vSeg': 'vSeg',
                    'total_vDesc': 'vDesc',
                    'total_vII': 'vII',
                    'total_vIPI': 'vIPI',
                    'total_vPIS': 'vPIS',
                    'total_vCOFINS': 'vCOFINS',
                    'total_vOutro': 'vOutro',
                    'total_vNF': 'vNF',
                    'total_vTotTrib': 'vTotTrib'
                }
                
                for field_key, xml_tag in icms_tot_fields.items():
                    value = self.find_element_text(ICMSTot, xml_tag)
                    if value:
                        header_data[field_key] = self._to_float(value)
                        
        except Exception as e:
            self.logger.error(f"Erro ao parsear ICMSTot: {e}", exc_info=True)
    
    def _parse_ibscbs_tot(self, total, header_data):
        """Parse do grupo IBSCBSTot (15+ campos)"""
        try:
            IBSCBSTot = self.find_element(total, 'IBSCBSTot')
            if IBSCBSTot is not None:
                header_data['total_vBCIBSCBS'] = self._to_float(
                    self.find_element_text(IBSCBSTot, 'vBCIBSCBS')
                )
                
                # Parse dos subgrupos
                self._parse_gibs(IBSCBSTot, header_data)
                self._parse_gcbs(IBSCBSTot, header_data)
                self._parse_gmono(IBSCBSTot, header_data)
                self._parse_gestornocred(IBSCBSTot, header_data)
                        
        except Exception as e:
            self.logger.error(f"Erro ao parsear IBSCBSTot: {e}", exc_info=True)
    
    def _parse_gibs(self, ibscbstot, header_data):
        """Parse do grupo gIBS dentro do IBSCBSTot"""
        try:
            gibs = self.find_element(ibscbstot, 'gIBS')
            if gibs is not None:
                # Grupo gIBSUF
                gibsuf = self.find_element(gibs, 'gIBSUF')
                if gibsuf is not None:
                    header_data['total_gIBS_gIBSUF_vDif'] = self._to_float(self.find_element_text(gibsuf, 'vDif'))
                    header_data['total_gIBS_gIBSUF_vDevTrib'] = self._to_float(self.find_element_text(gibsuf, 'vDevTrib'))
                    header_data['total_gIBS_gIBSUF_vIBSUF'] = self._to_float(self.find_element_text(gibsuf, 'vIBSUF'))
                
                # Grupo gIBSMun
                gibsmun = self.find_element(gibs, 'gIBSMun')
                if gibsmun is not None:
                    header_data['total_gIBS_gIBSMun_vDif'] = self._to_float(self.find_element_text(gibsmun, 'vDif'))
                    header_data['total_gIBS_gIBSMun_vDevTrib'] = self._to_float(self.find_element_text(gibsmun, 'vDevTrib'))
                    header_data['total_gIBS_gIBSMun_vIBSMun'] = self._to_float(self.find_element_text(gibsmun, 'vIBSMun'))
                
                # Campos diretos do gIBS
                header_data['total_gIBS_vIBS'] = self._to_float(self.find_element_text(gibs, 'vIBS'))
                header_data['total_gIBS_vCredPres'] = self._to_float(self.find_element_text(gibs, 'vCredPres'))
                header_data['total_gIBS_vCredPresCondSus'] = self._to_float(self.find_element_text(gibs, 'vCredPresCondSus'))
                
        except Exception as e:
            self.logger.error(f"Erro ao parsear gIBS: {e}", exc_info=True)
    
    def _parse_gcbs(self, ibscbstot, header_data):
        """Parse do grupo gCBS dentro do IBSCBSTot"""
        try:
            gcbs = self.find_element(ibscbstot, 'gCBS')
            if gcbs is not None:
                header_data['total_gCBS_vDif'] = self._to_float(self.find_element_text(gcbs, 'vDif'))
                header_data['total_gCBS_vDevTrib'] = self._to_float(self.find_element_text(gcbs, 'vDevTrib'))
                header_data['total_gCBS_vCBS'] = self._to_float(self.find_element_text(gcbs, 'vCBS'))
                header_data['total_gCBS_vCredPres'] = self._to_float(self.find_element_text(gcbs, 'vCredPres'))
                header_data['total_gCBS_vCredPresCondSus'] = self._to_float(self.find_element_text(gcbs, 'vCredPresCondSus'))
                
        except Exception as e:
            self.logger.error(f"Erro ao parsear gCBS: {e}", exc_info=True)
    
    def _parse_gmono(self, ibscbstot, header_data):
        """Parse do grupo gMono dentro do IBSCBSTot"""
        try:
            gmono = self.find_element(ibscbstot, 'gMono')
            if gmono is not None:
                header_data['total_gMono_vIBSMono'] = self._to_float(self.find_element_text(gmono, 'vIBSMono'))
                header_data['total_gMono_vCBSMono'] = self._to_float(self.find_element_text(gmono, 'vCBSMono'))
                header_data['total_gMono_vIBSMonoReten'] = self._to_float(self.find_element_text(gmono, 'vIBSMonoReten'))
                header_data['total_gMono_vCBSMonoReten'] = self._to_float(self.find_element_text(gmono, 'vCBSMonoReten'))
                header_data['total_gMono_vIBSMonoRet'] = self._to_float(self.find_element_text(gmono, 'vIBSMonoRet'))
                header_data['total_gMono_vCBSMonoRet'] = self._to_float(self.find_element_text(gmono, 'vCBSMonoRet'))
                
        except Exception as e:
            self.logger.error(f"Erro ao parsear gMono: {e}", exc_info=True)
    
    def _parse_gestornocred(self, ibscbstot, header_data):
        """Parse do grupo gEstornoCred dentro do IBSCBSTot"""
        try:
            gestornocred = self.find_element(ibscbstot, 'gEstornoCred')
            if gestornocred is not None:
                header_data['total_gEstornoCred_vIBSEstCred'] = self._to_float(self.find_element_text(gestornocred, 'vIBSEstCred'))
                header_data['total_gEstornoCred_vCBSEstCred'] = self._to_float(self.find_element_text(gestornocred, 'vCBSEstCred'))
                
        except Exception as e:
            self.logger.error(f"Erro ao parsear gEstornoCred: {e}", exc_info=True)
    
    def _parse_vnftot(self, total, header_data):
        """Parse do campo vNFTot"""
        try:
            vNFTot = self.find_element_text(total, 'vNFTot')
            if vNFTot:
                header_data['vNFTot'] = self._to_float(vNFTot)
            else:
                # Se vNFTot não estiver disponível, usar total_vNF como fallback
                header_data['vNFTot'] = header_data.get('total_vNF')
                
        except Exception as e:
            self.logger.error(f"Erro ao parsear vNFTot: {e}", exc_info=True)
    
    def _parse_transporte(self, inf_nfe, header_data):
        """Parse do grupo de transporte (3 campos)"""
        try:
            transp = self.find_element(inf_nfe, 'transp')
            if transp is not None:
                header_data['transp_modFrete'] = self.find_element_text(transp, 'modFrete')
                
                transporta = self.find_element(transp, 'transporta')
                if transporta is not None:
                    header_data['transp_transporta_xNome'] = self.find_element_text(transporta, 'xNome')
                    header_data['transp_transporta_IE'] = self.find_element_text(transporta, 'IE')
                    
        except Exception as e:
            self.logger.error(f"Erro ao parsear transporte: {e}", exc_info=True)
    
    def _parse_pagamento(self, inf_nfe, header_data):
        """Parse do grupo de pagamento (2 campos)"""
        try:
            pag = self.find_element(inf_nfe, 'pag')
            if pag is not None:
                det_pag_elements = self.find_all_elements(pag, 'detPag')
                if det_pag_elements:
                    det_pag = det_pag_elements[0]
                    header_data['pag_detPag_tPag'] = self.find_element_text(det_pag, 'tPag')
                    header_data['pag_detPag_vPag'] = self._to_float(self.find_element_text(det_pag, 'vPag'))
                            
        except Exception as e:
            self.logger.error(f"Erro ao parsear pagamento: {e}", exc_info=True)
    
    def _extract_header_data(self, inf_nfe) -> Dict[str, Any]:
        """
        Extrai TODOS os dados do cabeçalho da NF-e (50+ campos)
        
        Args:
            inf_nfe: Elemento infNFe
            
        Returns:
            Dicionário com dados completos do cabeçalho
        """
        header_data = {}
        
        try:
            # Atributos do infNFe
            header_data['Id'] = inf_nfe.get('Id')
            header_data['versao_nfe'] = inf_nfe.get('versao')
            
            # Grupos principais
            self._parse_emitente(inf_nfe, header_data)
            self._parse_identificacao(inf_nfe, header_data)
            self._parse_destinatario(inf_nfe, header_data)
            self._parse_totais(inf_nfe, header_data)
            self._parse_transporte(inf_nfe, header_data)
            self._parse_pagamento(inf_nfe, header_data)
            
            self.logger.debug(f"Cabeçalho extraído: NF-e {header_data.get('nNF')} - {len(header_data)} campos")
            
        except Exception as e:
            self.logger.error(f"Erro ao extrair cabeçalho: {e}", exc_info=True)
        
        return header_data
    
    def _parse_produto(self, prod, item_data):
        """Parse completo do grupo do produto (18 campos)"""
        try:
            if prod is not None:
                produto_fields = {
                    'cProd': 'cProd',
                    'cEAN': 'cEAN',
                    'xProd': 'xProd',
                    'NCM': 'NCM',
                    'CFOP': 'CFOP',
                    'uCom': 'uCom',
                    'qCom': 'qCom',
                    'vUnCom': 'vUnCom',
                    'vProd': 'vProd',
                    'uTrib': 'uTrib',
                    'qTrib': 'qTrib',
                    'vUnTrib': 'vUnTrib',
                    'vFrete': 'vFrete',
                    'vSeg': 'vSeg',
                    'vDesc': 'vDesc',
                    'vOutro': 'vOutro',
                    'indTot': 'indTot',
                    'tpCredPresIBSZFM': 'tpCredPresIBSZFM'
                }
                
                for field_key, xml_tag in produto_fields.items():
                    value = self.find_element_text(prod, xml_tag)
                    if value:
                        if field_key in ['qCom', 'vUnCom', 'vProd', 'qTrib', 'vUnTrib', 'vFrete', 'vSeg', 'vDesc', 'vOutro']:
                            item_data[field_key] = self._to_float(value)
                        else:
                            item_data[field_key] = value
                
                # Crédito Presumido
                self._parse_credito_presumido(prod, item_data)
                        
        except Exception as e:
            self.logger.error(f"Erro ao parsear produto: {e}", exc_info=True)
    
    def _parse_credito_presumido(self, prod, item_data):
        """Parse do grupo de crédito presumido - Reforma Tributária (3 campos)"""
        try:
            gCred = self.find_element(prod, 'gCred')
            if gCred is not None:
                item_data['gCred_cCredPresumido'] = self.find_element_text(gCred, 'cCredPresumido')
                item_data['gCred_pCredPresumido'] = self._to_float(self.find_element_text(gCred, 'pCredPresumido'))
                item_data['gCred_vCredPresumido'] = self._to_float(self.find_element_text(gCred, 'vCredPresumido'))
        except Exception as e:
            self.logger.error(f"Erro ao parsear crédito presumido: {e}", exc_info=True)
    
    def _parse_partilha_icms(self, icms_elem, icms_type, item_data):
        """Parse da Partilha do ICMS - DIFAL (8 campos)"""
        try:
            vBCUFDest = self.find_element_text(icms_elem, 'vBCUFDest')
            if vBCUFDest is not None:
                partilha_fields = {
                    f'ICMS_{icms_type}_Partilha_vBCUFDest': 'vBCUFDest',
                    f'ICMS_{icms_type}_Partilha_pFCPUFDest': 'pFCPUFDest',
                    f'ICMS_{icms_type}_Partilha_pICMSUFDest': 'pICMSUFDest',
                    f'ICMS_{icms_type}_Partilha_pICMSInter': 'pICMSInter',
                    f'ICMS_{icms_type}_Partilha_pICMSInterPart': 'pICMSInterPart',
                    f'ICMS_{icms_type}_Partilha_vFCPUFDest': 'vFCPUFDest',
                    f'ICMS_{icms_type}_Partilha_vICMSUFDest': 'vICMSUFDest',
                    f'ICMS_{icms_type}_Partilha_vICMSUFRemet': 'vICMSUFRemet'
                }
                
                for field_key, xml_tag in partilha_fields.items():
                    value = self.find_element_text(icms_elem, xml_tag)
                    if value:
                        item_data[field_key] = self._to_float(value)
                        
        except Exception as e:
            self.logger.error(f"Erro ao parsear partilha ICMS: {e}", exc_info=True)
    
    def _parse_icms_completo(self, imposto, item_data):
        """Parse completo do ICMS com todos os tipos (30+ campos)"""
        try:
            icms = self.find_element(imposto, 'ICMS')
            if icms is not None:
                for icms_type in ['ICMS00', 'ICMS20', 'ICMS40', 'ICMS51', 'ICMS90', 'ICMSSN101']:
                    icms_elem = self.find_element(icms, icms_type)
                    if icms_elem is not None:
                        icms_basic_fields = {
                            f'ICMS_{icms_type}_CST': 'CST',
                            f'ICMS_{icms_type}_CSOSN': 'CSOSN',
                            f'ICMS_{icms_type}_orig': 'orig',
                            f'ICMS_{icms_type}_vBC': 'vBC',
                            f'ICMS_{icms_type}_pICMS': 'pICMS',
                            f'ICMS_{icms_type}_vICMS': 'vICMS',
                            f'ICMS_{icms_type}_pFCP': 'pFCP',
                            f'ICMS_{icms_type}_vFCP': 'vFCP'
                        }
                        
                        for field_key, xml_tag in icms_basic_fields.items():
                            value = self.find_element_text(icms_elem, xml_tag)
                            if value:
                                item_data[field_key] = self._to_float(value) if field_key not in [f'ICMS_{icms_type}_CST', f'ICMS_{icms_type}_CSOSN', f'ICMS_{icms_type}_orig'] else value
                        
                        # Desoneração
                        vICMSDeson = self.find_element_text(icms_elem, 'vICMSDeson')
                        if vICMSDeson:
                            item_data[f'ICMS_{icms_type}_vICMSDeson'] = self._to_float(vICMSDeson)
                            item_data[f'ICMS_{icms_type}_motDesICMS'] = self.find_element_text(icms_elem, 'motDesICMS')
                        
                        # PARTILHA DO ICMS (DIFAL)
                        self._parse_partilha_icms(icms_elem, icms_type, item_data)
                        
                        break
                    
        except Exception as e:
            self.logger.error(f"Erro ao parsear ICMS: {e}", exc_info=True)
    
    def _parse_pis_item(self, imposto, item_data):
        """Parse do PIS (4 campos)"""
        try:
            pis = self.find_element(imposto, 'PIS')
            if pis is not None:
                for pis_type in ['PISAliq', 'PISQtde', 'PISNT', 'PISOutr']:
                    pis_elem = self.find_element(pis, pis_type)
                    if pis_elem is not None:
                        pis_fields = {
                            'PIS_CST': 'CST',
                            'PIS_vBC': 'vBC',
                            'PIS_pPIS': 'pPIS',
                            'PIS_vPIS': 'vPIS'
                        }
                        
                        for field_key, xml_tag in pis_fields.items():
                            value = self.find_element_text(pis_elem, xml_tag)
                            if value:
                                item_data[field_key] = self._to_float(value) if field_key != 'PIS_CST' else value
                        break
        except Exception as e:
            self.logger.error(f"Erro ao parsear PIS: {e}", exc_info=True)
    
    def _parse_cofins_item(self, imposto, item_data):
        """Parse do COFINS (4 campos)"""
        try:
            cofins = self.find_element(imposto, 'COFINS')
            if cofins is not None:
                for cofins_type in ['COFINSAliq', 'COFINSQtde', 'COFINSNT', 'COFINSOutr']:
                    cofins_elem = self.find_element(cofins, cofins_type)
                    if cofins_elem is not None:
                        cofins_fields = {
                            'COFINS_CST': 'CST',
                            'COFINS_vBC': 'vBC',
                            'COFINS_pCOFINS': 'pCOFINS',
                            'COFINS_vCOFINS': 'vCOFINS'
                        }
                        
                        for field_key, xml_tag in cofins_fields.items():
                            value = self.find_element_text(cofins_elem, xml_tag)
                            if value:
                                item_data[field_key] = self._to_float(value) if field_key != 'COFINS_CST' else value
                        break
        except Exception as e:
            self.logger.error(f"Erro ao parsear COFINS: {e}", exc_info=True)
    
    def _parse_gtribregular(self, gibscbs_elem, item_data):
        """Parse do grupo de tributação regular - Reforma Tributária (8 campos)"""
        try:
            gTribRegular = self.find_element(gibscbs_elem, 'gTribRegular')
            if gTribRegular is not None:
                gtrib_fields = {
                    'gTribRegular_CSTReg': 'CSTReg',
                    'gTribRegular_cClassTribReg': 'cClassTribReg',
                    'gTribRegular_pAliqEfetRegIBSUF': 'pAliqEfetRegIBSUF',
                    'gTribRegular_vTribRegIBSUF': 'vTribRegIBSUF',
                    'gTribRegular_pAliqEfetRegIBSMun': 'pAliqEfetRegIBSMun',
                    'gTribRegular_vTribRegIBSMun': 'vTribRegIBSMun',
                    'gTribRegular_pAliqEfetRegCBS': 'pAliqEfetRegCBS',
                    'gTribRegular_vTribRegCBS': 'vTribRegCBS'
                }
                
                for field_key, xml_tag in gtrib_fields.items():
                    value = self.find_element_text(gTribRegular, xml_tag)
                    if value:
                        if 'pAliq' in field_key or 'vTrib' in field_key:
                            item_data[field_key] = self._to_float(value)
                        else:
                            item_data[field_key] = value
                
        except Exception as e:
            self.logger.error(f"Erro ao parsear gTribRegular: {e}", exc_info=True)
    
    def _parse_ibscbs_item(self, imposto, item_data):
        """Parse completo de IBS/CBS - Reforma Tributária (20+ campos)"""
        try:
            ibscbs = self.find_element(imposto, 'IBSCBS')
            if ibscbs is not None:
                # Campos básicos
                item_data['ibscbs_CST'] = self.find_element_text(ibscbs, 'CST')
                item_data['ibscbs_cClassTrib'] = self.find_element_text(ibscbs, 'cClassTrib')
                
                # Grupo gIBSCBS
                gibscbs = self.find_element(ibscbs, 'gIBSCBS')
                if gibscbs is not None:
                    item_data['ibscbs_vBC'] = self._to_float(self.find_element_text(gibscbs, 'vBC'))
                    item_data['ibscbs_vIBS'] = self._to_float(self.find_element_text(gibscbs, 'vIBS'))
                    
                    # Subgrupos
                    gibsuf = self.find_element(gibscbs, 'gIBSUF')
                    if gibsuf is not None:
                        item_data['ibscbs_gIBSUF_pIBSUF'] = self._to_float(self.find_element_text(gibsuf, 'pIBSUF'))
                        item_data['ibscbs_gIBSUF_vIBSUF'] = self._to_float(self.find_element_text(gibsuf, 'vIBSUF'))
                    
                    gibsmun = self.find_element(gibscbs, 'gIBSMun')
                    if gibsmun is not None:
                        item_data['ibscbs_gIBSMun_pIBSMun'] = self._to_float(self.find_element_text(gibsmun, 'pIBSMun'))
                        item_data['ibscbs_gIBSMun_vIBSMun'] = self._to_float(self.find_element_text(gibsmun, 'vIBSMun'))
                    
                    gcbs = self.find_element(gibscbs, 'gCBS')
                    if gcbs is not None:
                        item_data['ibscbs_gCBS_pCBS'] = self._to_float(self.find_element_text(gcbs, 'pCBS'))
                        item_data['ibscbs_gCBS_vCBS'] = self._to_float(self.find_element_text(gcbs, 'vCBS'))
                    
                    # gTribRegular
                    self._parse_gtribregular(gibscbs, item_data)
            else:
                # Marcar como não aplicável
                item_data['ibscbs_CST'] = 'NA'
                item_data['ibscbs_cClassTrib'] = 'NA'
                    
        except Exception as e:
            self.logger.error(f"Erro ao parsear IBSCBS do item: {e}", exc_info=True)
    
    def _extract_item_data(self, det, header_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extrai TODOS os dados de um item da NF-e (100+ campos)
        
        Args:
            det: Elemento det (item)
            header_data: Dados do cabeçalho
            
        Returns:
            Dicionário com dados completos do item
        """
        item_data = header_data.copy()
        
        try:
            item_data['nItem'] = det.get('nItem')
            
            # Produto completo
            prod = self.find_element(det, 'prod')
            self._parse_produto(prod, item_data)
            
            # vItem
            vItem = self.find_element_text(det, 'vItem')
            if vItem:
                item_data['vItem'] = self._to_float(vItem)
            else:
                item_data['vItem'] = item_data.get('vProd')
            
            # Impostos completos
            imposto = self.find_element(det, 'imposto')
            if imposto is not None:
                item_data['vTotTrib'] = self._to_float(self.find_element_text(imposto, 'vTotTrib'))
                
                self._parse_icms_completo(imposto, item_data)
                self._parse_pis_item(imposto, item_data)
                self._parse_cofins_item(imposto, item_data)
                self._parse_ibscbs_item(imposto, item_data)
            
            self.logger.debug(f"Item {item_data.get('nItem')} extraído - {len(item_data)} campos")
            
        except Exception as e:
            self.logger.error(f"Erro ao extrair item: {e}", exc_info=True)
        
        return item_data
    
    def parse_xml_stream(self, 
                        file_path: str,
                        progress_callback: Optional[Callable[[int, int], None]] = None) -> List[Dict[str, Any]]:
        """
        Parse XML usando streaming para economizar memória
        
        Args:
            file_path: Caminho do arquivo XML
            progress_callback: Função callback(items_processed, total_items) para progresso
            
        Returns:
            Lista de dicionários com dados dos itens
            
        Example:
            >>> parser = StreamingNFeParser()
            >>> def on_progress(current, total):
            ...     print(f"Processando {current}/{total}")
            >>> data = parser.parse_xml_stream('nota.xml', on_progress)
        """
        self.logger.info(f"Iniciando parse streaming de {file_path}")
        
        items_data = []
        header_data = {}
        inf_nfe = None
        total_items = 0
        
        try:
            # Primeira passagem: contar itens e extrair cabeçalho
            self.logger.debug("Primeira passagem: contando itens...")
            for event, elem in ET.iterparse(file_path, events=('start', 'end')):
                if event == 'end':
                    if elem.tag.endswith('infNFe'):
                        inf_nfe = elem
                        header_data = self._extract_header_data(elem)
                    elif elem.tag.endswith('det'):
                        total_items += 1
            
            self.logger.info(f"Total de itens encontrados: {total_items}")
            
            # Segunda passagem: processar itens
            self.logger.debug("Segunda passagem: processando itens...")
            items_processed = 0
            
            for event, elem in ET.iterparse(file_path, events=('start', 'end')):
                if event == 'end' and elem.tag.endswith('det'):
                    # Processar item
                    item_data = self._extract_item_data(elem, header_data)
                    items_data.append(item_data)
                    items_processed += 1
                    
                    # Callback de progresso
                    if progress_callback:
                        progress_callback(items_processed, total_items)
                    
                    # Liberar memória
                    elem.clear()
                    
                    # Log a cada 10 itens
                    if items_processed % 10 == 0:
                        self.logger.debug(f"Processados {items_processed}/{total_items} itens")
            
            self.logger.info(f"Parse concluído: {len(items_data)} itens extraídos")
            
        except ET.ParseError as e:
            self.logger.error(f"Erro ao parsear XML: {e}", exc_info=True)
            raise
        except Exception as e:
            self.logger.error(f"Erro inesperado: {e}", exc_info=True)
            raise
        
        return items_data
    
    def parse_multiple_files(self,
                           file_paths: List[str],
                           progress_callback: Optional[Callable[[int, int, str], None]] = None) -> List[Dict[str, Any]]:
        """
        Parse múltiplos arquivos XML
        
        Args:
            file_paths: Lista de caminhos de arquivos
            progress_callback: Função callback(file_index, total_files, filename)
            
        Returns:
            Lista consolidada de dados de todos os arquivos
        """
        self.logger.info(f"Iniciando parse de {len(file_paths)} arquivos")
        
        all_data = []
        total_files = len(file_paths)
        
        for idx, file_path in enumerate(file_paths, 1):
            try:
                filename = Path(file_path).name
                self.logger.info(f"Processando arquivo {idx}/{total_files}: {filename}")
                
                if progress_callback:
                    progress_callback(idx, total_files, filename)
                
                data = self.parse_xml_stream(file_path)
                all_data.extend(data)
                
                self.logger.info(f"Arquivo {filename}: {len(data)} itens extraídos")
                
            except Exception as e:
                self.logger.error(f"Erro ao processar {file_path}: {e}", exc_info=True)
                continue
        
        self.logger.info(f"Parse completo: {len(all_data)} itens de {total_files} arquivos")
        return all_data


# Exemplo de uso
if __name__ == '__main__':
    from src.utils.logger import setup_logger
    
    # Configurar logging
    setup_logger(log_level='DEBUG')
    
    # Criar parser
    parser = StreamingNFeParser()
    
    # Callback de progresso
    def on_progress(current, total):
        percent = (current / total) * 100
        print(f"Progresso: {current}/{total} ({percent:.1f}%)")
    
    # Parse de arquivo (exemplo)
    # data = parser.parse_xml_stream('exemplo.xml', on_progress)
    # print(f"Total de itens: {len(data)}")

# Made with Bob
