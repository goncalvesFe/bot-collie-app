from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Automation:
    id: Optional[int] = None
    name: str = ""
    description: str = ""
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

@dataclass
class Command:
    id: Optional[int] = None
    automation_id: int = 0
    type: str = ""
    subtype: str = ""
    command: str = ""
    cmdOrder: int = 0