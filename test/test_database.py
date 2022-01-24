from database.database import IClinicDatabase, DatabaseStatus
from database.model import Prescriptions_t
from model.prescription import Prescription
from peewee import DatabaseError
from uuid import uuid4


class MockedPrescriptionModelBase:
    def __init__(self, physician_id, patient_id, text, clinic_id=0, metric_id=""):
        self.id = 1
        self.physician_id = physician_id
        self.patient_id = patient_id
        self.clinic_id = clinic_id
        self.text = text
        self.metric_id = metric_id

    @staticmethod
    def create_table():
        return True

    @staticmethod
    def table_exists():
        return False


def test_database_register_prescription():
    def setup():
        class MockedPrescription_t(MockedPrescriptionModelBase):
            @staticmethod
            def save():
                return MockedPrescription_t

        p = Prescription(clinic_id=1,
                         physician_id=3,
                         patient_id=5,
                         text="Dipirona 1x ao dia")

        db = IClinicDatabase(prescriptions_t=MockedPrescription_t)
        return db, p

    db, p = setup()
    status, p = db.register_prescription(prescription=p)
    assert status == DatabaseStatus.REGISTER_PRESCRIPTION_SUCCESS
    assert p.id == 1
    assert p.clinic_id == 1
    assert p.physician_id == 3
    assert p.patient_id == 5
    assert p.text == "Dipirona 1x ao dia"
    assert p.metric_id == ""


def test_database_register_error():
    def setup():
        class MockedPrescription_t(MockedPrescriptionModelBase):
            @staticmethod
            def save():
                raise DatabaseError()

        p = Prescription(clinic_id=1,
                         physician_id=3,
                         patient_id=5,
                         text="Dipirona 1x ao dia")
        db = IClinicDatabase(prescriptions_t=MockedPrescription_t)
        return db, p

    db, p = setup()
    status, p = db.register_prescription(prescription=p)
    assert status == DatabaseStatus.REGISTER_PRESCRIPTION_ERROR
    assert not p


def test_database_update_prescription():
    def setup():
        class MockExecute:
            def execute(self):
                pass

        class MockWhere:
            def where(self, condition):
                return MockExecute()

        class MockedPrescription_t(MockedPrescriptionModelBase):
            id = 1
            @staticmethod
            def update(clinic_id, physician_id, patient_id, text, metric_id):
                return MockWhere()

        p = Prescription(clinic_id=1,
                         physician_id=3,
                         patient_id=5,
                         text="Dipirona 1x ao dia")
        db = IClinicDatabase(prescriptions_t=MockedPrescription_t)
        p.id = 1
        return db, p

    db, registered_prescription = setup()
    registered_prescription.metric_id = uuid4()
    status, p = db.update_prescription(prescription=registered_prescription)
    assert status == DatabaseStatus.UPDATE_PRESCRIPTION_SUCCESS
    assert p.id == registered_prescription.id
    assert p.clinic_id == registered_prescription.clinic_id
    assert p.physician_id == registered_prescription.physician_id
    assert p.patient_id == registered_prescription.patient_id
    assert p.text == registered_prescription.text
    assert p.metric_id == registered_prescription.metric_id


def test_database_update_prescription_error():
    def setup():
        class MockExecute:
            def execute(self):
                raise DatabaseError()

        class MockWhere:
            def where(self, condition):
                return MockExecute()

        class MockedPrescription_t(MockedPrescriptionModelBase):
            id = 1
            @staticmethod
            def update(clinic_id, physician_id, patient_id, text, metric_id):
                return MockWhere()

        p = Prescription(id=1,
                         clinic_id=1,
                         physician_id=3,
                         patient_id=5,
                         text="Dipirona 1x ao dia")
        db = IClinicDatabase(prescriptions_t=MockedPrescription_t)
        return db, p

    db, registered_prescription = setup()
    registered_prescription.metric_id = uuid4()
    status, p = db.update_prescription(prescription=registered_prescription)
    assert status == DatabaseStatus.UPDATE_PRESCRIPTION_ERROR
    assert not p


def test_database_remove_prescription():
    def setup():
        class MockExecute:
            def execute(self):
                pass

        class MockWhere:
            def where(self, condition):
                return MockExecute()

        class MockedPrescription_t(MockedPrescriptionModelBase):
            id = 1
            @staticmethod
            def delete():
                return MockWhere()
        p = Prescription(clinic_id=1,
                         physician_id=3,
                         patient_id=5,
                         text="Dipirona 1x ao dia")
        db = IClinicDatabase(prescriptions_t=MockedPrescription_t)
        return db, p

    db, registered_prescription = setup()
    status, p = db.remove_prescription(prescription=registered_prescription)
    assert status == DatabaseStatus.REMOVE_PRESCRIPTION_SUCCESS


def test_database_remove_prescription_error():
    def setup():
        class MockExecute:
            def execute(self):
                raise DatabaseError()

        class MockWhere:
            def where(self, condition):
                return MockExecute()

        class MockedPrescription_t(MockedPrescriptionModelBase):
            id = 1
            @staticmethod
            def delete():
                return MockWhere()

        p = Prescription(id=1,
                         clinic_id=1,
                         physician_id=3,
                         patient_id=5,
                         text="Dipirona 1x ao dia")
        db = IClinicDatabase(prescriptions_t=MockedPrescription_t)
        return db, p

    db, p = setup()
    status, p = db.remove_prescription(prescription=p)
    assert status == DatabaseStatus.REMOVE_PRESCRIPTION_ERROR






