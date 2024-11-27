from modelo import Venda, ItemVenda, Pagamento, PagamentoFactory
from repositorio import VendaRepository
from util import verificar_estoque

class VendaService:
    def __init__(self):
        self.repository = VendaRepository()

    def criar_venda(self, cliente: str) -> int:
        venda = Venda(id=self.repository.counter, cliente=cliente)
        self.repository.salvar(venda)
        self.repository.counter += 1
        return venda.id

    def adicionar_item(self, venda_id: int, item: ItemVenda):
        venda = self.repository.buscar_por_id(venda_id)
        if not venda:
            raise Exception("Venda não encontrada")
        
        if not verificar_estoque(item.produto_id, item.quantidade):
            raise Exception("Produto indisponível no estoque")

        venda.itens.append(item)
        venda.total += item.quantidade * 100.0 
        self.repository.salvar(venda)

    def finalizar_venda(self, venda_id: int, metodo_pagamento: str):
        venda = self.repository.buscar_por_id(venda_id)
        if not venda:
            raise Exception("Venda não encontrada")
        if venda.finalizada:
            raise Exception("Venda já finalizada")
        
        pagamento = Pagamento(valor=venda.total, metodo_pagamento=metodo_pagamento)
        pagamento_strategy = PagamentoFactory.get_pagamento_strategy(metodo_pagamento)

        if not pagamento_strategy.processar(pagamento):
            raise Exception("Erro ao processar pagamento")

        venda.finalizada = True
        self.repository.salvar(venda)

# Padrão Factory Method