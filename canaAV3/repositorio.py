from modelo import Venda, ItemVenda
from typing import Dict

class VendaRepository:
    def __init__(self):
        self.vendas: Dict[int, Venda] = {}
        self.counter = 1

    def salvar(self, venda: Venda):
        self.vendas[venda.id] = venda

    def buscar_por_id(self, venda_id: int) -> Venda:
        return self.vendas.get(venda_id)

    def listar(self) -> Dict[int, Venda]:
        return self.vendas
