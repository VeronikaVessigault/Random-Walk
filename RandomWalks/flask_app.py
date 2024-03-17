from math import remainder
from flask import Flask, render_template, request, redirect, url_for
import walks
import sys
import vars
import os
import csv
 
app = Flask(__name__, static_url_path = "/upload", static_folder = "upload")
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

polyas_constants = ["100%","100%","34.0537%","19.3206%","13.5178%","10.4715%","8.58449%","7.29126%"]

def format_vectors_for_stats_temp(dim, ending_vecs):
    vectors = []
    each_line = (10-int(dim)//2)
    remainder = len(ending_vecs) % each_line
    for i in range(len(ending_vecs)//(each_line)):
        string = ""
        for j in range(each_line):
            string += str(ending_vecs[i*each_line+j]) + ", "
        vectors.append(string[:-2])
    last_entry = ""
    for i in range(remainder,0,-1):
        last_entry += str(ending_vecs[i*-1]) + ", "
    last_entry = last_entry[:-2]
    return vectors

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
        if "2" == str(dim) and int(steps)>199 and int(steps)<7501:
            #return redirect(url_for(".loading", steps=steps))
            walks.animate_2d(int(steps))
            return redirect('/visualization')
        elif not ("2" == str(dim)) and (int(steps)<199 or int(steps)>7501):
            return render_template("random_walk_viz.html", error_message = "error_message_dim_and_steps_viz.html", steps = steps, dim = dim)
        elif (int(steps)<199 or int(steps)>7501):
            return render_template("random_walk_viz.html", error_message = "error_message_steps_viz.html", steps = steps)
        elif not "2" == str(dim):
            return render_template("random_walk_viz.html", error_message = "error_message_dim_viz.html", dim = dim)
    else:
        return render_template("random_walk_viz.html", error_message = "empty.html")
    
#@app.route('/loading', methods=["GET", "POST"])
#def loading():
#    try:
#        steps = request.form.get("steps") 
#        print(steps)
#    except:
#        steps = -1
#        print(steps)
#        
#    if request.method == "POST":
#        if int(steps)>199 and int(steps)<15001:
#            walks.animate_2d(int(steps))
#            return redirect("/visualization")
#    return render_template("loading.html")


@app.route('/visualization', methods=["GET"])
def visualization():
    return render_template('visualization.html')

@app.route('/bulk-random-walk', methods =["GET", "POST"])
def bulk_random_walk():
    dim = -1
    steps = -1
    runs = -1
    if request.method == 'POST':
        dim = request.form['dim']
        steps = request.form['steps']
        runs = request.form['number of walks']

        #walks.set_valid_keys_by_steps()
        #walks.set_valid_keys_by_dimension()

        allowed_dim = [1,2,3,4,5,6,7,8]
        if int(dim) in allowed_dim and int(steps)>199 and int(steps)<15001 and int(runs) > 0 and int(runs) < 100001:
            if int(steps) < 7501 and int(steps) % 100 == 0:
                ending_vecs, how_many_rec = walks.many_walks(int(dim), int(steps), int(runs))
                #print(ending_vecs)
                percent_rec = str(round(how_many_rec/int(runs)*100,4)) + "%"
                vectors = format_vectors_for_stats_temp(dim, ending_vecs)
                return render_template('random_walk_bulk_w_stats.html', vectors = vectors, how_many_rec = how_many_rec, percent_rec = percent_rec, dim = dim, steps = steps, runs = runs, polyas = polyas_constants[int(dim)-1])
            elif int(steps) % 500 == 0:
                ending_vecs, how_many_rec = walks.many_walks(int(dim), int(steps), int(runs))
                percent_rec = str(round(how_many_rec/int(runs)*100,4)) + "%"
                vectors = format_vectors_for_stats_temp(dim, ending_vecs)
                return render_template('random_walk_bulk_w_stats.html', vectors = vectors, how_many_rec = how_many_rec, percent_rec = percent_rec, dim = dim, steps = steps, runs = runs, polyas = polyas_constants[int(dim)-1])
        else:    
            dim_right = False
            steps_right = False
            runs_right = False
            if int(dim) in allowed_dim:
                dim_right = True
            if (int(steps) > 199 and int(steps) < 7501 and int(steps) % 100 == 0) or (int(steps) > 7499 and int(steps) < 15001 and int(steps) % 500 == 0):
                steps_right = True
            if int(runs) > 0 and int(runs) < 25001:
                runs_right = True
            if not (dim_right or steps_right or runs_right):
                return render_template('random_walk_bulk.html', error_message = "error_message_dim_steps_runs.html", dim = dim, steps = steps, runs = runs)
            elif not (dim_right or steps_right):
                return render_template('random_walk_bulk.html', error_message = "error_message_dim_steps.html", dim = dim, steps = steps)
            elif not (dim_right or runs_right):
                return render_template('random_walk_bulk.html', error_message = "error_message_dim_runs.html", dim = dim, runs = runs)
            elif not (steps_right or runs_right):
                return render_template('random_walk_bulk.html', error_message = "error_message_steps_runs.html", steps = steps, runs = runs)
            elif not dim_right:
                return render_template('random_walk_bulk.html', error_message = "error_message_dim.html", dim = dim)
            elif not steps_right:
                return render_template('random_walk_bulk.html', error_message = "error_message_steps.html", steps = steps)
            elif not runs_right:
                return render_template('random_walk_bulk.html', error_message = "error_message_runs.html", runs = runs)
    return render_template('random_walk_bulk.html', error_message = "empty.html")

@app.route('/total-statistics')
def stats():
    #walks.set_valid_keys_by_steps()
    #walks.set_valid_keys_by_dimension()
    #walks.set_all_dim_to_zero()
    #walks.set_all_steps_dim_to_zero()
    dim_keys = walks.get_list_csv("valid_keys_by_dimension")
    dim_steps_keys = walks.get_list_csv("valid_keys_by_steps")
    percent_rec_dim_dict = walks.get_and_set_percent_recurrent_by_dimension()
    percent_rec_steps_dict = walks.get_and_set_percent_recurrent_by_steps()
    avg_mag_dim_dict = walks.get_dict_csv("average_magnitude_by_dimension")
    avg_mag_steps_dict = walks.get_dict_csv("average_magnitude_by_steps")
    tot_runs_dim_dict = walks.get_dict_csv("total_runs_by_dimension")
    tot_runs_steps_dict = walks.get_dict_csv("total_runs_by_steps")
    rec_runs_dim_dict = walks.get_dict_csv("total_recurrent_runs_by_dimension")
    rec_runs_steps_dict = walks.get_dict_csv("total_recurrent_runs_by_steps")

    steps_keys_by_dim = []
    for i in range(len(dim_keys)):
        steps_keys_by_dim.append(dim_steps_keys[i*89:(i+1)*89])

    return render_template('total_stats.html', dim_keys = dim_keys, dim_steps_keys = dim_steps_keys, percent_rec_dim_dict = percent_rec_dim_dict,
                           percent_rec_steps_dict = percent_rec_steps_dict, avg_mag_dim_dict = avg_mag_dim_dict, avg_mag_steps_dict = avg_mag_steps_dict,
                           tot_runs_dim_dict = tot_runs_dim_dict, tot_runs_steps_dict = tot_runs_steps_dict, rec_runs_dim_dict = rec_runs_dim_dict,
                           rec_runs_steps_dict = rec_runs_steps_dict, polyas = polyas_constants, steps_keys_by_dim = steps_keys_by_dim)
 
@app.route('/data/', methods = ['POST', 'GET'])
def data():
    if request.method == 'GET':
        return f"The URL /data is accessed directly. Try going to '/form' to submit form"
    if request.method == 'POST':
        form_data = request.form
        return render_template('data.html',form_data = form_data)
 
 
#app.run(host='localhost', port=5000)