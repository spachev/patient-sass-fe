# Infrastructure test page.
import os,sys
import random
from flask import Flask
from flask import request
from flask import Markup
from flask import render_template,jsonify,make_response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from init import create_app
import model
import dbhelper
import datetime
import json
import sqlalchemy.exc

def mk_error(msg, code):
    return make_response({"msg" : msg}, code)

def mk_rsp(rsp_o, code=200):
    return make_response(jsonify(rsp_o), code)

def handle_record_post(table, op):
    try:
        content = request.get_json()
        myDict,myTable = dbhelper.convert_json(db,table, op, content)
    except:
        # TODO: do not assume that exception happened due to malformed request,
        # differentiate among exceptions
        return mk_error("Malformed request", 400)

    id = None
    try:
        if op == "insert":
            db_o = dbhelper.add_instance(myTable,**myDict)
            id = db_o.id
        elif op == "update":
            dbhelper.update_instance(model = myTable,**myDict)
        else:
            return mk_error("Unknown operation", 400)
    except sqlalchemy.exc.IntegrityError as e:
        return mk_error("Record already exists", 409)
    return mk_rsp({"msg": "Operation Successful" , "id" : id}, 201)

def handle_record_get(table, id):
    try:
        # TODO - fetch_instance should be fixed to exclude hidden columns, like password hash
        return make_response(dbhelper.fetch_instance(table, id).to_json(), 200)
    except Exception as e:
        # TODO: do not assume that exception happened due to malformed request,
        # differentiate among exceptions
        sys.stderr.write("Exception {}".format(e))
        return mk_error("Malformed request", 400)

app = create_app()

db = SQLAlchemy(app)
db.create_all()

@app.route("/test_vue")
def test_vue():
    return render_template('vue.html', name="vue-test")

@app.route("/test_db")
def test_db():
    n = random.randint(0, 10000)
    str = f'abc{n}'
    p = model.Patient(name=str)
    db.session.add(p)
    db.session.commit()
    for p in model.Patient.query.all():
        str += p.__repr__() + "<br />"
    result = Markup(f'<span style="color: green;">Init DB<br />{str}</span>')
    return render_template('test-patient.html', result=result)

@app.route("/")
def test():
    mysql_result = False
    query_string = text("select concat(table_schema,'.',table_name) from information_schema.tables where table_schema = 'patient_sass'")
    rows = db.engine.execute(query_string)

    # Return the page with the result.
    return render_template('db-test.html', rows=rows)

# TODO: GET /patient needs to require ADMIN login, but we do not have ADMIN setup yet
@app.route("/patient/<id>",methods=["GET"])
def handle_patient_get(id):
    return handle_record_get("Patient", id)

@app.route("/patient/<method>",methods=["POST"])
def handle_patient_post(method):
    return handle_record_post("Patient", method)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80 ,debug=False)
