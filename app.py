from flask import Flask, jsonify, request
import db

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

@app.route("/setup")

def setup():
    try:
        db.cursor.execute("CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY,name VARCHAR(100), age VARCHAR(50));")
        db.conn.commit()
        
        return "Table 'users' created successfully", 200
        

        
    except db.pg.Error as e:
        return f"An error occured : {e}"


# All Users
@app.route("/users", methods = ["GET"])
def get():

    try:

        db.cursor.execute("SELECT * FROM users;")

        data = db.cursor.fetchall()
        


        result  = [{"id" : row[0], "name" : row[1], "age" : row[2]} for row in data]

        return jsonify(result)

    except db.pg.Error as e:

        return jsonify({"Error : " , str(e)})
        





# Get by id
@app.route('/users/<int:id>')
def getById(id):
    return jsonify({"User" : users[id - 1]})


# Create User route
@app.route("/create", methods = ["POST"])
def createUser():

    try:
        data = request.json
        name =data.get("name")
        age = data.get("age")
        
        db.cursor.execute("INSERT INTO users (name, age) VALUES (%s, %s);", (name, age))
        db.conn.commit()

        return jsonify({"message" : "User added"})
    
    except db.pg.Error as e:

        db.conn.rollback()
        return jsonify({"Error occured" : str(e)})

    

# update User
@app.route("/update/<int:id>", methods = ["PUT"])
def updateById(id):
    try:

        user_data = request.json
        id_str = str(id)

        update_field = []
        query_params = []

        if 'age' in user_data:
            query_params.append(user_data['age'])
            update_field.append("age = %s")
        if "name" in user_data:
            query_params.append(user_data['name'])
            update_field.append("name = %s")

        if not update_field:
            return "No data Given"
        
        update_fields_str = ", ".join(update_field)
        
        db.cursor.execute(f"Update users SET {update_fields_str} WHERE id = %s", (query_params + [id_str]))

        db.conn.commit()

        return "User Updated"

    except db.pg.Error as e:

        db.conn.rollback();
        return jsonify({"Error" : str(e)})
# Delete user
@app.route("/delete/<int:id>", methods = ["DELETE"])
def deleteById(id):
    try:
        id_str = str(id)
        db.cursor.execute("DELETE FROM users WHERE id = %s;",(id_str))
        db.conn.commit()

        return jsonify({"message" : "DELETED"})
    
    except db.pg.Error as e:

        db.conn.rollback()
        return jsonify({"Error" : e})




if __name__== "__main__":
    app.run(host = "localhost" , port = PORT, debug= True)