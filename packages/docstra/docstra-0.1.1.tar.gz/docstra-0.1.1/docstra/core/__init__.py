"""Core module for Docstra."""

from docstra.core.interfaces import IDocstraService
from docstra.core.factory import create_service

__all__ = ["IDocstraService", "create_service"]
