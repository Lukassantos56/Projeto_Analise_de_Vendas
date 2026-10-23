"""
Roda as 7 consultas de sql/analises.sql contra os CSVs em dados/ (usando
SQLite em memória, com pequenas adaptações de sintaxe) e imprime os
resultados — serve para validar que os números do README/CONCLUSOES
realmente batem com os dados atuais.

Uso:
    python scripts/testar_consultas.py
"""
import sqlite3
import pandas as pd
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DADOS_DIR = os.path.join(BASE_DIR, "dados")

con = sqlite3.connect(":memory:")
for tabela in ["clientes", "produtos", "vendedores", "vendas"]:
    pd.read_csv(os.path.join(DADOS_DIR, f"{tabela}.csv")).to_sql(tabela, con, index=False)

CONSULTAS = {
    "KPIs principais": """
        SELECT SUM(faturamento) AS faturamento, COUNT(DISTINCT id_pedido) AS pedidos,
               SUM(quantidade) AS unidades_vendidas,
               ROUND(SUM(faturamento) * 1.0 / COUNT(DISTINCT id_pedido), 2) AS ticket_medio,
               COUNT(DISTINCT id_cliente) AS clientes
        FROM vendas
    """,
    "Faturamento por mes": """
        SELECT strftime('%Y-%m', data_pedido) AS mes, SUM(faturamento) AS faturamento
        FROM vendas GROUP BY 1 ORDER BY 1
    """,
    "Faturamento por categoria": """
        SELECT p.categoria, SUM(v.faturamento) AS faturamento, SUM(v.quantidade) AS unidades
        FROM vendas v JOIN produtos p ON p.id_produto = v.id_produto
        GROUP BY p.categoria ORDER BY faturamento DESC
    """,
    "Ranking de produtos": """
        SELECT p.produto, SUM(v.faturamento) AS faturamento, SUM(v.quantidade) AS unidades
        FROM vendas v JOIN produtos p ON p.id_produto = v.id_produto
        GROUP BY p.produto ORDER BY faturamento DESC
    """,
    "Faturamento por regiao": """
        SELECT c.regiao, SUM(v.faturamento) AS faturamento, COUNT(DISTINCT v.id_pedido) AS pedidos
        FROM vendas v JOIN clientes c ON c.id_cliente = v.id_cliente
        GROUP BY c.regiao ORDER BY faturamento DESC
    """,
    "Performance de vendedores": """
        SELECT ve.vendedor, SUM(v.faturamento) AS faturamento,
               COUNT(DISTINCT v.id_pedido) AS pedidos,
               ROUND(SUM(v.faturamento) * 1.0 / COUNT(DISTINCT v.id_pedido), 2) AS ticket_medio
        FROM vendas v JOIN vendedores ve ON ve.id_vendedor = v.id_vendedor
        GROUP BY ve.vendedor ORDER BY faturamento DESC
    """,
    "Top 10 clientes": """
        SELECT c.nome, c.uf, c.regiao, SUM(v.faturamento) AS faturamento
        FROM vendas v JOIN clientes c ON c.id_cliente = v.id_cliente
        GROUP BY c.id_cliente, c.nome, c.uf, c.regiao
        ORDER BY faturamento DESC LIMIT 10
    """,
}

if __name__ == "__main__":
    for nome, sql in CONSULTAS.items():
        print(f"\n=== {nome} ===")
        print(pd.read_sql(sql, con).to_string(index=False))
    print("\nTodas as consultas executaram sem erro.")
