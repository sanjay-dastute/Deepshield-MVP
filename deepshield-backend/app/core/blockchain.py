import hashlib
import json
from datetime import datetime
from typing import Any, Dict

class SimpleBlockchain:
    @staticmethod
    def create_hash(data: Dict[str, Any]) -> str:
        """Create a hash of the data for verification purposes"""
        # Add timestamp to make each hash unique
        data_with_timestamp = {
            **data,
            "timestamp": datetime.utcnow().isoformat()
        }
        data_string = json.dumps(data_with_timestamp, sort_keys=True)
        return hashlib.sha256(data_string.encode()).hexdigest()

    @staticmethod
    def verify_hash(data: Dict[str, Any], stored_hash: str) -> bool:
        """Verify if the data matches the stored hash"""
        data_string = json.dumps(data, sort_keys=True)
        current_hash = hashlib.sha256(data_string.encode()).hexdigest()
        return current_hash == stored_hash
