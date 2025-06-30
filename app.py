import csv
from flask import Flask, render_template,request,redirect,url_for
import diseaseprediction
import sqlite3
#import mySQLdb

app = Flask(__name__)
#conn = MySQLdb.connect(host='localhost',user='root',password='',db='disease_database')

with open('templates/Testing.csv', newline='') as f:
        reader = csv.reader(f)
        symptoms = next(reader)
        symptoms = symptoms[:len(symptoms)-1]
@app.route('/', methods=['GET'])
def dropdown():
        return render_template('includes/signup.html',symptoms=symptoms)

@app.route('/logon')
def logon():
	return render_template('signup.html')

@app.route('/login')
def login():
	return render_template('signin.html')

@app.route("/signup")
def signup():
	user = request.args.get('user','')
	email = request.args.get('email','')
	password = request.args.get('pass','')
	number = request.args.get('mobile','')
	name = request.args.get('name','')
	con = sqlite3.connect('signup.db')
	cur = con.cursor()
	cur.execute("insert into `info` (`user`,`email`, `password`,`mobile`,`name`) VALUES (?, ?, ?, ?, ?)",(user,email,password,number,name))
	con.commit()
	con.close()
	return render_template("signin.html")

@app.route("/signin")
def signin():

    mail1 = request.args.get('user','')
    password1 = request.args.get('pass','')
    con = sqlite3.connect('signup.db')
    cur = con.cursor()
    cur.execute("select `user`, `password` from info where `user` = ? AND `password` = ?",(mail1,password1,))
    data = cur.fetchone()

    if data == None:
        return render_template("signin.html")    

    elif mail1 == 'admin' and password1 == 'admin':
         return render_template('includes/default.html', symptoms=symptoms)
    elif mail1 == str(data[0]) and password1 == str(data[1]):
       return render_template('includes/default.html', symptoms=symptoms)
    else:
        return render_template('includes/default.html', symptoms=symptoms)
    

@app.route('/disease_predict', methods=['POST'])
def disease_predict():
    selected_symptoms = []
    if(request.form['Symptom1']!="") and (request.form['Symptom1'] not in selected_symptoms):
        selected_symptoms.append(request.form['Symptom1'])
    if(request.form['Symptom2']!="") and (request.form['Symptom2'] not in selected_symptoms):
        selected_symptoms.append(request.form['Symptom2'])
    if(request.form['Symptom3']!="") and (request.form['Symptom3'] not in selected_symptoms):
        selected_symptoms.append(request.form['Symptom3'])
    if(request.form['Symptom4']!="") and (request.form['Symptom4'] not in selected_symptoms):
        selected_symptoms.append(request.form['Symptom4'])
    if(request.form['Symptom5']!="") and (request.form['Symptom5'] not in selected_symptoms):
        selected_symptoms.append(request.form['Symptom5'])

    # disease_list = []
    # for i in range(7):
    #     disease = diseaseprediction.dosomething(selected_symptoms)
    #     disease_list.append(disease)
    # return render_template('disease_predict.html',disease_list=disease_list)
    disease = diseaseprediction.dosomething(selected_symptoms)
    return render_template('disease_predict.html',disease=disease,symptoms=symptoms)

# @app.route('/default')
# def default():
#         return render_template('includes/default.html')
 
@app.route('/find_doctor', methods=['POST'])
def get_location():
    location = request.form['doctor']
    return render_template('find_doctor.html',location=location,symptoms=symptoms)

@app.route('/drug', methods=['POST'])
def drugs():
    medicine = request.form['medicine']
    return render_template('homepage.html',medicine=medicine,symptoms=symptoms)

if __name__ == '__main__':
    app.run(host="localhost",port='5000', debug=True)