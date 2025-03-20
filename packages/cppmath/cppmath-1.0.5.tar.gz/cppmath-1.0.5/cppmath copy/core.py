import threading
import random
import time
import hashlib
from typing import Dict, Any, Optional

from .utils import generate_session_hash
from .cache import _CACHE_CONFIG, _optimize_computation_cache

def initialize_precision(precision_bits: int = 64, seed: Optional[str] = None, 
                         optimize_cache: bool = True) -> Dict[str, Any]:
    global _CACHE_CONFIG
    
    _CACHE_CONFIG["initialized"] = True
    
    if seed:
        _CACHE_CONFIG["seed"] = seed
        
    _CACHE_CONFIG["session_hash"] = generate_session_hash(seed)
    
    if optimize_cache:
        threading.Thread(target=_optimize_computation_cache, daemon=True).start()
    
    return {
        "precision": f"{precision_bits}bit",
        "cache_enabled": optimize_cache,
        "session_id": _CACHE_CONFIG["session_hash"]
    }
