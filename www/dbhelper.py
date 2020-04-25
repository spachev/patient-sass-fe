from model import db
import datetime
import model

def get_all(model_cl):
    data = model_cl.query.all()
    return data


def add_instance(model_cl, **kwargs):
    instance = model_cl(**kwargs)
    db.session.add(instance)
    commit_changes()
    return instance


def delete_instance(model_cl, id):
    model_cl.query.filter_by(id=id).delete()
    commit_changes()


def update_instance(model_cl, idin, **kwargs):
    instance = model_cl(**kwargs)
    model_cl.query.filter_by(id=idin).update(instance)
    commit_changes()


def fetch_instance(table, id):
    model_cl = getattr(model, table)
    rsp = model_cl.query.filter_by(id=id).all()
    if len(rsp) == 0:
        return None
    return rsp[0]

def commit_changes():
    db.session.commit()

#Takes a db_session, a str representing which table to use and the request as a Dict and creates serveral useful variables
#Like the final dictionary for db operation
def convert_json(db_session, table, op, content):
    data = content
    myTable = getattr(model, table)
    myFields = [i for i in myTable.__dict__.keys() if i[:1] != '_']
    fieldValues = [data.get(field) for field in myFields]
    if op == "update": #If it is an updated we dont neeed all fields
        myFields = data.keys()
        fieldValues = [data.get(field) for field in myFields ]
        if "last_update_datetime" in myFields: #creates datetime
            fieldValues[myFields.index("last_update_datetime")] = datetime.datetime.utcnow()
    elif op == "insert":
        if "create_datetime" in myFields:
            fieldValues[myFields.index("create_datetime")] = datetime.datetime.utcnow() #inserts created datetime
    for index, field in enumerate(fieldValues):
        if field == "None": #places the correct null values
            fieldValues[index] = db_session.null()
    myDict = {}
    for i, fieldName in enumerate(myFields): #creates the final dictionary of values
        myDict[fieldName] = fieldValues[i]
    return myDict,myTable
