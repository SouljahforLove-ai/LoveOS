"""
LoveOS Modules
═══════════════
Collection of all LoveOS modules and subsystems.
"""

from .sol import SolModule
from .identity.identity_module import IdentityModule

__all__ = [
    'SolModule',
    'IdentityModule'
]