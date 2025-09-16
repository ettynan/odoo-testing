# addons/om_hospital/tests/test_hospital.py
# -*- coding: utf-8 -*-
from odoo.tests import common, tagged

@tagged('post_install', '-at_install')
class TestHospital(common.TransactionCase):
    """Tests for hospital module."""

    def setUp(self):
        super().setUp()
        self.Patient = self.env["hospital.patient"]
        self.Doctor = self.env["hospital.doctor"]
        self.Appointment = self.env["hospital.appointment"]

    def test_create_patient(self):
        """Create a patient and verify data is stored correctly."""

        # create a new patient
        patient = self.Patient.create({
            "name": "John Doe",
            "age": 30,
        })

        # assertions: check if patient exists and data matches
        self.assertTrue(patient.id, "Patient record was not created")
        self.assertEqual(patient.name, "John Doe")
        self.assertEqual(patient.age, 30)
        print("✅ test_create_patient passed")
    
    def test_create_doctor(self):
        """Create a doctor and verify data is stored correctly."""

        # create a new doctor
        doctor = self.Doctor.create({
            "doctor_name": "Dr. James Johnston",
            "gender": "male",
        })
        
        self.assertTrue(doctor.id, "Doctor record was not created")
        self.assertEqual(doctor.doctor_name, "Dr. James Johnston")
        self.assertEqual(doctor.gender, "male")
        print("✅ test_create_doctor passed")
        
    def test_create_appointment(self):
        """Create an appointment linking patient and doctor."""
        
        # create a nee instance of each
        patient = self.Patient.create({
            "name": "Bob Smith",
            "age": 28,
            })

        doctor = self.Doctor.create({
            "doctor_name": "Dr. Brown",
            "gender": "female",
            })
        
        appointment = self.Appointment.create({
            "patient_id": patient.id,
            "doctor_id": doctor.id,
            "name": "Followup",
        })
        
        self.assertEqual(appointment.patient_id, patient)
        self.assertEqual(appointment.doctor_id, doctor)
        print("✅ test_create_appointment passed")



        

