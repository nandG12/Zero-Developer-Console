import os
import datetime
import shutil
import csv
import pandas as pd
from purge import *
from functools import wraps
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
from flask import Flask
from flask import Flask,jsonify,json
from flask import Flask, render_template, flash, request, redirect, url_for, session, logging

#Upload File Location
UPLOAD_FOLDER = 'D:\Projects\Test_Upload_Files'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'xml'}

app = Flask(__name__)
app.debug = True
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


#Check if user logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, Please login', 'danger')
            return redirect(url_for('login'))
    return wrap

#Home Page
@app.route('/')
def index():
    return render_template('home.html')

#History Page
@app.route('/history')
def history():
    with open('history.csv', 'r', newline='') as file:
        writer = csv.reader(file)
        first_line = True
        data = []
        for row in writer:
            if not first_line:
                data.append({
                "user": row[0],
                "filename": row[1],
                "location": row[2],
                "date": row[3]
                })
            else:
                first_line = False
    return render_template('history.html', data=data)

#For Purge
@app.route('/purge', methods=['GET','POST'])
@is_logged_in
def purge():
    if request.method == 'POST':
        text = request.form['url']
        #Purge.py File Function Called
        op = purgeFunTest(text)
        flash(op, 'primary')
        return render_template('dashboard.html') 
    return render_template('purge.html') 

#User Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        #Get Form Field
        username = request.form['username']
        password_candidate = request.form['password']
        with open('credential.csv', 'r', newline='') as file:
            writer = csv.reader(file)
            first_line = True
            for row in writer:
                if not first_line:
                    if row[0] == username:
                        if  row[1] == password_candidate:
                            session['name'] = username   
                            session['logged_in'] = True                 
                            flash('You are now Logged in', 'primary')
                            return redirect(url_for('dashboard'))
                        else:
                            error = 'Incorrect Password'
                            return render_template('login.html', error=error)
                else:
                    first_line = False

    return render_template('login.html')

#User Dashboard
@app.route('/dashboard')
@is_logged_in
def dashboard():
    return render_template('dashboard.html')

#Logout
@app.route('/logout')
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('login'))

#Upload File
@app.route('/upload', methods=['GET', 'POST'])
@is_logged_in
def upload_file(): 
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part','warning')
            return redirect(request.url)
        file = request.files['file']

        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No File Selected, Please select file', 'warning')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            #Search for Backup file on below path
            search_path = r'D:/Back_27_April'
            #find_files(request.files['file'],location)
            result = []
            # Wlaking top-down from the root
            #print("File is thissss" ,filename)
            today = datetime.datetime.now()
            year = today.strftime("%Y")
            month=today.strftime("%m")
            day=today.strftime("%d")
            hour=today.strftime("%H")
            minute=today.strftime("%M")
            second=today.strftime("%S")
            output = year +"-" + month + "-" + day + "-" + hour + "-" + minute + "-" + second + "/"  
            #print("Date is ", output)
            # Running One
            targetTemp = '//AAA/AAAAAAAAA/NNNNNNN/Project/user/'
            #For User Change
            target = os.path.join(targetTemp,session['name'])
            mydir = os.path.join(target, datetime.datetime.now().strftime('%d%B_%I-%M-%S-%p'))
            os.makedirs(mydir)
            shutil.copyfile(os.path.join(app.config['UPLOAD_FOLDER'],filename),os.path.join(mydir,filename))
            for root, dir, files in os.walk(search_path):
                if filename in files:
                    result.append(os.path.join(root,filename))
                    ftar = mydir + "/" + "Backup - " + filename
                    #List of different server name
                    env = ["",""]
                    for i in range(len(env)):
                        var = env[i]
                        final = var + result[0]
                    #When on Server put this in for loop
                    shutil.copyfile(result[0],ftar)

            #To Update the CSV File with new file updated
            with open('history.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([session['name'], filename, final, output])
            #Flash Message
            fmessage = filename + " Uploaded Successfully"
            flash(fmessage, 'success')
            return render_template('upload.html')

    return render_template('upload.html')


if __name__ == '__main__':
        global x 
        app.secret_key='secret123'
        app.run()
        