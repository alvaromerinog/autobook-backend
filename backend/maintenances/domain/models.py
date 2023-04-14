from dataclasses import dataclass, field
from datetime import datetime
from typing import List
from uuid import UUID


@dataclass
class Maintenance:
    id: UUID
    name: str
    odometer: int
    performed_at: datetime


@dataclass
class Vehicle:
    id: UUID
    name: str
    registration: str
    maintenances: List[Maintenance] = field(default_factory=list)
