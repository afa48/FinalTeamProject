import os

from typing import List, Dict
import simplejson as json
from flask import Flask, request, Response, redirect
from flask import render_template
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import logging
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


app = Flask(__name__)
mysql = MySQL(cursorclass=DictCursor)

app.config['MYSQL_DATABASE_HOST'] = 'db'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_DB'] = 'crashesData'
mysql.init_app(app)


@app.route('/', methods=['GET'])
def index():
    user = {'username': 'Number of Car Crashes in Catalonia from 2000 to 2011'}
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM crash_catalonia')
    result = cursor.fetchall()
    return render_template('index.html', title='Home', user=user, crashes=result)



@app.route('/view/<int:crash_id>', methods=['GET'])
def record_view(crash_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM crash_catalonia WHERE id=%s', crash_id)
    result = cursor.fetchall()
    return render_template('view.html', title='View Form', crash=result[0])

@app.route('/edit/<int:crash_id>', methods=['GET'])
def form_edit_get(crash_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM crash_catalonia WHERE id=%s', crash_id)
    result = cursor.fetchall()
    return render_template('edit.html', title='Edit Form', crash=result[0])


@app.route('/edit/<int:crash_id>', methods=['POST'])
def form_update_post(crash_id):
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('Day_of_Week'), request.form.get('Number_of_Crashes'), crash_id)
    sql_update_query = """UPDATE crash_catalonia t SET t.Day_of_Week = %s, Number_of_Crashes = %s, WHERE t.id = %s """
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)

@app.route('/crashes/new', methods=['GET'])
def form_insert_get():
    return render_template('new.html', title='New Crash Form')


@app.route('/crashes/new', methods=['POST'])
def form_insert_post():
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('Day_of_Week'), request.form.get('Number_of_Crashes'))
    sql_insert_query = """INSERT INTO crash_catalonia (Day_of_Week,Number_of_Crashes) VALUES (%s, %s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)

@app.route('/delete/<int:crash_id>', methods=['POST'])
def form_delete_post(crash_id):
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM crash_catalonia WHERE id = %s """
    cursor.execute(sql_delete_query, crash_id)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/api/v1/crashes', methods=['GET'])
def api_browse() -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM crash_catalonia')
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/crashes/<int:crash_id>', methods=['GET'])
def api_retrieve(crash_id) -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM crash_catalonia WHERE id=%s', crash_id)
    result = cursor.fetchall()
    json_result = json.dumps(result);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/crashes/<int:crash_id>', methods=['PUT'])
def api_edit(crash_id) -> str:
    cursor = mysql.get_db().cursor()
    content = request.json
    inputData = (content['Day_of_Week'], content['Number_of_Crashes'],crash_id)
    sql_update_query = """UPDATE crash_catalonia t SET t.Day_of_Week = %s, t.Number_of_Crashes =%s WHERE t.id = %s """
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    resp = Response(status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/crashes', methods=['POST'])
def api_add() -> str:

    content = request.json

    cursor = mysql.get_db().cursor()
    inputData = (content['Day_of_Week'], request.form.get('Number_of_Crashes'))
    sql_insert_query = """INSERT INTO crash_catalonia (Day_of_Week, Number_of_Crashes) VALUES (%s, %s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    resp = Response(status=201, mimetype='application/json')
    return resp


@app.route('/api/v1/crashes/<int:crash_id>', methods=['DELETE'])
def api_delete(crash_id) -> str:
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM crash_catalonia WHERE id = %s """
    cursor.execute(sql_delete_query, crash_id)
    mysql.get_db().commit()
    resp = Response(status=200, mimetype='application/json')
    return resp

@app.route('/view/chart', methods=['GET'])
def display_chart():
    return render_template('chart.html', title='Chart of Crashes')

@app.route('/view/chart1', methods=['GET'])
def display_chart1():
    return render_template('chart1.html', title='Chart')

@app.route('/api/chart', methods=['GET'])
def api_crashes_chart() -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('select Number_of_Crashes, count(*) as count from Day_of_Week')
    result = cursor.fetchall()
    json_result = json.dumps(result)
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp

@app.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html', title='Register Form')

@app.route('/api/login', methods=['POST'])
def api_login() -> str:
    email, password = request.form.get('email'), request.form.get('password')
    # Verify that email isn't already in database
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT email, password FROM user WHERE email=%s', email)
    result = cursor.fetchall()
    # if no account with that email return 403
    if len(result) == 0:
        return Response(json.dumps({'message': "Invalid email"}), status=403, mimetype='application/json')

    if result[0]['password'] != password:
        return Response(json.dumps({'message': "Invalid password"}), status=404, mimetype='application/json')

    return redirect('/', code=302)

@app.route('/register', methods=['GET'])
def register_page():
    return render_template('register.html', title='Register Form')

@app.route('/api/register', methods=['POST'])
def api_register() -> str:
    email, password = request.form.get('email').strip(), request.form.get('password').strip()

    # Verify that email isn't already in database
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT COUNT(*) as ct FROM user WHERE email=%s', email)
    result = cursor.fetchall()
    if result[0]['ct'] != 0:
        return Response(json.dumps({message: "Email already registered"}), status=404, mimetype='application/json')
    #Add user to database
    sql_insert_query = """INSERT INTO user (email,password) VALUES (%s, %s) """
    cursor.execute(sql_insert_query, (email, password))
    mysql.get_db().commit()

    message = Mail(
        from_email='afa48@njit.edu',
        to_emails=email,
        subject='Email Verification',
        html_content=f'<strong>Hi {email}</strong>')
    try:
        # hardcoding for now, but please put somewhere safe
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API'))
        response = sg.send(message)
        logger.info('Sendgrid', response)
        return redirect("/", code=302)
    except Exception as e:
        logger.error('Sendgrid Error', e)
        return Response(json.dumps({'message': e.message}), status=404, mimetype='application/json')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)