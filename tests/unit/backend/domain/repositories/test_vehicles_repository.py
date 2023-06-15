from datetime import datetime
import uuid

import pytest

from backend.maintenances.domain.models import Maintenance, Vehicle
from backend.maintenances.domain.repositories.vehicles_repository import VehiclesRepository
from backend.maintenances.utils import get_uuid


class DummyVehiclesRepository(VehiclesRepository):
    def __init__(self) -> None:
        self.committed = False
        self.closed = False
        self.vehicles = []

    def add(self, vehicle: Vehicle) -> None:
        found_vehicle = next(filter(lambda saved_vehicle: vehicle.id == saved_vehicle.id or vehicle.registration == saved_vehicle.registration, self.vehicles), None)
        if found_vehicle:
            raise Exception("Can not save a vehicle with same id or registration")
        self.vehicles.append(vehicle)

    def find_by_id(self, vehicle_id: uuid.UUID) -> Vehicle:
        return next(filter(lambda vehicle: vehicle.id == vehicle_id, self.vehicles), None)

    def add_maintenance(self, vehicle_id: uuid.UUID, maintenance: Maintenance) -> None:
        vehicle = self.find_by_id(vehicle_id)
        vehicle.maintenances.append(maintenance)

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
    assert vehicles_repository.vehicles == [vehicle]
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
    vehicles_repository.vehicles = [vehicle]

    # when
    found_vehicle = vehicles_repository.find_by_id(vehicle.id)

    # then
    assert found_vehicle == vehicle


def test_add_duplicated_vehicle():
    # given
    vehicle = Vehicle(
        id=get_uuid(),
        name="dummy_vehicle",
        registration="dummy_registration",
        maintenances=[]
    )
    vehicles_repository = DummyVehiclesRepository()
    vehicles_repository.add(vehicle)
    vehicles_repository.commit()

    # when
    with pytest.raises(Exception):
        vehicles_repository.add(vehicle)

    # Same registration
    vehicle.id = get_uuid()
    with pytest.raises(Exception):
        vehicles_repository.add(vehicle)

def test_add_maintenance():
    # given
    vehicle, vehicles_repository = create_vehicle()
    maintenance = Maintenance(
        id=get_uuid(),
        type="Cambio",
        components=["Aceite", "Filtro aceite"],
        odometer=100,
        performed_at=datetime.utcnow()
    )

    # when
    vehicles_repository.add_maintenance(vehicle.id, maintenance)
    vehicles_repository.commit()
    vehicles_repository.close()

    # then
    vehicle.maintenances.append(maintenance)
    assert vehicles_repository.vehicles == [vehicle]

def create_vehicle():
    vehicle = Vehicle(
        id=get_uuid(),
        name="dummy_vehicle",
        registration="dummy_registration",
        maintenances=[]
    )
    vehicles_repository = DummyVehiclesRepository()
    vehicles_repository.add(vehicle)
    vehicles_repository.commit()
    return vehicle, vehicles_repository