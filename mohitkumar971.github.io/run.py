from flask import *
from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient('mongodb://dbuser:dbpassword12@cluster0-shard-00-00.6u96h.mongodb.net:27017,cluster0-shard-00-01.6u96h.mongodb.net:27017,cluster0-shard-00-02.6u96h.mongodb.net:27017/myFirstDatabase?ssl=true&replicaSet=atlas-t0kf45-shard-0&authSource=admin&retryWrites=true&w=majority')
db = client.Library

app = Flask(__name__)

@app.route('/')
def grid():
    return render_template("grid.html"); 

@app.route('/students')
def students():  
    return render_template("students.html")

@app.route('/add')
def add():  
    return render_template("add.html")

@app.route("/savedetails",methods = ["POST","GET"])  
def savedetails(): 
    details = db.details
    msg = "msg"  
    if request.method == "POST":  

        try:  
           name = request.form["name"]  
           roll_no = request.form["roll_no"]  
           email = request.form["email"]  
           department = request.form["department"]  
           personDocument={

           "name": name,
           "roll_no": roll_no,
           "email": email,
           "department":department
           }
           details.insert_one(personDocument)
           print("record updated")
        except:  
           msg = "We can not add the Student to the list"  
        finally:  
           return render_template("success.html",msg = msg) 

@app.route("/findstudent",methods = ["POST","GET"])  
def findstudent():
    details = db.details
    if request.method == "POST":

        search = request.form["search"]
        userid = ObjectId(search)
        rows = details.find_one({"_id": userid})
        
        name=""
        email=""
        roll_no=""
        department=""
        
        for key, val in rows.items():
            if key == 'name': name = val
            if key == 'roll_no': roll_no = val
            if key == 'email': email = val
            if key == 'department': department = val 

    return render_template("findstudent.html", name=name , email=email , roll_no=roll_no , department=department )  

if __name__ == "__main__":  
    app.run(debug = True)  