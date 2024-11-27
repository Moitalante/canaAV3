from pydantic import BaseModel
from typing import List

class ItemVenda(BaseModel):
    produto_id: int
    quantidade: int

class Venda(BaseModel):
    id: int
    cliente: str
    itens: List[ItemVenda] = []
    total: float = 0.0
    finalizada: bool = False

class VendaRequest(BaseModel):
    cliente: str

class Pagamento(BaseModel):
    valor: float
    metodo_pagamento: str

class PagamentoStrategy:
    def processar(self, pagamento: Pagamento) -> bool:
        pass

# Padrão Factory Method