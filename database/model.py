from peewee import *
from database.connector import get_connector
import datetime
from model.prescription import Prescription


class BaseModel(Model):
    class Meta:
        database = get_connector()


class Prescriptions_t(BaseModel):
    id = AutoField()
    clinic_id = IntegerField(default=0)
    physician_id = IntegerField()
    patient_id = IntegerField()
    text = TextField()
    metric_id = TextField(default="")
