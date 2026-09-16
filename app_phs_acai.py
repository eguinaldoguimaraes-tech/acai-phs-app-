import streamlit as st
import pandas as pd
import numpy as np
from calculadora_phs_acai import CalculadoraPHSAcai, PISO_CONAB_LATA, FATOR_VALORIZACAO_PHS

# Configuração da Página
st.set_page_config(
    page_title="Tecnologia Social: Precificação Justa do Açaí (PHS)",
    page_icon="🌴",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilização Visual Regional
st.markdown("""
<style>
    .main-header { font-size: 26px; font-weight: bold; color: #1e4620; text-align: center; margin-bottom: 5px; }
    .sub-header { font-size: 16px; color: #4a5568; text-align: center; margin-bottom: 25px; }
    .card-piso { background-color: #fff5f5; border-left: 6px solid #e53e3e; padding: 15px; border-radius: 8px; margin-bottom: 15px; }
    .card-phs { background-color: #f0fff4; border-left: 6px solid #38a169; padding: 15px; border-radius: 8px; margin-bottom: 15px; }
    .card-porto { background-color: #ebf8ff; border-left: 6px solid #3182ce; padding: 15px; border-radius: 8px; margin-bottom: 15px; }
    .card-conab { background-color: #fffff0; border-left: 6px solid #d69e2e; padding: 15px; border-radius: 8px; margin-bottom: 15px; }
    .big-stat { font-size: 24px; font-weight: bold; margin-top: 5px; }
    .stat-label { font-size: 13px; text-transform: uppercase; color: #718096; }
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='main-header'>🌴 APP PRECIFICAÇÃO JUSTA DO AÇAÍ (PHS)</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-header'>Tecnologia Social de Código Aberto para Agricultores Familiares Ribeirinhos (AFR)</div>", unsafe_allow_html=True)

# --- SIDEBAR: PAINEL DE ENTRADAS DO AGRICULTOR ---
st.sidebar.header("⚙️ 1. Dados da Colheita & Custos")
qtd_latas = st.sidebar.number_input("Latas de 14 kg Colhidas no Dia", min_value=1.0, max_value=500.0, value=20.0, step=1.0)
valor_diaria = st.sidebar.number_input("Valor da Diária Familiar (R$)", min_value=30.0, max_value=300.0, value=80.0, step=5.0)
horas_colheita = st.sidebar.slider("Horas de Trabalho da Família no Dia", 1.0, 14.0, 6.0, 0.5)

st.sidebar.subheader("⛽ Insumos & Combustível")
litros_colheita = st.sidebar.number_input("Litros de Gasolina/Diesel na Colheita", min_value=0.0, max_value=100.0, value=4.0, step=0.5)
preco_gasolina = st.sidebar.number_input("Preço do Litro do Combustível (R$)", min_value=3.0, max_value=15.0, value=6.50, step=0.10)
custo_sacos = st.sidebar.number_input("Gastos com Sacos de Nylon/Apetrechos (R$)", min_value=0.0, max_value=100.0, value=10.0, step=2.0)

st.sidebar.header("🚤 2. Logística Fluvial & Transporte")
embarcacao = st.sidebar.selectbox("Tipo de Embarcacao", ["Rabeta", "Voadeira", "Catraia", "Lancha"])
horas_navegacao = st.sidebar.slider("Tempo Total de Viagem (Ida + Espera + Volta - Horas)", 0.5, 16.0, 5.0, 0.5)
litros_viagem = st.sidebar.number_input("Litros de Gasolina na Viagem ao Porto", min_value=0.0, max_value=200.0, value=8.0, step=1.0)

st.sidebar.header("📊 3. Preços de Mercado (R$/Lata de 14 kg)")
preco_beira_rio = st.sidebar.number_input("Preço Oferecido no Beira-Rio (R$ / lata 14kg)", min_value=5.0, max_value=200.0, value=35.0, step=1.0)
preco_porto = st.sidebar.number_input("Preço Cotado no Porto Urbano (R$ / lata 14kg)", min_value=5.0, max_value=250.0, value=55.0, step=1.0)

# --- INSTANCIAÇÃO DA CALCULADORA ---
calc = CalculadoraPHSAcai(
    qtd_latas=qtd_latas,
    valor_diaria_familiar=valor_diaria,
    horas_trabalho_familia=horas_colheita,
    litros_combustivel_colheita=litros_colheita,
    preco_litro_combustivel=preco_gasolina,
    custo_sacos_nylon=custo_sacos
)

privado = calc.calcular_custo_privado()
logistica = calc.simular_logistica_porto(
    preco_beira_rio_lata=preco_beira_rio,
    preco_porto_lata=preco_porto,
    horas_navegacao_total=horas_navegacao,
    litros_combustivel_viagem=litros_viagem
)
phs = calc.calcular_phs(preco_mercado_lata=preco_beira_rio)
pgpm = calc.verificar_pgpmbio(preco_oferecido_lata=preco_beira_rio)

# --- CONTEÚDO PRINCIPAL: DASHBOARD DE DECISÃO ---

col1, col2 = st.columns(2)

with col1:
    st.markdown("<div class='card-piso'>", unsafe_allow_html=True)
    st.markdown("<div class='stat-label'>🔴 Custo Privado & Preço Piso de Sobrevivência</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='big-stat'>R$ {privado['preco_piso_sobrevivencia_lata']:.2f} <span style='font-size:14px; font-weight:normal;'>/ lata de 14 kg</span></div>", unsafe_allow_html=True)
    st.write(f"• **Custo Total da Colheita:** R$ {privado['custo_total_privado']:.2f}")
    st.write(f"• **Custo de Produção por Lata:** R$ {privado['custo_por_lata_14kg']:.2f}")
    st.write(f"• **Mão de Obra Familiar (Diária):** R$ {privado['custo_mao_obra_familia']:.2f}")
    st.caption("Aviso: Vender abaixo desse piso gera prejuízo direto para o agricultor!")
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='card-phs'>", unsafe_allow_html=True)
    st.markdown("<div class='stat-label'>🟢 Preço Hedônico Socioambiental (PHS - Valor Intrínseco)</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='big-stat'>R$ {phs['preco_phs_lata']:.2f} <span style='font-size:14px; font-weight:normal;'>/ lata de 14 kg (+49,31%)</span></div>", unsafe_allow_html=True)
    st.write(f"• **Ganho Adicional por Lata:** + R$ {phs['ganho_adicional_por_lata']:.2f}")
    st.write(f"• **Ganho Adicional na Safra ({qtd_latas:.0f} latas):** + R$ {phs['ganho_adicional_total_safra']:.2f}")
    st.write(f"• **Composição da Lata:** Econômico (R$ {phs['decomposicao_lata']['componente_economico_40.3%']:.2f}) | Social (R$ {phs['decomposicao_lata']['componente_social_46.8%']:.2f}) | Ambiental (R$ {phs['decomposicao_lata']['componente_ambiental_12.9%']:.2f})")
    st.caption("Valor de referência para negociações com Cooperativas, Agroindústrias e Exportação.")
    st.markdown("</div>", unsafe_allow_html=True)

col3, col4 = st.columns(2)

with col3:
    st.markdown("<div class='card-porto'>", unsafe_allow_html=True)
    st.markdown("<div class='stat-label'>🚤 Recomendação Logística (Tempo & Frete)</div>", unsafe_allow_html=True)
    rec_color = "green" if logistica['recomendacao'] == "IR AO PORTO" else "orange"
    st.markdown(f"<div class='big-stat' style='color:{rec_color};'>{logistica['recomendacao']}</div>", unsafe_allow_html=True)
    st.write(f"• **Lucro Líquido no Beira-Rio:** R$ {logistica['lucro_liquido_beira_rio']:.2f}")
    st.write(f"• **Lucro Líquido no Porto:** R$ {logistica['lucro_liquido_porto']:.2f}")
    st.write(f"• **Custo do Tempo de Navegação ({horas_navegacao}h):** R$ {logistica['cot_transporte']:.2f}")
    st.write(f"• **Custo Total de Circulação:** R$ {logistica['custo_circulacao_total']:.2f}")
    st.markdown("</div>", unsafe_allow_html=True)

with col4:
    st.markdown("<div class='card-conab'>", unsafe_allow_html=True)
    st.markdown("<div class='stat-label'>⚖️ Proteção Social PGPM-Bio (Conab)</div>", unsafe_allow_html=True)
    if pgpm['elegivel_subvencao']:
        st.markdown(f"<div class='big-stat' style='color:#c53030;'>SUBVENÇÃO DISPONÍVEL</div>", unsafe_allow_html=True)
        st.write(f"• **Piso Oficial Conab:** R$ {PISO_CONAB_LATA:.2f} / lata (R$ 1,98/kg)")
        st.write(f"• **Diferença por Lata:** R$ {pgpm['subvencao_por_lata']:.2f}")
        st.write(f"• **Total a Receber da Conab:** R$ {pgpm['subvencao_total_receber']:.2f}")
    else:
        st.markdown(f"<div class='big-stat' style='color:#2f855a;'>PREÇO ACIMA DO PISO</div>", unsafe_allow_html=True)
        st.write(f"• **Piso Oficial Conab:** R$ {PISO_CONAB_LATA:.2f} / lata (R$ 1,98/kg)")
        st.write("• O preço de mercado atual cobre a exigência mínima governamental.")
    st.markdown("</div>", unsafe_allow_html=True)

# --- FICHA DE COMPROVANTE OFFLINE ---
st.subheader("📜 Comprovante / Ficha de Negociação Coletiva PHS")
ficha_text = f"""
====================================================================
           FICHA DE PRECIFICAÇÃO SOCIOAMBIENTAL DO AÇAÍ
====================================================================
Data / Safra: {qtd_latas:.0f} Latas de 14 kg (Total: {qtd_latas*14:.0f} kg)
Preço de Mercado Convencional: R$ {preco_beira_rio:.2f} / lata
--------------------------------------------------------------------
PREÇO HEDÔNICO SOCIOAMBIENTAL (PHS): R$ {phs['preco_phs_lata']:.2f} / lata
  - Valor Econômico (40,3%): R$ {phs['decomposicao_lata']['componente_economico_40.3%']:.2f}
  - Valor Social (46,8%): R$ {phs['decomposicao_lata']['componente_social_46.8%']:.2f}
  - Valor Ambiental (12,9%): R$ {phs['decomposicao_lata']['componente_ambiental_12.9%']:.2f}
--------------------------------------------------------------------
VALOR TOTAL DA SAFRA (MERCADO): R$ {preco_beira_rio * qtd_latas:.2f}
VALOR TOTAL DA SAFRA (PHS):     R$ {phs['preco_phs_lata'] * qtd_latas:.2f}
VALORIZAÇÃO JUSTA REPASSADA AO PRODUTOR: + R$ {phs['ganho_adicional_total_safra']:.2f}
====================================================================
"""
st.code(ficha_text, language="text")
