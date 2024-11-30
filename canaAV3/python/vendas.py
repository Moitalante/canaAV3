from flask import Flask, request, jsonify
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from waitress import serve


DATABASE_URL = "mysql+pymysql://root:Carlopio120505@localhost:3306/vendas"
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()


class Venda(Base):
    __tablename__ = "vendas"
    id = Column(Integer, primary_key=True, autoincrement=True)
    data_venda = Column(DateTime, default=datetime.utcnow)
    nome_func = Column(String(255), nullable=False)
    veiculo_vendido = Column(String(255), nullable=False)

Base.metadata.create_all(engine)


def registrar_venda_no_banco(nome_func, veiculo_vendido):
    session = SessionLocal()
    
    try:
        venda = Venda(nome_func=nome_func, veiculo_vendido=veiculo_vendido)
        session.add(venda)
        session.commit()
        session.refresh(venda) 
        return venda.id
    except Exception as e:
        session.rollback()  
        print(f"Erro ao registrar venda: {e}")
    finally:
        session.close()  

app = Flask(__name__)

@app.route("/vendas", methods=["POST"])
def registrar_venda_api():
    try:
        dados = request.get_json()
        if not dados:
            return jsonify({"error": "Dados inválidos ou não enviados"}), 400

        nome_func = dados.get("nome_func")
        veiculo = dados.get("veiculo_vendido")

        if not nome_func or not veiculo:
            return jsonify({"error": "Campos 'nome_func' ou 'veiculo_vendido' faltando"}), 400

        venda_id = registrar_venda_no_banco(nome_func, veiculo)

        return jsonify({"message": "Venda registrada com sucesso", "venda_id": venda_id})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=5002)
