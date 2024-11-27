import requests

ESTOQUE_URL = "http://estoque-service:"
PAGAMENTO_URL = "http://pagamento-service:"

def verificar_estoque(produto_id: int, quantidade: int) -> bool:
    url = f"{ESTOQUE_URL}/estoque/produto/{produto_id}"
    response = requests.get(url)
    if response.status_code != 200:
        return False
    
    dados = response.json()
    return dados["quantidade_disponivel"] >= quantidade

def processar_pagamento(valor: float, metodo_pagamento: str) -> bool:
    url = f"{PAGAMENTO_URL}/pagamento"
    payload = {"valor": valor, "metodo_pagamento": metodo_pagamento}
    response = requests.post(url, json=payload)
    return response.status_code == 200
