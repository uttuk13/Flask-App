from flask import Flask, render_template, request
import sqlite3 as sql
import cx_Oracle

app = Flask(__name__, static_url_path='/static')

@app.route('/')
def home():
    return render_template('about.html')

@app.route('/enternew')
def enternew():
   return render_template('student.html')

@app.route('/addrec',methods = ['POST', 'GET'])
def addrec():
   if request.method == 'POST':
      try:
         nm = request.form['nm']
         addr = request.form['add']
         city = request.form['city']
         pin = request.form['pin']
         
         with sql.connect("database.db") as con:
            cur = con.cursor()
            
            cur.execute("INSERT INTO students (name,addr,city,pin) VALUES (?,?,?,?)",(nm,addr,city,pin) )
            
            con.commit()
            msg = "Record successfully added"
      except:
         con.rollback()
         msg = "error in insert operation"
      
      finally:
         con.close()
         return render_template("result.html",msg = msg)

@app.route('/list')
def list():
   con = sql.connect("database.db")
   con.row_factory = sql.Row
   
   cur = con.cursor()
   cur.execute("select * from students")
   
   rows = cur.fetchall()
   return render_template("list.html",rows = rows)



@app.route('/listOracleDB')
def listOracleDB():
   con = cx_Oracle.connect("system/system@localhost:1521/XE")
   cur = con.cursor()
   rows = cur.fetchall()
   return render_template("listOracleDB.html",rows = rows)

if __name__ == '__main__':
   app.run(debug = True)
