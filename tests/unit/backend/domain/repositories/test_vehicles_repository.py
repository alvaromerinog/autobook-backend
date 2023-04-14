import uuid

from backend.maintenances.domain.models import Vehicle
from backend.maintenances.domain.repositories.vehicles_repository import VehiclesRepository
from backend.maintenances.utils import get_uuid


class DummyVehiclesRepository(VehiclesRepository):
    def __init__(self) -> None:
        self.committed = False
        self.closed = False
        self.vehicle = False

    def add(self, vehicle: Vehicle) -> None:
        self.vehicle = vehicle

    def find_by_id(self, vehicle_id: uuid.UUID) -> Vehicle:
        return self.vehicle if self.vehicle.id == vehicle_id else None

    def commit(self) -> None:
        self.committed = True

    def close(self) -> None:
        self.closed = True

    def rollback(self) -> None:
        self.committed = False


def test_add_vehicle():
    # given
    vehicle = Vehicle(
        id=get_uuid(),
        name="dummy_vehicle",
        registration="dummy_registration",
        maintenances=[]
    )
    vehicles_repository = DummyVehiclesRepository()

    # when
    vehicles_repository.add(vehicle)
    vehicles_repository.commit()
    vehicles_repository.close()

    # then
    assert vehicles_repository.vehicle == vehicle
    assert vehicles_repository.committed is True
    assert vehicles_repository.closed is True


def test_find_vehicle():
    # given
    vehicle = Vehicle(
        id=get_uuid(),
        name="dummy_vehicle",
        registration="dummy_registration",
        maintenances=[]
    )
    vehicles_repository = DummyVehiclesRepository()
    vehicles_repository.vehicle = vehicle

    # when
    found_vehicle = vehicles_repository.find_by_id(vehicle.id)

    # then
    assert found_vehicle == vehicle
