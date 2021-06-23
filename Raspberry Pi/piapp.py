from flask import Flask, render_template, jsonify, request, make_response, redirect
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests
from time import strftime
import datetime

app = Flask(__name__)

scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
credential = ServiceAccountCredentials.from_json_keyfile_name('##########.json', scope)
client = gspread.authorize(credential)
dht_sheet = client.open("########").sheet1
bme_sheet = client.open("########"").get_worksheet(1)

posts = [
    {
        'author': 'Corey Shafer',
        'title': 'Blog Post 1',
        'content': 'First post content',
        'date_posted': 'April 20, 2020'
    },
    {
        'author': 'Jane Doe',
        'title': 'Blog Post 2',
        'content': 'Second post content',
        'date_posted': 'April 21, 2020'
    }
]

index_package = {'username' : ' ', 'email' : ' ', 'password' : ' ', 'ledRadio1' : ' ', 'tivaLED' : ' '}

dht_package = {'name' : ' ', 'message' : ' '}
bme_package = {'name' : ' '}

@app.route('/')
def hello_world():
    return 'Hello! Welcome to House Mamba!'

@app.route('/home')
def home_page():
    return render_template('home.html', posts=posts)

@app.route('/about')
def about_page():
    return render_template('about.html', title='About')

@app.route('/jsonpackage')
def json_package():
    json_package = {}
    json_package['name'] = 'Myles'
    json_package['email'] = 'myles.pedronan@gmail.com'
    json_package['index'] = 1
    json_package['status'] = 'pinOn(1)'

    return jsonify({'House' : json_package}), 200

@app.route('/index', methods=['GET'])
def index_page():
    return jsonify({'index' : index_package, 'dht' : dht_package, 'bme' : bme_package})

@app.route('/json', methods=["GET", "POST"])
def json_page():
    if request.method == "POST":
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        ledRadio1 = request.form['ledRadio1']
        tivaLED = request.form['tivaLED']

        entry = {}
        entry['username'] = username
        entry['email'] = email
        entry['password'] = password
        entry['ledRadio1'] = ledRadio1
        entry['tivaLED'] = tivaLED

        index_package.update(entry)

        return redirect(request.url)

    return render_template('json.html', title='JSON')

@app.route('/dht')
def dht():
    return render_template('dht.html')

@app.route('/dht/create', methods=["POST"])
def dht_read():
    req = request.get_json(force=True)

    print(req)
    dht_package.update(req)

    res = make_response(jsonify(req), 200)

    print(res)

    return res

@app.route('/dht/data', methods=["POST"])
def dht_data():
    req = request.get_json()
    date = datetime.datetime.now().strftime('%m/%d/%Y')
    time = datetime.datetime.now().strftime('%I:%M:%S')
    tempc = req['tempc']
    tempf = req['tempf']
    hum = req['hum']

    if not tempc or not tempf or not hum:
        return jsonify({'message' : 'Bad Values'}), 400

    row = [date, time, tempc, tempf, hum]
    dht_sheet.append_row(row)

    return jsonify({'message' : 'success'}), 200

@app.route('/bme')
def bme():
    return render_template('bme.html')

@app.route('/bme/create', methods=["POST"])
def bme_read():
    req = request.get_json(force=True)

    print(req)
    bme_package.update(req)

    res = make_response(jsonify(req), 200)

    print(res)

    return res

@app.route('/bme/data', methods=["POST"])
def bme_data():
    req = request.get_json()
    date = datetime.datetime.now().strftime('%m/%d/%Y')
    time = datetime.datetime.now().strftime('%I:%M:%S')
    tempc = req['tempc']
    tempf = req['tempf']
    pres = req['pres']
    hum = req['hum']
    sealevel = req['sealevel']
    altitude = req['altitude']
    dewpoint = req['dewpoint']

    if not tempc or not tempf or not pres or not hum or not sealevel or not altitude or not dewpoint:
        return jsonify({'message' : 'Bad Values'}), 400

    row = [date, time, tempc, tempf, pres, hum, sealevel, altitude, dewpoint]
    bme_sheet.append_row(row)

    return jsonify({'message' : 'success'}), 200

if __name__ == '__main__':
    app.run(debug=True)
