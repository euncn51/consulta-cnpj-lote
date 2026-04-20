import xml.etree.ElementTree as ET
import os
import pandas as pd
from datetime import datetime
import glob
import numpy as np
from decimal import Decimal
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

# =============================================================================
# 1. GRUPO DE INFORMAÇÕES DO EMITENTE
# =============================================================================

@dataclass
class EnderecoEmitente:
    """Grupo de endereço do emitente"""
    xLgr: str
    nro: str
    xBairro: str
    cMun: str
    xMun: str
    UF: str
    CEP: str
    cPais: Optional[str] = "1058"
    xPais: Optional[str] = "BRASIL"
    fone: Optional[str] = None

@dataclass
class Emitente:
    """Grupo do emitente (emit)"""
    CNPJ: Optional[str] = None
    CPF: Optional[str] = None
    xNome: str = None
    xFant: Optional[str] = None
    enderEmit: Optional[EnderecoEmitente] = None
    IE: str = None
    IEST: Optional[str] = None
    IM: Optional[str] = None
    CNAE: Optional[str] = None
    CRT: str = None

# =============================================================================
# 2. GRUPO DE INFORMAÇÕES DE IDENTIFICAÇÃO DA NF-E
# =============================================================================

@dataclass
class IdentificacaoNFE:
    """Grupo de identificação da NF-e (ide)"""
    cUF: str
    cNF: str
    natOp: str
    mod: str
    serie: str
    nNF: str
    dhEmi: str
    dhSaiEnt: Optional[str] = None
    dPrevEntrega: Optional[str] = None
    tpNF: str = None
    idDest: str = None
    cMunFG: str = None
    cMunFGIBS: Optional[str] = None
    tpImp: str = None
    tpEmis: str = None
    cDV: str = None
    tpAmb: str = None
    finNFe: str = None
    tpNFDebito: Optional[str] = None
    tpNFCredito: Optional[str] = None
    indFinal: str = None
    indPres: str = None
    indIntermed: Optional[str] = None
    procEmi: str = None
    verProc: str = None
    dhCont: Optional[str] = None
    xJust: Optional[str] = None

# =============================================================================
# 3. GRUPO DE INFORMAÇÕES DO DESTINATÁRIO
# =============================================================================

@dataclass
class EnderecoDestinatario:
    """Grupo de endereço do destinatário"""
    xLgr: str
    nro: str
    xBairro: str
    cMun: str
    xMun: str
    UF: str
    CEP: str
    cPais: Optional[str] = "1058"
    xPais: Optional[str] = "BRASIL"
    fone: Optional[str] = None

@dataclass
class Destinatario:
    """Grupo do destinatário (dest)"""
    CNPJ: Optional[str] = None
    CPF: Optional[str] = None
    idEstrangeiro: Optional[str] = None
    xNome: Optional[str] = None
    enderDest: Optional[EnderecoDestinatario] = None
    indIEDest: str = None
    IE: Optional[str] = None
    ISUF: Optional[str] = None
    IM: Optional[str] = None
    email: Optional[str] = None

# =============================================================================
# 4. GRUPO DE ITEM DA NF-E
# =============================================================================

# 4.1 DETALHE DO PRODUTO
@dataclass
class CreditoPresumido:
    """Grupo de Crédito Presumido (gCred) - NOVO Reforma Tributária"""
    cCredPresumido: str
    pCredPresumido: Decimal
    vCredPresumido: Decimal

@dataclass
class Produto:
    """Grupo de produtos (det/prod)"""
    nItem: int
    cProd: str
    cEAN: str
    cBarra: Optional[str] = None
    xProd: str = None
    NCM: str = None
    NVE: Optional[str] = None
    CEST: Optional[str] = None
    indEscala: Optional[str] = None
    CNPJFab: Optional[str] = None
    cBenef: Optional[str] = None
    EXTIPI: Optional[str] = None
    CFOP: str = None
    uCom: str = None
    qCom: Decimal = None
    vUnCom: Decimal = None
    vProd: Decimal = None
    cEANTrib: str = None
    cBarraTrib: Optional[str] = None
    uTrib: str = None
    qTrib: Decimal = None
    vUnTrib: Decimal = None
    vFrete: Optional[Decimal] = None
    vSeg: Optional[Decimal] = None
    vDesc: Optional[Decimal] = None
    vOutro: Optional[Decimal] = None
    indTot: str = None
    indBemMovelUsado: Optional[str] = None
    tpCredPresIBSZFM: Optional[str] = None
    gCred: Optional[CreditoPresumido] = None

# 4.2 DETALHE DO ICMS
@dataclass
class PartilhaICMS:
    """Grupo de Partilha do ICMS (DIFAL) - Para operações interestaduais"""
    vBCUFDest: Optional[Decimal] = None
    pFCPUFDest: Optional[Decimal] = None
    pICMSUFDest: Optional[Decimal] = None
    pICMSInter: Optional[Decimal] = None
    pICMSInterPart: Optional[Decimal] = None
    vFCPUFDest: Optional[Decimal] = None
    vICMSUFDest: Optional[Decimal] = None
    vICMSUFRemet: Optional[Decimal] = None

@dataclass
class DesoneracaoICMS:
    """Grupo de desoneração do ICMS"""
    vICMSDeson: Decimal
    motDesICMS: str
    indDeduzDeson: Optional[str] = None

@dataclass
class ICMS00:
    """ICMS00 - Tributada integralmente"""
    orig: str
    CST: str = "00"
    modBC: str = None
    vBC: Decimal = None
    pICMS: Decimal = None
    vICMS: Decimal = None
    pFCP: Optional[Decimal] = None
    vFCP: Optional[Decimal] = None
    partilha: Optional[PartilhaICMS] = None

@dataclass
class ICMS20:
    """ICMS20 - Com redução de base de cálculo"""
    orig: str
    CST: str = "20"
    modBC: str = None
    pRedBC: Decimal = None
    vBC: Decimal = None
    pICMS: Decimal = None
    vICMS: Decimal = None
    pFCP: Optional[Decimal] = None
    vFCP: Optional[Decimal] = None
    vBCFCP: Optional[Decimal] = None
    desoneracao: Optional[DesoneracaoICMS] = None
    partilha: Optional[PartilhaICMS] = None

# 4.3 DETALHE DO PIS
@dataclass
class PISAliq:
    """PIS Alíquota"""
    CST: str
    vBC: Decimal
    pPIS: Decimal
    vPIS: Decimal

# 4.4 DETALHE DO COFINS
@dataclass
class COFINSAliq:
    """COFINS Alíquota"""
    CST: str
    vBC: Decimal
    pCOFINS: Decimal
    vCOFINS: Decimal

# 4.5 DETALHE DO IBSCBS
@dataclass
class GTribRegular:
    """Grupo de Tributação Regular (gTribRegular) - NOVO Reforma Tributária"""
    CSTReg: str
    cClassTribReg: str
    pAliqEfetRegIBSUF: Decimal
    vTribRegIBSUF: Decimal
    pAliqEfetRegIBSMun: Decimal
    vTribRegIBSMun: Decimal
    pAliqEfetRegCBS: Decimal
    vTribRegCBS: Decimal

# 4.6 DETALHE DO IMPOSTO (CONSOLIDADO)
@dataclass
class ImpostoProduto:
    """Grupo de impostos do produto - Consolidado"""
    vTotTrib: Optional[Decimal] = None
    ICMS: Optional[Any] = None
    PIS: Optional[Any] = None
    COFINS: Optional[Any] = None
    gTribRegular: Optional[GTribRegular] = None
    ISSQN: Optional[Any] = None

# 4.7 DETALHE DO ITEM (CONSOLIDADO)
@dataclass
class ItemNFE:
    """Item completo da NF-e (det) - Consolidado"""
    produto: Produto
    imposto: ImpostoProduto

# =============================================================================
# 5. GRUPO DE TOTAIS DA NF-E
# =============================================================================

# 5.1 GRUPO DE ICMSTot
@dataclass
class ICMSTot:
    """Grupo de totais do ICMS"""
    vBC: Decimal
    vICMS: Decimal
    vICMSDeson: Decimal
    vFCPUFDest: Decimal
    vICMSUFDest: Decimal
    vICMSUFRemet: Decimal
    vFCP: Decimal
    vBCST: Decimal
    vST: Decimal
    vFCPST: Decimal
    vFCPSTRet: Decimal
    vProd: Decimal
    vFrete: Decimal
    vSeg: Decimal
    vDesc: Decimal
    vII: Decimal
    vIPI: Decimal
    vIPIDevol: Decimal
    vPIS: Decimal
    vCOFINS: Decimal
    vOutro: Decimal
    vNF: Decimal
    vTotTrib: Decimal

# 5.2 GRUPO DE IBSCBSTot
@dataclass
class IBSCBSTot:
    """Grupo de totais do IBS/CBS - NOVO Reforma Tributária"""
    vTotTribIBSUF: Decimal
    vTotTribIBSMun: Decimal
    vTotTribCBS: Decimal

# 5.3 GRUPO DE TOTAL (CONSOLIDADO)
@dataclass
class TotalNFE:
    """Grupo de totais da NF-e (total) - Consolidado"""
    ICMSTot: Optional[ICMSTot] = None
    IBSCBSTot: Optional[IBSCBSTot] = None
    ISSQNTot: Optional[Any] = None
    retTrib: Optional[Any] = None

# =============================================================================
# 6. GRUPO DE INFORMAÇÕES DO TRANSPORTE
# =============================================================================

@dataclass
class Transportador:
    """Grupo do transportador"""
    CNPJ: Optional[str] = None
    CPF: Optional[str] = None
    xNome: str = None
    IE: Optional[str] = None
    xEnder: Optional[str] = None
    xMun: Optional[str] = None
    UF: Optional[str] = None

@dataclass
class Transporte:
    """Grupo de transporte"""
    modFrete: str
    transporta: Optional[Transportador] = None
    veicTransp: Optional[Any] = None

# =============================================================================
# 7. GRUPO DE INFORMAÇÕES DO PAGAMENTO
# =============================================================================

@dataclass
class DetalhePagamento:
    """Grupo de detalhe do pagamento"""
    tPag: str
    vPag: Decimal
    indPag: Optional[str] = None

@dataclass
class Pagamento:
    """Grupo de pagamento (pag)"""
    detPag: List[DetalhePagamento] = None
    vTroco: Optional[Decimal] = None

# =============================================================================
# ESTRUTURA COMPLETA DA NF-E
# =============================================================================

@dataclass
class NFE:
    """Estrutura completa da NF-e"""
    # 1. Emitente
    emitente: Emitente
    # 2. Identificação
    identificacao: IdentificacaoNFE
    # 3. Destinatário
    destinatario: Optional[Destinatario] = None
    # 4. Itens
    itens: List[ItemNFE] = None
    # 5. Totais
    total: Optional[TotalNFE] = None
    # 6. Transporte
    transporte: Optional[Transporte] = None
    # 7. Pagamento
    pagamento: Optional[Pagamento] = None
    
    def __post_init__(self):
        if self.itens is None:
            self.itens = []

# =============================================================================
# PARSER PRINCIPAL
# =============================================================================

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
        elem = parent.find(f'nfe:{tag_name}', self.namespaces)
        if elem is None:
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
        elems = parent.findall(f'nfe:{tag_name}', self.namespaces)
        if not elems:
            elems = parent.findall(tag_name)
        return elems

    def _to_float(self, value):
        """Converte string para float seguro"""
        try:
            return float(value) if value else None
        except (ValueError, TypeError):
            return None

    # =============================================================================
    # 1. GRUPO DE INFORMAÇÕES DO EMITENTE
    # =============================================================================

    def parse_emitente(self, inf_nfe, header_data):
        """Parse do grupo do emitente"""
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
            print(f"Erro ao parsear emitente: {e}")

    # =============================================================================
    # 2. GRUPO DE INFORMAÇÕES DE IDENTIFICAÇÃO DA NF-E
    # =============================================================================

    def parse_identificacao(self, inf_nfe, header_data):
        """Parse do grupo de identificação da NF-e"""
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
                    # NOVOS CAMPOS REFORMA TRIBUTÁRIA
                    'cMunFGIBS': 'cMunFGIBS',
                    'tpNFDebito': 'tpNFDebito',
                    'tpNFCredito': 'tpNFCredito'
                }
                
                for field_key, xml_tag in identificacao_fields.items():
                    value = self.find_element_text(ide, xml_tag)
                    if value:
                        header_data[field_key] = value
                        
        except Exception as e:
            print(f"Erro ao parsear identificação: {e}")

    # =============================================================================
    # 3. GRUPO DE INFORMAÇÕES DO DESTINATÁRIO
    # =============================================================================

    def parse_destinatario(self, inf_nfe, header_data):
        """Parse do grupo do destinatário"""
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
            print(f"Erro ao parsear destinatário: {e}")

    # =============================================================================
    # 4. GRUPO DE ITEM DA NF-E
    # =============================================================================

    # 4.1 DETALHE DO PRODUTO
    def parse_produto(self, prod, item_data):
        """Parse do grupo do produto"""
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
                self.parse_credito_presumido(prod, item_data)
                        
        except Exception as e:
            print(f"Erro ao parsear produto: {e}")

    def parse_credito_presumido(self, prod, item_data):
        """Parse do grupo de crédito presumido - NOVO Reforma Tributária"""
        try:
            gCred = self.find_element(prod, 'gCred')
            if gCred is not None:
                item_data['gCred_cCredPresumido'] = self.find_element_text(gCred, 'cCredPresumido')
                item_data['gCred_pCredPresumido'] = self._to_float(self.find_element_text(gCred, 'pCredPresumido'))
                item_data['gCred_vCredPresumido'] = self._to_float(self.find_element_text(gCred, 'vCredPresumido'))
        except Exception as e:
            print(f"Erro ao parsear crédito presumido: {e}")

    # 4.2 DETALHE DO ICMS
    def parse_partilha_icms(self, icms_elem, icms_type, item_data):
        """Parse da Partilha do ICMS (DIFAL)"""
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
            print(f"Erro ao parsear partilha ICMS: {e}")

    def parse_gtribregular(self, gibscbs_elem, item_data):
        """Parse do grupo de tributação regular (gTribRegular) - NOVO Reforma Tributária"""
        try:
            gTribRegular = self.find_element(gibscbs_elem, 'gTribRegular')
            if gTribRegular is not None:
                print("gTribRegular encontrado no item")
                
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
                        print(f"  {field_key}: {value}")
            else:
                print("gTribRegular não encontrado dentro do gIBSCBS")
                
        except Exception as e:
            print(f"Erro ao parsear gTribRegular: {e}")

    def parse_icms_item(self, imposto, item_data):
        """Parse completo do ICMS"""
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
                                item_data[field_key] = self._to_float(value) if field_key not in ['CST', 'CSOSN', 'orig'] else value
                        
                        # Desoneração
                        vICMSDeson = self.find_element_text(icms_elem, 'vICMSDeson')
                        if vICMSDeson:
                            item_data[f'ICMS_{icms_type}_vICMSDeson'] = self._to_float(vICMSDeson)
                            item_data[f'ICMS_{icms_type}_motDesICMS'] = self.find_element_text(icms_elem, 'motDesICMS')
                        
                        # PARTILHA DO ICMS (DIFAL)
                        self.parse_partilha_icms(icms_elem, icms_type, item_data)
                        
                        break
                    
        except Exception as e:
            print(f"Erro ao parsear ICMS: {e}")

    # 4.3 DETALHE DO PIS
    def parse_pis_item(self, imposto, item_data):
        """Parse do PIS"""
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
            print(f"Erro ao parsear PIS: {e}")

    # 4.4 DETALHE DO COFINS
    def parse_cofins_item(self, imposto, item_data):
        """Parse do COFINS"""
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
            print(f"Erro ao parsear COFINS: {e}")

    # 4.5 DETALHE DO IBSCBS - COM VALIDAÇÃO COMPLETA
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
                    
                    # AGORA PROCURA gTribRegular DENTRO DO gIBSCBS
                    self.parse_gtribregular(gibscbs, item_data)
                else:
                    print("Grupo gIBSCBS não encontrado no item")
            else:
                print("IBSCBS não encontrado no item")
                # Marcar como não aplicável
                item_data['ibscbs_CST'] = 'NA'
                item_data['ibscbs_cClassTrib'] = 'NA'
                    
        except Exception as e:
            print(f"Erro ao parsear IBSCBS do item: {e}")

    # 4.6 DETALHE DO IMPOSTO (CONSOLIDADO)
    def parse_impostos_item(self, imposto, item_data):
        """Parse consolidado de todos os impostos do item"""
        try:
            if imposto is not None:
                item_data['vTotTrib'] = self._to_float(self.find_element_text(imposto, 'vTotTrib'))
                
                self.parse_icms_item(imposto, item_data)
                self.parse_pis_item(imposto, item_data)
                self.parse_cofins_item(imposto, item_data)
                self.parse_ibscbs_item(imposto, item_data)
                
        except Exception as e:
            print(f"Erro ao parsear impostos consolidados: {e}")

    # 4.7 DETALHE DO ITEM (CONSOLIDADO)
    def parse_itens(self, inf_nfe, header_data):
        """Parse consolidado de todos os itens da NF-e"""
        try:
            all_items_data = []
            det_elements = self.find_all_elements(inf_nfe, 'det')
            
            for det in det_elements:
                item_data = header_data.copy()
                item_data['nItem'] = det.get('nItem')
                
                # 4.1 Produto
                prod = self.find_element(det, 'prod')
                self.parse_produto(prod, item_data)
                
                # vItem
                item_data['vItem'] = self._to_float(self.find_element_text(det, 'vItem'))
                
                # 4.6 Impostos Consolidados
                imposto = self.find_element(det, 'imposto')
                self.parse_impostos_item(imposto, item_data)
                
                all_items_data.append(item_data)
            
            return all_items_data
            
        except Exception as e:
            print(f"Erro ao parsear itens: {e}")
            return []

    # =============================================================================
    # 5. GRUPO DE TOTAIS DA NF-E
    # =============================================================================

    def parse_totais(self, inf_nfe, header_data):
        """Parse do grupo de totais da NF-e"""
        try:
            total = self.find_element(inf_nfe, 'total')
            if total is not None:
                self.parse_icms_tot(total, header_data)
                self.parse_ibscbs_tot(total, header_data)
                
        except Exception as e:
            print(f"Erro ao parsear totais: {e}")

    # 5.1 GRUPO DE ICMSTot
    def parse_icms_tot(self, total, header_data):
        """Parse do grupo ICMSTot"""
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
            print(f"Erro ao parsear ICMSTot: {e}")

    # 5.2 GRUPO DE IBSCBSTot
    def parse_ibscbs_tot(self, total, header_data):
        """Parse do grupo IBSCBSTot"""
        try:
            IBSCBSTot = self.find_element(total, 'IBSCBSTot')
            if IBSCBSTot is not None:
                ibscbs_tot_fields = {
                    'total_vTotTribIBSUF': 'vTotTribIBSUF',
                    'total_vTotTribIBSMun': 'vTotTribIBSMun',
                    'total_vTotTribCBS': 'vTotTribCBS'
                }
                
                for field_key, xml_tag in ibscbs_tot_fields.items():
                    value = self.find_element_text(IBSCBSTot, xml_tag)
                    if value:
                        header_data[field_key] = self._to_float(value)
                        
        except Exception as e:
            print(f"Erro ao parsear IBSCBSTot: {e}")

    # =============================================================================
    # 6. GRUPO DE INFORMAÇÕES DO TRANSPORTE
    # =============================================================================

    def parse_transporte(self, inf_nfe, header_data):
        """Parse do grupo de transporte"""
        try:
            transp = self.find_element(inf_nfe, 'transp')
            if transp is not None:
                header_data['transp_modFrete'] = self.find_element_text(transp, 'modFrete')
                
                transporta = self.find_element(transp, 'transporta')
                if transporta is not None:
                    header_data['transp_transporta_xNome'] = self.find_element_text(transporta, 'xNome')
                    header_data['transp_transporta_IE'] = self.find_element_text(transporta, 'IE')
                    
        except Exception as e:
            print(f"Erro ao parsear transporte: {e}")

    # =============================================================================
    # 7. GRUPO DE INFORMAÇÕES DO PAGAMENTO
    # =============================================================================

    def parse_pagamento(self, inf_nfe, header_data):
        """Parse do grupo de pagamento"""
        try:
            pag = self.find_element(inf_nfe, 'pag')
            if pag is not None:
                det_pag_elements = self.find_all_elements(pag, 'detPag')
                if det_pag_elements:
                    det_pag = det_pag_elements[0]
                    header_data['pag_detPag_tPag'] = self.find_element_text(det_pag, 'tPag')
                    header_data['pag_detPag_vPag'] = self._to_float(self.find_element_text(det_pag, 'vPag'))
                            
        except Exception as e:
            print(f"Erro ao parsear pagamento: {e}")

    # =============================================================================
    # MÉTODO PRINCIPAL DE PARSE
    # =============================================================================

    def parse_nfe_xml(self, xml_content):
        """
        Parses an NFe XML string seguindo a ordem do schema da NF-e
        """
        try:
            root = ET.fromstring(xml_content)
            all_items_data = []
            
            nfe = self.find_element(root, 'NFe')
            inf_nfe = self.find_element(nfe, 'infNFe') if nfe is not None else self.find_element(root, 'infNFe')
            
            if inf_nfe is None:
                return []
            
            header_data = {}
            
            header_data['Id'] = inf_nfe.get('Id')
            header_data['versao_nfe'] = inf_nfe.get('versao')
            
            # 1. GRUPO DE INFORMAÇÕES DO EMITENTE
            self.parse_emitente(inf_nfe, header_data)
            
            # 2. GRUPO DE INFORMAÇÕES DE IDENTIFICAÇÃO DA NF-E
            self.parse_identificacao(inf_nfe, header_data)
            
            # 3. GRUPO DE INFORMAÇÕES DO DESTINATÁRIO
            self.parse_destinatario(inf_nfe, header_data)
            
            # 5. GRUPO DE TOTAIS DA NF-E
            self.parse_totais(inf_nfe, header_data)
            
            # 6. GRUPO DE INFORMAÇÕES DO TRANSPORTE
            self.parse_transporte(inf_nfe, header_data)
            
            # 7. GRUPO DE INFORMAÇÕES DO PAGAMENTO
            self.parse_pagamento(inf_nfe, header_data)
            
            # 4. GRUPO DE ITEM DA NF-E
            all_items_data = self.parse_itens(inf_nfe, header_data)
            
            return all_items_data
            
        except Exception as e:
            print(f" Erro ao processar XML: {e}")
            import traceback
            traceback.print_exc()
            return []

# =============================================================================
# FUNÇÕES DE EXPORTAÇÃO MELHORADAS
# =============================================================================

def ordenar_colunas_por_schema(df):
    """Ordena as colunas do DataFrame conforme o schema da NF-e"""
    
    ordem_schema = [
        # 1. IDENTIFICAÇÃO DA NF-E
        'Id', 'versao_nfe', 'cUF', 'cNF', 'natOp', 'mod', 'serie', 'nNF', 'dhEmi', 'tpNF', 
        'tpEmis', 'finNFe', 'indPres', 'verProc',
        
        # 2. EMITENTE
        'emit_CNPJ', 'emit_xNome', 'emit_CRT',
        
        # 3. DESTINATÁRIO
        'dest_CNPJ', 'dest_xNome', 'dest_indIEDest',
        
        # 4. ITENS
        'nItem', 'cProd', 'xProd', 'NCM', 'CFOP', 'uCom', 'qCom', 'vUnCom', 'vProd', 
        'uTrib', 'qTrib', 'vUnTrib', 'vOutro', 'indTot', 'vItem', 'vTotTrib',
        
        # 4.3 PIS
        'PIS_CST', 'PIS_vBC', 'PIS_pPIS', 'PIS_vPIS',
        
        # 4.4 COFINS
        'COFINS_CST', 'COFINS_vBC', 'COFINS_pCOFINS', 'COFINS_vCOFINS',
        
        # 4.5 IBSCBS - COM TODOS OS CAMPOS DA VALIDAÇÃO
        'ibscbs_CST', 'ibscbs_cClassTrib', 'ibscbs_vBC', 'ibscbs_vIBS',
        'ibscbs_gIBSUF_pIBSUF', 'ibscbs_gIBSUF_vIBSUF', 'ibscbs_gIBSMun_pIBSMun', 'ibscbs_gIBSMun_vIBSMun',
        'ibscbs_gCBS_pCBS', 'ibscbs_gCBS_vCBS',
        
        # 4.6 GTRIBREGULAR - NOVOS CAMPOS
        'gTribRegular_CSTReg', 'gTribRegular_cClassTribReg', 'gTribRegular_pAliqEfetRegIBSUF', 
        'gTribRegular_vTribRegIBSUF', 'gTribRegular_pAliqEfetRegIBSMun', 'gTribRegular_vTribRegIBSMun',
        'gTribRegular_pAliqEfetRegCBS', 'gTribRegular_vTribRegCBS',
        
        # 5. TOTAIS - INCLUINDO vNFTot
        'total_vBC', 'total_vICMS', 'total_vICMSDeson', 'total_vFCPUFDest', 'total_vICMSUFDest',
        'total_vICMSUFRemet', 'total_vFCP', 'total_vBCST', 'total_vST', 'total_vProd', 'total_vFrete',
        'total_vSeg', 'total_vDesc', 'total_vII', 'total_vIPI', 'total_vPIS', 'total_vCOFINS',
        'total_vOutro', 'total_vNF', 'total_vTotTrib',
        
        # 4.2 ICMS (campos dinâmicos - serão adicionados depois)
    ]
    
    # Colunas existentes na ordem do schema
    colunas_ordenadas = []
    for col in ordem_schema:
        if col in df.columns:
            colunas_ordenadas.append(col)
    
    # Adicionar colunas de ICMS (que podem variar por tipo)
    colunas_icms = sorted([col for col in df.columns if col.startswith('ICMS_') and col not in colunas_ordenadas])
    colunas_ordenadas.extend(colunas_icms)
    
    # Adicionar colunas restantes em ordem alfabética
    colunas_restantes = sorted([col for col in df.columns if col not in colunas_ordenadas])
    colunas_ordenadas.extend(colunas_restantes)
    
    return df[colunas_ordenadas]

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
    if 'vItem' in df.columns:
        estatisticas.append({'Estatística': 'Valor Total Itens (R$)', 'Valor': f"R$ {df['vItem'].sum():,.2f}"})
    
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
    
    # Estatísticas IBSCBS
    if 'ibscbs_CST' in df.columns:
        total_ibscbs = df['ibscbs_CST'].notna().sum()
        total_na = (df['ibscbs_CST'] == 'NA').sum()
        total_com_dados = total_ibscbs - total_na
        
        estatisticas.append({'Estatística': 'Itens com IBSCBS', 'Valor': total_com_dados})
        estatisticas.append({'Estatística': 'Itens sem IBSCBS', 'Valor': total_na})
        estatisticas.append({'Estatística': 'Percentual com IBSCBS', 'Valor': f"{(total_com_dados/len(df))*100:.1f}%"})
    
    # Estatísticas GTribRegular
    gtrib_campos = [col for col in df.columns if 'gTribRegular' in col]
    if gtrib_campos:
        campos_principais = [col for col in gtrib_campos if 'CSTReg' in col]
        if campos_principais:
            count_gtrib = df[campos_principais[0]].notna().sum()
            estatisticas.append({'Estatística': 'Itens com GTribRegular', 'Valor': count_gtrib})
    
    return pd.DataFrame(estatisticas)

def criar_aba_resumo(df):
    """Cria aba de resumo para o Excel - INCLUINDO emit_CNPJ, serie, vItem e total_vNF"""
    resumo_data = []
    
    # Resumo por NFe
    if 'nNF' in df.columns:
        nfes_agrupadas = df.groupby('nNF').agg({
            'serie': 'first',
            'emit_CNPJ': 'first',
            'emit_xNome': 'first',
            'dhEmi': 'first',
            'vProd': 'sum',
            'vItem': 'sum',
            'total_vNF': 'first',
            'idDest': 'first'
        }).reset_index()
        
        for _, nfe in nfes_agrupadas.iterrows():
            tipo_destino = {
                '1': 'Operação Interna',
                '2': 'Operação Interestadual',
                '3': 'Operação com Exterior'
            }.get(nfe['idDest'], 'Desconhecido')
            
            resumo_data.append({
                'Série': nfe['serie'],
                'Número NFe': nfe['nNF'],
                'CNPJ Emitente': nfe['emit_CNPJ'],
                'Emitente': nfe['emit_xNome'],
                'Data Emissão': nfe['dhEmi'],
                'Tipo Destino': tipo_destino,
                'Valor Produtos': nfe['vProd'],
                'Valor Itens': nfe['vItem'],
                'Valor NF': nfe['total_vNF']
            })
    
    return pd.DataFrame(resumo_data)

def criar_aba_detalhes_icms(df):
    """Cria aba com detalhes do ICMS - INCLUINDO emit_CNPJ"""
    icms_colunas = [col for col in df.columns if 'ICMS_' in col]
    if icms_colunas:
        colunas_base = ['serie', 'nNF', 'emit_CNPJ', 'nItem', 'cProd', 'xProd', 'NCM', 'CFOP', 'vProd']
        colunas_detalhes = colunas_base + icms_colunas
        return df[colunas_detalhes]
    else:
        return pd.DataFrame({'Mensagem': ['Nenhum dado de ICMS encontrado']})

def criar_aba_detalhes_ibscbs(df):
    """Cria aba com detalhes do IBSCBS incluindo GTribRegular"""
    ibscbs_colunas = [col for col in df.columns if 'ibscbs_' in col]
    gtrib_colunas = [col for col in df.columns if 'gTribRegular' in col]
    
    todas_colunas = ibscbs_colunas + gtrib_colunas
    
    if todas_colunas:
        colunas_base = ['serie', 'nNF', 'emit_CNPJ', 'cProd', 'xProd', 'NCM', 'CFOP', 'vProd']
        colunas_detalhes = colunas_base + todas_colunas
        
        # Criar DataFrame com descrições para GTribRegular
        df_detalhes = df[colunas_detalhes].copy()
        
        # Adicionar descrições para facilitar a análise
        if 'ibscbs_CST' in df_detalhes.columns:
            df_detalhes['ibscbs_CST_Desc'] = df_detalhes['ibscbs_CST'].apply(
                lambda x: 'Alíquota reduzida' if x == '200' else 'Suspensão' if x == '550' else x
            )
        
        # Reordenar colunas para melhor visualização
        colunas_ordenadas = colunas_base + ['ibscbs_CST', 'ibscbs_CST_Desc'] + [col for col in todas_colunas if col != 'ibscbs_CST']
        return df_detalhes[colunas_ordenadas]
    else:
        return pd.DataFrame({'Mensagem': ['Nenhum dado de IBSCBS/GTribRegular encontrado']})

def criar_aba_gtribregular(df):
    """Cria aba específica para GTribRegular com todas as informações"""
    gtrib_colunas = [col for col in df.columns if 'gTribRegular' in col]
    
    if gtrib_colunas:
        colunas_base = ['serie', 'nNF', 'emit_CNPJ', 'cProd', 'xProd', 'NCM', 'CFOP', 'vProd']
        colunas_detalhes = colunas_base + gtrib_colunas
        
        df_gtrib = df[colunas_detalhes].copy()
        
        # Adicionar descrições para CSTReg
        if 'gTribRegular_CSTReg' in df_gtrib.columns:
            df_gtrib['CSTReg_Desc'] = df_gtrib['gTribRegular_CSTReg'].apply(
                lambda x: 'Tributação Regular' if x == '000' else 'Alíquota reduzida' if x == '200' else 'Suspensão' if x == '550' else x
            )
        
        return df_gtrib
    else:
        return pd.DataFrame({'Mensagem': ['Nenhum dado de GTribRegular encontrado']})

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
        
        # Ordenar colunas conforme schema da NF-e
        df = ordenar_colunas_por_schema(df)
        
        return df
    else:
        return pd.DataFrame()

def analisar_dados_completos(df):
    """Analisa todos os dados extraidos"""
    print(f"\n ANÁLISE COMPLETA DOS DADOS:")
    
    # Campos básicos
    print(f" CAMPOS BASICOS:")
    print(f"   • Total de NFes: {df['nNF'].nunique()}")
    print(f"   • Total de itens: {len(df)}")
    print(f"   • Emitentes: {df['emit_xNome'].nunique()}")
    
    # Valores monetários
    print(f"\n VALORES MONETARIOS:")
    campos_valores = ['vProd', 'vItem', 'total_vNF', 'total_vProd']
    for campo in campos_valores:
        if campo in df.columns and df[campo].notna().any():
            print(f"   • {campo}: R$ {df[campo].sum():,.2f}")
    
    # Análise IBSCBS
    print(f"\n ANÁLISE IBSCBS:")
    if 'ibscbs_CST' in df.columns:
        total_ibscbs = df['ibscbs_CST'].notna().sum()
        total_na = (df['ibscbs_CST'] == 'NA').sum()
        total_com_dados = total_ibscbs - total_na
        
        print(f"   • Itens com IBSCBS: {total_com_dados}")
        print(f"   • Itens sem IBSCBS: {total_na}")
        print(f"   • Percentual com IBSCBS: {(total_com_dados/len(df))*100:.1f}%")
        
        # Analisar campos específicos do IBSCBS
        campos_ibscbs = ['ibscbs_vBC', 'ibscbs_vIBS', 'ibscbs_gIBSUF_vIBSUF', 'ibscbs_gIBSMun_vIBSMun', 'ibscbs_gCBS_vCBS']
        for campo in campos_ibscbs:
            if campo in df.columns:
                count = df[campo].notna().sum()
                if count > 0:
                    print(f"   • {campo}: presente em {count} registros")
    
    # GTribRegular
    print(f"\n GTRIBREGULAR:")
    gtrib_campos = [col for col in df.columns if 'gTribRegular' in col]
    if gtrib_campos:
        print(f"   • Campos gTribRegular encontrados: {len(gtrib_campos)}")
        campos_principais = [col for col in gtrib_campos if 'CSTReg' in col]
        if campos_principais:
            count_gtrib = df[campos_principais[0]].notna().sum()
            print(f"   • Registros com gTribRegular: {count_gtrib}")
            
            # Mostrar valores únicos de CSTReg
            if 'gTribRegular_CSTReg' in df.columns:
                cst_values = df['gTribRegular_CSTReg'].dropna().unique()
                if len(cst_values) > 0:
                    print(f"   • Valores de CSTReg encontrados: {', '.join(map(str, cst_values))}")

# USO
if __name__ == "__main__":
    caminho = r"C:\Users\08748D631\Desktop\nfe_xml"
    
    print("INICIANDO PROCESSAMENTO NF-e 4.00 COMPLETO")
    print("ORGANIZADO CONFORME SCHEMA DA NF-E")
    print("INCLUINDO VALIDAÇÃO COMPLETA DO IBSCBS E GTRIBREGULAR")
    
    df = processar_pasta_xmls(caminho)
    
    if not df.empty:
        # Exportar
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        excel_file = f"nfe_organizada_schema_{timestamp}.xlsx"
        csv_file = f"nfe_organizada_schema_{timestamp}.csv"
        
        try:
            # Exportar para Excel com múltiplas abas organizadas
            with pd.ExcelWriter(excel_file, engine='openpyxl') as writer:
                # ABA 1: Dados Completos (ordenados por schema) 
                df.to_excel(writer, sheet_name='NFes_Completas', index=False)
                
                # ABA 2: Resumo por NFe 
                resumo = criar_aba_resumo(df)
                resumo.to_excel(writer, sheet_name='Resumo_NFe', index=False)
                
                # ABA 3: Estatísticas
                estatisticas = criar_aba_estatisticas(df)
                estatisticas.to_excel(writer, sheet_name='Estatisticas', index=False)
                
                # ABA 4: Detalhes ICMS 
                detalhes_icms = criar_aba_detalhes_icms(df)
                detalhes_icms.to_excel(writer, sheet_name='Detalhes_ICMS', index=False)
                
                # ABA 5: Detalhes IBSCBS (incluindo GTribRegular)
                detalhes_ibscbs = criar_aba_detalhes_ibscbs(df)
                detalhes_ibscbs.to_excel(writer, sheet_name='Detalhes_IBSCBS', index=False)
                
                # ABA 6: GTribRegular Específico
                gtribregular = criar_aba_gtribregular(df)
                gtribregular.to_excel(writer, sheet_name='GTribRegular', index=False)
            
            print(f" Excel exportado com sucesso: {excel_file}")
            
        except Exception as e:
            print(f" Erro ao exportar Excel: {e}")
        
        # Exportar para CSV
        df.to_csv(csv_file, index=False, encoding='utf-8-sig')
        print(f" CSV exportado com sucesso: {csv_file}")
        
        print(f"\n ARQUIVOS EXPORTADOS:")
        print(f"   Excel: {excel_file} (com 6 abas organizadas)")
        print(f"   CSV: {csv_file}")
        
        # Mostrar estrutura
        print(f"\n ESTRUTURA DO ARQUIVO EXCEL:")
        print("   ABA 1: NFes_Completas - Todos os dados ordenados por schema")
        print("   ABA 2: Resumo_NFe - Resumo por nota fiscal") 
        print("   ABA 3: Estatisticas - Estatísticas consolidadas")
        print("   ABA 4: Detalhes_ICMS - Foco em informações do ICMS")
        print("   ABA 5: Detalhes_IBSCBS - IBSCBS + GTribRegular")
        print("   ABA 6: GTribRegular - Foco em tributação regular")
        
        # Mostrar amostra
        print(f"\n AMOSTRA DOS DADOS (primeiras 3 linhas):")
        colunas_amostra = ['nItem', 'xProd', 'vProd', 'vItem', 'total_vNF', 'idDest', 'emit_CNPJ', 'serie']
        colunas_disponiveis = [col for col in colunas_amostra if col in df.columns]
        if colunas_disponiveis:
            print(df[colunas_disponiveis].head(3))
        
        # Analisar dados
        analisar_dados_completos(df)
        
    else:
        print("\n Nenhum dado processado.")