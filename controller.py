from flask import Flask
from datetime import datetime
from flask import render_template,request,redirect,url_for,jsonify,session
import re
import sys
from config import app,db,mycursor
from flask.wrappers import Request
from models import login_details
from sqlalchemy import text

global unqmail 
global orderid
global totalvar
unqmail = ''

@app.route('/')
def home1():
   unqmail=''
   return render_template('signup.html')


@app.route('/home')
def home():
   return render_template('index.html')
if __name__ == '__main__':
       app.run()
       



@app.route("/menu",methods = ['POST','GET'])
def order():
        if request.method== 'GET':
              return render_template("menu.html")
        elif request.method== 'POST':
              p1 = int(request.form.get('p1'))
              p2 = int(request.form.get('p2'))
              p3 = int(request.form.get('p3'))
              p4 = int(request.form.get('p4'))
              p5 = int(request.form.get('s1'))
              p6 = int(request.form.get('s2'))
              p7 = int(request.form.get('s3'))
              iprice1=12.50
              iprice2 = 15.50
              iprice3 = 16.50
              iprice4 = 20.00
              iprice5 = 8.50
              iprice6 = 9.50
              iprice7 = 10.50
              total =iprice1*p1+iprice2*p2+iprice3*p3+iprice4*p4+iprice5*p5+iprice6*p6+iprice7*p7
              global totalvar
              totalvar = total
              sql_statement = text("INSERT INTO order_table (uid, price) SELECT u_id, :total FROM user_table WHERE email = :unqmail")
              db.session.execute(sql_statement, {"unqmail": unqmail, "total": total})
              db.session.commit()
              sql_statement = text("SELECT oid FROM order_table WHERE uid = (SELECT u_id FROM user_table WHERE email = :unqmail) ORDER BY oid DESC LIMIT 1")
              res = db.session.execute(sql_statement, {"unqmail": unqmail})
              res = res.fetchall()
              tempvar =str(res[0]) 
              tempvar = tempvar.strip('(')
              tempvar = tempvar.strip(')')
              tempvar = tempvar.strip(',')
              tempvar = int(tempvar)
              global orderid 
              orderid = tempvar
              
              if p1>0:
                     sql_statement = text("INSERT INTO order_item VALUES (:tempvar, (SELECT nameitem FROM menu_table WHERE menuid = 1), :p1)")
                     db.session.execute(sql_statement, {"tempvar": tempvar, "p1": p1})
                     db.session.commit()
              if p2>0:
                     sql_statement = text("INSERT INTO order_item VALUES (:tempvar, (SELECT nameitem FROM menu_table WHERE menuid = 2), :p2)")
                     db.session.execute(sql_statement, {"tempvar": tempvar, "p2": p2})
                     db.session.commit()
              if p3>0:
                     sql_statement = text("INSERT INTO order_item VALUES (:tempvar, (SELECT nameitem FROM menu_table WHERE menuid = 3), :p3)")
                     db.session.execute(sql_statement, {"tempvar": tempvar, "p3": p3})
                     db.session.commit()
              if p4>0:
                     sql_statement = text("INSERT INTO order_item VALUES (:tempvar, (SELECT nameitem FROM menu_table WHERE menuid = 4), :p4)")
                     db.session.execute(sql_statement, {"tempvar": tempvar, "p4": p4})
                     db.session.commit()
              if p5>0:
                     sql_statement = text("INSERT INTO order_item VALUES (:tempvar, (SELECT nameitem FROM menu_table WHERE menuid = 5), :p5)")
                     db.session.execute(sql_statement, {"tempvar": tempvar, "p5": p5})
                     db.session.commit()
              if p6>0:
                     sql_statement = text("INSERT INTO order_item VALUES (:tempvar, (SELECT nameitem FROM menu_table WHERE menuid = 6), :p6)")
                     db.session.execute(sql_statement, {"tempvar": tempvar, "p6": p6})
                     db.session.commit()
              if p7>0:
                     sql_statement = text("INSERT INTO order_item VALUES (:tempvar, (SELECT nameitem FROM menu_table WHERE menuid = 7), :p7)")
                     db.session.execute(sql_statement, {"tempvar": tempvar, "p7": p7})
                     db.session.commit()   

              return redirect(url_for('bill'))
              

@app.route("/signup",methods = ['POST','GET'] )
def about():
       if request.method== 'GET':
              return render_template("signup.html")
       elif request.method== 'POST':
              p1 = request.form.get('fname')
              p2 = request.form.get('lname')
              p3 = request.form.get('email')
              p4 = request.form.get('gen')
              p5 = request.form.get('addr')
              p6 = request.form.get('number')
              p7 = request.form.get('pswd')
              sql_statement = text("insert into user_table(f_name, l_name, email, gender, address, create_date, mobile_number) values(:p1, :p2, :p3, :p4, :p5, current_date, :p6)")
              db.session.execute(sql_statement, {"p1": p1, "p2": p2, "p3": p3, "p4": p4, "p5": p5, "p6": p6})
              db.session.commit()
              unqmail =p3
              sql_statement = text("insert into login_details values(:p3, :p7)")
              db.session.execute(sql_statement, {"p3": p3, "p7": p7})
              db.session.commit()
              return redirect(url_for('home1'))
@app.route("/loginuser",methods = ['POST','GET'] )
def userlogin():
       error = None
       if request.method== 'GET':
              return render_template("signup.html")
       elif request.method== 'POST':
              p1 =request.form.get('email')
              p2 = request.form.get('pswd')
              global unqmail
              unqmail = p1
              sql_statement = text("select user_mail from login_details where user_mail = :p1 and user_password = :p2")
              res = db.session.execute(sql_statement, {"p1": p1, "p2": p2})
              res = res.fetchall()[0][0]
              if res!=p1:
                     error = "INVALID PASSWORD"
                     return render_template("signup.html",error=error)
              else:
                  return redirect(url_for('home'))   

@app.route("/cart",methods = ['POST','GET'])    
def cartout():
       if request.method == 'GET':
              return render_template("cart.html")
       elif request.method =='POST':
              session['data'] = request.json
              data = session.get('data', None)
              print("session items: " ,data)
       return redirect(url_for('home')) 
@app.route('/bill')
def bill():
    mycursor.execute("SELECT * FROM order_item where orderid = '{}'".format(orderid))
    data = mycursor.fetchall()
    return render_template('bill.html', data=data,total=totalvar)

@app.route('/deleteorder')
def deleteorder():
       sql_statement = text("DELETE FROM order_item WHERE orderid = :orderid")
       db.session.execute(sql_statement, {"orderid": orderid})
       db.session.commit()
       return redirect(url_for('order')) 

