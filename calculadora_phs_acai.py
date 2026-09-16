"""
Motor Matemático e de Precificação Justa do Açaí (PHS)
Tecnologia Social de Código Aberto para Agricultores Familiares Ribeirinhos (AFR)
Unidade Padrão: Lata / Rasa de 14 kg
"""

import math

# --- CONSTANTES METROLÓGICAS E DE MERCADO ---
PESO_LATA_KG = 14.0  # 1 lata/rasa = 14 kg
PISO_CONAB_KG = 1.98  # R$/kg (PGPM-Bio Pará)
PISO_CONAB_LATA = PISO_CONAB_KG * PESO_LATA_KG  # R$ 27.72 por lata de 14 kg

# --- CONSTANTES PHS (ESTRUTURA DE CUSTOS E VALORIZAÇÃO) ---
COMPOSICAO_PHS = {
    'economico': 0.403,  # 40,3% custos econômicos/privados
    'social': 0.468,     # 46,8% custos sociais (capital humano e trabalho)
    'ambiental': 0.129   # 12,9% custos ambientais (serviços ecossistêmicos)
}
FATOR_VALORIZACAO_PHS = 0.4931  # +49,31% sobre o preço de mercado convencional

class CalculadoraPHSAcai:
    def __init__(
        self,
        qtd_latas: float,
        valor_diaria_familiar: float = 80.0,
        horas_trabalho_familia: float = 8.0,
        litros_combustivel_colheita: float = 0.0,
        preco_litro_combustivel: float = 6.50,
        custo_sacos_nylon: float = 0.0,
        custo_ferramentas_dia: float = 5.0,
        ajudantes_diarias_pagas: float = 0.0,
        taxa_perdas_clima: float = 0.08  # 8% de taxa de perdas/risco
    ):
        self.qtd_latas = float(qtd_latas)
        self.valor_diaria_familiar = float(valor_diaria_familiar)
        self.valor_hora_familiar = self.valor_diaria_familiar / 8.0
        self.horas_trabalho_familia = float(horas_trabalho_familia)
        self.litros_combustivel_colheita = float(litros_combustivel_colheita)
        self.preco_litro_combustivel = float(preco_litro_combustivel)
        self.custo_sacos_nylon = float(custo_sacos_nylon)
        self.custo_ferramentas_dia = float(custo_ferramentas_dia)
        self.ajudantes_diarias_pagas = float(ajudantes_diarias_pagas)
        self.taxa_perdas_clima = float(taxa_perdas_clima)

    def calcular_custo_privado(self) -> dict:
        """Calcula os Custos Variáveis e Fixos da colheita familiar"""
        # Custo do trabalho familiar na colheita
        custo_mao_obra_familia = self.horas_trabalho_familia * self.valor_hora_familiar
        
        # Custos insumos diretos
        custo_combustivel = self.litros_combustivel_colheita * self.preco_litro_combustivel
        custo_direto_insumos = (
            custo_combustivel + 
            self.custo_sacos_nylon + 
            self.custo_ferramentas_dia + 
            self.ajudantes_diarias_pagas
        )
        
        # Custos Variáveis (VC)
        vc_subtotal = custo_mao_obra_familia + custo_direto_insumos
        reserva_risco = vc_subtotal * self.taxa_perdas_clima
        vc_total = vc_subtotal + reserva_risco
        
        # Custos Fixos (FC) - Depreciação e Custo de Capital Próprio
        depreciacao_equipamentos = 5.0  # R$/dia estimado para barco/motor/ferramentas
        custo_capital = vc_total * 0.10  # 10% de oportunidade do capital
        fc_total = depreciacao_equipamentos + custo_capital
        
        custo_total_privado = vc_total + fc_total
        custo_por_lata = custo_total_privado / self.qtd_latas if self.qtd_latas > 0 else 0.0
        
        # Preço de sobrevivência (Custo por lata + 15% markup de garantia)
        preco_piso_sobrevivencia = custo_por_lata * 1.15

        return {
            'custo_mao_obra_familia': round(custo_mao_obra_familia, 2),
            'custo_insumos_diretos': round(custo_direto_insumos, 2),
            'reserva_risco': round(reserva_risco, 2),
            'vc_total': round(vc_total, 2),
            'fc_total': round(fc_total, 2),
            'custo_total_privado': round(custo_total_privado, 2),
            'custo_por_lata_14kg': round(custo_por_lata, 2),
            'preco_piso_sobrevivencia_lata': round(preco_piso_sobrevivencia, 2)
        }

    def simular_logistica_porto(
        self,
        preco_beira_rio_lata: float,
        preco_porto_lata: float,
        horas_navegacao_total: float,
        litros_combustivel_viagem: float,
        frete_terceiros: float = 0.0,
        depreciacao_embarcacao_viagem: float = 10.0
    ) -> dict:
        """Compara a venda na beira do rio vs. transporte até o porto urbano incluindo o Custo de Oportunidade do Tempo (COT)"""
        # Custo do tempo de viagem do agricultor
        cot_transporte = horas_navegacao_total * self.valor_hora_familiar
        
        # Custo financeiro do transporte
        custo_combustivel_viagem = litros_combustivel_viagem * self.preco_litro_combustivel
        custo_circulacao_total = (
            custo_combustivel_viagem + 
            frete_terceiros + 
            depreciacao_embarcacao_viagem + 
            cot_transporte
        )
        
        # Receita e Lucro na Beira-Rio
        receita_beira_rio = self.qtd_latas * preco_beira_rio_lata
        custo_privado = self.calcular_custo_privado()['custo_total_privado']
        lucro_beira_rio = receita_beira_rio - custo_privado
        
        # Receita e Lucro no Porto Urbano
        receita_porto = self.qtd_latas * preco_porto_lata
        lucro_porto_liquido = receita_porto - custo_privado - custo_circulacao_total
        
        diferenca_lucro = lucro_porto_liquido - lucro_beira_rio
        recomendacao = "IR AO PORTO" if diferenca_lucro > 0 else "VENDER NA BEIRA-RIO"

        return {
            'cot_transporte': round(cot_transporte, 2),
            'custo_combustivel_viagem': round(custo_combustivel_viagem, 2),
            'custo_circulacao_total': round(custo_circulacao_total, 2),
            'lucro_liquido_beira_rio': round(lucro_beira_rio, 2),
            'lucro_liquido_porto': round(lucro_porto_liquido, 2),
            'ganho_liquido_viagem': round(diferenca_lucro, 2),
            'recomendacao': recomendacao
        }

    def calcular_phs(self, preco_mercado_lata: float, margem_wtp_percentual: float = 0.0) -> dict:
        """Calcula o Preço Hedônico Socioambiental (PHS) por lata de 14 kg"""
        # PHS com fator de valorização de +49,31%
        preco_phs_base = preco_mercado_lata * (1.0 + FATOR_VALORIZACAO_PHS)
        
        # Adicional de Disposição a Pagar (WTP+) para mercados de nicho
        preco_phs_final = preco_phs_base * (1.0 + (margem_wtp_percentual / 100.0))
        
        # Decomposição do Valor Intrínseco
        valor_economico = preco_phs_final * COMPOSICAO_PHS['economico']
        valor_social = preco_phs_final * COMPOSICAO_PHS['social']
        valor_ambiental = preco_phs_final * COMPOSICAO_PHS['ambiental']
        
        ganho_por_lata = preco_phs_final - preco_mercado_lata
        ganho_total_safra = ganho_por_lata * self.qtd_latas

        return {
            'preco_mercado_lata': round(preco_mercado_lata, 2),
            'preco_phs_lata': round(preco_phs_final, 2),
            'fator_valorizacao': "+49.31%",
            'decomposicao_lata': {
                'componente_economico_40.3%': round(valor_economico, 2),
                'componente_social_46.8%': round(valor_social, 2),
                'componente_ambiental_12.9%': round(valor_ambiental, 2)
            },
            'ganho_adicional_por_lata': round(ganho_por_lata, 2),
            'ganho_adicional_total_safra': round(ganho_total_safra, 2)
        }

    def verificar_pgpmbio(self, preco_oferecido_lata: float) -> dict:
        """Verifica se o preço oferecido está abaixo do piso da PGPM-Bio (Conab - R$ 27,72/lata de 14 kg)"""
        abaixo_do_piso = preco_oferecido_lata < PISO_CONAB_LATA
        diferenca_por_lata = PISO_CONAB_LATA - preco_oferecido_lata if abaixo_do_piso else 0.0
        subvencao_total = diferenca_por_lata * self.qtd_latas if abaixo_do_piso else 0.0

        return {
            'piso_conab_lata_14kg': PISO_CONAB_LATA,
            'preco_oferecido_lata': round(preco_oferecido_lata, 2),
            'elegivel_subvencao': abaixo_do_piso,
            'subvencao_por_lata': round(diferenca_por_lata, 2),
            'subvencao_total_receber': round(subvencao_total, 2)
        }


# --- TESTE UNITÁRIO E SIMULAÇÃO NUMÉRICA ---
if __name__ == "__main__":
    print("=== TESTE DE CAMPO: COLHEITA DE 20 LATAS DE 14 KG ===")
    calc = CalculadoraPHSAcai(
        qtd_latas=20,
        valor_diaria_familiar=80.0,
        horas_trabalho_familia=6.0,
        litros_combustivel_colheita=4.0,
        preco_litro_combustivel=6.50,
        custo_sacos_nylon=10.0,
        custo_ferramentas_dia=5.0
    )
    
    privado = calc.calcular_custo_privado()
    print("1. Custo Privado:", privado)
    
    logistica = calc.simular_logistica_porto(
        preco_beira_rio_lata=35.0,
        preco_porto_lata=55.0,
        horas_navegacao_total=5.0,
        litros_combustivel_viagem=8.0
    )
    print("2. Logística Fluvial:", logistica)
    
    phs = calc.calcular_phs(preco_mercado_lata=35.0)
    print("3. Preço Hedônico Socioambiental (PHS):", phs)
    
    pgpm = calc.verificar_pgpmbio(preco_oferecido_lata=25.0)
    print("4. Alerta PGPM-Bio Conab:", pgpm)
