from flask import Flask, render_template, request, redirect, url_for
from celery import Celery
import walks
import sys
import vars
import os
import csv


from matplotlib import pyplot as plt
from matplotlib import animation
import matplotlib
matplotlib.use('agg') 
 
app = Flask(__name__, static_url_path = "/upload", static_folder = "upload")
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'

global celery
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])



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
            animate_2d.apply_async(args=[int(steps)])
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
    

@celery.task
def animate_2d(steps):
    dimension = 2

    x = []
    y = []

    valid_keys_by_steps = walks.get_list_csv("valid_keys_by_steps")
    valid_keys_by_dimension = walks.get_list_csv("valid_keys_by_dimension")

    if (dimension, steps) in valid_keys_by_steps:
        total_runs_one, total_recurrent_runs_one, new_magnitude, animation_steps = walks.run_walk(dimension, steps, animated = True)


        average_magnitude_by_dimension = walks.get_dict_csv("average_magnitude_by_dimension")
        total_runs_by_dimension = walks.get_dict_csv("total_runs_by_dimension")
        try:
            old_avg_mag_by_dim = float(average_magnitude_by_dimension[str(dimension)])*float(total_runs_by_dimension[str(dimension)])
        except KeyError:
            average_magnitude_by_dimension[str(dimension)] = 0
            total_runs_by_dimension[str(dimension)] = 0
            old_avg_mag_by_dim = 0
        total_runs_by_dimension[str(dimension)] = float(total_runs_by_dimension[str(dimension)]) + total_runs_one
        walks.set_dict_csv("total_runs_by_dimension", total_runs_by_dimension)
        total_recurrent_runs_by_dimension = walks.get_dict_csv("total_recurrent_runs_by_dimension")
        try:
            total_recurrent_runs_by_dimension[str(dimension)] = float(total_recurrent_runs_by_dimension[str(dimension)]) + total_recurrent_runs_one
        except KeyError:
            total_recurrent_runs_by_dimension[str(dimension)] = 0
            total_recurrent_runs_by_dimension[str(dimension)] = float(total_recurrent_runs_by_dimension[str(dimension)]) + total_recurrent_runs_one
        walks.set_dict_csv("total_recurrent_runs_by_dimension", total_recurrent_runs_by_dimension)
        average_magnitude_by_dimension[str(dimension)] = (old_avg_mag_by_dim+new_magnitude)/total_runs_by_dimension[str(dimension)]
        walks.set_dict_csv("average_magnitude_by_dimension", average_magnitude_by_dimension)


        average_magnitude_by_steps = walks.get_dict_csv("average_magnitude_by_steps")
        total_runs_by_steps = walks.get_dict_csv("total_runs_by_steps")
        try:
            old_avg_mag_by_dim = float(average_magnitude_by_steps[str((dimension, steps))])*float(total_runs_by_steps[str((dimension, steps))])
        except KeyError:
            average_magnitude_by_steps[str((dimension, steps))] = 0
            total_runs_by_steps[str((dimension, steps))] = 0
            old_avg_mag_by_dim = 0
        total_runs_by_steps[str((dimension, steps))] = float(total_runs_by_steps[str((dimension, steps))]) + total_runs_one
        walks.set_dict_csv("total_runs_by_steps", total_runs_by_steps)
        total_recurrent_runs_by_steps = walks.set_dict_csv("total_recurrent_runs_by_steps")
        try:
            total_recurrent_runs_by_steps[str((dimension, steps))] = float(total_recurrent_runs_by_steps[str((dimension, steps))]) + total_recurrent_runs_one
        except KeyError:
            total_recurrent_runs_by_steps[str((dimension, steps))] = 0
            total_recurrent_runs_by_steps[str((dimension, steps))] += total_recurrent_runs_one
        walks.set_dict_csv("total_recurrent_runs_by_steps", total_recurrent_runs_by_steps)
        average_magnitude_by_steps[str((dimension, steps))] = (old_avg_mag_by_dim+new_magnitude)/total_runs_by_steps[str((dimension, steps))]
        walks.set_dict_csv("average_magnitude_by_steps", average_magnitude_by_steps)

        
        for element in animation_steps:
            x.append(element[0])
            y.append(element[1])

        fig, ax = plt.subplots(figsize=(4, 3), dpi=880/4)

        if total_recurrent_runs_one:
            line, = ax.plot(x, y, color='g')
        elif not total_recurrent_runs_one:
            line, = ax.plot(x, y, color='r')

        plt.axhline(0, color='grey', alpha = 0.25, dashes = [0,0,1])
        plt.axvline(0, color='grey', alpha = 0.25, dashes = [0,0,1])
        plt.title("{} steps in {}-D Random Walk".format(steps, 2))

        def update(num, x, y, line):
            line.set_data(x[:num], y[:num])
            line.axes.axis([min(x)-5, max(x)+5, min(y)-5, max(y)+5])
            return line,

        ani = animation.FuncAnimation(fig, update, len(x), fargs=[x, y, line],
                                      interval=25, blit=False)
        ani.save('upload/new_walk.gif')

        if os.path.isfile("upload/new_walk.gif"):
            #if os.path.isfile("upload/walk10.gif"):
            #    os.remove("upload/walk10.gif")
            if os.path.isfile("upload/walk9.gif"):
                os.rename("upload/walk9.gif", "upload/walk10.gif")
            if os.path.isfile("upload/walk8.gif"):
                os.rename("upload/walk8.gif", "upload/walk9.gif")
            if os.path.isfile("upload/walk7.gif"):
                os.rename("upload/walk7.gif", "upload/walk8.gif")
            if os.path.isfile("upload/walk6.gif"):
                os.rename("upload/walk6.gif", "upload/walk7.gif")
            if os.path.isfile("upload/walk5.gif"):
                os.rename("upload/walk5.gif", "upload/walk6.gif")
            if os.path.isfile("upload/walk4.gif"):
                os.rename("upload/walk4.gif", "upload/walk5.gif")
            if os.path.isfile("upload/walk3.gif"):
                os.rename("upload/walk3.gif", "upload/walk4.gif")
            if os.path.isfile("upload/walk2.gif"):
                os.rename("upload/walk2.gif", "upload/walk3.gif")
            if os.path.isfile("upload/walk1.gif"):
                os.rename("upload/walk1.gif", "upload/walk2.gif")
            if os.path.isfile("upload/walk0.gif"):
                os.rename("upload/walk0.gif", "upload/walk1.gif")
            os.rename("upload/new_walk.gif", "upload/walk0.gif")
        else:
            print("animation not createdwtf")
        #plt.show()
            
    elif dimension in valid_keys_by_dimension:
        print("valid dim key")
        total_runs_one, total_recurrent_runs_one, new_magnitude, animation_steps = walks.run_walk(dimension, steps, animated = True)


        average_magnitude_by_dimension = walks.get_dict_csv("average_magnitude_by_dimension")
        total_runs_by_dimension = walks.get_dict_csv("total_runs_by_dimension")
        try:
            old_avg_mag_by_dim = average_magnitude_by_dimension[dimension]*total_runs_by_dimension[dimension]
        except KeyError:
            average_magnitude_by_dimension[dimension] = 0
            total_runs_by_dimension[dimension] = 0
            old_avg_mag_by_dim = 0
        total_runs_by_dimension[dimension] += total_runs_one
        walks.set_dict_csv("total_runs_by_dimension", total_runs_by_dimension)
        total_recurrent_runs_by_dimension = walks.get_dict_csv("total_recurrent_runs_by_dimension")
        try:
            total_recurrent_runs_by_dimension[dimension] += total_recurrent_runs_one
        except KeyError:
            total_recurrent_runs_by_dimension[dimension] = 0
            total_recurrent_runs_by_dimension[dimension] += total_recurrent_runs_one
        walks.set_dict_csv("total_recurrent_runs_by_dimension", total_recurrent_runs_by_dimension)
        average_magnitude_by_dimension[dimension] = (old_avg_mag_by_dim+new_magnitude)/total_runs_by_dimension[dimension]
        walks.set_dict_csv("average_magnitude_by_dimension", average_magnitude_by_dimension)
        
        for element in animation_steps:
            x.append(element[0])
            y.append(element[1])

        fig, ax = plt.subplots(figsize=(4, 3), dpi=880/4)

        if total_recurrent_runs_one:
            line, = ax.plot(x, y, color='g')
        elif not total_recurrent_runs_one:
            line, = ax.plot(x, y, color='r')

        plt.axhline(0, color='grey', alpha = 0.25, dashes = [0,0,1])
        plt.axvline(0, color='grey', alpha = 0.25, dashes = [0,0,1])
        plt.title("{} steps in {}-D Random Walk".format(steps, 2))

        def update(num, x, y, line):
            line.set_data(x[:num], y[:num])
            line.axes.axis([min(x)-5, max(x)+5, min(y)-5, max(y)+5])
            return line,

        ani = animation.FuncAnimation(fig, update, len(x), fargs=[x, y, line],
                                      interval=25, blit=False)
        ani.save('upload/new_walk.gif')

        if os.path.isfile("upload/new_walk.gif"):
            #if os.path.isfile("upload/walk10.gif"):
            #    os.remove("upload/walk10.gif")
            if os.path.isfile("upload/walk9.gif"):
                os.rename("upload/walk9.gif", "upload/walk10.gif")
            if os.path.isfile("upload/walk8.gif"):
                os.rename("upload/walk8.gif", "upload/walk9.gif")
            if os.path.isfile("upload/walk7.gif"):
                os.rename("upload/walk7.gif", "upload/walk8.gif")
            if os.path.isfile("upload/walk6.gif"):
                os.rename("upload/walk6.gif", "upload/walk7.gif")
            if os.path.isfile("upload/walk5.gif"):
                os.rename("upload/walk5.gif", "upload/walk6.gif")
            if os.path.isfile("upload/walk4.gif"):
                os.rename("upload/walk4.gif", "upload/walk5.gif")
            if os.path.isfile("upload/walk3.gif"):
                os.rename("upload/walk3.gif", "upload/walk4.gif")
            if os.path.isfile("upload/walk2.gif"):
                os.rename("upload/walk2.gif", "upload/walk3.gif")
            if os.path.isfile("upload/walk1.gif"):
                os.rename("upload/walk1.gif", "upload/walk2.gif")
            if os.path.isfile("upload/walk0.gif"):
                os.rename("upload/walk0.gif", "upload/walk1.gif")
            os.rename("upload/new_walk.gif", "upload/walk0.gif")
        else:
            print("animation not createdwtf")
        #plt.show()