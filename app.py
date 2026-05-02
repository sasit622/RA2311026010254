from flask import Flask,request,jsonify

user={
    1:{"name":"Nishant","age":28},
    2:{"name":"Ayush" , "age":28}
}

app=Flask(__name__)

app.route("/user/<int:user_id>",methods=["GET"])
def get_user(user_id):
    if user_id not in user:
        return jsonify({"error":"User not found"}),404
    return jsonify(user[user_id])

app.route("/user/<int:user_id>",methods=['PUT'])
def adduser(user_id):
    if user_id not in user:
        return jsonify({"error":"User already exists"}),400
    
    data = request.json
    user[user_id] = data
    return jsonify(user[user_id]),201

if __name__ == "__main__":
    app.run(debug=True)
