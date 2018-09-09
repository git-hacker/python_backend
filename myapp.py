from flask import Flask, render_template, jsonify, request,session
from models import *
import os
from sqlalchemy import desc
import json
from flask_cors import *
import requests

app = Flask(__name__)
CORS(app, supports_credentials=True)

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres://postgres:111111@localhost:5432/postgres"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

global userID

@app.route("/") # start
def login():
    return render_template("index.html")
# the session includes fn, ln,password, carinfo, journey, points, age, gender

@app.route("/user", methods=["POST","PUT","GET"]) # start
def log():
    if request.method == "POST":
        # add a new user
        pw = request.form.get("password")
        id = request.form.get("name")
        userID = id
        abc=Driver.query.filter_by(id=id).count()
        if abc == 0:
            # fn = request.form.get("FirstName")
            # ln = request.form.get("LastName")
            
            add_user(id, pw)
            session[id] = [pw,0,[],0,None,None]
            db.session.commit()
            return jsonify({
                           "name": id,
                           })
    
    
        abcd=Driver.query.filter_by(id=id).first()
        password =abcd.password
        if password==pw:
            #cars = Car.query.filter_by(owner=userID).all()
            #trips = Journey.query.filter_by(driver=userID).all()
            #gender = abcd.gender
            #point = abcd.point
            #age = abcd.age
            #session[userID] = [pw,[],[],point,age,gender]
            #for car in cars:
            #    session[userID][1].append(car.numb)
            #for trip in trips:
            #    session[userID][2].append(trip.id)
            return jsonify({
                           "name": id
                           })
        else:
            return jsonify({"error":"wrong"}), 400

if request.method =='GET':
    if session == {}:
        return jsonify({"error":"wrong"}), 401
        for id in session:
            userID = id
            break
    dictionary1 = {}
        dictionary1["car"]=session[userID][1]
        dictionary1["trip"]=session[userID][2]
        dictionary1["point"]=session[userID][3]
        dictionary1["age"]=session[userID][4]
        dictionary1["gender"]=session[userID][5]
        dictionary1["name"]= userID
        return jsonify(dictionary1)
if session != {}:
    return jsonify({"error":"wrong"}), 401
    user=Driver.query.filter_by(username=session[userID]).first()
    user.gender = request.form.get("gender")
    user.age = request.form.get("age")
    user.password = request.form.get("password")
    # user.lastname= request.form.get("lastname")
    # user.firstname= request.form.get("firstname")
    
    # session[userID][0]=user.firstname
    # session[userID][1]=user.lastname
    session[userID][0]=user.password
    session[userID][4]=user.age
    session[userID][5]=user.gender
    db.session.commit()
    return jsonify({
                   "condition": "success"
                   })

@app.route("/score", methods=["GET"])
def ranking():
    if request.method == 'GET':
        users= Driver.query.order_by(Driver.point.desc()).all()
        rank = 0
        score =0
        id = None
        for user in users:
            if user.id != session[userID]:
                rank +=1
            else:
                score= user.point
                id = user.id
                break
        return jsonify({
                       "username": id,
                       "score": score,
                       "rank": rank,
                       })

@app.route("/journey",methods=['POST'])
def journey():
    address = "https://restapi.amap.com/v4/direction/truck?key=f2d1df02fc1c58d8a4ed23bfc0b584bd&"
        origin=request.form.get("origin")
        passing = request.form.get("passing")
        destination = request.form.get("destination")
        time= request.form.get("starttime")-request.form.get("endtime")
        truck = Car.query.filter_by(owner=userID).first()
        address += "origin={origin}&destination={destination}&output=json&size={truck.size}&height={truck.weight}&width={truck.width}&weight={truck.weight}&waypoints={passing}&axis={truck.axlesNum}&province={truck.province}&number={truck.numbe}"
        res= requests.get(address)
        data=res.json()
        dis=data["data"]["route"]["paths"]["distance"]
        givetime=res["data"]["route"]["paths"]["duration"]
        score = dis/100
        fs = 0
        pro = time-givetime
        pro = pro/time
        if pro < 0.15 and pro > -0.15:
            fs = score
    else:
        fs = score*(1-abs(pro))
        user=Driver.query.filter_by(id=userID).first()
        user.point += fs
        session[userID][3]+=fs
        
        journey=Journey(id="from {origin} to {destination}",origin=origin,destination=destination, time=time,driver=userID)
        db.session.add(journey)
        user.journey += "/{journey.id}"
        session[userID][2].append(journey.id)
        db.session.commit()
        return "seccess"






@app.route("/truck",methods= ["POST","GET"])
def add_truck():
    for ida in session.keys():
        userID = ida
        break
    if request.method == "POST":
        numbe = request.form.get("numbe")
        policy = 1
        size = request.form.get("size")
        width = request.form.get("width")
        height = request.form.get("height")
        load = request.form.get("load")
        weight = request.form.get("weight")
        axlesNum = request.form.get("axlesNum")
        province = request.form.get("province")
        owner = request.form.get("owner")
        if width == None:
            width = 2.5
        if height == None:
            height = 1.6
        if load == None:
            load = 0.9
        if weight ==None:
            weight = 10
        if axlesNum == None:
            axlesNum = 2
        userID = ""
        for ida in session.keys():
            userID = ida
            break
        #user = Driver.query.filter_by(id=userID).first()
        #user.cars =1
        #session[userID][1] +=1
        owner = userID
        truck = Car(numbe=numbe,policy=policy,size=size,width=width,height=height,load=load,weight=weight,axlesNum=axlesNum,province=province,owner=owner)
        db.session.add(truck)




db.session.commit()
return jsonify({
               "condition":"success"
               })
    
    
    else:
        dict = {}
        for ida in session:
            userID = id
            break
        cars=Car.query.filter_by(owner=session[userID]).all()
        for a in cars:
            dict["{a.numbe} "]=[a.numbe, a.policy, a.size, a.width, a.height, a.load, a.weight, a.axlesNum, a.province, a.owner]
        return json.dumps(dict)
if __name__== '__main__':
    app.run(
            host = '0.0.0.0',
            port = 5000,
            debug = True
            )






















@app.route("/forget") # forget the password
def Forget():
    return "you cannot do this at this stage"

@app.route("/car", methods=["POST"]) # enter the infor of car
def car():
    fn = request.form.get("FirstName")
    ln = request.form.get("LastName")
    pw = request.form.get("NP")
    id = request.form.get("NewID")
    Driver.add_user(id, fn, ln , pw)
    return jsonify({
                   "origin": fn,
                   "destination": ln,
                   "duration": pw,
                   "passengers": id
                   })

# def car():
#     fn = request.form.get("Firstname")
#     ln = request.form.get("Lastname")
#     pw = request.form.get("NP")
#     id = request.form.get("NewID")
#     Driver.add_user(id, fn, ln , pw)
#
#     return render_template("car.html")


@app.route("/car_check", methods=["POST"]) # check the info of car
def car_check():
    id = request.form.get("OldID")
    if id != None:
        if Driver.query.filter_by(id = request.form.get(id)):
            return "1"
    return "111111"

@app.route("/personal")
def personal():
    # store all the info
    car = Car("""info of car""")
    driver = Driver("""info of driver""")


@app.route("/journey", methods= ['POST']) # check the route
def JOURNEY_info():
    journey = Journey("""info""")
    
    return '11111'
# Route for handling the login page logic
# @app.route('/login', methods=["POST"])
# def login():
#     error = None
#     if request.method == "POST":
#         if request.form[userID] != 'admin' or request.form['password'] != 'admin':
#             error = 'Invalid Credentials. Please try again.'
#         else:
#             return redirect(url_for('home'))
#     return render_template('login.html', error=error)
