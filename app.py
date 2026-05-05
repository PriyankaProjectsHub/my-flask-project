from dotenv import load_dotenv
import os

load_dotenv()
from flask import Flask, render_template, request
import mysql.connector
import plotly.express as px
from collections import Counter

app = Flask(__name__)

# Database connection
db = mysql.connector.connect(
    host='localhost',
    user='root',
    password='root',
    database='company'
)

cursor = db.cursor()

@app.route('/')
def index():
    return render_template("index.html")


@app.route("/submit", methods=["POST"])
def submit():
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    department = request.form['department']
    designation = request.form['designation']
    salary = request.form['salary']
    joining_date = request.form['joining_date']

    query = """
    INSERT INTO employees
    (name, email, phone, department, designation, salary, joining_date)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    values = (name, email, phone, department, designation, salary, joining_date)

    cursor.execute(query, values)
    db.commit()

    return "Employee Data saved Successfully"


@app.route('/dashboard')
def dashboard():
    cursor.execute("""
      select name , email , phone, department , designation , salary ,joining_date 
      from  employees
    """)
    data = cursor.fetchall()

    # getting data in variables
    department = [i[3] for i in data]
    designation= [i[4] for i in data]
    salaries= [i[5] for i in data]
    joining_date=[i[6] for i in data]
    
    dept_count = Counter(department)
    desig_count = Counter(designation)
    join_count = Counter(joining_date)
    

    fig_dept = px.pie(
      names= list(dept_count.keys()),
      values= list(dept_count.values()),
      title =  "Department Wise Employees count" 
    )
    fig_dept.update_layout(template=None)
  
    fig_desig = px.pie(
      names= list(desig_count.keys()),
      values= list(desig_count.values()),
      title =  "Designation Wise Employees count" 
    )
    fig_desig.update_layout(template=None)
    
    fig_salary = px.histogram(
      salaries,
      nbins = 5,
      title = "Salary Distribution"
    )
    fig_salary.update_layout(template=None) 

    fig_join=px.line(
      x=list(join_count.keys()),
      y=list(join_count.values()),
      title="Joining Trend"
    )
    fig_join.update_layout(template=None)

    return render_template(
      "dashboard.html",
      dept_chart=fig_dept.to_html(full_html=False),
      desig_chart=fig_desig.to_html(full_html=False),
      salary_chart=fig_salary.to_html(full_html=False),
      join_chart=fig_join.to_html(full_html=False),
      employees=data
    )
if __name__ == "__main__":
    app.run(debug=True)