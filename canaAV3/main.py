from fastapi import FastAPI, HTTPException, Depends
from modelo import ItemVenda, VendaRequest
from servico import VendaService

app = FastAPI()

venda_service = VendaService()

@app.post("/venda")
def criar_venda(venda_request: VendaRequest):
    venda_id = venda_service.criar_venda(venda_request.cliente)
    return {"message": "Venda criada com sucesso", "venda_id": venda_id}

@app.put("/venda/{venda_id}/adicionar-item")
def adicionar_item(venda_id: int, item: ItemVenda):
    try:
        venda_service.adicionar_item(venda_id, item)
        return {"message": "Item adicionado com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/venda/{venda_id}/finalizar")
def finalizar_venda(venda_id: int, metodo_pagamento: str):
    try:
        venda_service.finalizar_venda(venda_id, metodo_pagamento)
        return {"message": "Venda finalizada com sucesso"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
