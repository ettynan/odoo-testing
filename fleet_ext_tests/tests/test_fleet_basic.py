# -*- coding: utf-8 -*-
from odoo.tests import common, new_test_user
from odoo import fields

class TestFleetExternal(common.TransactionCase):
    def setUp(self):
        super().setUp()
        self.user = new_test_user(self.env, "test base user", groups="base.group_user")
        self.Brand = self.env["fleet.vehicle.model.brand"]
        self.Model = self.env["fleet.vehicle.model"]
        self.Vehicle = self.env["fleet.vehicle"]
        self.Odometer = self.env["fleet.vehicle.odometer"]
        self.ContractLog = self.env["fleet.vehicle.log.contract"]

        self.brand = self.Brand.create({"name": "Audi"})
        self.model = self.Model.create({"brand_id": self.brand.id, "name": "A3"})

    def _make_vehicle(self):
        return self.Vehicle.create({
            "model_id": self.model.id,
            "driver_id": self.user.partner_id.id,
            "plan_to_change_car": False,
        })

    def test_vehicle_creation(self):
        """Vehicle creates and links to model & driver."""
        car = self._make_vehicle()
        self.assertTrue(car.id)
        self.assertEqual(car.model_id, self.model)
        self.assertEqual(car.driver_id, self.user.partner_id)
        print("✅ test_vehicle_creation passed")


    def test_odometer_log(self):
        """Odometer entry links to vehicle with correct value."""
        car = self._make_vehicle()
        odo = self.Odometer.create({
            "vehicle_id": car.id,
            "value": 12345,
            "date": fields.Date.today(),
        })
        self.assertEqual(odo.vehicle_id, car)
        self.assertEqual(odo.value, 12345)
        print("✅ test_odometer_log passed")

    def test_contract_due_soon(self):
        """Contract expiring soon flags the vehicle."""
        car = self._make_vehicle()
        self.ContractLog.create({
            "vehicle_id": car.id,
            "expiration_date": fields.Date.add(fields.Date.today(), days=10),
        })
        res = self.Vehicle.search([
            ("contract_renewal_due_soon", "=", True),
            ("id", "=", car.id),
        ])
        self.assertEqual(res, car)
        print("✅ test_contract_due_soon passed")

    def test_contract_overdue(self):
        """Expired contract flags the vehicle as overdue."""
        car = self._make_vehicle()
        self.ContractLog.create({
            "vehicle_id": car.id,
            "expiration_date": fields.Date.add(fields.Date.today(), days=-10),
        })
        res = self.Vehicle.search([
            ("contract_renewal_overdue", "=", True),
            ("id", "=", car.id),
        ])
        self.assertEqual(res, car)
        print("✅ test_contract_overdue passed")
         
    # Delete_vehicle test needed next
    def test_delete_vehicle(self):
        """Deleting a vehicle from the fleet."""
        car = self._make_vehicle()
        car_id = car.id
        
        # Create dependent records
        odo = self.Odometer.create({
            "vehicle_id": car.id,
            "value": 12345,
            "date": fields.Date.today(),
        })
        contract = self.ContractLog.create({
            "vehicle_id": car.id,
            "expiration_date": fields.Date.add(fields.Date.today(), days=10),
        })
        
        # Delete related records before delete vehicle
        self.env["fleet.vehicle.assignation.log"].search([("vehicle_id", "=", car_id)]).unlink()
        odo.unlink()
        contract.unlink()
        
        # Delete the vehicle
        car.unlink()
        
        # Confirm it no longer exists
        res = self.Vehicle.search([("id", "=", car_id)])
        self.assertFalse(res, "Vehicle not deleted")
        
        print("✅ test_delete_vehicle passed")

        
                                   