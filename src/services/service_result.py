from __future__ import annotations
 
from dataclasses import dataclass, field
from typing import Any
 
 
@dataclass
class ServiceResult:
    success: bool
    message: str
    data: dict[str, Any] = field(default_factory=dict)
 
    @classmethod
    def ok(cls, message: str, **data: Any) -> "ServiceResult":
        return cls(success=True, message=message, data=data)
 
    @classmethod
    def fail(cls, message: str, **data: Any) -> "ServiceResult":
        return cls(success=False, message=message, data=data)