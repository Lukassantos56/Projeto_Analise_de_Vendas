-- Projeto 1 | Análise de Vendas
-- Banco: PostgreSQL

DROP TABLE IF EXISTS vendas, vendedores, produtos, clientes CASCADE;

CREATE TABLE clientes (
    id_cliente INT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    uf CHAR(2) NOT NULL,
    regiao VARCHAR(30) NOT NULL
);

CREATE TABLE produtos (
    id_produto INT PRIMARY KEY,
    produto VARCHAR(100) NOT NULL,
    categoria VARCHAR(50) NOT NULL,
    subcategoria VARCHAR(50) NOT NULL,
    preco_unitario NUMERIC(12,2) NOT NULL
);

CREATE TABLE vendedores (
    id_vendedor INT PRIMARY KEY,
    vendedor VARCHAR(100) NOT NULL
);

CREATE TABLE vendas (
    id_item INT PRIMARY KEY,
    id_pedido INT NOT NULL,
    data_pedido DATE NOT NULL,
    id_cliente INT NOT NULL REFERENCES clientes(id_cliente),
    id_produto INT NOT NULL REFERENCES produtos(id_produto),
    id_vendedor INT NOT NULL REFERENCES vendedores(id_vendedor),
    quantidade INT NOT NULL,
    preco_unitario NUMERIC(12,2) NOT NULL,
    desconto NUMERIC(5,2) NOT NULL,
    valor_bruto NUMERIC(14,2) NOT NULL,
    valor_desconto NUMERIC(14,2) NOT NULL,
    faturamento NUMERIC(14,2) NOT NULL
);

-- Depois de criar as tabelas, importe os CSVs da pasta dados.
-- Em ferramentas como pgAdmin/DBeaver, use o recurso de importação de CSV.

CREATE INDEX idx_vendas_data ON vendas(data_pedido);
CREATE INDEX idx_vendas_cliente ON vendas(id_cliente);
CREATE INDEX idx_vendas_produto ON vendas(id_produto);
CREATE INDEX idx_vendas_vendedor ON vendas(id_vendedor);

-- 1. KPIs principais
SELECT
    SUM(faturamento) AS faturamento,
    COUNT(DISTINCT id_pedido) AS pedidos,
    SUM(quantidade) AS unidades_vendidas,
    ROUND(SUM(faturamento) / COUNT(DISTINCT id_pedido), 2) AS ticket_medio
FROM vendas;

-- 2. Faturamento por mês
SELECT
    DATE_TRUNC('month', data_pedido)::date AS mes,
    SUM(faturamento) AS faturamento
FROM vendas
GROUP BY 1
ORDER BY 1;

-- 3. Faturamento por categoria
SELECT
    p.categoria,
    SUM(v.faturamento) AS faturamento,
    SUM(v.quantidade) AS unidades
FROM vendas v
JOIN produtos p ON p.id_produto = v.id_produto
GROUP BY p.categoria
ORDER BY faturamento DESC;

-- 4. Ranking de produtos
SELECT
    p.produto,
    SUM(v.faturamento) AS faturamento,
    SUM(v.quantidade) AS unidades
FROM vendas v
JOIN produtos p ON p.id_produto = v.id_produto
GROUP BY p.produto
ORDER BY faturamento DESC;

-- 5. Faturamento por região
SELECT
    c.regiao,
    SUM(v.faturamento) AS faturamento,
    COUNT(DISTINCT v.id_pedido) AS pedidos
FROM vendas v
JOIN clientes c ON c.id_cliente = v.id_cliente
GROUP BY c.regiao
ORDER BY faturamento DESC;

-- 6. Performance de vendedores
SELECT
    ve.vendedor,
    SUM(v.faturamento) AS faturamento,
    COUNT(DISTINCT v.id_pedido) AS pedidos,
    ROUND(SUM(v.faturamento) / COUNT(DISTINCT v.id_pedido), 2) AS ticket_medio
FROM vendas v
JOIN vendedores ve ON ve.id_vendedor = v.id_vendedor
GROUP BY ve.vendedor
ORDER BY faturamento DESC;

-- 7. Clientes com maior faturamento
SELECT
    c.nome,
    c.uf,
    c.regiao,
    SUM(v.faturamento) AS faturamento
FROM vendas v
JOIN clientes c ON c.id_cliente = v.id_cliente
GROUP BY c.id_cliente, c.nome, c.uf, c.regiao
ORDER BY faturamento DESC
LIMIT 10;
