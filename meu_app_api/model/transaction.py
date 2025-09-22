"""Defines the Transaction model for financial entries and expenses."""
from typing import Optional
from sqlalchemy import Column, String, Integer, Float, Boolean, Date
from model import Base

class Transaction(Base):
    """Represents a single financial transaction (entry or expense)."""
    __tablename__ = 'transaction'

    id = Column("pk_transaction", Integer, primary_key=True, unique=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
    t_date = Column(Date, nullable=False)
    amount = Column(Float, nullable=False)
    t_type = Column(String(20), nullable=False)
    category = Column(String(30), nullable=False)
    t_status = Column(Boolean, default=False)
    comment = Column(String(50), nullable=True)

    def __init__(
            self,
            name: str,
            t_date: Date,
            amount: float,
            t_type: str,
            category: str,
            t_status: bool = False,
            comment: Optional[str] = None
    ):

        """ Create a new transaction entry. Arguments:
            name: Name of the transaction.
            t_date: Date of transaction.
            amount: Value of the transaction.
            t_type: Type of transaction ("Entrada" or "Saída").
            category: Category of the transaction (e.g., "cash", "supplier").
            t_status: Status indicating if processed in external system.
            comment: Optional notes.
        """
        self.name = name
        self.t_date = t_date
        self.amount = amount
        self.t_type = t_type
        self.category = category
        self.t_status = t_status
        self.comment = comment
