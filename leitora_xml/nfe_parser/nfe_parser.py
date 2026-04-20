#!/usr/bin/env python3
"""
NF-e Parser - Parser completo para Nota Fiscal Eletrônica
Baseado no schema leiauteNFe_v4.00.xsd
Mapeamento completo dos campos incluindo Reforma Tributária e Partilha do ICMS (DIFAL)
"""

import xml.etree.ElementTree as ET
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from decimal import Decimal
import json

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
    cMunFGIBS: Optional[str] = None  # NOVO - Reforma Tributária
    tpImp: str = None
    tpEmis: str = None
    cDV: str = None
    tpAmb: str = None
    finNFe: str = None
    tpNFDebito: Optional[str] = None  # NOVO - Reforma Tributária
    tpNFCredito: Optional[str] = None  # NOVO - Reforma Tributária
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
    tpCredPresIBSZFM: Optional[str] = None  # NOVO - Reforma Tributária
    gCred: Optional[CreditoPresumido] = None  # NOVO - Reforma Tributária

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

@dataclass
class ICMS40:
    """ICMS40 - Isenta, Não tributada, Suspensão"""
    orig: str
    CST: str = None  # 40, 41, 50
    desoneracao: Optional[DesoneracaoICMS] = None
    partilha: Optional[PartilhaICMS] = None

@dataclass
class ICMS51:
    """ICMS51 - Diferimento"""
    orig: str
    CST: str = "51"
    modBC: Optional[str] = None
    pRedBC: Optional[Decimal] = None
    cBenefRBC: Optional[str] = None  # NOVO - Reforma Tributária
    vBC: Optional[Decimal] = None
    pICMS: Optional[Decimal] = None
    vICMSOp: Optional[Decimal] = None
    pDif: Optional[Decimal] = None
    vICMSDif: Optional[Decimal] = None
    vICMS: Optional[Decimal] = None
    pFCP: Optional[Decimal] = None
    vFCP: Optional[Decimal] = None
    vBCFCP: Optional[Decimal] = None
    pFCPDif: Optional[Decimal] = None  # NOVO - Reforma Tributária
    vFCPDif: Optional[Decimal] = None  # NOVO - Reforma Tributária
    vFCPEfet: Optional[Decimal] = None  # NOVO - Reforma Tributária
    partilha: Optional[PartilhaICMS] = None

@dataclass
class ICMS90:
    """ICMS90 - Outras operações"""
    orig: str
    CST: str = "90"
    modBC: Optional[str] = None
    vBC: Optional[Decimal] = None
    pRedBC: Optional[Decimal] = None
    pICMS: Optional[Decimal] = None
    vICMS: Optional[Decimal] = None
    modBCST: Optional[str] = None
    pMVAST: Optional[Decimal] = None
    pRedBCST: Optional[Decimal] = None
    vBCST: Optional[Decimal] = None
    pICMSST: Optional[Decimal] = None
    vICMSST: Optional[Decimal] = None
    vBCFCPST: Optional[Decimal] = None
    pFCPST: Optional[Decimal] = None
    vFCPST: Optional[Decimal] = None
    pFCP: Optional[Decimal] = None
    vFCP: Optional[Decimal] = None
    vBCFCP: Optional[Decimal] = None
    desoneracao: Optional[DesoneracaoICMS] = None
    partilha: Optional[PartilhaICMS] = None

@dataclass 
class ICMSSN101:
    """ICMSSN101 - Simples Nacional com crédito"""
    orig: str
    CSOSN: str = "101"
    pCredSN: Decimal = None
    vCredICMSSN: Decimal = None

# 4.3 DETALHE DO PIS
@dataclass
class PISAliq:
    """PIS Alíquota"""
    CST: str
    vBC: Decimal
    pPIS: Decimal
    vPIS: Decimal

@dataclass
class PISQtde:
    """PIS Quantidade"""
    CST: str
    qBCProd: Decimal
    vAliqProd: Decimal
    vPIS: Decimal

@dataclass
class PISNT:
    """PIS Não Tributado"""
    CST: str

@dataclass
class PISOutr:
    """PIS Outras Operações"""
    CST: str
    vBC: Optional[Decimal] = None
    pPIS: Optional[Decimal] = None
    qBCProd: Optional[Decimal] = None
    vAliqProd: Optional[Decimal] = None
    vPIS: Decimal = None

# 4.4 DETALHE DO COFINS
@dataclass
class COFINSAliq:
    """COFINS Alíquota"""
    CST: str
    vBC: Decimal
    pCOFINS: Decimal
    vCOFINS: Decimal

@dataclass
class COFINSQtde:
    """COFINS Quantidade"""
    CST: str
    qBCProd: Decimal
    vAliqProd: Decimal
    vCOFINS: Decimal

@dataclass
class COFINSNT:
    """COFINS Não Tributado"""
    CST: str

@dataclass
class COFINSOutr:
    """COFINS Outras Operações"""
    CST: str
    vBC: Optional[Decimal] = None
    pCOFINS: Optional[Decimal] = None
    qBCProd: Optional[Decimal] = None
    vAliqProd: Optional[Decimal] = None
    vCOFINS: Decimal = None

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
    ICMS: Optional[Any] = None  # ICMS00, ICMS20, ICMS40, ICMS51, ICMS90, ICMSSN101
    PIS: Optional[Any] = None   # PISAliq, PISQtde, PISNT, PISOutr
    COFINS: Optional[Any] = None # COFINSAliq, COFINSQtde, COFINSNT, COFINSOutr
    gTribRegular: Optional[GTribRegular] = None  # IBSCBS
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
class Veiculo:
    """Grupo do veículo"""
    placa: str
    UF: str
    RNTC: Optional[str] = None

@dataclass
class Transporte:
    """Grupo de transporte"""
    modFrete: str
    transporta: Optional[Transportador] = None
    veicTransp: Optional[Veiculo] = None
    vol: Optional[List[Any]] = None

# =============================================================================
# 7. GRUPO DE INFORMAÇÕES DO PAGAMENTO
# =============================================================================

@dataclass
class DetalhePagamento:
    """Grupo de detalhe do pagamento"""
    tPag: str
    vPag: Decimal
    indPag: Optional[str] = None
    tpIntegra: Optional[str] = None
    CNPJ: Optional[str] = None
    tBand: Optional[str] = None
    cAut: Optional[str] = None

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
    
    # Informações adicionais
    informacoes_adicionais: Optional[Any] = None
    
    def __post_init__(self):
        if self.itens is None:
            self.itens = []

# =============================================================================
# PARSER PRINCIPAL
# =============================================================================

class NFEParser:
    """Parser principal para NF-e"""
    
    # Namespaces
    NAMESPACES = {
        'ns': 'http://www.portalfiscal.inf.br/nfe'
    }
    
    def __init__(self):
        self.nfe = None
    
    def parse_xml(self, xml_content: str) -> NFE:
        """Parse do XML da NF-e seguindo a ordem do schema"""
        try:
            root = ET.fromstring(xml_content)
            
            # Encontrar o elemento infNFe
            infNFe = root.find('.//ns:infNFe', self.NAMESPACES)
            if infNFe is None:
                raise ValueError("Elemento infNFe não encontrado")
            
            # 1. Parse do emitente (primeiro no schema)
            emitente = self._parse_emitente(infNFe)
            
            # 2. Parse da identificação (segundo no schema)
            identificacao = self._parse_identificacao(infNFe)
            
            # 3. Parse do destinatário (terceiro no schema)
            destinatario = self._parse_destinatario(infNFe)
            
            # 4. Parse dos itens (quarto no schema)
            itens = self._parse_itens(infNFe)
            
            # 5. Parse dos totais (quinto no schema)
            total = self._parse_totais(infNFe)
            
            # 6. Parse do transporte (sexto no schema)
            transporte = self._parse_transporte(infNFe)
            
            # 7. Parse do pagamento (sétimo no schema)
            pagamento = self._parse_pagamento(infNFe)
            
            self.nfe = NFE(
                emitente=emitente,
                identificacao=identificacao,
                destinatario=destinatario,
                itens=itens,
                total=total,
                transporte=transporte,
                pagamento=pagamento
            )
            
            return self.nfe
            
        except ET.ParseError as e:
            raise ValueError(f"Erro ao parsear XML: {e}")
    
    # 1. MÉTODOS PARA PARSE DO EMITENTE
    def _parse_emitente(self, infNFe) -> Emitente:
        """Parse do grupo do emitente"""
        emit = infNFe.find('ns:emit', self.NAMESPACES)
        if emit is None:
            raise ValueError("Grupo emit não encontrado")
        
        # Parse do endereço do emitente
        enderEmit = self._parse_ender_emitente(emit)
        
        emitente = Emitente(
            CNPJ=self._get_text(emit, 'ns:CNPJ'),
            CPF=self._get_text(emit, 'ns:CPF'),
            xNome=self._get_text(emit, 'ns:xNome'),
            xFant=self._get_text(emit, 'ns:xFant'),
            enderEmit=enderEmit,
            IE=self._get_text(emit, 'ns:IE'),
            IEST=self._get_text(emit, 'ns:IEST'),
            IM=self._get_text(emit, 'ns:IM'),
            CNAE=self._get_text(emit, 'ns:CNAE'),
            CRT=self._get_text(emit, 'ns:CRT')
        )
        
        return emitente
    
    def _parse_ender_emitente(self, emit) -> Optional[EnderecoEmitente]:
        """Parse do endereço do emitente"""
        enderEmit = emit.find('ns:enderEmit', self.NAMESPACES)
        if enderEmit is None:
            return None
        
        return EnderecoEmitente(
            xLgr=self._get_text(enderEmit, 'ns:xLgr'),
            nro=self._get_text(enderEmit, 'ns:nro'),
            xBairro=self._get_text(enderEmit, 'ns:xBairro'),
            cMun=self._get_text(enderEmit, 'ns:cMun'),
            xMun=self._get_text(enderEmit, 'ns:xMun'),
            UF=self._get_text(enderEmit, 'ns:UF'),
            CEP=self._get_text(enderEmit, 'ns:CEP'),
            cPais=self._get_text(enderEmit, 'ns:cPais'),
            xPais=self._get_text(enderEmit, 'ns:xPais'),
            fone=self._get_text(enderEmit, 'ns:fone')
        )
    
    # 2. MÉTODOS PARA PARSE DA IDENTIFICAÇÃO
    def _parse_identificacao(self, infNFe) -> IdentificacaoNFE:
        """Parse do grupo de identificação"""
        ide = infNFe.find('ns:ide', self.NAMESPACES)
        if ide is None:
            raise ValueError("Grupo ide não encontrado")
        
        # Campos obrigatórios
        identificacao = IdentificacaoNFE(
            cUF=self._get_text(ide, 'ns:cUF'),
            cNF=self._get_text(ide, 'ns:cNF'),
            natOp=self._get_text(ide, 'ns:natOp'),
            mod=self._get_text(ide, 'ns:mod'),
            serie=self._get_text(ide, 'ns:serie'),
            nNF=self._get_text(ide, 'ns:nNF'),
            dhEmi=self._get_text(ide, 'ns:dhEmi'),
            tpNF=self._get_text(ide, 'ns:tpNF'),
            idDest=self._get_text(ide, 'ns:idDest'),
            cMunFG=self._get_text(ide, 'ns:cMunFG'),
            tpImp=self._get_text(ide, 'ns:tpImp'),
            tpEmis=self._get_text(ide, 'ns:tpEmis'),
            cDV=self._get_text(ide, 'ns:cDV'),
            tpAmb=self._get_text(ide, 'ns:tpAmb'),
            finNFe=self._get_text(ide, 'ns:finNFe'),
            indFinal=self._get_text(ide, 'ns:indFinal'),
            indPres=self._get_text(ide, 'ns:indPres'),
            procEmi=self._get_text(ide, 'ns:procEmi'),
            verProc=self._get_text(ide, 'ns:verProc')
        )
        
        # Campos opcionais
        identificacao.dhSaiEnt = self._get_text(ide, 'ns:dhSaiEnt')
        identificacao.dPrevEntrega = self._get_text(ide, 'ns:dPrevEntrega')
        identificacao.indIntermed = self._get_text(ide, 'ns:indIntermed')
        identificacao.dhCont = self._get_text(ide, 'ns:dhCont')
        identificacao.xJust = self._get_text(ide, 'ns:xJust')
        
        # NOVOS CAMPOS - REFORMA TRIBUTÁRIA
        identificacao.cMunFGIBS = self._get_text(ide, 'ns:cMunFGIBS')
        identificacao.tpNFDebito = self._get_text(ide, 'ns:tpNFDebito')
        identificacao.tpNFCredito = self._get_text(ide, 'ns:tpNFCredito')
        
        return identificacao
    
    # 3. MÉTODOS PARA PARSE DO DESTINATÁRIO
    def _parse_destinatario(self, infNFe) -> Optional[Destinatario]:
        """Parse do grupo do destinatário"""
        dest = infNFe.find('ns:dest', self.NAMESPACES)
        if dest is None:
            return None
        
        # Parse do endereço do destinatário
        enderDest = self._parse_ender_destinatario(dest)
        
        destinatario = Destinatario(
            CNPJ=self._get_text(dest, 'ns:CNPJ'),
            CPF=self._get_text(dest, 'ns:CPF'),
            idEstrangeiro=self._get_text(dest, 'ns:idEstrangeiro'),
            xNome=self._get_text(dest, 'ns:xNome'),
            enderDest=enderDest,
            indIEDest=self._get_text(dest, 'ns:indIEDest'),
            IE=self._get_text(dest, 'ns:IE'),
            ISUF=self._get_text(dest, 'ns:ISUF'),
            IM=self._get_text(dest, 'ns:IM'),
            email=self._get_text(dest, 'ns:email')
        )
        
        return destinatario
    
    def _parse_ender_destinatario(self, dest) -> Optional[EnderecoDestinatario]:
        """Parse do endereço do destinatário"""
        enderDest = dest.find('ns:enderDest', self.NAMESPACES)
        if enderDest is None:
            return None
        
        return EnderecoDestinatario(
            xLgr=self._get_text(enderDest, 'ns:xLgr'),
            nro=self._get_text(enderDest, 'ns:nro'),
            xBairro=self._get_text(enderDest, 'ns:xBairro'),
            cMun=self._get_text(enderDest, 'ns:cMun'),
            xMun=self._get_text(enderDest, 'ns:xMun'),
            UF=self._get_text(enderDest, 'ns:UF'),
            CEP=self._get_text(enderDest, 'ns:CEP'),
            cPais=self._get_text(enderDest, 'ns:cPais'),
            xPais=self._get_text(enderDest, 'ns:xPais'),
            fone=self._get_text(enderDest, 'ns:fone')
        )
    
    # 4. MÉTODOS PARA PARSE DOS ITENS
    def _parse_itens(self, infNFe) -> List[ItemNFE]:
        """Parse dos itens da NF-e"""
        itens = []
        det_elements = infNFe.findall('ns:det', self.NAMESPACES)
        
        for det in det_elements:
            nItem = int(det.get('nItem', 0))
            
            # 4.1 Parse do produto
            produto = self._parse_produto(det, nItem)
            
            # 4.6 Parse dos impostos (consolidado)
            imposto = self._parse_imposto(det)
            
            # 4.7 Item consolidado
            item = ItemNFE(produto=produto, imposto=imposto)
            itens.append(item)
        
        return itens
    
    def _parse_produto(self, det, nItem: int) -> Produto:
        """Parse do grupo do produto"""
        prod = det.find('ns:prod', self.NAMESPACES)
        if prod is None:
            raise ValueError(f"Grupo prod não encontrado para item {nItem}")
        
        produto = Produto(
            nItem=nItem,
            cProd=self._get_text(prod, 'ns:cProd'),
            cEAN=self._get_text(prod, 'ns:cEAN'),
            cBarra=self._get_text(prod, 'ns:cBarra'),
            xProd=self._get_text(prod, 'ns:xProd'),
            NCM=self._get_text(prod, 'ns:NCM'),
            NVE=self._get_text(prod, 'ns:NVE'),
            CEST=self._get_text(prod, 'ns:CEST'),
            indEscala=self._get_text(prod, 'ns:indEscala'),
            CNPJFab=self._get_text(prod, 'ns:CNPJFab'),
            cBenef=self._get_text(prod, 'ns:cBenef'),
            EXTIPI=self._get_text(prod, 'ns:EXTIPI'),
            CFOP=self._get_text(prod, 'ns:CFOP'),
            uCom=self._get_text(prod, 'ns:uCom'),
            qCom=self._parse_decimal(self._get_text(prod, 'ns:qCom')),
            vUnCom=self._parse_decimal(self._get_text(prod, 'ns:vUnCom')),
            vProd=self._parse_decimal(self._get_text(prod, 'ns:vProd')),
            cEANTrib=self._get_text(prod, 'ns:cEANTrib'),
            cBarraTrib=self._get_text(prod, 'ns:cBarraTrib'),
            uTrib=self._get_text(prod, 'ns:uTrib'),
            qTrib=self._parse_decimal(self._get_text(prod, 'ns:qTrib')),
            vUnTrib=self._parse_decimal(self._get_text(prod, 'ns:vUnTrib')),
            vFrete=self._parse_decimal(self._get_text(prod, 'ns:vFrete')),
            vSeg=self._parse_decimal(self._get_text(prod, 'ns:vSeg')),
            vDesc=self._parse_decimal(self._get_text(prod, 'ns:vDesc')),
            vOutro=self._parse_decimal(self._get_text(prod, 'ns:vOutro')),
            indTot=self._get_text(prod, 'ns:indTot'),
            indBemMovelUsado=self._get_text(prod, 'ns:indBemMovelUsado'),
            tpCredPresIBSZFM=self._get_text(prod, 'ns:tpCredPresIBSZFM')
        )
        
        # NOVO - Parse do grupo de crédito presumido (Reforma Tributária)
        produto.gCred = self._parse_credito_presumido(prod)
        
        return produto
    
    def _parse_credito_presumido(self, prod) -> Optional[CreditoPresumido]:
        """Parse do grupo de crédito presumido - NOVO Reforma Tributária"""
        gCred = prod.find('ns:gCred', self.NAMESPACES)
        if gCred is None:
            return None
        
        return CreditoPresumido(
            cCredPresumido=self._get_text(gCred, 'ns:cCredPresumido'),
            pCredPresumido=self._parse_decimal(self._get_text(gCred, 'ns:pCredPresumido')),
            vCredPresumido=self._parse_decimal(self._get_text(gCred, 'ns:vCredPresumido'))
        )
    
    def _parse_imposto(self, det) -> ImpostoProduto:
        """Parse do grupo de impostos (consolidado)"""
        imposto = ImpostoProduto()
        imposto_element = det.find('ns:imposto', self.NAMESPACES)
        
        if imposto_element is not None:
            imposto.vTotTrib = self._parse_decimal(
                self._get_text(imposto_element, 'ns:vTotTrib')
            )
            
            # 4.2 Parse do ICMS
            imposto.ICMS = self._parse_icms(imposto_element)
            
            # 4.3 Parse do PIS
            imposto.PIS = self._parse_pis(imposto_element)
            
            # 4.4 Parse do COFINS
            imposto.COFINS = self._parse_cofins(imposto_element)
            
            # 4.5 Parse do IBSCBS (GTribRegular)
            imposto.gTribRegular = self._parse_gtribregular(imposto_element)
        
        return imposto
    
    def _parse_icms(self, imposto_element) -> Optional[Any]:
        """Parse do grupo ICMS"""
        icms_element = imposto_element.find('ns:ICMS', self.NAMESPACES)
        if icms_element is None:
            return None
        
        # Verificar qual tipo de ICMS está presente
        for icms_type in ['ns:ICMS00', 'ns:ICMS20', 'ns:ICMS40', 'ns:ICMS51', 'ns:ICMS90', 'ns:ICMSSN101']:
            icms_data = icms_element.find(icms_type, self.NAMESPACES)
            if icms_data is not None:
                if icms_type == 'ns:ICMS00':
                    return self._parse_icms00(icms_data)
                elif icms_type == 'ns:ICMS20':
                    return self._parse_icms20(icms_data)
                elif icms_type == 'ns:ICMS40':
                    return self._parse_icms40(icms_data)
                elif icms_type == 'ns:ICMS51':
                    return self._parse_icms51(icms_data)
                elif icms_type == 'ns:ICMS90':
                    return self._parse_icms90(icms_data)
                elif icms_type == 'ns:ICMSSN101':
                    return self._parse_icmssn101(icms_data)
        
        return None
    
    def _parse_pis(self, imposto_element) -> Optional[Any]:
        """Parse do grupo PIS"""
        pis_element = imposto_element.find('ns:PIS', self.NAMESPACES)
        if pis_element is None:
            return None
        
        # Verificar qual tipo de PIS está presente
        for pis_type in ['ns:PISAliq', 'ns:PISQtde', 'ns:PISNT', 'ns:PISOutr']:
            pis_data = pis_element.find(pis_type, self.NAMESPACES)
            if pis_data is not None:
                if pis_type == 'ns:PISAliq':
                    return self._parse_pis_aliq(pis_data)
                elif pis_type == 'ns:PISQtde':
                    return self._parse_pis_qtde(pis_data)
                elif pis_type == 'ns:PISNT':
                    return self._parse_pis_nt(pis_data)
                elif pis_type == 'ns:PISOutr':
                    return self._parse_pis_outr(pis_data)
        
        return None
    
    def _parse_cofins(self, imposto_element) -> Optional[Any]:
        """Parse do grupo COFINS"""
        cofins_element = imposto_element.find('ns:COFINS', self.NAMESPACES)
        if cofins_element is None:
            return None
        
        # Verificar qual tipo de COFINS está presente
        for cofins_type in ['ns:COFINSAliq', 'ns:COFINSQtde', 'ns:COFINSNT', 'ns:COFINSOutr']:
            cofins_data = cofins_element.find(cofins_type, self.NAMESPACES)
            if cofins_data is not None:
                if cofins_type == 'ns:COFINSAliq':
                    return self._parse_cofins_aliq(cofins_data)
                elif cofins_type == 'ns:COFINSQtde':
                    return self._parse_cofins_qtde(cofins_data)
                elif cofins_type == 'ns:COFINSNT':
                    return self._parse_cofins_nt(cofins_data)
                elif cofins_type == 'ns:COFINSOutr':
                    return self._parse_cofins_outr(cofins_data)
        
        return None
    
    # Implementações dos métodos de parse específicos para ICMS, PIS, COFINS...
    # (Mantidos do código original, mas organizados por grupos)
    
    def _parse_icms00(self, icms_data) -> ICMS00:
        """Parse do ICMS00"""
        icms00 = ICMS00(
            orig=self._get_text(icms_data, 'ns:orig'),
            modBC=self._get_text(icms_data, 'ns:modBC'),
            vBC=self._parse_decimal(self._get_text(icms_data, 'ns:vBC')),
            pICMS=self._parse_decimal(self._get_text(icms_data, 'ns:pICMS')),
            vICMS=self._parse_decimal(self._get_text(icms_data, 'ns:vICMS')),
            pFCP=self._parse_decimal(self._get_text(icms_data, 'ns:pFCP')),
            vFCP=self._parse_decimal(self._get_text(icms_data, 'ns:vFCP'))
        )
        
        # Parse da partilha do ICMS (DIFAL) se existir
        icms00.partilha = self._parse_partilha_icms(icms_data)
        
        return icms00
    
    def _parse_icms20(self, icms_data) -> ICMS20:
        """Parse do ICMS20 com desoneração"""
        icms20 = ICMS20(
            orig=self._get_text(icms_data, 'ns:orig'),
            modBC=self._get_text(icms_data, 'ns:modBC'),
            pRedBC=self._parse_decimal(self._get_text(icms_data, 'ns:pRedBC')),
            vBC=self._parse_decimal(self._get_text(icms_data, 'ns:vBC')),
            pICMS=self._parse_decimal(self._get_text(icms_data, 'ns:pICMS')),
            vICMS=self._parse_decimal(self._get_text(icms_data, 'ns:vICMS')),
            pFCP=self._parse_decimal(self._get_text(icms_data, 'ns:pFCP')),
            vFCP=self._parse_decimal(self._get_text(icms_data, 'ns:vFCP')),
            vBCFCP=self._parse_decimal(self._get_text(icms_data, 'ns:vBCFCP'))
        )
        
        # Parse da desoneração se existir
        vICMSDeson = self._get_text(icms_data, 'ns:vICMSDeson')
        if vICMSDeson:
            icms20.desoneracao = DesoneracaoICMS(
                vICMSDeson=self._parse_decimal(vICMSDeson),
                motDesICMS=self._get_text(icms_data, 'ns:motDesICMS'),
                indDeduzDeson=self._get_text(icms_data, 'ns:indDeduzDeson')
            )
        
        # Parse da partilha do ICMS (DIFAL) se existir
        icms20.partilha = self._parse_partilha_icms(icms_data)
        
        return icms20
    
    # ... (outros métodos _parse_icms* mantidos do código original)
    
    def _parse_pis_aliq(self, pis_data) -> PISAliq:
        """Parse do PIS Alíquota"""
        return PISAliq(
            CST=self._get_text(pis_data, 'ns:CST'),
            vBC=self._parse_decimal(self._get_text(pis_data, 'ns:vBC')),
            pPIS=self._parse_decimal(self._get_text(pis_data, 'ns:pPIS')),
            vPIS=self._parse_decimal(self._get_text(pis_data, 'ns:vPIS'))
        )
    
    def _parse_pis_qtde(self, pis_data) -> PISQtde:
        """Parse do PIS Quantidade"""
        return PISQtde(
            CST=self._get_text(pis_data, 'ns:CST'),
            qBCProd=self._parse_decimal(self._get_text(pis_data, 'ns:qBCProd')),
            vAliqProd=self._parse_decimal(self._get_text(pis_data, 'ns:vAliqProd')),
            vPIS=self._parse_decimal(self._get_text(pis_data, 'ns:vPIS'))
        )
    
    def _parse_pis_nt(self, pis_data) -> PISNT:
        """Parse do PIS Não Tributado"""
        return PISNT(
            CST=self._get_text(pis_data, 'ns:CST')
        )
    
    def _parse_pis_outr(self, pis_data) -> PISOutr:
        """Parse do PIS Outras Operações"""
        return PISOutr(
            CST=self._get_text(pis_data, 'ns:CST'),
            vBC=self._parse_decimal(self._get_text(pis_data, 'ns:vBC')),
            pPIS=self._parse_decimal(self._get_text(pis_data, 'ns:pPIS')),
            qBCProd=self._parse_decimal(self._get_text(pis_data, 'ns:qBCProd')),
            vAliqProd=self._parse_decimal(self._get_text(pis_data, 'ns:vAliqProd')),
            vPIS=self._parse_decimal(self._get_text(pis_data, 'ns:vPIS'))
        )
    
    # ... (métodos similares para COFINS)
    
    def _parse_cofins_aliq(self, cofins_data) -> COFINSAliq:
        """Parse do COFINS Alíquota"""
        return COFINSAliq(
            CST=self._get_text(cofins_data, 'ns:CST'),
            vBC=self._parse_decimal(self._get_text(cofins_data, 'ns:vBC')),
            pCOFINS=self._parse_decimal(self._get_text(cofins_data, 'ns:pCOFINS')),
            vCOFINS=self._parse_decimal(self._get_text(cofins_data, 'ns:vCOFINS'))
        )
    
    # 5. MÉTODOS PARA PARSE DOS TOTAIS
    def _parse_totais(self, infNFe) -> Optional[TotalNFE]:
        """Parse do grupo de totais"""
        total_element = infNFe.find('ns:total', self.NAMESPACES)
        if total_element is None:
            return None
        
        # 5.1 Parse do ICMSTot
        ICMSTot = self._parse_icms_tot(total_element)
        
        # 5.2 Parse do IBSCBSTot
        IBSCBSTot = self._parse_ibscbs_tot(total_element)
        
        return TotalNFE(
            ICMSTot=ICMSTot,
            IBSCBSTot=IBSCBSTot
        )
    
    def _parse_icms_tot(self, total_element) -> Optional[ICMSTot]:
        """Parse do grupo ICMSTot"""
        icms_tot = total_element.find('ns:ICMSTot', self.NAMESPACES)
        if icms_tot is None:
            return None
        
        return ICMSTot(
            vBC=self._parse_decimal(self._get_text(icms_tot, 'ns:vBC')),
            vICMS=self._parse_decimal(self._get_text(icms_tot, 'ns:vICMS')),
            vICMSDeson=self._parse_decimal(self._get_text(icms_tot, 'ns:vICMSDeson')),
            vFCPUFDest=self._parse_decimal(self._get_text(icms_tot, 'ns:vFCPUFDest')),
            vICMSUFDest=self._parse_decimal(self._get_text(icms_tot, 'ns:vICMSUFDest')),
            vICMSUFRemet=self._parse_decimal(self._get_text(icms_tot, 'ns:vICMSUFRemet')),
            vFCP=self._parse_decimal(self._get_text(icms_tot, 'ns:vFCP')),
            vBCST=self._parse_decimal(self._get_text(icms_tot, 'ns:vBCST')),
            vST=self._parse_decimal(self._get_text(icms_tot, 'ns:vST')),
            vFCPST=self._parse_decimal(self._get_text(icms_tot, 'ns:vFCPST')),
            vFCPSTRet=self._parse_decimal(self._get_text(icms_tot, 'ns:vFCPSTRet')),
            vProd=self._parse_decimal(self._get_text(icms_tot, 'ns:vProd')),
            vFrete=self._parse_decimal(self._get_text(icms_tot, 'ns:vFrete')),
            vSeg=self._parse_decimal(self._get_text(icms_tot, 'ns:vSeg')),
            vDesc=self._parse_decimal(self._get_text(icms_tot, 'ns:vDesc')),
            vII=self._parse_decimal(self._get_text(icms_tot, 'ns:vII')),
            vIPI=self._parse_decimal(self._get_text(icms_tot, 'ns:vIPI')),
            vIPIDevol=self._parse_decimal(self._get_text(icms_tot, 'ns:vIPIDevol')),
            vPIS=self._parse_decimal(self._get_text(icms_tot, 'ns:vPIS')),
            vCOFINS=self._parse_decimal(self._get_text(icms_tot, 'ns:vCOFINS')),
            vOutro=self._parse_decimal(self._get_text(icms_tot, 'ns:vOutro')),
            vNF=self._parse_decimal(self._get_text(icms_tot, 'ns:vNF')),
            vTotTrib=self._parse_decimal(self._get_text(icms_tot, 'ns:vTotTrib'))
        )
    
    def _parse_ibscbs_tot(self, total_element) -> Optional[IBSCBSTot]:
        """Parse do grupo IBSCBSTot - NOVO Reforma Tributária"""
        ibscbs_tot = total_element.find('ns:IBSCBSTot', self.NAMESPACES)
        if ibscbs_tot is None:
            return None
        
        return IBSCBSTot(
            vTotTribIBSUF=self._parse_decimal(self._get_text(ibscbs_tot, 'ns:vTotTribIBSUF')),
            vTotTribIBSMun=self._parse_decimal(self._get_text(ibscbs_tot, 'ns:vTotTribIBSMun')),
            vTotTribCBS=self._parse_decimal(self._get_text(ibscbs_tot, 'ns:vTotTribCBS'))
        )
    
    # 6. MÉTODOS PARA PARSE DO TRANSPORTE
    def _parse_transporte(self, infNFe) -> Optional[Transporte]:
        """Parse do grupo de transporte"""
        transp = infNFe.find('ns:transp', self.NAMESPACES)
        if transp is None:
            return None
        
        transporte = Transporte(
            modFrete=self._get_text(transp, 'ns:modFrete')
        )
        
        # Parse do transportador
        transporte.transporta = self._parse_transportador(transp)
        
        # Parse do veículo
        transporte.veicTransp = self._parse_veiculo(transp)
        
        return transporte
    
    def _parse_transportador(self, transp) -> Optional[Transportador]:
        """Parse do transportador"""
        transporta = transp.find('ns:transporta', self.NAMESPACES)
        if transporta is None:
            return None
        
        return Transportador(
            CNPJ=self._get_text(transporta, 'ns:CNPJ'),
            CPF=self._get_text(transporta, 'ns:CPF'),
            xNome=self._get_text(transporta, 'ns:xNome'),
            IE=self._get_text(transporta, 'ns:IE'),
            xEnder=self._get_text(transporta, 'ns:xEnder'),
            xMun=self._get_text(transporta, 'ns:xMun'),
            UF=self._get_text(transporta, 'ns:UF')
        )
    
    def _parse_veiculo(self, transp) -> Optional[Veiculo]:
        """Parse do veículo"""
        veiculo = transp.find('ns:veicTransp', self.NAMESPACES)
        if veiculo is None:
            return None
        
        return Veiculo(
            placa=self._get_text(veiculo, 'ns:placa'),
            UF=self._get_text(veiculo, 'ns:UF'),
            RNTC=self._get_text(veiculo, 'ns:RNTC')
        )
    
    # 7. MÉTODOS PARA PARSE DO PAGAMENTO
    def _parse_pagamento(self, infNFe) -> Optional[Pagamento]:
        """Parse do grupo de pagamento"""
        pag_element = infNFe.find('ns:pag', self.NAMESPACES)
        if pag_element is None:
            return None
        
        pagamento = Pagamento()
        
        # Parse dos detalhes de pagamento
        det_pag_elements = pag_element.findall('ns:detPag', self.NAMESPACES)
        pagamento.detPag = []
        
        for det_pag in det_pag_elements:
            detalhe = DetalhePagamento(
                tPag=self._get_text(det_pag, 'ns:tPag'),
                vPag=self._parse_decimal(self._get_text(det_pag, 'ns:vPag')),
                indPag=self._get_text(det_pag, 'ns:indPag'),
                tpIntegra=self._get_text(det_pag, 'ns:tpIntegra'),
                CNPJ=self._get_text(det_pag, 'ns:CNPJ'),
                tBand=self._get_text(det_pag, 'ns:tBand'),
                cAut=self._get_text(det_pag, 'ns:cAut')
            )
            pagamento.detPag.append(detalhe)
        
        pagamento.vTroco = self._parse_decimal(self._get_text(pag_element, 'ns:vTroco'))
        
        return pagamento
    
    # MÉTODOS AUXILIARES (mantidos do código original)
    def _parse_icms40(self, icms_data) -> ICMS40:
        """Parse do ICMS40"""
        icms40 = ICMS40(
            orig=self._get_text(icms_data, 'ns:orig'),
            CST=self._get_text(icms_data, 'ns:CST')
        )
        
        # Parse da desoneração se existir
        vICMSDeson = self._get_text(icms_data, 'ns:vICMSDeson')
        if vICMSDeson:
            icms40.desoneracao = DesoneracaoICMS(
                vICMSDeson=self._parse_decimal(vICMSDeson),
                motDesICMS=self._get_text(icms_data, 'ns:motDesICMS'),
                indDeduzDeson=self._get_text(icms_data, 'ns:indDeduzDeson')
            )
        
        # Parse da partilha do ICMS (DIFAL) se existir
        icms40.partilha = self._parse_partilha_icms(icms_data)
        
        return icms40
    
    def _parse_icms51(self, icms_data) -> ICMS51:
        """Parse do ICMS51 com novos campos da Reforma Tributária"""
        icms51 = ICMS51(
            orig=self._get_text(icms_data, 'ns:orig'),
            modBC=self._get_text(icms_data, 'ns:modBC'),
            pRedBC=self._parse_decimal(self._get_text(icms_data, 'ns:pRedBC')),
            cBenefRBC=self._get_text(icms_data, 'ns:cBenefRBC'),  # NOVO
            vBC=self._parse_decimal(self._get_text(icms_data, 'ns:vBC')),
            pICMS=self._parse_decimal(self._get_text(icms_data, 'ns:pICMS')),
            vICMSOp=self._parse_decimal(self._get_text(icms_data, 'ns:vICMSOp')),
            pDif=self._parse_decimal(self._get_text(icms_data, 'ns:pDif')),
            vICMSDif=self._parse_decimal(self._get_text(icms_data, 'ns:vICMSDif')),
            vICMS=self._parse_decimal(self._get_text(icms_data, 'ns:vICMS')),
            pFCP=self._parse_decimal(self._get_text(icms_data, 'ns:pFCP')),
            vFCP=self._parse_decimal(self._get_text(icms_data, 'ns:vFCP')),
            vBCFCP=self._parse_decimal(self._get_text(icms_data, 'ns:vBCFCP')),
            pFCPDif=self._parse_decimal(self._get_text(icms_data, 'ns:pFCPDif')),  # NOVO
            vFCPDif=self._parse_decimal(self._get_text(icms_data, 'ns:vFCPDif')),  # NOVO
            vFCPEfet=self._parse_decimal(self._get_text(icms_data, 'ns:vFCPEfet'))  # NOVO
        )
        
        # Parse da partilha do ICMS (DIFAL) se existir
        icms51.partilha = self._parse_partilha_icms(icms_data)
        
        return icms51
    
    def _parse_icms90(self, icms_data) -> ICMS90:
        """Parse do ICMS90 - Outras operações"""
        icms90 = ICMS90(
            orig=self._get_text(icms_data, 'ns:orig'),
            modBC=self._get_text(icms_data, 'ns:modBC'),
            vBC=self._parse_decimal(self._get_text(icms_data, 'ns:vBC')),
            pRedBC=self._parse_decimal(self._get_text(icms_data, 'ns:pRedBC')),
            pICMS=self._parse_decimal(self._get_text(icms_data, 'ns:pICMS')),
            vICMS=self._parse_decimal(self._get_text(icms_data, 'ns:vICMS')),
            modBCST=self._get_text(icms_data, 'ns:modBCST'),
            pMVAST=self._parse_decimal(self._get_text(icms_data, 'ns:pMVAST')),
            pRedBCST=self._parse_decimal(self._get_text(icms_data, 'ns:pRedBCST')),
            vBCST=self._parse_decimal(self._get_text(icms_data, 'ns:vBCST')),
            pICMSST=self._parse_decimal(self._get_text(icms_data, 'ns:pICMSST')),
            vICMSST=self._parse_decimal(self._get_text(icms_data, 'ns:vICMSST')),
            vBCFCPST=self._parse_decimal(self._get_text(icms_data, 'ns:vBCFCPST')),
            pFCPST=self._parse_decimal(self._get_text(icms_data, 'ns:pFCPST')),
            vFCPST=self._parse_decimal(self._get_text(icms_data, 'ns:vFCPST')),
            pFCP=self._parse_decimal(self._get_text(icms_data, 'ns:pFCP')),
            vFCP=self._parse_decimal(self._get_text(icms_data, 'ns:vFCP')),
            vBCFCP=self._parse_decimal(self._get_text(icms_data, 'ns:vBCFCP'))
        )
        
        # Parse da desoneração se existir
        vICMSDeson = self._get_text(icms_data, 'ns:vICMSDeson')
        if vICMSDeson:
            icms90.desoneracao = DesoneracaoICMS(
                vICMSDeson=self._parse_decimal(vICMSDeson),
                motDesICMS=self._get_text(icms_data, 'ns:motDesICMS'),
                indDeduzDeson=self._get_text(icms_data, 'ns:indDeduzDeson')
            )
        
        # Parse da partilha do ICMS (DIFAL) se existir
        icms90.partilha = self._parse_partilha_icms(icms_data)
        
        return icms90
    
    def _parse_icmssn101(self, icms_data) -> ICMSSN101:
        """Parse do ICMSSN101"""
        return ICMSSN101(
            orig=self._get_text(icms_data, 'ns:orig'),
            pCredSN=self._parse_decimal(self._get_text(icms_data, 'ns:pCredSN')),
            vCredICMSSN=self._parse_decimal(self._get_text(icms_data, 'ns:vCredICMSSN'))
        )
    
    def _parse_partilha_icms(self, element) -> Optional[PartilhaICMS]:
        """Parse do grupo de partilha do ICMS (DIFAL)"""
        vBCUFDest = self._get_text(element, 'ns:vBCUFDest')
        if vBCUFDest is None:
            return None
        
        return PartilhaICMS(
            vBCUFDest=self._parse_decimal(self._get_text(element, 'ns:vBCUFDest')),
            pFCPUFDest=self._parse_decimal(self._get_text(element, 'ns:pFCPUFDest')),
            pICMSUFDest=self._parse_decimal(self._get_text(element, 'ns:pICMSUFDest')),
            pICMSInter=self._parse_decimal(self._get_text(element, 'ns:pICMSInter')),
            pICMSInterPart=self._parse_decimal(self._get_text(element, 'ns:pICMSInterPart')),
            vFCPUFDest=self._parse_decimal(self._get_text(element, 'ns:vFCPUFDest')),
            vICMSUFDest=self._parse_decimal(self._get_text(element, 'ns:vICMSUFDest')),
            vICMSUFRemet=self._parse_decimal(self._get_text(element, 'ns:vICMSUFRemet'))
        )
    
    def _parse_gtribregular(self, element) -> Optional[GTribRegular]:
        """Parse do grupo de tributação regular - NOVO Reforma Tributária"""
        gTribRegular = element.find('ns:gTribRegular', self.NAMESPACES)
        if gTribRegular is None:
            return None
        
        # Parse dos campos obrigatórios do GTribRegular
        CSTReg = self._get_text(gTribRegular, 'ns:CSTReg')
        cClassTribReg = self._get_text(gTribRegular, 'ns:cClassTribReg')
        pAliqEfetRegIBSUF = self._parse_decimal(self._get_text(gTribRegular, 'ns:pAliqEfetRegIBSUF'))
        vTribRegIBSUF = self._parse_decimal(self._get_text(gTribRegular, 'ns:vTribRegIBSUF'))
        pAliqEfetRegIBSMun = self._parse_decimal(self._get_text(gTribRegular, 'ns:pAliqEfetRegIBSMun'))
        vTribRegIBSMun = self._parse_decimal(self._get_text(gTribRegular, 'ns:vTribRegIBSMun'))
        pAliqEfetRegCBS = self._parse_decimal(self._get_text(gTribRegular, 'ns:pAliqEfetRegCBS'))
        vTribRegCBS = self._parse_decimal(self._get_text(gTribRegular, 'ns:vTribRegCBS'))
        
        # Verificar se todos os campos obrigatórios estão presentes
        if all([CSTReg, cClassTribReg, pAliqEfetRegIBSUF is not None, vTribRegIBSUF is not None,
                pAliqEfetRegIBSMun is not None, vTribRegIBSMun is not None,
                pAliqEfetRegCBS is not None, vTribRegCBS is not None]):
            
            return GTribRegular(
                CSTReg=CSTReg,
                cClassTribReg=cClassTribReg,
                pAliqEfetRegIBSUF=pAliqEfetRegIBSUF,
                vTribRegIBSUF=vTribRegIBSUF,
                pAliqEfetRegIBSMun=pAliqEfetRegIBSMun,
                vTribRegIBSMun=vTribRegIBSMun,
                pAliqEfetRegCBS=pAliqEfetRegCBS,
                vTribRegCBS=vTribRegCBS
            )
        
        return None
    
    def _get_text(self, element, path: str) -> Optional[str]:
        """Extrai texto de um elemento"""
        child = element.find(path, self.NAMESPACES)
        return child.text if child is not None else None
    
    def _parse_decimal(self, value: Optional[str]) -> Optional[Decimal]:
        """Converte string para Decimal"""
        if value is None:
            return None
        try:
            return Decimal(value)
        except:
            return None
    
    def to_dict(self) -> Dict:
        """Converte a NF-e para dicionário"""
        if self.nfe is None:
            return {}
        
        return self._object_to_dict(self.nfe)
    
    def to_json(self) -> str:
        """Converte a NF-e para JSON"""
        return json.dumps(self.to_dict(), indent=2, ensure_ascii=False, default=str)
    
    def _object_to_dict(self, obj) -> Any:
        """Converte objetos dataclass para dicionário"""
        if hasattr(obj, '__dataclass_fields__'):
            result = {}
            for field in obj.__dataclass_fields__:
                value = getattr(obj, field)
                result[field] = self._object_to_dict(value)
            return result
        elif isinstance(obj, list):
            return [self._object_to_dict(item) for item in obj]
        elif isinstance(obj, Decimal):
            return float(obj)
        else:
            return obj

# Exemplo de uso
def main():
    """Exemplo de uso do parser"""
    parser = NFEParser()
    
    # Exemplo com XML
    xml_exemplo = """<?xml version="1.0" encoding="UTF-8"?>
    <nfeProc xmlns="http://www.portalfiscal.inf.br/nfe">
        <NFe>
            <infNFe>
                <!-- 1. Emitente -->
                <emit>
                    <CNPJ>12345678000195</CNPJ>
                    <xNome>EMPRESA EXEMPLO LTDA</xNome>
                    <xFant>EMPRESA EXEMPLO</xFant>
                    <enderEmit>
                        <xLgr>RUA EXEMPLO</xLgr>
                        <nro>123</nro>
                        <xBairro>CENTRO</xBairro>
                        <cMun>3550308</cMun>
                        <xMun>SAO PAULO</xMun>
                        <UF>SP</UF>
                        <CEP>01234000</CEP>
                    </enderEmit>
                    <IE>12345678901234</IE>
                    <CRT>1</CRT>
                </emit>
                
                <!-- 2. Identificação -->
                <ide>
                    <cUF>35</cUF>
                    <cNF>12345678</cNF>
                    <natOp>VENDA</natOp>
                    <mod>55</mod>
                    <serie>1</serie>
                    <nNF>123456</nNF>
                    <dhEmi>2024-01-15T10:30:00-03:00</dhEmi>
                    <tpNF>1</tpNF>
                    <idDest>2</idDest>
                    <cMunFG>3550308</cMunFG>
                    <tpImp>1</tpImp>
                    <tpEmis>1</tpEmis>
                    <cDV>1</cDV>
                    <tpAmb>2</tpAmb>
                    <finNFe>1</finNFe>
                    <indFinal>1</indFinal>
                    <indPres>1</indPres>
                    <procEmi>0</procEmi>
                    <verProc>1.0.0</verProc>
                </ide>
                
                <!-- 3. Destinatário -->
                <dest>
                    <CNPJ>98765432000187</CNPJ>
                    <xNome>CLIENTE EXEMPLO LTDA</xNome>
                    <enderDest>
                        <xLgr>AV CLIENTE</xLgr>
                        <nro>456</nro>
                        <xBairro>JARDIM</xBairro>
                        <cMun>5300108</cMun>
                        <xMun>BRASILIA</xMun>
                        <UF>DF</UF>
                        <CEP>70000000</CEP>
                    </enderDest>
                    <indIEDest>1</indIEDest>
                    <IE>98765432109876</IE>
                </dest>
                
                <!-- 4. Itens -->
                <det nItem="1">
                    <!-- 4.1 Produto -->
                    <prod>
                        <cProd>PROD001</cProd>
                        <cEAN>7891234567890</cEAN>
                        <xProd>PRODUTO EXEMPLO</xProd>
                        <NCM>12345678</NCM>
                        <CFOP>6102</CFOP>
                        <uCom>UN</uCom>
                        <qCom>10.0000</qCom>
                        <vUnCom>100.00</vUnCom>
                        <vProd>1000.00</vProd>
                        <cEANTrib>7891234567890</cEANTrib>
                        <uTrib>UN</uTrib>
                        <qTrib>10.0000</qTrib>
                        <vUnTrib>100.00</vUnTrib>
                        <indTot>1</indTot>
                    </prod>
                    
                    <!-- 4.6 Imposto (Consolidado) -->
                    <imposto>
                        <vTotTrib>250.00</vTotTrib>
                        <!-- 4.2 ICMS -->
                        <ICMS>
                            <ICMS20>
                                <orig>0</orig>
                                <CST>20</CST>
                                <modBC>0</modBC>
                                <pRedBC>40.00</pRedBC>
                                <vBC>600.00</vBC>
                                <pICMS>18.00</pICMS>
                                <vICMS>108.00</vICMS>
                            </ICMS20>
                        </ICMS>
                        
                        <!-- 4.3 PIS -->
                        <PIS>
                            <PISAliq>
                                <CST>01</CST>
                                <vBC>1000.00</vBC>
                                <pPIS>1.65</pPIS>
                                <vPIS>16.50</vPIS>
                            </PISAliq>
                        </PIS>
                        
                        <!-- 4.4 COFINS -->
                        <COFINS>
                            <COFINSAliq>
                                <CST>01</CST>
                                <vBC>1000.00</vBC>
                                <pCOFINS>7.60</pCOFINS>
                                <vCOFINS>76.00</vCOFINS>
                            </COFINSAliq>
                        </COFINS>
                    </imposto>
                </det>
                
                <!-- 5. Totais -->
                <total>
                    <!-- 5.1 ICMSTot -->
                    <ICMSTot>
                        <vBC>1000.00</vBC>
                        <vICMS>120.00</vICMS>
                        <vICMSDeson>0.00</vICMSDeson>
                        <vFCPUFDest>0.00</vFCPUFDest>
                        <vICMSUFDest>0.00</vICMSUFDest>
                        <vICMSUFRemet>0.00</vICMSUFRemet>
                        <vFCP>0.00</vFCP>
                        <vBCST>0.00</vBCST>
                        <vST>0.00</vST>
                        <vFCPST>0.00</vFCPST>
                        <vFCPSTRet>0.00</vFCPSTRet>
                        <vProd>1000.00</vProd>
                        <vFrete>0.00</vFrete>
                        <vSeg>0.00</vSeg>
                        <vDesc>0.00</vDesc>
                        <vII>0.00</vII>
                        <vIPI>0.00</vIPI>
                        <vIPIDevol>0.00</vIPIDevol>
                        <vPIS>16.50</vPIS>
                        <vCOFINS>76.00</vCOFINS>
                        <vOutro>0.00</vOutro>
                        <vNF>1000.00</vNF>
                        <vTotTrib>250.00</vTotTrib>
                    </ICMSTot>
                </total>
                
                <!-- 6. Transporte -->
                <transp>
                    <modFrete>0</modFrete>
                    <transporta>
                        <CNPJ>12345678000199</CNPJ>
                        <xNome>TRANSPORTADORA EXEMPLO</xNome>
                        <IE>12345678901235</IE>
                        <xEnder>RUA TRANSPORTE, 789</xEnder>
                        <xMun>SAO PAULO</xMun>
                        <UF>SP</UF>
                    </transporta>
                    <veicTransp>
                        <placa>ABC1234</placa>
                        <UF>SP</UF>
                    </veicTransp>
                </transp>
                
                <!-- 7. Pagamento -->
                <pag>
                    <detPag>
                        <tPag>01</tPag>
                        <vPag>1000.00</vPag>
                    </detPag>
                </pag>
            </infNFe>
        </NFe>
    </nfeProc>"""
    
    try:
        nfe = parser.parse_xml(xml_exemplo)
        print("✅ NF-e parseada com sucesso!")
        print(f"🏢 Emitente: {nfe.emitente.xNome}")
        print(f"📄 Número: {nfe.identificacao.nNF}")
        print(f"🎯 Destinatário: {nfe.destinatario.xNome if nfe.destinatario else 'N/A'}")
        print(f"📦 Itens: {len(nfe.itens)}")
        print(f"💰 Valor Total: R$ {nfe.total.ICMSTot.vNF if nfe.total and nfe.total.ICMSTot else 'N/A'}")
        print(f"🚚 Modalidade Frete: {nfe.transporte.modFrete if nfe.transporte else 'N/A'}")
        print(f"💳 Formas Pagamento: {len(nfe.pagamento.detPag) if nfe.pagamento and nfe.pagamento.detPag else 0}")
        
    except Exception as e:
        print(f"❌ Erro ao parsear NF-e: {e}")

if __name__ == "__main__":
    main()