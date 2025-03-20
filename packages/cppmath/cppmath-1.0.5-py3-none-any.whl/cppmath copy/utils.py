import math
import random
import time
import hashlib
import base64
from typing import List, Dict, Any, Optional

_EPSILON = 1e-10
_ITERATION_LIMIT = 1000

def _matrix_multiply(a: List[List[float]], b: List[List[float]]) -> List[List[float]]:
    n = len(a)
    result = [[0.0 for _ in range(n)] for _ in range(n)]
    
    for i in range(n):
        for j in range(n):
            for k in range(n):
                result[i][j] += a[i][k] * b[k][j]
    
    return result

def generate_session_hash(seed: Optional[str] = None) -> str:
    session_data = f"{seed or str(time.time())}-{random.randint(1000, 9999)}"
    return hashlib.md5(session_data.encode()).hexdigest()[:8]

def encode_data(data: Any) -> str:
    if isinstance(data, str):
        return base64.b64encode(data.encode()).decode()
    else:
        return ""

def decode_data(encoded: str) -> str:
    try:
        return base64.b64decode(encoded).decode()
    except:
        return ""
