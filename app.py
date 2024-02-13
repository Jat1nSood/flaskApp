from flask import Flask, jsonify, request

app = Flask(__name__)
PORT = 8080

users  = [
    {"name" : 'Jatin', "id" : 1, "age" : 24 },
    {"name" : 'OM',"id" : 2, "age" : 23}
]

#defalut route
@app.route("/")
def index():
    return "Welcome to My Flask app"



# All Users
@app.route("/users", methods = ["GET"])
def get():
    return jsonify({"Users" : users})



# Get by id
@app.route('/users/<int:id>')
def getById(id):
    return jsonify({"User" : users[id - 1]})


# Create User route
@app.route("/create", methods = ["POST"])
def createUser():
    user_data = request.json
    users.append(user_data)
    return "Useradded"

# update User
@app.route("/update/<int:id>", methods = ["PUT"])
def updateById(id):

    for user in users:
        print(user["id"])
        if(user["id"] == id):
            
            user["name"] = "NewName"
            return "User Updated"
    return "No User found"

# Delete user
@app.route("/delete/<int:id>", methods = ["DELETE"])
def deleteById(id):
    for user in users:
        if(user["id"] == id):
            users.remove(user)
            return "User Deleted"
        else:
            return "User Not Found"




if __name__== "__main__":
    app.run(host = "localhost" , port = PORT, debug= True)