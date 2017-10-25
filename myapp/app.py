from flask import Flask
from flask import render_template
from flask_mysqldb import MySQL
from flask_prometheus import monitor 
mysql = MySQL()
app = Flask(__name__)
# My SQL Instance configurations 
# Change the HOST IP and Password to match your instance configurations
 
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'P@ssw0rd'
app.config['MYSQL_DB'] = 'todolist'
app.config['MYSQL_HOST'] = '35.197.208.200'
mysql.init_app(app)

@app.route('/')
@app.route('/<name>')
def statichtml(name=None):
    return render_template('index.html', name=name)

# The first route to access the webservice from http://35.189.100.87:5000/ 
#@pp.route("/add") this will create a new endpoints that can be accessed using http://external-ip:5000/add
@app.route("/list")
def hello(): # Name of the method
    cur = mysql.connection.cursor() #create a connection to the SQL instance
    cur.execute('''SELECT * FROM list''') # execute an SQL statment
    rv = cur.fetchall() #Retreive all rows returend by the SQL statment
    return render_template('index.html', name=str(rv))     #Return the data in a string format

@app.route("/insert/<name>")
def add(name=None):
    cur= mysql.connection.cursor()
    insert_stmt = (
                 "INSERT INTO list (todoname) "
                 "VALUES (%s)")
    data=(name)
    cur.execute(insert_stmt, data)
    mysql.connection.commit()
    return render_template('index.html', name="New Record is added to the database")  

@app.route("/update/<name>/<todoid>")
def update(name=None, todoid=None):
    cur=mysql.connection.cursor()
    update_stmt = (
        "UPDATE list SET todoname = %s " 
        "WHERE todoid = %s")
    data=(name,todoid)
    cur.execute(update_stmt, data)
    mysql.connection.commit()
    return render_template('index.html', name="Todo recored was updated")      #Return the data in a string format

@app.route("/delete/<name>")
def delete(name=None):
    cur=mysql.connection.cursor()
    delstatmt = "DELETE FROM list WHERE todoname = ' {} ' ".format(name)
    print(delstatmt)                
   
    cur.execute(delstatmt)
    mysql.connection.commit()
    return render_template('index.html', name="Todo recored was deleted")      #Return the data in a string format

if __name__ == "__main__":
        monitor(app, port=8000)
        app.run(host='0.0.0.0', port='5000')
