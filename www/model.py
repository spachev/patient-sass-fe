import flask_sqlalchemy
import json,sys,datetime

db = flask_sqlalchemy.SQLAlchemy()

def var_to_json_type(v):
    if isinstance(v, datetime.datetime):
        return str(v)
    return v

class BaseModel(db.Model):
  __abstract__ = True
  def to_json(self):
    return json.dumps({c.name: var_to_json_type(getattr(self, c.name)) for c in self.__table__.columns})


class User(BaseModel):
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(128), index=True, unique=True)
    email = db.Column(db.String(128), index=True, unique=True)
    role = db.Column(db.String(128))
    password_hash = db.Column(db.String(128))
    tenant_id = db.Column(db.BigInteger)
    def __repr__(self):
        return '<User {}>'.format(self.username)

class Tenant(BaseModel):
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(64), index=True)
    url = db.Column(db.String(256), index=True, unique=True)
    status = db.Column(db.String(64))
    create_datetime = db.Column(db.DateTime)
    def __repr__(self):
        return '<Tenant {}>'.format(self.name)

class PatientLogin(BaseModel):
    patient_id = db.Column(db.BigInteger)
    id = db.Column(db.BigInteger, primary_key=True)
    password_hash = db.Column(db.String(128))
    last_login_datetime = db.Column(db.DateTime)
    def __repr__(self):
            return 'Patient id: %r | Time: %r' % (self.patient_id,self.last_login_datetime)


class Patient(BaseModel):
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(128), unique=False, nullable=False)
    email = db.Column(db.String(128), index=True, unique=True)
    mobile_number = db.Column(db.String(25))
    postal_address = db.Column(db.String(50))
    create_datetime = db.Column(db.DateTime)
    tenant_id = db.Column(db.BigInteger)
    def __repr__(self):
        return 'Patient: %r' % self.name

class PatientRequest(BaseModel):
    id = db.Column(db.BigInteger, primary_key=True)
    patient_id = db.Column(db.BigInteger)
    category_id = db.Column(db.BigInteger)
    status = db.Column(db.String(128), unique=False, nullable=False)
    create_datetime = db.Column(db.DateTime)
    last_update_datetime = db.Column(db.DateTime)
    last_updated_user_id = db.Column(db.BigInteger)
    def __repr__(self):
        return 'Patient Request Id: %r' % self.id

class ResultCategory(BaseModel):
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    score_range = db.Column(db.String(128), nullable=False)
    tenant_id = db.Column(db.BigInteger)

class PatientNotification(BaseModel):
    id = db.Column(db.BigInteger, primary_key=True)
    request_id = db.Column(db.BigInteger)
    template_id = db.Column(db.BigInteger)
    tenant_id = db.Column(db.BigInteger)
    message_body = db.Column(db.Text)
    create_datetime = db.Column(db.DateTime)

class Symptom(BaseModel):
    id = db.Column(db.BigInteger, primary_key=True)
    symptom_description = db.Column(db.String(2048))
    scale = db.Column(db.Integer)
    correlated_factor = db.Column(db.Float)
    binary = db.Column(db.Boolean)
    tenant_id = db.Column(db.BigInteger)

class AgeGroup(BaseModel):
    id = db.Column(db.BigInteger, primary_key=True)
    range = db.Column(db.String(64))
    correlated_factor = db.Column(db.Float)
    tenant_id = db.Column(db.BigInteger)

class AcuteSymptom(BaseModel):
    id = db.Column(db.BigInteger, primary_key=True)
    symptom_description = db.Column(db.String(2048))
    tenant_id = db.Column(db.BigInteger)

class Gender(BaseModel):
    id = db.Column(db.BigInteger, primary_key=True)
    description = db.Column(db.String(128))
    correlated_factor = db.Column(db.Float)

class UnderlyingDisease(BaseModel):
    id = db.Column(db.BigInteger, primary_key=True)
    description = db.Column(db.String(2048))
    scale = db.Column(db.Integer)
    correlated_factor = db.Column(db.Float)
    binary = db.Column(db.Boolean)
    tenant_id = db.Column(db.BigInteger)

class GuideContent(BaseModel):
    id = db.Column(db.BigInteger, primary_key=True)
    description = db.Column(db.String(2048))
    url = db.Column(db.String(256), index=True, unique=True)
    tenant_id = db.Column(db.BigInteger)
