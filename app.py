from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="users"
)

@app.route("/")
def Index():
    string = "Hello World!"
    return render_template("hello.html", data = string )

@app.route('/users')
def users():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users")
    users_data = cursor.fetchall()
    return render_template('users.html', users=users_data)


@app.route('/new_user', methods=['GET', 'POST'])
def new_user():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']

        cursor = db.cursor()
        query = "INSERT INTO users (name, email) VALUES (%s, %s)"
        values = (name, email)
        cursor.execute(query, values)
        db.commit()
        return "User added successfully!"
    return render_template('new_user.html')


#@app.route('/users/<int:user_id>')
#def user_details(id):
    cursor = db.cursor()
    query = "SELECT * FROM users WHERE id = %s"
    values = (id,)
    cursor.execute(query, values)
    user_data = cursor.fetchone()
    if user_data:
        return render_template('user_details.html', user=user_data)
    else:
        return "User not found"
    
#@app.route('/user_info', methods=['GET', 'POST'])
#def user_info():
    if request.method == 'POST':
        user_id = int(request.form.get('user_id'))
        if user_id in users:
            user = users[user_id]
            return render_template('user_info.html', user=user)
        else:
            return "User not found"
    return render_template('user_info.html', user=None)
    
    # Route for the user_info page
@app.route('/user_info', methods=['GET'])
def user_info():
    return render_template('user_info.html')

# Route for getting user information
@app.route('/get_user_info', methods=['POST'])
def get_user_info():
    # Retrieve the entered ID from the form data
    user_id = int(request.form.get('userId'))

    # Perform a database query to fetch user information
    cursor = db.cursor()
    query = "SELECT id, name, email FROM users WHERE id = %s"
    values = (user_id,)
    cursor.execute(query, values)
    user_data = cursor.fetchone()

    # Render the user_info template with the retrieved user information
    if user_data:
        user = {
            'id': user_data[0],
            'name': user_data[1],
            'email': user_data[2]
        }
        return render_template('user_info.html', user=user)
    else:
        return render_template('user_info.html', not_found=True)



@app.errorhandler(404)
def not_found_error(error):
    return "404 Not Found"


if __name__ == '__main__':
    app.run(debug=True)
