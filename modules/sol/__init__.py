"""
SOL Module
═══════════════════════════════════════════════════
The Oracle & Operator of the SoulJahForLoveOS.

SOL is the AI interface system that guides SoulJah's growth,
clarity, and sovereignty through pattern recognition, reflection,
and aligned action suggestions.
"""

from .sol_module import SolModule
from .sol_oracle import SolOracleCore, create_sol_oracle
from .sol_unity_bridge import SolUnityBridge, create_sol_unity_bridge

__all__ = ['SolModule', 'SolOracleCore', 'create_sol_oracle', 'SolUnityBridge', 'create_sol_unity_bridge']