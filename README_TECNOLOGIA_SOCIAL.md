# 🌴 Tecnologia Social: Precificação Justa do Açaí (PHS)

**Sistema Integrado de Valoração e Precificação Socioambiental para Agricultores Familiares Ribeirinhos (AFR) na Amazônia**

---

## 📌 1. Manifesto e Objetivo Social

Os agricultores familiares ribeirinhos (AFR) da Amazônia — especialmente nas regiões do estuário, arquipélago do Marajó e municípios como Igarapé-Miri, Belém, Curralinho e Soure — enfrentam severas assimetrias de informação no comércio do açaí. Tradicionalmente, o preço do fruto é ditado por intermediários (marreteiros) e indústrias de processamento sem considerar os **custos reais de produção**, o **tempo de trabalho familiar** e a **preservação dos serviços ecossistêmicos da várzea**.

Esta **Tecnologia Social de Código Aberto e Gratuita** foi desenvolvida para empoderar os ribeirinhos e suas organizações coletivas (cooperativas e associações), permitindo precificar o açaí a partir do seu **valor intrínseco completo**, combinando o **Preço Hedônico Socioambiental (PHS)** com a valoração do tempo de transporte e a proteção social da PGPM-Bio.

---

## 📐 2. Fundamentação Metodológica

### A. Padronização Metrológica Regional
* **Unidade Base:** **Lata / Rasa de 14 kg** (padrão regional de comercialização nos portos do Pará e Amapá).
* **Fator de Conversão:** 1 saca industrial (60 kg) = 4,28 latas de 14 kg.
* **Piso Oficial PGPM-Bio (Conab):** R$ 1,98/kg = **R$ 27,72 por lata de 14 kg**.

### B. Preço Hedônico Socioambiental (PHS)
O PHS incorpora explicitamente os custos ocultados pelo mercado convencional:
1. **Custos Econômicos (40,3% do custo):** Insumos diretos, combustível, sacos de nylon, apetrechos (peçonhas, terçados) e depreciação da embarcação.
2. **Custos Sociais (46,8% do custo):** Remuneração da mão de obra familiar, pró-labore do gestor da unidade familiar e valorização do saber tradicional.
3. **Custos Ambientais (12,9% do custo):** Custo de oportunidade da terra, valoração dos serviços ecossistêmicos (água e solo) e sequestro de carbono da floresta de várzea mantida em pé.

> **Resultado:** O PHS proporciona uma valorização justa de **+49,31%** sobre o preço de mercado convencional.

### C. Valoração do Tempo de Navegação Fluvial (COT)
O tempo de viagem do ribeirinho em embarcações (rabetas, voadeiras) é integrado à planilha de transporte via **Custo de Oportunidade do Tempo (COT)**:
$$\text{COT}_{\text{transporte}} = \text{Horas Totais de Viagem} \times \left( \frac{\text{Valor da Diária Familiar}}{8 \text{ horas}} \right)$$

---

## 🛠️ 3. Componentes da Solução Tecnológica

Este repositório contém quatro artefatos prontos para implementação:

1. **`calculadora_phs_acai.py` (Motor Matemático em Python):**
   * Classe orientada a objetos sem dependências externas complexas.
   * Modula custos privados, simulação logística, matriz PHS e checagem de subvenção Conab.

2. **`schema_offline.sql` (Esquema de Banco de Dados SQLite):**
   * Estrutura relacional offline-first otimizada para smartphones rurais e sistemas de cooperativas.
   * Inclui tabelas para cadastros de várzea, registros de colheita em latas de 14 kg, viagens logísticas e a view consultiva `v_resumo_safra_phs`.

3. **`app_phs_acai.py` (Protótipo Interativo Streamlit):**
   * Interface gráfica responsiva com painéis semafóricos (Vermelho: Custo Piso / Verde: PHS / Azul: Logística / Amarelo: Conab).
   * Gerador automático de **Ficha de Precificação Socioambiental** para emissão de comprovantes de negociação.

4. **`README_TECNOLOGIA_SOCIAL.md` (Manual da Tecnologia Social):**
   * Este documento de orientação geral para difusão e replicação comunitária.

---

## 🚀 4. Guia de Instalação e Execução Local

### Pré-requisitos
* Python 3.9+ instalado.
* SQLite3 instalado.

### Instalação das Dependências (Gratuitas)
```bash
pip install streamlit pandas numpy
```

### Como Executar o Aplicativo Protótipo
```bash
streamlit run app_phs_acai.py
```

---

## 🤝 5. Diretrizes para Replicação por Universidades e ATER

Esta Tecnologia Social foi concebida para ser adotada, sem custos de licenciamento, por:
* **Entidades de Extensão Rural (EMATER / ATER Privada e Comunitária):** Para utilização em cadernos de campo digitais.
* **Institutos de Pesquisa e Universidades (UFPA, UFRA, Embrapa):** Para servir de base em projetos de extensão com cooperativas extrativistas.
* **Cooperativas e Associações de Ribeirinhos:** Para implantação na sede ou nos trapiches comunitários.

---

## 📜 6. Licença e Direitos

Este projeto é disponibilizado sob a licença **Creative Commons Atribuição-CompartilhaIgual (CC BY-SA 4.0)** e **MIT License**. É livre para cópia, modificação, distribuição e uso por qualquer comunidade tradicional ou instituição pública.
