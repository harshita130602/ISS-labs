from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

database_file = "mysql://root:root@localhost:3306/studentDatabase.db"
app.config['SQLALCHEMY_DATABASE_URI'] = database_file
db = SQLAlchemy(app)

class Student(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	rollnumber = db.Column(db.Integer, nullable = False)
	name = db.Column(db.String(80), nullable=False)
	email = db.Column(db.String(120), nullable=False)	

@app.route('/')
def root():
	return "Hello"

@app.route('/addStudent', methods = ['GET', 'POST'])
def add():
	if request.form:
		form = request.form
		s = Student(name = form['name'], rollnumber = form['rollnumber'], email = form['email'])
		db.session.add(s)
		db.session.commit()
		return redirect(url_for('getStudents'))
	return render_template('home.html')

@app.route('/getStudents', methods = ['GET'])
def getStudents():
	students = Student.query.all()
	return render_template('students.html', data = students)

@app.route('/getStudent')
def getOneStudent():
	name = request.args.get('name')
	s = Student.query.filter_by(name=name).first()
	obj = {
			"username" : s.name,
			"rollnumber" : s.rollnumber,
			"email" : s.email
	}
	return str(obj)

	
if __name__ == '__main__':
	app.run(debug = True)
