"""
Gera o dataset simulado de vendas (clientes, vendedores, vendas) a partir
do catálogo de produtos em dados/produtos.csv.

Reprodutível: usa seed fixa (42), então rodar este script sempre gera
exatamente os mesmos dados.

Uso:
    python scripts/gerar_dados.py
"""
import pandas as pd
import numpy as np
import random
import os

random.seed(42)
np.random.seed(42)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DADOS_DIR = os.path.join(BASE_DIR, "dados")

produtos = pd.read_csv(os.path.join(DADOS_DIR, "produtos.csv"))

regioes = {
    "Sudeste": ["SP", "RJ", "MG", "ES"],
    "Sul": ["PR", "SC", "RS"],
    "Nordeste": ["BA", "PE", "CE", "MA"],
    "Centro-Oeste": ["GO", "MT", "MS", "DF"],
    "Norte": ["AM", "PA"],
}

nomes = ["Ana","Bruno","Carla","Diego","Elaine","Fabio","Gabriela","Hugo","Ines","Joao",
         "Karina","Lucas","Marina","Nelson","Olivia","Pedro","Queila","Rafael","Sofia","Thiago",
         "Ursula","Vitor","Wanda","Xavier","Yasmin","Zeca","Bianca","Caio","Debora","Erick",
         "Flavia","Gustavo","Helena","Igor","Julia","Kevin","Laura","Marcelo","Natalia","Otavio",
         "Patricia","Rodrigo","Simone","Tatiane","Ulisses","Vera","Wagner","Ximena","Yuri","Zilda"]

sobrenomes = ["Silva","Souza","Oliveira","Pereira","Costa","Santos","Almeida","Ferreira","Rodrigues","Lima"]

clientes_rows = []
cid = 1
n_por_regiao = {"Sudeste": 24, "Sul": 12, "Nordeste": 12, "Centro-Oeste": 8, "Norte": 4}
for regiao, ufs in regioes.items():
    for _ in range(n_por_regiao[regiao]):
        nome = f"{random.choice(nomes)} {random.choice(sobrenomes)}"
        uf = random.choice(ufs)
        clientes_rows.append([cid, nome, uf, regiao])
        cid += 1

clientes = pd.DataFrame(clientes_rows, columns=["id_cliente", "nome", "uf", "regiao"])

vendedores = pd.DataFrame({
    "id_vendedor": range(1, 9),
    "vendedor": ["Carlos Mendes", "Beatriz Rocha", "Felipe Nogueira", "Aline Barros",
                 "Rogerio Dias", "Camila Teixeira", "Andre Luz", "Priscila Nunes"],
})

N_PEDIDOS = 400
datas = pd.date_range("2026-01-01", "2026-06-30", freq="D")
pesos_produtos = [0.22, 0.18, 0.14, 0.10, 0.08, 0.07, 0.07, 0.06, 0.05, 0.03]

vendas_rows = []
for pedido_id in range(1, N_PEDIDOS + 1):
    data = np.random.choice(datas)
    cliente = clientes.sample(1).iloc[0]
    produto = produtos.sample(1, weights=pesos_produtos).iloc[0]
    vendedor_id = random.randint(1, 8)
    quantidade = int(np.random.choice([1, 2, 3, 4, 5], p=[0.45, 0.25, 0.15, 0.10, 0.05]))
    preco_unit = float(produto["preco_unitario"])
    desconto_pct = round(float(np.random.choice([0, 0, 0, 0.05, 0.10, 0.15])), 2)
    valor_bruto = round(preco_unit * quantidade, 2)
    valor_desconto = round(valor_bruto * desconto_pct, 2)
    faturamento = round(valor_bruto - valor_desconto, 2)
    vendas_rows.append([
        pedido_id, pedido_id, pd.Timestamp(data).date().isoformat(),
        int(cliente["id_cliente"]), int(produto["id_produto"]), vendedor_id,
        quantidade, preco_unit, desconto_pct, valor_bruto, valor_desconto, faturamento,
    ])

vendas = pd.DataFrame(vendas_rows, columns=[
    "id_item", "id_pedido", "data_pedido", "id_cliente", "id_produto", "id_vendedor",
    "quantidade", "preco_unitario", "desconto", "valor_bruto", "valor_desconto", "faturamento",
])

clientes.to_csv(os.path.join(DADOS_DIR, "clientes.csv"), index=False)
vendedores.to_csv(os.path.join(DADOS_DIR, "vendedores.csv"), index=False)
vendas.to_csv(os.path.join(DADOS_DIR, "vendas.csv"), index=False)

print(f"Faturamento total: {vendas['faturamento'].sum():,.2f}")
print(f"Pedidos: {vendas['id_pedido'].nunique()}")
print(f"Unidades: {vendas['quantidade'].sum()}")
print(f"Ticket médio: {vendas['faturamento'].sum() / vendas['id_pedido'].nunique():,.2f}")
