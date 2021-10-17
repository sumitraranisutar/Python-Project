from bson import ObjectId
from flask import Flask
import pymongo
from flask import render_template
from flask import request

app = Flask(__name__)
con = pymongo.MongoClient("localhost")
db = con['Student']
col = db['details']


@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("home.html")


@app.route("/getDetails", methods=["GET", "POST"])
def get_student_data(form=None):
    print("inside")
    if request.form and request.method == 'POST':
        print(request.form.get("roll_no"))
        if request.form.get("roll_no"):
            q = request.form.get("roll_no")
            s = list(col.find({"roll_no": q}))
            if not len(s):
                s = "Student with entered roll number doesn't exist."
            return render_template("getDetail.html", data=s)
        else:
            return render_template("getDetail.html", data="Please enter the Roll Number.")
    if request.form and request.method == 'PUT':
        print(request.json)
        d = request.form.to_dict()
        if d["roll_no"] and d["name"]:
            p = col.insert_one(d)
            data = list(col.find({"_id": p.inserted_id}))
        return render_template("getDetail.html", data=data)
    return render_template("getDetail.html", data="", form=form)


@app.route("/addDetails", methods=["GET", "POST"])
def add_student_data(form=None):
    if request.form and request.method == 'POST':
        print(request.json)
        d = request.form.to_dict()
        if d["roll_no"] and d["name"]:
            p = col.insert_one(d)
            data = list(col.find({"_id": p.inserted_id}))
            return render_template("addDetails.html", data=data)
        else:
            return render_template("addDetails.html", data="Please enter all required fields.")
    return render_template("addDetails.html", form=form)


@app.route('/delete/<string:id>', methods=['GET', 'POST'])
def delete_student_data(id):
    print(id)
    resp = col.delete_one({"_id": ObjectId(id)})

    return render_template("delete.html")


if __name__ == "__main__":
    app.run(host='localhost', debug=True)
