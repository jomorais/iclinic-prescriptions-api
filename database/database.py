from database.model import Prescriptions_t
from model.prescription import Prescription
from peewee import DatabaseError


class DatabaseStatus:
    REGISTER_PRESCRIPTION_SUCCESS = 0
    REGISTER_PRESCRIPTION_ERROR = 1

    SELECT_PRESCRIPTION_SUCCESS = 2
    SELECT_PRESCRIPTION_ERROR = 3
    SELECT_PRESCRIPTION_NOT_FOUND = 4

    UPDATE_PRESCRIPTION_SUCCESS = 5
    UPDATE_PRESCRIPTION_ERROR = 6

    REMOVE_PRESCRIPTION_SUCCESS = 7
    REMOVE_PRESCRIPTION_ERROR = 8


class IClinicDatabase:
    def __init__(self, prescriptions_t=Prescriptions_t):
        self.prescriptions_t = prescriptions_t
        self.init()

    def init(self):
        if self.prescriptions_t.table_exists() is False:
            self.prescriptions_t.create_table()
            return True
        else:
            return False

    def register_prescription(self, prescription: Prescription):
        try:
            new_prescription = self.prescriptions_t(clinic_id=prescription.clinic_id,
                                                    physician_id=prescription.physician_id,
                                                    patient_id=prescription.patient_id,
                                                    text=prescription.text)
            new_prescription.save()
            prescription.id = new_prescription.id

            return DatabaseStatus.REGISTER_PRESCRIPTION_SUCCESS, prescription
        except DatabaseError as ex:
            return DatabaseStatus.REGISTER_PRESCRIPTION_ERROR, None

    def update_prescription(self, prescription: Prescription):
        try:
            query = self.prescriptions_t.update(clinic_id=prescription.clinic_id,
                                                physician_id=prescription.physician_id,
                                                patient_id=prescription.patient_id,
                                                text=prescription.text,
                                                metric_id=prescription.metric_id) \
                .where(self.prescriptions_t.id == prescription.id)
            query.execute()
            return DatabaseStatus.UPDATE_PRESCRIPTION_SUCCESS, prescription
        except DatabaseError as ex:
            return DatabaseStatus.UPDATE_PRESCRIPTION_ERROR, None

    def remove_prescription(self, prescription: Prescription):
        try:
            self.prescriptions_t.delete().where(self.prescriptions_t.id == prescription.id).execute()
            return DatabaseStatus.REMOVE_PRESCRIPTION_SUCCESS, prescription
        except DatabaseError as ex:
            return DatabaseStatus.REMOVE_PRESCRIPTION_ERROR, None
