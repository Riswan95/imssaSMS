from flask import Flask, render_template, request, send_file, abort, redirect, url_for, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from datetime import datetime
from sqlalchemy.ext.automap import automap_base

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ybh_imssa1.db'
app.config['SECRET_KEY'] = 'ALLAH_AKBAR'
db = SQLAlchemy(app)
base = automap_base()
base.prepare(db.engine, reflect=True)

login_manager = LoginManager()
login_manager.init_app(app)

class User(UserMixin, db.Model):
    __tablename__ = 'Teacher'
    id = db.Column('id', db.String, primary_key = True)

#Student = db.Table('Student', db.metadata, autoload=True, autoload_with=db.engine)
#teacher_class_table = db.Table('teacher_class_table', db.metadata, autoload=True, autoload_with=db.engine)
#Class = db.Table('Class', db.metadata, autoload=True, autoload_with=db.engine)
#Attendance = db.Table('Attendance', db.metadata, autoload=True, autoload_with=db.engine)
Student = base.classes.Student
teacher_class_table = base.classes.teacher_class_table
Class = base.classes.Class
Attendance = base.classes.Attendance
#print(dir(teacher))

@login_manager.user_loader
def load_user(userID):
    return User.query.get(userID)

@app.route('/', methods = ['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        user = User.query.filter_by(id =request.form['madrasahID'].upper()).first()
        if user:
            login_user(user)
            session['userID'] = user.id
            print(session['userID'] + ' logged in!')
            return redirect(url_for('dashboard'))
        else:
            return "Login Error"

# @app.route('/getClass', methods = ['POST', 'GET'])
# @login_required
def getClass(user=current_user):
    classes = db.session.query(teacher_class_table).filter_by(teacher_id=user.id).all()
    class_list = []
    for x in classes:
        #print(x.teachers)
        class_list.append(x.class_name)
    session['classList'] = class_list
    #return class_list

# @app.route('/getTeacher', methods = ['POST', 'GET'])
# @login_required
def getTeacher(user=current_user):
    teacher = db.session.query(Student).filter_by(student_id=user.id).first()
    session['userName'] = teacher.student_name 
    #return teacher

@app.route('/attendance/<className>', methods = ['POST', 'GET'])
@login_required
def attendPg(className):
    listNames = getNames(className)
    if request.method == 'GET':
        #return render_template('attndPg.html', namesList = listNames, className = className, name = db.session.query(Student).filter_by(student_id=current_user.id).first().student_name)
        return render_template('attndPg.html', namesList = listNames, className = className, name = session['userName'])

@app.route('/update/<className>', methods = ['POST', 'GET'])
@login_required
def updateAttendance(className):
    attendData = request.form.to_dict()
    print(attendData)
    currDate = datetime.now()
    today = datetime(currDate.year, currDate.month, currDate.day)
    s = db.text('INSERT INTO Attendance (date, presence, student_id) VALUES (:currDate,:presence,:student_id)')
    for x in attendData:
        buffer_attend = Attendance(date = today, presence=int(attendData[x]), student_id = x)
        db.session.add(buffer_attend)
    db.session.commit()
    return 'updated'

@app.route('/dashboard')
@login_required
def dashboard(user=current_user):
    getTeacher()
    getClass()
    #return render_template('dashboard.html', name = session['userName'], classList = session['classList'])
    return render_template('dashboard.html')
    #return render_template('dashboard.html', name = teacher.student_name, classList = class_list)
    #return 'The current user is ' + session['userID'] + current_user.id

@app.route('/retrieveAttendance', methods = ['POST', 'GET'])
@login_required
def retrieveAttendance(user=current_user):
    classList = session['classList']
    results = {}
    for class_ in classList:
        #get the first student from each class
        retrieved_student = db.session.query(Student).filter_by(class_name = class_).first()
        #get the attendance for that student
        retrieved_attendances = db.session.query(Attendance.date.distinct()).filter_by(student_id = retrieved_student.student_id).all()
        results[class_] = retrieved_attendances

    #results = db.session.query(Attendance.date.distinct()).all()
    print(results)
    return results


@app.route('/logout')
@login_required
def logout():
    logout_user()
    #return 'You are now logged out!'
    return redirect(url_for('login'))
    #return login()


def getNames(className):
    print(className)
    results = db.session.query(Student).filter_by(class_name=className).all()
    #results = db.session.query(Class).first()
    print(results)
    return results


if __name__ == '__main__':
   app.run(debug = True)