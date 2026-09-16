-- ============================================================================
-- ESQUEMA DE BANCO DE DADOS OFFLINE-FIRST (SQLite / SQLCipher)
-- Tecnologia Social para Precificação Justa do Açaí dos AFR
-- Unidade Padrão: Lata / Rasa de 14 kg
-- ============================================================================

PRAGMA foreign_keys = ON;

-- ----------------------------------------------------------------------------
-- 1. CADASTRO DO AGROECOSSISTEMA E PRODUTOR
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS agroecossistema (
    id TEXT PRIMARY KEY,                       -- UUID v4
    nome_produtor TEXT NOT NULL,
    comunidade_rio TEXT NOT NULL,
    municipio TEXT NOT NULL DEFAULT 'Igarapé-Miri',
    area_manejo_ha REAL NOT NULL,
    tipologia_varzea TEXT CHECK(tipologia_varzea IN ('ALTA', 'BAIXA')) NOT NULL,
    densidade_dap INTEGER NOT NULL,            -- Palmeiras produtoras/ha
    valor_diaria_familiar REAL NOT NULL DEFAULT 80.00,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ----------------------------------------------------------------------------
-- 2. REGISTRO DIÁRIO DE COLHEITA (UNIDADE: LATA DE 14 KG)
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS colheita_diaria (
    id TEXT PRIMARY KEY,                       -- UUID v4
    agroecossistema_id TEXT NOT NULL,
    data_colheita DATE NOT NULL,
    quantidade_latas_14kg REAL NOT NULL,
    horas_trabalho_familia REAL NOT NULL DEFAULT 8.0,
    litros_combustivel_colheita REAL DEFAULT 0.0,
    preco_litro_combustivel REAL DEFAULT 6.50,
    custo_sacos_nylon REAL DEFAULT 0.0,
    custo_ferramentas_dia REAL DEFAULT 5.0,
    ajudantes_diarias_pagas REAL DEFAULT 0.0,
    observacao_qualidade TEXT,                 -- Atributos de maturidade/rendimento
    gtv_emitida INTEGER CHECK(gtv_emitida IN (0, 1)) DEFAULT 0,
    synced INTEGER CHECK(synced IN (0, 1)) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (agroecossistema_id) REFERENCES agroecossistema(id) ON DELETE CASCADE
);

-- ----------------------------------------------------------------------------
-- 3. LOGÍSTICA FLUVIAL E VALORAÇÃO DO TEMPO DE NAVEGAÇÃO
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS viagem_logistica (
    id TEXT PRIMARY KEY,                       -- UUID v4
    colheita_id TEXT NOT NULL,
    destino_porto TEXT NOT NULL,               -- Ex: "Porto do Jurunas (Belém)", "Macapá"
    tipo_embarcacao TEXT CHECK(tipo_embarcacao IN ('RABETA', 'VOADEIRA', 'LANCHA', 'CATRAIA')) NOT NULL,
    horas_navegacao_total REAL NOT NULL,       -- Tempo total gasto (Ida + Espera + Volta)
    litros_combustivel_viagem REAL NOT NULL,
    frete_terceiros REAL DEFAULT 0.0,
    preco_beira_rio_lata REAL NOT NULL,        -- Preço oferecido pelo marreteiro (R$/lata 14kg)
    preco_porto_lata REAL NOT NULL,            -- Preço cotado no porto urbano (R$/lata 14kg)
    cot_transporte_calculado REAL NOT NULL,    -- Custo de Oportunidade do Tempo do Produtor
    lucro_beira_rio_calculado REAL NOT NULL,
    lucro_porto_calculado REAL NOT NULL,
    recomendacao_sistema TEXT CHECK(recomendacao_sistema IN ('IR AO PORTO', 'VENDER NA BEIRA-RIO')) NOT NULL,
    synced INTEGER CHECK(synced IN (0, 1)) DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (colheita_id) REFERENCES colheita_diaria(id) ON DELETE CASCADE
);

-- ----------------------------------------------------------------------------
-- 4. MATRIZ DE REFERÊNCIA PHS E TABELAS PÚBLICAS (CACHE LOCAL)
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS matriz_phs_referencia (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    peso_economico REAL NOT NULL DEFAULT 0.403,  -- 40,3%
    peso_social REAL NOT NULL DEFAULT 0.468,     -- 46,8%
    peso_ambiental REAL NOT NULL DEFAULT 0.129,  -- 12,9%
    fator_valorizacao_theta REAL NOT NULL DEFAULT 0.4931, -- +49.31%
    piso_pgpmbio_lata_14kg REAL NOT NULL DEFAULT 27.72,   -- R$ 1.98/kg * 14 kg
    versao_tabela INTEGER NOT NULL DEFAULT 1,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Inserção inicial dos parâmetros oficiais PHS
INSERT INTO matriz_phs_referencia (peso_economico, peso_social, peso_ambiental, fator_valorizacao_theta, piso_pgpmbio_lata_14kg, versao_tabela)
VALUES (0.403, 0.468, 0.129, 0.4931, 27.72, 1);

-- ----------------------------------------------------------------------------
-- 5. FILA DE SINCRONIZAÇÃO ASSÍNCRONA (STORE-AND-FORWARD)
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS sync_queue (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tabela_origem TEXT NOT NULL,
    registro_id TEXT NOT NULL,
    acao TEXT CHECK(acao IN ('INSERT', 'UPDATE', 'DELETE')) NOT NULL,
    dados_json TEXT NOT NULL,
    tentativas INTEGER DEFAULT 0,
    status TEXT CHECK(status IN ('PENDENTE', 'EM_PROCESSAMENTO', 'SUCESSO', 'FALHA')) DEFAULT 'PENDENTE',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ----------------------------------------------------------------------------
-- ÍNDICES DE PERFORMANCE E VIEWS CONSULTIVAS
-- ----------------------------------------------------------------------------
CREATE INDEX IF NOT EXISTS idx_colheita_data ON colheita_diaria(data_colheita);
CREATE INDEX IF NOT EXISTS idx_colheita_synced ON colheita_diaria(synced);
CREATE INDEX IF NOT EXISTS idx_viagem_synced ON viagem_logistica(synced);

-- View consultiva: Resumo completo de produção e precificação por safra
CREATE VIEW IF NOT EXISTS v_resumo_safra_phs AS
SELECT 
    c.id AS colheita_id,
    a.nome_produtor,
    a.comunidade_rio,
    c.data_colheita,
    c.quantidade_latas_14kg,
    v.preco_beira_rio_lata,
    (c.quantidade_latas_14kg * v.preco_beira_rio_lata) AS receita_bruta_beira_rio,
    ROUND(v.preco_beira_rio_lata * 1.4931, 2) AS preco_phs_lata_14kg,
    ROUND((c.quantidade_latas_14kg * v.preco_beira_rio_lata * 1.4931), 2) AS receita_phs_potencial,
    v.recomendacao_sistema,
    CASE 
        WHEN v.preco_beira_rio_lata < 27.72 THEN ROUND((27.72 - v.preco_beira_rio_lata) * c.quantidade_latas_14kg, 2)
        ELSE 0.0 
    END AS subvencao_conab_estimada
FROM colheita_diaria c
JOIN agroecossistema a ON c.agroecossistema_id = a.id
LEFT JOIN viagem_logistica v ON v.colheita_id = c.id;
