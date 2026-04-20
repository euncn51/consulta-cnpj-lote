import xml.etree.ElementTree as ET
import os
import pandas as pd
from datetime import datetime
import glob
import numpy as np
from decimal import Decimal
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

@dataclass
class CreditoPresumido:
    """Grupo de Crédito Presumido (gCred) - NOVO Reforma Tributária"""
    cCredPresumido: str
    pCredPresumido: Decimal
    vCredPresumido: Decimal

@dataclass
class DesoneracaoICMS:
    """Grupo de desoneração do ICMS"""
    vICMSDeson: Decimal
    motDesICMS: str
    indDeduzDeson: Optional[str] = None

class NFeParser:
    def __init__(self):
        self.namespaces = {
            'nfe': 'http://www.portalfiscal.inf.br/nfe',
            'ds': 'http://www.w3.org/2000/09/xmldsig#'
        }
    
    def find_element(self, parent, tag_name):
        """Busca elemento com namespace"""
        if parent is None:
            return None
        # Tentar com namespace nfe
        elem = parent.find(f'nfe:{tag_name}', self.namespaces)
        if elem is None:
            # Tentar sem namespace
            elem = parent.find(tag_name)
        return elem
    
    def find_element_text(self, parent, tag_name):
        """Busca texto do elemento"""
        elem = self.find_element(parent, tag_name)
        return elem.text if elem is not None else None
    
    def find_all_elements(self, parent, tag_name):
        """Busca todos os elementos"""
        if parent is None:
            return []
        # Tentar com namespace nfe
        elems = parent.findall(f'nfe:{tag_name}', self.namespaces)
        if not elems:
            # Tentar sem namespace
            elems = parent.findall(tag_name)
        return elems

    def _to_float(self, value):
        """Converte string para float seguro"""
        try:
            return float(value) if value else None
        except (ValueError, TypeError):
            return None

    def parse_partilha_icms(self, icms_elem, icms_type, item_data):
        """Parse da Partilha do ICMS (DIFAL)"""
        try:
            # Verificar se existe algum campo da partilha
            vBCUFDest = self.find_element_text(icms_elem, 'vBCUFDest')
            if vBCUFDest is not None:
                print(f"Partilha ICMS encontrada para {icms_type}")
                
                # Campos da Partilha do ICMS
                item_data[f'ICMS_{icms_type}_Partilha_vBCUFDest'] = self._to_float(vBCUFDest)
                item_data[f'ICMS_{icms_type}_Partilha_pFCPUFDest'] = self._to_float(self.find_element_text(icms_elem, 'pFCPUFDest'))
                item_data[f'ICMS_{icms_type}_Partilha_pICMSUFDest'] = self._to_float(self.find_element_text(icms_elem, 'pICMSUFDest'))
                item_data[f'ICMS_{icms_type}_Partilha_pICMSInter'] = self._to_float(self.find_element_text(icms_elem, 'pICMSInter'))
                item_data[f'ICMS_{icms_type}_Partilha_pICMSInterPart'] = self._to_float(self.find_element_text(icms_elem, 'pICMSInterPart'))
                item_data[f'ICMS_{icms_type}_Partilha_vFCPUFDest'] = self._to_float(self.find_element_text(icms_elem, 'vFCPUFDest'))
                item_data[f'ICMS_{icms_type}_Partilha_vICMSUFDest'] = self._to_float(self.find_element_text(icms_elem, 'vICMSUFDest'))
                item_data[f'ICMS_{icms_type}_Partilha_vICMSUFRemet'] = self._to_float(self.find_element_text(icms_elem, 'vICMSUFRemet'))
                
        except Exception as e:
            print(f"Erro ao parsear partilha ICMS: {e}")

    def parse_gtribregular(self, icms_elem, icms_type, item_data):
        """Parse do grupo de tributação regular (gTribRegular) - NOVO Reforma Tributária"""
        try:
            gTribRegular = self.find_element(icms_elem, 'gTribRegular')
            if gTribRegular is not None:
                print(f"gTribRegular encontrado para {icms_type}")
                
                # Campos obrigatórios do gTribRegular
                CSTReg = self.find_element_text(gTribRegular, 'CSTReg')
                cClassTribReg = self.find_element_text(gTribRegular, 'cClassTribReg')
                pAliqEfetRegIBSUF = self.find_element_text(gTribRegular, 'pAliqEfetRegIBSUF')
                vTribRegIBSUF = self.find_element_text(gTribRegular, 'vTribRegIBSUF')
                pAliqEfetRegIBSMun = self.find_element_text(gTribRegular, 'pAliqEfetRegIBSMun')
                vTribRegIBSMun = self.find_element_text(gTribRegular, 'vTribRegIBSMun')
                pAliqEfetRegCBS = self.find_element_text(gTribRegular, 'pAliqEfetRegCBS')
                vTribRegCBS = self.find_element_text(gTribRegular, 'vTribRegCBS')
                
                # Campos do gTribRegular
                if CSTReg:
                    item_data[f'ICMS_{icms_type}_gTribRegular_CSTReg'] = CSTReg
                if cClassTribReg:
                    item_data[f'ICMS_{icms_type}_gTribRegular_cClassTribReg'] = cClassTribReg
                if pAliqEfetRegIBSUF:
                    item_data[f'ICMS_{icms_type}_gTribRegular_pAliqEfetRegIBSUF'] = self._to_float(pAliqEfetRegIBSUF)
                if vTribRegIBSUF:
                    item_data[f'ICMS_{icms_type}_gTribRegular_vTribRegIBSUF'] = self._to_float(vTribRegIBSUF)
                if pAliqEfetRegIBSMun:
                    item_data[f'ICMS_{icms_type}_gTribRegular_pAliqEfetRegIBSMun'] = self._to_float(pAliqEfetRegIBSMun)
                if vTribRegIBSMun:
                    item_data[f'ICMS_{icms_type}_gTribRegular_vTribRegIBSMun'] = self._to_float(vTribRegIBSMun)
                if pAliqEfetRegCBS:
                    item_data[f'ICMS_{icms_type}_gTribRegular_pAliqEfetRegCBS'] = self._to_float(pAliqEfetRegCBS)
                if vTribRegCBS:
                    item_data[f'ICMS_{icms_type}_gTribRegular_vTribRegCBS'] = self._to_float(vTribRegCBS)
                
        except Exception as e:
            print(f"Erro ao parsear gTribRegular: {e}")

    def parse_icms_item(self, imposto, item_data):
        """Parse completo do ICMS com FCP, desoneração, partilha e gTribRegular"""
        try:
            icms = self.find_element(imposto, 'ICMS')
            if icms is not None:
                # Verificar todos os tipos de ICMS
                for icms_type in ['ICMS00', 'ICMS02', 'ICMS10', 'ICMS15', 'ICMS20', 'ICMS30', 
                                 'ICMS40', 'ICMS51', 'ICMS53', 'ICMS60', 'ICMS61', 'ICMS70', 
                                 'ICMS90', 'ICMSPart', 'ICMSST', 'ICMSSN101', 'ICMSSN102', 
                                 'ICMSSN201', 'ICMSSN202', 'ICMSSN500', 'ICMSSN900']:
                    
                    icms_elem = self.find_element(icms, icms_type)
                    if icms_elem is not None:
                        item_data[f'ICMS_{icms_type}_CST'] = self.find_element_text(icms_elem, 'CST') or self.find_element_text(icms_elem, 'CSOSN')
                        item_data[f'ICMS_{icms_type}_orig'] = self.find_element_text(icms_elem, 'orig')
                        
                        # Valores básicos do ICMS
                        item_data[f'ICMS_{icms_type}_vBC'] = self._to_float(self.find_element_text(icms_elem, 'vBC'))
                        item_data[f'ICMS_{icms_type}_pICMS'] = self._to_float(self.find_element_text(icms_elem, 'pICMS'))
                        item_data[f'ICMS_{icms_type}_vICMS'] = self._to_float(self.find_element_text(icms_elem, 'vICMS'))
                        
                        # FCP
                        item_data[f'ICMS_{icms_type}_pFCP'] = self._to_float(self.find_element_text(icms_elem, 'pFCP'))
                        item_data[f'ICMS_{icms_type}_vFCP'] = self._to_float(self.find_element_text(icms_elem, 'vFCP'))
                        item_data[f'ICMS_{icms_type}_vBCFCP'] = self._to_float(self.find_element_text(icms_elem, 'vBCFCP'))
                        
                        # FCP ST
                        item_data[f'ICMS_{icms_type}_pFCPST'] = self._to_float(self.find_element_text(icms_elem, 'pFCPST'))
                        item_data[f'ICMS_{icms_type}_vFCPST'] = self._to_float(self.find_element_text(icms_elem, 'vFCPST'))
                        item_data[f'ICMS_{icms_type}_vBCFCPST'] = self._to_float(self.find_element_text(icms_elem, 'vBCFCPST'))
                        
                        # Desoneração
                        vICMSDeson = self.find_element_text(icms_elem, 'vICMSDeson')
                        if vICMSDeson:
                            item_data[f'ICMS_{icms_type}_vICMSDeson'] = self._to_float(vICMSDeson)
                            item_data[f'ICMS_{icms_type}_motDesICMS'] = self.find_element_text(icms_elem, 'motDesICMS')
                            item_data[f'ICMS_{icms_type}_indDeduzDeson'] = self.find_element_text(icms_elem, 'indDeduzDeson')
                        
                        # Desoneração ST
                        vICMSSTDeson = self.find_element_text(icms_elem, 'vICMSSTDeson')
                        if vICMSSTDeson:
                            item_data[f'ICMS_{icms_type}_vICMSSTDeson'] = self._to_float(vICMSSTDeson)
                            item_data[f'ICMS_{icms_type}_motDesICMSST'] = self.find_element_text(icms_elem, 'motDesICMSST')
                        
                        # ST
                        item_data[f'ICMS_{icms_type}_vBCST'] = self._to_float(self.find_element_text(icms_elem, 'vBCST'))
                        item_data[f'ICMS_{icms_type}_pICMSST'] = self._to_float(self.find_element_text(icms_elem, 'pICMSST'))
                        item_data[f'ICMS_{icms_type}_vICMSST'] = self._to_float(self.find_element_text(icms_elem, 'vICMSST'))
                        
                        # PARTILHA DO ICMS (DIFAL)
                        self.parse_partilha_icms(icms_elem, icms_type, item_data)
                        
                        # GTRIBREGULAR - NOVO REFORMA TRIBUTÁRIA
                        self.parse_gtribregular(icms_elem, icms_type, item_data)
                        
                        break  # Sair após encontrar o primeiro tipo de ICMS
                        
        except Exception as e:
            print(f"Erro ao parsear ICMS: {e}")

    def parse_ipi_item(self, imposto, item_data):
        """Parse do IPI"""
        try:
            ipi = self.find_element(imposto, 'IPI')
            if ipi is not None:
                item_data['IPI_vBC'] = self._to_float(self.find_element_text(ipi, 'vBC'))
                item_data['IPI_pIPI'] = self._to_float(self.find_element_text(ipi, 'pIPI'))
                item_data['IPI_vIPI'] = self._to_float(self.find_element_text(ipi, 'vIPI'))
                item_data['IPI_CST'] = self.find_element_text(ipi, 'CST')
        except Exception as e:
            print(f"Erro ao parsear IPI: {e}")

    def parse_pis_item(self, imposto, item_data):
        """Parse do PIS"""
        try:
            pis = self.find_element(imposto, 'PIS')
            if pis is not None:
                # Verificar tipos de PIS
                for pis_type in ['PISAliq', 'PISQtde', 'PISNT', 'PISOutr']:
                    pis_elem = self.find_element(pis, pis_type)
                    if pis_elem is not None:
                        item_data['PIS_CST'] = self.find_element_text(pis_elem, 'CST')
                        item_data['PIS_vBC'] = self._to_float(self.find_element_text(pis_elem, 'vBC'))
                        item_data['PIS_pPIS'] = self._to_float(self.find_element_text(pis_elem, 'pPIS'))
                        item_data['PIS_vPIS'] = self._to_float(self.find_element_text(pis_elem, 'vPIS'))
                        item_data['PIS_qBCProd'] = self._to_float(self.find_element_text(pis_elem, 'qBCProd'))
                        item_data['PIS_vAliqProd'] = self._to_float(self.find_element_text(pis_elem, 'vAliqProd'))
                        break
        except Exception as e:
            print(f"Erro ao parsear PIS: {e}")

    def parse_cofins_item(self, imposto, item_data):
        """Parse do COFINS"""
        try:
            cofins = self.find_element(imposto, 'COFINS')
            if cofins is not None:
                # Verificar tipos de COFINS
                for cofins_type in ['COFINSAliq', 'COFINSQtde', 'COFINSNT', 'COFINSOutr']:
                    cofins_elem = self.find_element(cofins, cofins_type)
                    if cofins_elem is not None:
                        item_data['COFINS_CST'] = self.find_element_text(cofins_elem, 'CST')
                        item_data['COFINS_vBC'] = self._to_float(self.find_element_text(cofins_elem, 'vBC'))
                        item_data['COFINS_pCOFINS'] = self._to_float(self.find_element_text(cofins_elem, 'pCOFINS'))
                        item_data['COFINS_vCOFINS'] = self._to_float(self.find_element_text(cofins_elem, 'vCOFINS'))
                        item_data['COFINS_qBCProd'] = self._to_float(self.find_element_text(cofins_elem, 'qBCProd'))
                        item_data['COFINS_vAliqProd'] = self._to_float(self.find_element_text(cofins_elem, 'vAliqProd'))
                        break
        except Exception as e:
            print(f"Erro ao parsear COFINS: {e}")

    def parse_ii_item(self, imposto, item_data):
        """Parse do Imposto de Importação"""
        try:
            ii = self.find_element(imposto, 'II')
            if ii is not None:
                item_data['II_vBC'] = self._to_float(self.find_element_text(ii, 'vBC'))
                item_data['II_vDespAdu'] = self._to_float(self.find_element_text(ii, 'vDespAdu'))
                item_data['II_vII'] = self._to_float(self.find_element_text(ii, 'vII'))
                item_data['II_vIOF'] = self._to_float(self.find_element_text(ii, 'vIOF'))
        except Exception as e:
            print(f"Erro ao parsear II: {e}")

    def parse_credito_presumido(self, prod, item_data):
        """Parse do grupo de crédito presumido - NOVO Reforma Tributária"""
        try:
            gCred = self.find_element(prod, 'gCred')
            if gCred is not None:
                item_data['gCred_cCredPresumido'] = self.find_element_text(gCred, 'cCredPresumido')
                item_data['gCred_pCredPresumido'] = self._to_float(self.find_element_text(gCred, 'pCredPresumido'))
                item_data['gCred_vCredPresumido'] = self._to_float(self.find_element_text(gCred, 'vCredPresumido'))
                print("Crédito Presumido encontrado")
        except Exception as e:
            print(f"Erro ao parsear crédito presumido: {e}")

    def parse_ibscbs_item(self, imposto, item_data):
        """Parse do IBSCBS por item - com tratamento para ausência"""
        try:
            ibscbs = self.find_element(imposto, 'IBSCBS')
            if ibscbs is not None:
                print("IBSCBS encontrado no item")
                
                # Campos básicos
                item_data['ibscbs_CST'] = self.find_element_text(ibscbs, 'CST')
                item_data['ibscbs_cClassTrib'] = self.find_element_text(ibscbs, 'cClassTrib')
                
                # Grupo gIBSCBS (pode não existir)
                gibscbs = self.find_element(ibscbs, 'gIBSCBS')
                if gibscbs is not None:
                    item_data['ibscbs_vBC'] = self._to_float(self.find_element_text(gibscbs, 'vBC'))
                    item_data['ibscbs_vIBS'] = self._to_float(self.find_element_text(gibscbs, 'vIBS'))
                    
                    # Subgrupos (podem não existir)
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
                else:
                    print("Grupo gIBSCBS não encontrado no item")
            else:
                print("IBSCBS não encontrado no item")
                # Marcar como não aplicável
                item_data['ibscbs_CST'] = 'NA'
                item_data['ibscbs_cClassTrib'] = 'NA'
                        
        except Exception as e:
            print(f"Erro ao parsear IBSCBS do item: {e}")

    def parse_nfe_xml(self, xml_content):
        """
        Parses an NFe XML string com todos os campos expandidos
        """
        try:
            root = ET.fromstring(xml_content)
            all_items_data = []
            
            # Encontrar infNFe
            nfe = self.find_element(root, 'NFe')
            inf_nfe = self.find_element(nfe, 'infNFe') if nfe is not None else self.find_element(root, 'infNFe')
            
            if inf_nfe is None:
                return []
            
            header_data = {}
            
            # Dados básicos da NFe
            header_data['Id'] = inf_nfe.get('Id')
            header_data['versao_nfe'] = inf_nfe.get('versao')
            
            # Identificação
            ide = self.find_element(inf_nfe, 'ide')
            if ide is not None:
                header_data.update({
                    'cUF': self.find_element_text(ide, 'cUF'),
                    'cNF': self.find_element_text(ide, 'cNF'),
                    'natOp': self.find_element_text(ide, 'natOp'),
                    'mod': self.find_element_text(ide, 'mod'),
                    'serie': self.find_element_text(ide, 'serie'),
                    'nNF': self.find_element_text(ide, 'nNF'),
                    'dhEmi': self.find_element_text(ide, 'dhEmi'),
                    'tpNF': self.find_element_text(ide, 'tpNF'),
                    'tpAmb': self.find_element_text(ide, 'tpAmb'),
                    'cMunFG': self.find_element_text(ide, 'cMunFG'),
                    'idDest': self.find_element_text(ide, 'idDest'),  # Importante para partilha
                    # NOVOS CAMPOS REFORMA
                    'cMunFGIBS': self.find_element_text(ide, 'cMunFGIBS'),
                    'tpNFDebito': self.find_element_text(ide, 'tpNFDebito'),
                    'tpNFCredito': self.find_element_text(ide, 'tpNFCredito')
                })
            
            # Emitente
            emit = self.find_element(inf_nfe, 'emit')
            if emit is not None:
                header_data.update({
                    'emit_CNPJ': self.find_element_text(emit, 'CNPJ'),
                    'emit_xNome': self.find_element_text(emit, 'xNome'),
                    'emit_IE': self.find_element_text(emit, 'IE'),
                    'emit_CRT': self.find_element_text(emit, 'CRT')
                })
            
            # Destinatário
            dest = self.find_element(inf_nfe, 'dest')
            if dest is not None:
                header_data.update({
                    'dest_CNPJ': self.find_element_text(dest, 'CNPJ'),
                    'dest_xNome': self.find_element_text(dest, 'xNome'),
                    'dest_IE': self.find_element_text(dest, 'IE'),
                    'dest_UF': self.find_element_text(self.find_element(dest, 'enderDest'), 'UF') if self.find_element(dest, 'enderDest') else None
                })
            
            # Totais
            total = self.find_element(inf_nfe, 'total')
            if total is not None:
                # ICMSTot
                ICMSTot = self.find_element(total, 'ICMSTot')
                if ICMSTot is not None:
                    header_data.update({
                        'total_vProd': self._to_float(self.find_element_text(ICMSTot, 'vProd')),
                        'total_vNF': self._to_float(self.find_element_text(ICMSTot, 'vNF')),
                        'total_vBC': self._to_float(self.find_element_text(ICMSTot, 'vBC')),
                        'total_vICMS': self._to_float(self.find_element_text(ICMSTot, 'vICMS')),
                        'total_vST': self._to_float(self.find_element_text(ICMSTot, 'vST')),
                        'total_vFCP': self._to_float(self.find_element_text(ICMSTot, 'vFCP')),
                        'total_vFCPST': self._to_float(self.find_element_text(ICMSTot, 'vFCPST')),
                        'total_vIPI': self._to_float(self.find_element_text(ICMSTot, 'vIPI')),
                        'total_vPIS': self._to_float(self.find_element_text(ICMSTot, 'vPIS')),
                        'total_vCOFINS': self._to_float(self.find_element_text(ICMSTot, 'vCOFINS')),
                        # Campos da Partilha nos totais
                        'total_vFCPUFDest': self._to_float(self.find_element_text(ICMSTot, 'vFCPUFDest')),
                        'total_vICMSUFDest': self._to_float(self.find_element_text(ICMSTot, 'vICMSUFDest')),
                        'total_vICMSUFRemet': self._to_float(self.find_element_text(ICMSTot, 'vICMSUFRemet'))
                    })
                
                # vNFTot 
                header_data['total_vNFTot'] = self._to_float(self.find_element_text(total, 'vNFTot'))
            
            # Processar itens
            det_elements = self.find_all_elements(inf_nfe, 'det')
            
            for det in det_elements:
                item_data = header_data.copy()
                item_data['nItem'] = det.get('nItem')
                
                # Produto
                prod = self.find_element(det, 'prod')
                if prod is not None:
                    item_data.update({
                        'cProd': self.find_element_text(prod, 'cProd'),
                        'xProd': self.find_element_text(prod, 'xProd'),
                        'NCM': self.find_element_text(prod, 'NCM'),
                        'CFOP': self.find_element_text(prod, 'CFOP'),
                        'uCom': self.find_element_text(prod, 'uCom'),
                        'qCom': self._to_float(self.find_element_text(prod, 'qCom')),
                        'vUnCom': self._to_float(self.find_element_text(prod, 'vUnCom')),
                        'vProd': self._to_float(self.find_element_text(prod, 'vProd')),
                        'vFrete': self._to_float(self.find_element_text(prod, 'vFrete')),
                        'vSeg': self._to_float(self.find_element_text(prod, 'vSeg')),
                        'vDesc': self._to_float(self.find_element_text(prod, 'vDesc')),
                        'vOutro': self._to_float(self.find_element_text(prod, 'vOutro')),
                        'indTot': self.find_element_text(prod, 'indTot'),
                        # NOVO - Campos Reforma
                        'tpCredPresIBSZFM': self.find_element_text(prod, 'tpCredPresIBSZFM')
                    })
                    
                    # Crédito Presumido
                    self.parse_credito_presumido(prod, item_data)
                
                # vItem - NOVO CAMPO
                item_data['vItem'] = self._to_float(self.find_element_text(det, 'vItem'))
                
                # Impostos
                imposto = self.find_element(det, 'imposto')
                if imposto is not None:
                    # vTotTrib
                    item_data['vTotTrib'] = self._to_float(self.find_element_text(imposto, 'vTotTrib'))
                    
                    # Parse de todos os impostos
                    self.parse_icms_item(imposto, item_data)
                    self.parse_ipi_item(imposto, item_data)
                    self.parse_pis_item(imposto, item_data)
                    self.parse_cofins_item(imposto, item_data)
                    self.parse_ii_item(imposto, item_data)
                    self.parse_ibscbs_item(imposto, item_data)
                
                all_items_data.append(item_data)
            
            return all_items_data
            
        except Exception as e:
            print(f" Erro ao processar XML: {e}")
            import traceback
            traceback.print_exc()
            return []

def criar_aba_estatisticas(df):
    """Cria aba de estatísticas para o Excel"""
    estatisticas = []
    
    # Estatísticas básicas
    estatisticas.append({'Estatística': 'Total de NFes', 'Valor': df['nNF'].nunique()})
    estatisticas.append({'Estatística': 'Total de Itens', 'Valor': len(df)})
    estatisticas.append({'Estatística': 'Total de Emitentes', 'Valor': df['emit_xNome'].nunique()})
    
    # Valores totais
    if 'vProd' in df.columns:
        estatisticas.append({'Estatística': 'Valor Total Produtos (R$)', 'Valor': f"R$ {df['vProd'].sum():,.2f}"})
    if 'total_vNF' in df.columns:
        estatisticas.append({'Estatística': 'Valor Total NF (R$)', 'Valor': f"R$ {df['total_vNF'].sum():,.2f}"})
    if 'total_vNFTot' in df.columns:
        estatisticas.append({'Estatística': 'Valor Total NFTot (R$)', 'Valor': f"R$ {df['total_vNFTot'].sum():,.2f}"})
    
    # Tributos totais
    campos_tributos = {
        'total_vICMS': 'ICMS Total',
        'total_vIPI': 'IPI Total', 
        'total_vPIS': 'PIS Total',
        'total_vCOFINS': 'COFINS Total',
        'total_vFCP': 'FCP Total',
        'total_vFCPUFDest': 'FCP UF Destino Total',
        'total_vICMSUFDest': 'ICMS UF Destino Total',
        'total_vICMSUFRemet': 'ICMS UF Remetente Total'
    }
    
    for campo, nome in campos_tributos.items():
        if campo in df.columns and df[campo].notna().any():
            estatisticas.append({'Estatística': f'{nome} (R$)', 'Valor': f"R$ {df[campo].sum():,.2f}"})
    
    return pd.DataFrame(estatisticas)

def criar_aba_resumo(df):
    """Cria aba de resumo para o Excel"""
    resumo_data = []
    
    # Resumo por NFe
    if 'nNF' in df.columns:
        nfes_agrupadas = df.groupby('nNF').agg({
            'emit_xNome': 'first',
            'dhEmi': 'first',
            'vProd': 'sum',
            'total_vNF': 'first',
            'total_vNFTot': 'first',
            'idDest': 'first'
        }).reset_index()
        
        for _, nfe in nfes_agrupadas.iterrows():
            tipo_destino = {
                '1': 'Operação Interna',
                '2': 'Operação Interestadual',
                '3': 'Operação com Exterior'
            }.get(nfe['idDest'], 'Desconhecido')
            
            resumo_data.append({
                'Tipo': 'NFe',
                'Número': nfe['nNF'],
                'Emitente': nfe['emit_xNome'],
                'Data': nfe['dhEmi'],
                'Tipo Destino': tipo_destino,
                'Valor Produtos': nfe['vProd'],
                'Valor NF': nfe['total_vNF'],
                'Valor NFTot': nfe['total_vNFTot']
            })
    
    # Totais gerais
    resumo_data.append({
        'Tipo': 'TOTAL GERAL',
        'Número': '',
        'Emitente': '',
        'Data': '',
        'Tipo Destino': '',
        'Valor Produtos': df['vProd'].sum() if 'vProd' in df.columns else 0,
        'Valor NF': df['total_vNF'].sum() if 'total_vNF' in df.columns else 0,
        'Valor NFTot': df['total_vNFTot'].sum() if 'total_vNFTot' in df.columns else 0
    })
    
    return pd.DataFrame(resumo_data)

def processar_pasta_xmls(caminho_pasta, extensao='.xml'):
    """
    Processa todos os arquivos XML em uma pasta
    """
    parser = NFeParser()
    todos_dados = []
    
    arquivos_xml = glob.glob(os.path.join(caminho_pasta, f'*{extensao}'))
    print(f" Encontrados {len(arquivos_xml)} arquivos XML")
    
    for i, arquivo in enumerate(arquivos_xml, 1):
        try:
            print(f"\n{'='*50}")
            print(f" Processando {i}/{len(arquivos_xml)}: {os.path.basename(arquivo)}")
            
            with open(arquivo, 'r', encoding='utf-8') as file:
                xml_content = file.read()
            
            dados_nfe = parser.parse_nfe_xml(xml_content)
            
            if dados_nfe:
                todos_dados.extend(dados_nfe)
                print(f" {len(dados_nfe)} itens extraídos")
            else:
                print(f" Nenhum item extraído")
                
        except Exception as e:
            print(f" Erro ao processar {arquivo}: {e}")
    
    if todos_dados:
        df = pd.DataFrame(todos_dados)
        print(f"\n PROCESSAMENTO CONCLUÍDO!")
        print(f" Total de registros: {len(df)}")
        print(f" Total de colunas: {len(df.columns)}")
        
        # Ordenar colunas para melhor visualização
        df = ordenar_colunas_dataframe(df)
        
        # Estatísticas
        analisar_dados_completos(df)
        
        return df
    else:
        return pd.DataFrame()

def ordenar_colunas_dataframe(df):
    """Ordena as colunas do DataFrame de forma lógica"""
    colunas_prioridade = [
        'Id', 'nItem', 'cProd', 'xProd', 'NCM', 'CFOP', 'vProd', 'vItem',
        'natOp', 'mod', 'serie', 'nNF', 'dhEmi', 'tpNF', 'idDest', 'emit_CNPJ', 'emit_xNome',
        'total_vProd', 'total_vNF', 'total_vNFTot'
    ]
    
    # Colunas existentes na ordem de prioridade
    colunas_ordenadas = []
    for col in colunas_prioridade:
        if col in df.columns:
            colunas_ordenadas.append(col)
    
    # Adicionar colunas restantes em ordem alfabética
    colunas_restantes = sorted([col for col in df.columns if col not in colunas_ordenadas])
    colunas_ordenadas.extend(colunas_restantes)
    
    return df[colunas_ordenadas]

def analisar_dados_completos(df):
    """Analisa todos os dados extraidos"""
    print(f"\n ANÁLISE COMPLETA DOS DADOS:")
    
    # Campos básicos
    print(f" CAMPOS BASICOS:")
    print(f"   • Total de NFes: {df['nNF'].nunique()}")
    print(f"   • Total de itens: {len(df)}")
    print(f"   • Emitentes: {df['emit_xNome'].nunique()}")
    
    # Tipo de destino (importante para partilha)
    if 'idDest' in df.columns:
        destinos = df['idDest'].value_counts()
        print(f"   • Tipo de Destino:")
        for dest, count in destinos.items():
            tipo = {
                '1': 'Operação Interna',
                '2': 'Operação Interestadual', 
                '3': 'Operação com Exterior'
            }.get(dest, f'Desconhecido ({dest})')
            print(f"     - {tipo}: {count} registros")
    
    # Valores monetários
    print(f"\n VALORES MONETARIOS:")
    campos_valores = ['vProd', 'vItem', 'total_vNF', 'total_vNFTot', 'total_vProd']
    for campo in campos_valores:
        if campo in df.columns and df[campo].notna().any():
            print(f"   • {campo}: R$ {df[campo].sum():,.2f}")
    
    # Tributos
    print(f"\n TRIBUTOS:")
    campos_tributos = ['total_vICMS', 'total_vIPI', 'total_vPIS', 'total_vCOFINS', 'total_vFCP']
    for campo in campos_tributos:
        if campo in df.columns and df[campo].notna().any():
            print(f"   • {campo}: R$ {df[campo].sum():,.2f}")
    
    # Partilha do ICMS
    print(f"\n PARTILHA DO ICMS (DIFAL):")
    campos_partilha_totais = ['total_vFCPUFDest', 'total_vICMSUFDest', 'total_vICMSUFRemet']
    for campo in campos_partilha_totais:
        if campo in df.columns and df[campo].notna().any():
            print(f"   • {campo}: R$ {df[campo].sum():,.2f}")
    
    # Verificar partilha por item
    partilha_campos = [col for col in df.columns if 'Partilha' in col]
    if partilha_campos:
        print(f"   • Campos de partilha encontrados: {len(partilha_campos)}")
        for campo in partilha_campos[:5]:  # Mostrar primeiros 5
            count = df[campo].notna().sum()
            if count > 0:
                print(f"     - {campo}: presente em {count} registros")
    
    # GTribRegular
    print(f"\n GTRIBREGULAR - REFORMA TRIBUTARIA:")
    gtrib_campos = [col for col in df.columns if 'gTribRegular' in col]
    if gtrib_campos:
        print(f"   • Campos gTribRegular encontrados: {len(gtrib_campos)}")
        
        # Contar registros com dados do gTribRegular
        campos_principais = [col for col in gtrib_campos if 'CSTReg' in col or 'cClassTribReg' in col]
        if campos_principais:
            count_gtrib = df[campos_principais[0]].notna().sum()
            print(f"   • Registros com gTribRegular: {count_gtrib}")
            
            # Mostrar valores únicos de CSTReg
            cstreg_campos = [col for col in gtrib_campos if 'CSTReg' in col]
            if cstreg_campos:
                cst_values = df[cstreg_campos[0]].dropna().unique()
                if len(cst_values) > 0:
                    print(f"   • Valores de CSTReg encontrados: {', '.join(map(str, cst_values))}")
    
    # Reforma TributAria
    print(f"\n REFORMA TRIBUTARIA:")
    campos_reforma = ['cMunFGIBS', 'tpNFDebito', 'tpNFCredito', 'tpCredPresIBSZFM', 'gCred_vCredPresumido']
    for campo in campos_reforma:
        if campo in df.columns:
            count = df[campo].notna().sum()
            if count > 0:
                print(f"   • {campo}: presente em {count} registros")
            else:
                print(f"   • {campo}: não encontrado")

# USO
if __name__ == "__main__":
    caminho = r"C:\Users\08748D631\Desktop\nfe_xml"
    
    print("INICIANDO PROCESSAMENTO NF-e 4.00 COMPLETO")
    print("INCLUINDO: FCP, Desoneração, Reforma Tributária, IBSCBS, vItem, vNFTot, PARTILHA ICMS (DIFAL), GTRIBREGULAR")
    
    df = processar_pasta_xmls(caminho)
    
    if not df.empty:
        # Exportar
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        excel_file = f"nfe_completa_expandida_{timestamp}.xlsx"
        csv_file = f"nfe_completa_expandida_{timestamp}.csv"
        
        try:
            # Exportar para Excel com multiplas abas
            with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='NFes_Completas', index=False)
                
                # Criar aba de resumo
                resumo = criar_aba_resumo(df)
                resumo.to_excel(writer, sheet_name='Resumo', index=False)
                
                # Criar aba de estatísticas
                estatisticas = criar_aba_estatisticas(df)
                estatisticas.to_excel(writer, sheet_name='Estatisticas', index=False)
            
            print(f" Excel exportado com sucesso: {excel_file}")
            
        except Exception as e:
            print(f" Erro ao exportar Excel: {e}")
            # Exportar apenas CSV se houver erro no Excel
            excel_file = None
        
        # Exportar para CSV
        df.to_csv(csv_file, index=False, encoding='utf-8-sig')
        print(f" CSV exportado com sucesso: {csv_file}")
        
        print(f"\n ARQUIVOS EXPORTADOS:")
        if excel_file:
            print(f"   Excel: {excel_file}")
        print(f"   CSV: {csv_file}")
        
        # Mostrar amostra
        print(f"\n AMOSTRA DOS DADOS (primeiras 5 linhas):")
        colunas_amostra = ['nItem', 'xProd', 'vProd', 'vItem', 'total_vNF', 'total_vNFTot', 'idDest']
        colunas_disponiveis = [col for col in colunas_amostra if col in df.columns]
        if colunas_disponiveis:
            print(df[colunas_disponiveis].head())
        
        # Mostrar colunas disponiveis
        print(f"\n COLUNAS DISPONIVEIS ({len(df.columns)} no total):")
        print(", ".join(df.columns.tolist()[:20]))  # Primeiras 20 colunas
        if len(df.columns) > 20:
            print(f"... e mais {len(df.columns) - 20} colunas")
        
    else:
        print("\n Nenhum dado processado.")