from flask import Flask, redirect, url_for, render_template
from flask import request
from flask import session
from flask import jsonify
import mysql.connector

app = Flask(__name__)
app.secret_key = '123'


def interact_db(query, query_type: str):
    return_value = False
    connection = mysql.connector.connect(host='localhost',
                                         user='root',
                                         passwd='root',
                                         database='myflaskappdb')
    cursor = connection.cursor(named_tuple=True)
    cursor.execute(query)

    if query_type == 'commit':
        # Use for INSERT UPDATE, DELETE statements.
        # Returns: The number of rows affected by the query (a non-negative int).
        connection.commit()
        return_value = True

    if query_type == 'fetch':
        # Use for SELECT statement.
        # Returns: False if the query failed, or the result of the query if it succeeded.
        query_result = cursor.fetchall()
        return_value = query_result

    connection.close()
    cursor.close()
    return return_value

# ------------------------------------------------- #
# ------------------------------------------------- #


@app.route('/get_user', defaults={'user_id': 15, 'product_name': 'table'})
@app.route('/get_user/<user_id>/product/<product_name>', methods=['GET', "POST"])
def get_user(user_id, product_name):
    if request.method == "GET":
        # get from DB
        query = "SELECT * FROM users WHERE id='%s';" % user_id
        query_result = interact_db(query=query, query_type='fetch')
        if len(query_result) == 0:
            return jsonify({
                'success': 'False',
                "data": []
            })
        else:
            return jsonify({
                'success': 'True',
                'data': query_result[0],
                'product_name': product_name
            })
    if request.method == "POST":
        return f'The method is: {request.method}'


@app.route('/get_user_info')
def get_user_info():
    # checking
    print('Checking')
    user_id = request.args['user_id']
    product_name = request.args['product_name']
    return redirect(url_for('get_user', user_id=user_id, product_name=product_name))

# @app.route('/product', defaults={'sku': None})
# @app.route('/product/<float:sku>')
# def get_product(sku=None):
#     if sku:
#         return jsonify({
#             'success': True,
#             'sku': sku,
#             'product_data': 'component'
#         })
#     return jsonify({
#         'success': False,
#     })
#     # return f'SKU is: {sku} and the component is {component}'
#
#
# @app.route('/get_product/<float:sku>')
# def prepare_to_get_product(sku):
#     # some checks
#     return redirect(url_for('get_product', sku=sku, component='handle'))
# ------------------------------------------------- #
# ------------------------------------------------- #


@app.route('/users')
def users():
    query = "select * from users"
    query_result = interact_db(query=query, query_type='fetch')
    print(query_result)
    return render_template('users.html', users=query_result)

# ------------------------------------------------- #
# ------------------------------------------------- #

# @app.route('/users')
# def users():
#     query = "select * from users"
#     query_result = interact_db(query, 'fetch')
#     return render_template('users.html', users=query_result)


# ------------------------------------------------- #
# ------------------------------------------------- #

@app.route('/insert_user', methods=['GET', 'POST'])
def insert_user():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        query = "INSERT INTO users(name, email, password) VALUES ('%s', '%s', '%s')" % (name, email, password)
        interact_db(query=query, query_type='commit')
        return redirect('/users')
    return render_template('insert-user.html', req_method=request.method)

# ------------------------------------------------- #
# ------------------------------------------------- #

# @app.route('/insert_user', methods=['GET', 'POST'])
# def insert_user():
#     if request.method == 'POST':
#         name = request.form['name']
#         email = request.form['email']
#         password = request.form['password']
#         query = "INSERT INTO users(name, email, password) VALUES ('%s', '%s', '%s')" % (name, email, password)
#         interact_db(query, query_type='commit')
#         return redirect('/users')
#     return render_template('insert-user.html', req_method=request.method)

# @app.route('/insert_user', methods=['GET', 'POST'])
# def insert_user():
#     if request.method == 'POST':
#         name = request.form['name']
#         email = request.form['email']
#         password = request.form['password']
#         query = "INSERT INTO users(name, email, password) VALUES('%s','%s','%s');" % (name,email,password)
#         interact_db(query, 'commit')
#         return redirect(url_for('users'))
#     return render_template('insert-user.html')

# ------------------------------------------------- #
# ------------------------------------------------- #


@app.route('/delete_user', methods=['GET', 'POST'])
def delete_user():
    if request.method == 'GET':
        user_id = request.args['id']
        query = "DELETE FROM users WHERE id='%s';" % user_id
        interact_db(query=query, query_type='commit')
        # return f'user {user_id} deleted'
        return redirect('/users')
    return 'deleted user'


# ------------------------------------------------- #
# ------------------------------------------------- #

# @app.route('/delete_user', methods=['GET', 'POST'])
# def delete_user():
#     if request.method == 'GET':
#         user_id = request.args['id']
#         query = "DELETE FROM users WHERE id='%s';" % user_id
#         interact_db(query, query_type='commit')
#         return f'user {user_id} is deleted from db'
#     return redirect('/users')

# @app.route('/delete_user')
# def delete_user():
#     if request.method == 'GET':
#         user_id = request.args['id']
#         query = "DELETE FROM users WHERE id='%s';" % user_id
#         interact_db(query, 'commit')
#     return redirect('/users')

# cur.execute("DELETE FROM articles WHERE id=%s", [id])
# cur.execute("UPDATE articles SET title=%s, body=%s WHERE id=%s", (title, body, id))
# cur.execute("SELECT * FROM articles WHERE id=%s", [id])
# cur.execute("INSERT INTO articles(title, body, author) VALUES(%s, %s, %s)", (title, body, session['username']))
# result = cur.execute("SELECT * FROM articles")
# result = cur.execute('SELECT * FROM users WHERE username=%s', [username])
# cur.execute("INSERT INTO users(name, email, username, password) VALUES(%s,%s,%s,%s)", (name,email,username,password))
# result = cur.execute("SELECT * FROM articles WHERE id=%s", (id))


@app.route('/example', methods=['GET', 'POST'])
def example_func():
    username = ''
    second_name = ''

    if request.method == 'POST':
        # check in DB of the website

        username = request.form['username']
        session['logged_in'] = True
        session['username'] = username

    if request.method == 'GET':
        if 'second_name' in request.args:
            second_name = request.args['second_name']

    return render_template('example.html',
                           request_method=request.method,
                           username=username,
                           second_name=second_name)


@app.route('/catalog')
def catalog_func():
    if 'id' in request.args:
        curr_id = request.args['id']
        name = request.args['name']
        return f'Username: {name}, The id of product: {curr_id}'
    return 'in Catalog'


@app.route('/about')
def about_func():
    # get the name of the user
    if 'name' in request.args:
        name = request.args['name']
        return render_template('about.html', name=name)
    return render_template('about.html')


@app.route('/user')
def user_func():
    # get the name of the user
    user_from_DB = {'firstname': 'Ariel', 'lastname': 'Perchik',
                    'gender': 'boy'}
    return render_template('user.html', user=user_from_DB,
                           hobbies=['Prog', 'Paint', 'Teaching'],
                           degrees=('B.Sc', 'M.Sc')
                           )


@app.route('/home')
def home_func():
    # calculations
    # extraction from DB
    user_from_DB = {'firstname': 'Ariel', 'lastname': 'Perchik',
                    'gender': 'boy'}
    # user_from_DB = ''
    return render_template('home2.html',
                           user=user_from_DB,
                           hobbies=['Prog', 'Paint', 'Teaching'],
                           degrees=('B.Sc', 'M.Sc')
                           )



# @app.route('/home')
# def home_func():
    # get the name of the user
    # username = {"firstname": "Ariel", "lastname": "Perchik", "gender": "b"}
    # username = None
    # return 'Hello Home!'
    # return render_template('home.html',
    #                        username=username,
    #                        hobbies=["Prog", "Paint", "Football"],
    #                        degrees=('B.Sc', 'M.Sc'))


@app.route('/foo')
def foo_func():
    return "hello foo"


@app.route('/products', methods=['GET', 'POST', 'DELETE'])
def get_products():
    logged_in = True
    if logged_in:
        # return redirect('/about')
        return redirect(url_for('about_func'))
    else:
        return "Not logged in"


@app.route('/')
def index_func():
    # you get the name
    username = 'Ariel'
    return render_template('index2.html', name=username,
                           s_name="PerChiK")


if __name__ == '__main__':
    app.run(debug=True)
