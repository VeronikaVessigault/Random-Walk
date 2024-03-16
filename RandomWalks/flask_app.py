from flask import Flask, render_template, request, redirect, url_for
import walks
import sys
import vars
import os
import csv
 
app = Flask(__name__, static_url_path = "/upload", static_folder = "upload")
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0



@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


@app.route('/')
def home():
    return render_template("home.html")
 
#@app.route('/random-walk-visualization')
#def random_walk_viz():
#    return render_template('random_walk_viz.html')

@app.route('/random-walk-visualization', methods=['POST', "GET"])
def visual_para():
    dim = -1
    steps = -1
    if request.method == 'POST':
        dim = request.form['dim']
        steps = request.form['steps']
        if "2" == str(dim) and int(steps)>199 and int(steps)<15001:
            return redirect(url_for(".loading", steps=steps))
            walks.animate_2d(int(steps))
            return redirect('/visualization')
        elif not ("2" == str(dim)) and (int(steps)<199 or int(steps)>15001):
            return render_template("random_walk_viz.html", error_message = "error_message_dim_and_steps_viz.html", steps = steps, dim = dim)
        elif (int(steps)<199 or int(steps)>15001):
            return render_template("random_walk_viz.html", error_message = "error_message_steps_viz.html", steps = steps)
        elif not "2" == str(dim):
            return render_template("random_walk_viz.html", error_message = "error_message_dim_viz.html", dim = dim)
    else:
        return render_template("random_walk_viz.html", error_message = "empty.html")
    
@app.route('/loading', methods=["GET"])
def loading():
    try:
        steps = request.args.get("steps") 
    except:
        steps = -1
        
    if request.method == "GET":
        if int(steps)>199 and int(steps)<15001:
            walks.animate_2d(int(steps))
            return redirect("/visualization")
    return render_template("loading.html")


@app.route('/visualization', methods=["GET"])
def visualization():
    return render_template('visualization.html')

@app.route('/bulk-random-walk', methods =["GET", "POST"])
def bulk_random_walk():
    return render_template('random_walk_bulk.html')

@app.route('/total-statistics')
def stats():
    return render_template('total_stats.html')
 
@app.route('/data/', methods = ['POST', 'GET'])
def data():
    if request.method == 'GET':
        return f"The URL /data is accessed directly. Try going to '/form' to submit form"
    if request.method == 'POST':
        form_data = request.form
        return render_template('data.html',form_data = form_data)
 
 
#app.run(host='localhost', port=5000)