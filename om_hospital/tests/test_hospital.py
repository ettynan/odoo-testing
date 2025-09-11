# addons/om_hospital/tests/test_hospital.py
# -*- coding: utf-8 -*-
from odoo.tests import common, tagged

@tagged('post_install', '-at_install')
class TestHospital(common.TransactionCase):
    """Tests for hospital module."""


    def test_create_patient(self):
        """Create a patient and verify data is stored correctly."""
        Patient = self.env["hospital.patient"]

        # create a new patient
        patient = Patient.create({
            "name": "John Doe",
            "age": 30,
        })

        # assertions: check if patient exists and data matches
        self.assertTrue(patient.id, "Patient record was not created")
        self.assertEqual(patient.name, "John Doe")
        self.assertEqual(patient.age, 30)
        print("✅ test_create_patient passed")