from flask import Flask,render_template,request,jsonify,url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import case,func,or_,create_engine
import pymysql
from flask import redirect
from chatbot.chatbot import predict_class, get_response, intents
from sqlalchemy import DateTime
from datetime import datetime
app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqldb://root:@localhost:4306/patient'
engine = create_engine("mysql+pymysql://root:@localhost/patient", pool_pre_ping=True)  # SQLite database
pymysql.install_as_MySQLdb()
db = SQLAlchemy(app)
class Patient(db.Model):
    __tablename__ = 'patient'
    patient_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(20), nullable=False)
    age = db.Column(db.Integer, nullable=False)

    def __init__(self, name, address,age):
        self.name = name
        self.address = address
        self.age = age
class Doctor(db.Model):
  __tablename__='doctor'
  doctor_id=db.Column(db.Integer,primary_key=True,autoincrement=True)
  name=db.Column(db.String(20),nullable=False)
  specialization=db.Column(db.String(20),nullable=False)
  def __init__(self, name, specialization):
        self.name = name
        self.specialization = specialization
class PatientInteraction(db.Model):
  __tablename__='patient_interaction'
  interaction_key=db.Column(db.Integer,primary_key=True,autoincrement=True)
  patient_id = db.Column(db.Integer)
  doctor_id = db.Column(db.Integer)
  query=db.Column(db.String(20))
  response=db.Column(db.String(20))
  timestamp=db.Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
  def __init__(self, patient_id, doctor_id,query,response,timestamp):
        self.patient_id =patient_id
        self.doctor_id = doctor_id
        self.query=query
        self.response=response
        self.timestamp=timestamp

@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            patient_id = int(request.form['id'])  # Ensure patient_id is an integer
        except (ValueError, TypeError):
            return render_template('index.html', error="Invalid ID format")

        # Query the database to check if the patient exists
        patient = Patient.query.get(patient_id)  # Fetch a single record by ID
        
        if patient:
            return redirect(url_for('base', patient_id=patient_id))
        else:
            return render_template('index.html', error="Patient not found")

    return render_template('index.html')
@app.route('/base',methods=['GET','POST'])
def base():
  
  return render_template('base.html')
@app.route('/predict',methods=['GET','POST'])
def predict():
    try:
        data = request.get_json()
        text = data.get("message")

        if not text:
            return jsonify({"error": "No message provided"}), 400
        
        intents_list = predict_class(text)
        response = get_response(intents_list, intents)
        message = {"answer": response}
        return jsonify(message)

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": "An internal error occurred"}), 500
app.run(debug=True)