"""Drolta SQLite Query Engine.

Drolta is a query engine that wraps a  SQLite database to allow
users to write queries that are more declarative, composable,
and legible than raw SQL. Drolta pulls inspiration
from logic languages like Prolog and Datalog to give users an
easy-to-use database querying experience.

"""

__version__ = "0.4.0"

from .engine import QueryEngine

__all__ = ["QueryEngine"]
