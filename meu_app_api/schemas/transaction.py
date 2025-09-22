"""Schema definitions for API data validation and serialization."""
from typing import Optional, List
from datetime import date
from pydantic import BaseModel

class TransactionSchema(BaseModel):
    """Schema for creating a new financial transaction."""
    name: str
    t_date: date
    amount: float
    t_type: str
    category: str
    t_status: bool
    comment: Optional[str]


class SearchTransactionSchema(BaseModel):
    """Schema for searching a transaction by its name."""
    name: str


class TransactionsListSchema(BaseModel):
    """Schema for returning a list of transactions."""
    transactions: List[TransactionSchema]


class TransactionViewSchema(BaseModel):
    """Schema for viewing a transaction with its details."""
    id: int = 4
    name: str = "Gratificação John Doe"
    t_date: date = date(2025, 9, 20)
    amount: float = 600.50
    t_type: str = "Saída"
    category: str = "Gratificações"
    t_status: bool = True
    comment: Optional[str] = "Economia de Água"


class TransactionDelSchema(BaseModel):
    """Schema for confirming a transaction deletion."""
    message: str
    id: int

class UpdateStatusSchema(BaseModel):
    """Schema for updating the status of a transaction by name."""
    name: str
    t_status: bool


# Presentation functions for transaction schemas

def show_transaction(transaction):
    """Returns a transaction as a dictionary, following the TransactionViewSchema."""
    return {
        "id": transaction.id,
        "name": transaction.name,
        "t_date": transaction.t_date.isoformat() if transaction.t_date else None,
        "amount": transaction.amount,
        "t_type": transaction.t_type,
        "category": transaction.category,
        "t_status": transaction.t_status,
        "comment": transaction.comment, 
    }


def show_transactions(transactions):
    """Returns a list of transactions formatted according to the TransactionViewSchema."""
    result = []
    for transaction in transactions:
        result.append({
                "id": transaction.id,
                "name": transaction.name,
                "t_date": transaction.t_date.isoformat() if transaction.t_date else None,
                "amount": transaction.amount,
                "t_type": transaction.t_type,
                "category": transaction.category,
                "t_status": transaction.t_status,
                "comment": transaction.comment,
            })
    return {"transactions": result}
