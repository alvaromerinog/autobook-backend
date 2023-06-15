from abc import ABC, abstractmethod
from uuid import UUID

from backend.maintenances.domain.models import Maintenance, Vehicle


class VehiclesRepository(ABC):
    @abstractmethod
    def add(self, vehicle: Vehicle) -> None:
        raise NotImplementedError

    @abstractmethod
    def find_by_id(self, vehicle_id: UUID) -> Vehicle:
        raise NotImplementedError

    @abstractmethod
    def add_maintenance(self, vehicle_id: UUID, maintenance: Maintenance) -> None:
        raise NotImplementedError

    @abstractmethod
    def commit(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def close(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def rollback(self) -> None:
        raise NotImplementedError
