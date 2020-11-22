import re
import sqlite3 as lite
from flask import Flask,render_template,request, redirect
app = Flask(__name__)

error_message=''
student_message=''
quiz_message=''
result_message=''
add_result_message=''

@app.route('/')
def main():
    return redirect('/login')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    global error_message
    if 'username' in request.form:
        username = request.form['username']
        password = request.form['password']
        if username != 'admin' or password != 'password':
            error_message = 'Username or password is incorrect, please try again.'
            return render_template('login.html', error_message=error_message)
        else:
            return redirect('/dashboard')
    else:
        error_message=''
        return render_template('login.html', error_message=error_message)

@app.route('/dashboard')
def dashboard():
    con = lite.connect("hw13.db")
    global quiz_message
    global student_message
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM students")
        students = cur.fetchall()
        cur.execute("SELECT * FROM quizzes")
        quizzes = cur.fetchall()
    return render_template('dashboard.html', students=students,student_message=student_message,quizzes=quizzes,quiz_message=quiz_message)

@app.route('/student/add', methods = ['POST'])
def add_student():
    global student_message
    first_name=request.form["FirstName"]
    last_name=request.form["LastName"]
    if first_name=="" or last_name=="":
        student_message="Please input first name and last name"
    else:
        student_message = ""
        con = lite.connect("hw13.db")
        with con:
            cur = con.cursor()
            cur.execute("INSERT INTO students(first_name,last_name) VALUES('"+first_name+"','"+last_name+"')")
    return redirect('/dashboard')

@app.route('/quiz/add', methods = ['POST'])
def add_quiz():
    global quiz_message
    quiz_subject=request.form["QuizSubject"]
    Number_Of_Question=request.form["NumberOfQuestion"]
    QuizDate = request.form["QuizDate"]
    if quiz_subject=="" or Number_Of_Question=="" or QuizDate=="":
        quiz_message="Please input all the quiz information"
    else:
        quiz_message = ""
        con = lite.connect("hw13.db")
        with con:
            cur = con.cursor()
            cur.execute("INSERT INTO quizzes(quiz_subject,number_of_question,quiz_date) VALUES('"+quiz_subject+"',"+Number_Of_Question+",'"+QuizDate+"')")
    return redirect('/dashboard')

@app.route('/student/<n>')
def result(n):
    con = lite.connect("hw13.db")
    global result_message
    with con:
        cur = con.cursor()
        cur.execute("SELECT * FROM student_results WHERE student_id="+n)
        results = cur.fetchall()
    return render_template('quiz_result.html', results=results, result_message=result_message)

@app.route('/results/add', methods = ['GET', 'POST'])
def add_quiz_result():
    global add_result_message
    con = lite.connect("hw13.db")
    with con:
        cur = con.cursor()
        if 'Student' in request.form:
            student_id=request.form["Student"]
            quiz_id=request.form["Quiz"]
            score=request.form["Score"]
            if score!="":
                cur.execute("insert into student_results values("+student_id+","+quiz_id+","+score+")")
                return redirect('/dashboard')
            else:
                add_result_message="Please input all the information"
        cur.execute("SELECT student_id,first_name||' '||last_name AS student_name FROM students")
        students =cur.fetchall()
        cur.execute("SELECT * FROM quizzes")
        quizzes = cur.fetchall()

    return render_template('add_quiz_result.html', students=students,quizzes=quizzes, add_result_message=add_result_message)

if __name__ == '__main__':
    app.run(debug=True)