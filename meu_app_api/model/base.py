"""Defines the base model for SQLAlchemy ORM."""
from sqlalchemy.ext.declarative import declarative_base

# cria uma classe Base para o instanciamento de novos objetos/tabelas
Base = declarative_base()
