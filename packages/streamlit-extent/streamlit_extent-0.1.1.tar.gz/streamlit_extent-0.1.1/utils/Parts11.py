from flask import Flask,request,jsonify,url_for
from flask_jwt_extended import JWTManager,create_access_token,jwt_required,get_jwt_identity
from database import connect_db
import json

app=Flask(__name__)
app.config["JWT_SECRET_KEY"]="zxcvbnnbvcz"

jwt=JWTManager(app)

@app.route("/api/v1/SignIn",methods=["POST"])
def sing_in():
    data=request.json
    login=data["login"]
    password=data["password"]
    query=f"select * from Employees where Login='{login}' and Password='{password}'"
    user=connect_db(query)
    if not user or user=="[]":
        return "error"
    user_token=create_access_token(identity=login)
    return jsonify({"access_token":user_token})
    # return url_for("/api/v1/Documents",current_user=user_token)

@app.route("/api/v1/Documents",methods=["GET"])
@jwt_required()
def all_doc():
    query="select * from Documents"
    data=connect_db(query)
    print(data)
    return data
    # return "doc end"

@app.route("/api/v1/Document/<documentId>/Comments",methods=["GET","POST"])
@jwt_required()
def one_doc(documentId):

    if request.method=="GET":
        query=f"Select * From Comment where Id={documentId}"
        data=connect_db(query)
        print(data)
        return data
    
    if request.method=="POST":
        
        return

if __name__=="__main__":
    app.run(debug=True,port=1000,host="0.0.0.0")