"""Main application file for the Cashflow Tracker API using Flask and SQLAlchemy"""
from urllib.parse import unquote
from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from sqlalchemy.exc import IntegrityError
from model import Session, Transaction
from logger import logger
from schemas import *
from flask_cors import CORS

info = Info(title="Minha API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# Tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
transaction_tag = Tag(name="Lançamento", description="Adição, edição e visualização de lançamentos")

# Route 1 - Home (GET - Documentation)
@app.get('/', tags=[home_tag])
def home():
    """
    Redirect to the API documentation.
    """
    return redirect('/openapi')

# Route 2 - Add a new transaction (POST)
@app.post('/transaction', tags=[transaction_tag],
          responses={"200": TransactionViewSchema, "400": ErrorSchema})
def add_transaction(form: TransactionSchema):
    """
    Add a new financial transaction.
    Requires: name, date, amount, type, category, status, and optional comment.
    Returns the added transaction details or an error message.
    """
    transaction = Transaction(
        name=form.name,
        t_date=form.t_date,
        amount=form.amount,
        t_type=form.t_type,
        category=form.category,
        t_status=form.t_status,
        comment=form.comment
    )
    logger.debug("Adicionando lançamento: '%s'", transaction.name)
    try:
        with Session() as session:
            session.add(transaction)
            session.commit()
            logger.debug("Adicionado lançamento: '%s'", transaction.name)
            return show_transaction(transaction), 200
    except IntegrityError:
        error_msg = "Lançamento de mesmo nome já salvo na base. Tente outro nome."
        logger.warning("Erro ao adicionar lançamento '%s', %s", transaction.name, error_msg)
        return {"message": error_msg}, 409
    except Exception:
        error_msg = "Não foi possível salvar novo item. Tente novamente."
        logger.warning("Erro ao adicionar lançamento '%s', %s", transaction.name, error_msg)
        return {"message": error_msg}, 400


# Route 3 - List all transactions (GET)
@app.get('/transactions', tags=[transaction_tag],
         responses={"200": TransactionsListSchema, "404": ErrorSchema})
def get_transactions():
    """
    List all financial transactions in the database, ordered from most recent to oldest.
    Returns a list of transactions with all details.
    """
    logger.debug("Carregando lançamentos financeiros.")
    with Session() as session:
        transactions = session.query(Transaction).order_by(Transaction.t_date.desc()).all()
        if not transactions:
            return {"transactions": []}, 200
        logger.debug("%d lançamentos encontrados", len(transactions))
        return show_transactions(transactions), 200



# Route 4 - Get a transaction by name (GET)
@app.get('/transaction', tags=[transaction_tag],
         responses={"200": TransactionViewSchema, "404": ErrorSchema})
def get_transaction(query: SearchTransactionSchema):
    """
    Retrieve a single transaction by its name.
    Returns the transaction details if found.
    """
    transaction_name = query.name
    logger.debug("Carregando dados sobre o lançamento '%s'", transaction_name)
    with Session() as session:
        transaction = session.query(Transaction).filter(Transaction.name == transaction_name).first()
        if not transaction:
            error_msg = "Lançamento não encontrado na base."
            logger.warning("Erro ao buscar lançamento '%s', %s", transaction_name, error_msg)
            return {"message": error_msg}, 404
        logger.debug("Lançamento '%s' encontrado", transaction_name)
        return show_transaction(transaction), 200

# Route 5 - Update transaction status (PATCH)
@app.patch('/transaction/status', tags=[transaction_tag],
           responses={"200": TransactionViewSchema, "404": ErrorSchema})
def update_transaction_status(body: UpdateStatusSchema):
    """
    Update the status of a transaction by its name.
    Returns the updated transaction if found.
    """
    name = body.name
    t_status = body.t_status
    logger.debug("Atualizando status do lançamento '%s' para %s", body.name, body.t_status)
    with Session() as session:
        transaction = session.query(Transaction).filter(Transaction.name == name).first()
        if not transaction:
            error_msg = "Lançamento não encontrado na base."
            logger.warning("Erro ao atualizar status do lançamento '%s', %s", name, error_msg)
            return {"message": error_msg}, 404
        transaction.t_status = bool(t_status)
        session.commit()
        logger.debug("Status do lançamento '%s' atualizado para %s", name, t_status)
        return show_transaction(transaction), 200

# Route 6 - Delete a transaction by name (DELETE)
@app.delete('/transaction', tags=[transaction_tag],
            responses={"200": TransactionDelSchema, "404": ErrorSchema})
def del_transaction(query: SearchTransactionSchema):
    """
    Delete a transaction by its name.
    Returns a confirmation message if deleted, or an error if not found.
    """
    transaction_name = unquote(unquote(query.name))
    logger.debug("Deletando dados sobre o lançamento '%s'", transaction_name)
    with Session() as session:
        count = session.query(Transaction).filter(Transaction.name == transaction_name).delete()
        session.commit()
        if count:
            logger.debug("Deletado lançamento '%s'", transaction_name)
            return {"message": "Lançamento removido", "name": transaction_name}
        error_msg = "Lançamento não encontrado na base :/"
        logger.warning("Erro ao deletar lançamento '%s', %s", transaction_name, error_msg)
        return {"message": error_msg}, 404
