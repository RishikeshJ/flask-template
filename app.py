from flask import Flask, render_template, request, send_file, flash
import pathlib
import pandas as pd
import sqlite3 as sql
import base64
import os
import sqlite3
from datetime import datetime, timedelta
import numpy as np
from math import sin, cos, sqrt, atan2, radians
import sys

app = Flask(__name__)
app.secret_key = "secret"
conn = sqlite3.connect('q.db')
import csv
import base64

csvf = pd.read_csv("q.csv")
csvf[['date', 'time']] = csvf['time'].str.split('T', expand=True)
csvf['time'] = csvf['time'].str.split('.').str[0]
csvf.to_sql('e3', conn, if_exists='replace', index=False)

 
iport = int(os.getenv('PORT', 8000))
@app.route('/')
def home():
        return render_template('home.html')

# Get 5 Largest quakes
@app.route('/question5',methods=['POST'])
def question5():
   location = request.form['netval']
   cnt = 0
   con = sql.connect("q.db")
   con.row_factory = sql.Row
   cur = con.cursor()
   #Query for smallest msgNST
   cur.execute("select id, place, magNst from e3 where magNst is NOT NULL and net = \'"+location+"\' order by magNst asc LIMIT 1;")
   rows1 = cur.fetchall()
   
   cur1 = con.cursor()
   cur1.execute("select * from e3 where net = \'"+location+"\'")
   rowscn = cur1.fetchall()

   for row in rowscn:
        cnt += 1          
   return render_template("home.html",rows1 = rows1,count = cnt)

   

@app.route('/question5par',methods=['POST'])
def question5par():
   location = request.form['netvalhi']
   con = sql.connect("q.db")
   cnt2 = 0
   con.row_factory = sql.Row
   cur = con.cursor()
   #Query for smallest msgNST
   cur.execute("select id, place , magNst from e3 where magNst is NOT NULL and net = \'"+location+"\' order by magNst desc LIMIT 1;")
   rows2 = cur.fetchall()  

   cur2 = con.cursor()
   cur2.execute("select * from e3 where net = \'"+location+"\'")
   rowscn2 = cur2.fetchall()


   for row in rowscn2:
        cnt2 += 1       
   return render_template("home.html",rows2 = rows2, ct2 = cnt2)


@app.route('/question8',methods=['POST'])
def question8():
   location = request.form['loc']
   mag1 = request.form['m1']
   mag2 = request.form['m2']


   cnt3 = 0
   con = sql.connect("q.db")    
   con.row_factory = sql.Row
   cur = con.cursor() 

   cur.execute("SELECT id, mag,latitude,longitude,place,magnst FROM e3 WHERE magnst between \'"+mag1+"' and \'"+mag2+"' and place LIKE \'%"+location+"%\'")
   rows3 = cur.fetchall()  
   for row in rows3:
        cnt3 += 1
   return render_template("home.html",rows3 = rows3, ct3 = cnt3)

@app.route('/question8s',methods=['POST'])
def question8s():
   id = request.form['id']
   txt = request.form['txt']
   cnt3 = 0
   con = sql.connect("q.db")    
   con.row_factory = sql.Row
   cur = con.cursor()

   query = "update e3 set \"place\" = '"+txt+"' where \"id\" = \'"+id+"\'"  

   cur.execute(query)
   con.commit()

   return render_template("home.html")

if __name__ == '__main__':
    #print(iport)
    app.run(host='0.0.0.0', port=iport,debug = True)
    app.run()