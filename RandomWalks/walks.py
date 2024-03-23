from random import SystemRandom

cryto_gen_num = SystemRandom()

import os
import csv

from matplotlib import pyplot as plt
from matplotlib import animation
import matplotlib
matplotlib.use('agg')  

import vars


# keeping for easy copy paste if needed
def add_stats(valid_keys_by_steps = False, valid_keys_by_dimension = False, total_runs_by_steps = False,
              total_recurrent_runs_by_steps = False, average_magnitude_by_steps = False, total_runs_by_dimension = False,
              total_recurrent_runs_by_dimension = False, average_magnitude_by_dimension = False, percent_recurrent = False):
    print("oops")

def set_all_steps_dim_to_zero():
    valid_keys = get_list_csv("valid_keys_by_steps")
    avg_mag_dict = dict()
    total_runs_dict = dict()
    rec_runs_dict = dict()
    for key in valid_keys:
        avg_mag_dict[key] = 0
        total_runs_dict[key] = 0 
        rec_runs_dict[key] = 0
    set_dict_csv("average_magnitude_by_steps", avg_mag_dict)
    set_dict_csv("total_runs_by_steps", total_runs_dict)
    set_dict_csv("total_recurrent_runs_by_steps", rec_runs_dict)

def set_all_dim_to_zero():
    valid_keys = get_list_csv("valid_keys_by_dimension")
    avg_mag_dict = dict()
    total_runs_dict = dict()
    rec_runs_dict = dict()
    for key in valid_keys:
        avg_mag_dict[key] = 0
        total_runs_dict[key] = 0 
        rec_runs_dict[key] = 0
    set_dict_csv("average_magnitude_by_dimension", avg_mag_dict)
    set_dict_csv("total_runs_by_dimension", total_runs_dict)
    set_dict_csv("total_recurrent_runs_by_dimension", rec_runs_dict)

def get_and_set_percent_recurrent_by_dimension():
    file_list = ["percent_recurrent_by_dimension"]
    mydict_rec = get_dict_csv("total_recurrent_runs_by_dimension")
    mydict_total = get_dict_csv("total_runs_by_dimension")
    valid_keys = get_list_csv("valid_keys_by_dimension")
    percent_rec_dict = dict()
    for dim in valid_keys:
        try:
            percent_rec = str(round(float(mydict_rec[str(dim)])/float(mydict_total[str(dim)])*100,4)) + "%"
        except ZeroDivisionError:
            percent_rec = "N/A"
        percent_rec_dict[str(dim)] = percent_rec
    set_dict_csv("percent_recurrent_by_dimension", percent_rec_dict)
    return percent_rec_dict


def get_and_set_percent_recurrent_by_steps():
    file_list = ["percent_recurrent_by_steps"]
    mydict_rec = get_dict_csv("total_recurrent_runs_by_steps")
    mydict_total = get_dict_csv("total_runs_by_steps")
    valid_keys = get_list_csv("valid_keys_by_steps")
    percent_rec_dict = dict()
    for key in valid_keys:
        try:
            #print(key)
            percent_rec = str(round(float(mydict_rec[str(key)])/float(mydict_total[str(key)])*100,4)) + "%"
        except ZeroDivisionError:
            percent_rec = "N/A"
        except KeyError:
            try:
                percent_rec = str(round(float(mydict_rec[key])/float(mydict_total[key])*100,4)) + "%"
            except ZeroDivisionError:
                percent_rec = "N/A"
        percent_rec_dict[str(key)] = percent_rec
    set_dict_csv("percent_recurrent_by_steps", percent_rec_dict)
    return percent_rec_dict


def set_valid_keys_by_steps():
    valid_keys_by_steps = []
    for i in range(1,9):
        valid_keys_by_steps_1 = [(i,j) for j in range(200,7501,100)]
        valid_keys_by_steps_2 = [(i,j) for j in range(8000,15001,500)]
        valid_keys_by_steps.extend(valid_keys_by_steps_1)
        valid_keys_by_steps.extend(valid_keys_by_steps_2)
    set_list_csv("valid_keys_by_steps", valid_keys_by_steps)

def set_valid_keys_by_dimension():
    valid_keys_by_dimension = [i for i in range(1,9)]
    set_list_csv("valid_keys_by_dimension", valid_keys_by_dimension)


def get_list_csv(filename):
    file_list = ["valid_keys_by_steps", "valid_keys_by_dimension"]
    if os.path.isfile("{}.csv".format(filename)) and filename in file_list:
        with open('{}.csv'.format(filename)) as csv_file:
            reader = csv.reader(csv_file)
            mylist = list(reader)
            list_tuples = []
            for i in mylist[0]:
                list_tuples.append(eval(i))
            return list_tuples
    return list()


def set_list_csv(filename, mylist):
    file_list = ["valid_keys_by_steps", "valid_keys_by_dimension"]
    if os.path.isfile("{}.csv".format(filename)) and filename in file_list:
        with open('{}.csv'.format(filename), 'w') as csv_file:  
            writer = csv.writer(csv_file)
            writer.writerow(mylist)



def get_dict_csv(filename):
    file_list = ["total_runs_by_steps", "total_recurrent_runs_by_steps", "average_magnitude_by_steps", "percent_recurrent_by_steps",
                 "total_runs_by_dimension", "total_recurrent_runs_by_dimension", "average_magnitude_by_dimension", "percent_recurrent_by_dimension"]
    if os.path.isfile("{}.csv".format(filename)) and filename in file_list:
        with open('{}.csv'.format(filename)) as csv_file:
            reader = csv.reader(csv_file)
            mydict = dict(reader)
            return mydict

def set_dict_csv(filename, mydict):
    file_list = ["total_runs_by_steps", "total_recurrent_runs_by_steps", "average_magnitude_by_steps", "percent_recurrent_by_steps",
                 "total_runs_by_dimension", "total_recurrent_runs_by_dimension", "average_magnitude_by_dimension", "percent_recurrent_by_dimension"]
    if os.path.isfile("{}.csv".format(filename)) and filename in file_list:
        with open('{}.csv'.format(filename), 'w') as csv_file:  
            writer = csv.writer(csv_file)
            for key, value in mydict.items():
                writer.writerow([key, value])


def run_walk(dimension = 0, steps = 0, defined_start = False, animated = True):
    # checks if dimension and steps inputted is valid
    if dimension > 0 and steps > 9 and steps < 15001:
        if not animated:
            # if defined_start isn't defined, set it to origin
            if not defined_start:
                defined_start = [0] * dimension
            
            # to flag when we return to defined start
            recurrent = False
            
            # create vector for walking
            walk = defined_start.copy()
            
            # start walking
            for i in range(steps):
                
                # pick dimension, 0 adds 1 to that dimension, 1 adds -1 to that dimension
                walk[cryto_gen_num.randrange(dimension)] += 1 if cryto_gen_num.randrange(2) == 0 else -1
                
                # check if walk returns to start
                if walk == defined_start:
                    #if so flag as recurrent and break current for loop
                    recurrent = True
                    break
                    
            # continue the rest of the for loop (avoids unnesscary checks to maybe make barely faster)
            for j in range(steps-(i+1)):
                walk[cryto_gen_num.randrange(dimension)] += 1 if cryto_gen_num.randrange(2) == 0 else -1
                
                #iterations += 1
                
            #print(str(walk) + ", recurrent: " + str(recurrent) + ", iterations: " + str(iterations))
            #print(str(walk) + ", recurrent: " + str(recurrent))
            
            # calculate magnitude of walk from origin
            magnitude = 0
            for element in walk:
                magnitude += element**2
            magnitude = magnitude**(1/2)
            
            #print(walk)
            #print(magnitude)
            
            return 1, int(recurrent), magnitude, walk.copy()
        else:
            animation_steps = []
            
            # if defined_start isn't defined, set it to origin
            if not defined_start:
                defined_start = [0] * dimension
            
            # to flag when we return to defined start
            recurrent = False
            
            # create vector for walking
            walk = defined_start.copy()
            animation_steps.append(walk.copy())
            
            # start walking
            for i in range(steps):
                
                # pick dimension, 0 adds 1 to that dimension, 1 adds -1 to that dimension
                walk[cryto_gen_num.randrange(dimension)] += 1 if cryto_gen_num.randrange(2) == 0 else -1
                animation_steps.append(walk.copy())
                
                # check if walk returns to start
                if walk == defined_start:
                    #if so flag as recurrent and break current for loop
                    recurrent = True
                    break
                    
            # continue the rest of the for loop (avoids unnesscary checks to maybe make barely faster)
            for j in range(steps-(i+1)):
                walk[cryto_gen_num.randrange(dimension)] += 1 if cryto_gen_num.randrange(2) == 0 else -1
                animation_steps.append(walk.copy())
                
                #iterations += 1
                
            #print(str(walk) + ", recurrent: " + str(recurrent) + ", iterations: " + str(iterations))
            #print(str(walk) + ", recurrent: " + str(recurrent))
            
            # calculate magnitude of walk from origin
            magnitude = 0
            for element in walk:
                magnitude += element**2
            magnitude = magnitude**(1/2)
            
            #print(walk)
            #print(magnitude)
            
            return 1, int(recurrent), magnitude, animation_steps
    else:
        return False
    

def many_walks(dimension, steps, runs_to_complete):
    #dimension = int(dimension)
    #steps = int(steps)
    #runs_to_complete = int(runs_to_complete)
    final_vecs = []
    recurrent_count = 0
    if runs_to_complete > 0:
        valid_keys_by_steps = get_list_csv("valid_keys_by_steps")
        #valid_keys_by_dimension = get_list_csv("valid_keys_by_dimension")

        if (dimension, steps) in valid_keys_by_steps:
            for i in range(0, runs_to_complete):
                if i % 250 == 0 :
                    print("Starting on run " + str(i) + " of " + str(runs_to_complete) + " in dimension " + str(dimension) + " with " + str(steps) + " steps.")
                total_runs_one, total_recurrent_runs_one, new_magnitude, final_vec = run_walk(dimension, steps, animated = False)
                final_vecs.append(final_vec.copy())
                recurrent_count += total_recurrent_runs_one

                average_magnitude_by_dimension = get_dict_csv("average_magnitude_by_dimension")
                total_runs_by_dimension = get_dict_csv("total_runs_by_dimension")
                #try:
                old_avg_mag_by_dim = float(average_magnitude_by_dimension[str(dimension)])*float(total_runs_by_dimension[str(dimension)])
                #except KeyError:
                #    average_magnitude_by_dimension[str(dimension)] = 0
                #    total_runs_by_dimension[str(dimension)] = 0
                #    old_avg_mag_by_dim = 0
                total_runs_by_dimension[str(dimension)] = float(total_runs_by_dimension[str(dimension)]) + total_runs_one
                set_dict_csv("total_runs_by_dimension", total_runs_by_dimension)
                total_recurrent_runs_by_dimension = get_dict_csv("total_recurrent_runs_by_dimension")
                #try:
                total_recurrent_runs_by_dimension[str(dimension)] = float(total_recurrent_runs_by_dimension[str(dimension)]) + total_recurrent_runs_one
                
                #except KeyError:
                #    total_recurrent_runs_by_dimension[str(dimension)] = 0
                #    total_recurrent_runs_by_dimension[str(dimension)] = float(total_recurrent_runs_by_dimension[str(dimension)]) + total_recurrent_runs_one
                set_dict_csv("total_recurrent_runs_by_dimension", total_recurrent_runs_by_dimension)
                average_magnitude_by_dimension[str(dimension)] = (old_avg_mag_by_dim+new_magnitude)/total_runs_by_dimension[str(dimension)]
                set_dict_csv("average_magnitude_by_dimension", average_magnitude_by_dimension)


                average_magnitude_by_steps = get_dict_csv("average_magnitude_by_steps")
                total_runs_by_steps = get_dict_csv("total_runs_by_steps")
                #try:
                old_avg_mag_by_dim = float(average_magnitude_by_steps[str((dimension, steps))])*float(total_runs_by_steps[str((dimension, steps))])
                #except KeyError:
                #    average_magnitude_by_steps[str((dimension, steps))] = 0
                #    total_runs_by_steps[str((dimension, steps))] = 0
                #    old_avg_mag_by_dim = 0
                total_runs_by_steps[str((dimension, steps))] = float(total_runs_by_steps[str((dimension, steps))]) + total_runs_one
                set_dict_csv("total_runs_by_steps", total_runs_by_steps)
                total_recurrent_runs_by_steps = get_dict_csv("total_recurrent_runs_by_steps")
                #try:
                total_recurrent_runs_by_steps[str((dimension, steps))] = float(total_recurrent_runs_by_steps[str((dimension, steps))]) + total_recurrent_runs_one
                #except KeyError:
                #    total_recurrent_runs_by_steps[str((dimension, steps))] = 0
                #    total_recurrent_runs_by_steps[str((dimension, steps))] += total_recurrent_runs_one
                set_dict_csv("total_recurrent_runs_by_steps", total_recurrent_runs_by_steps)
                average_magnitude_by_steps[str((dimension, steps))] = (old_avg_mag_by_dim+new_magnitude)/total_runs_by_steps[str((dimension, steps))]
                set_dict_csv("average_magnitude_by_steps", average_magnitude_by_steps)

            return final_vecs, recurrent_count

        # only supporting valid dimension and step inputs
        #elif dimension in vars.valid_keys_by_dimension:
        #    for i in range(0, runs_to_complete):
        #        total_runs_one, total_recurrent_runs_one, new_magnitude, animation_steps = run_walk(dimension, steps, animated = False)

        #        old_avg_mag_by_dim = vars.average_magnitude_by_dimension[dimension]*vars.total_runs_by_dimension[dimension]
        #        vars.total_runs_by_dimension[dimension] += total_runs_one
        #        vars.total_recurrent_runs_by_dimension[dimension] += total_recurrent_runs_one
        #        vars.average_magnitude_by_dimension[dimension] = (old_avg_mag_by_dim+new_magnitude)/vars.total_runs_by_dimension[dimension]
        else:
            print("Not valid inputs for dimension or steps.")
    else:
        print("Not valid number entered for number of runs.")

def animate_2d(steps):
    dimension = 2

    x = []
    y = []

    valid_keys_by_steps = get_list_csv("valid_keys_by_steps")
    valid_keys_by_dimension = get_list_csv("valid_keys_by_dimension")

    if (dimension, steps) in valid_keys_by_steps:
        total_runs_one, total_recurrent_runs_one, new_magnitude, animation_steps = run_walk(dimension, steps, animated = True)


        average_magnitude_by_dimension = get_dict_csv("average_magnitude_by_dimension")
        total_runs_by_dimension = get_dict_csv("total_runs_by_dimension")
        try:
            old_avg_mag_by_dim = float(average_magnitude_by_dimension[str(dimension)])*float(total_runs_by_dimension[str(dimension)])
        except KeyError:
            average_magnitude_by_dimension[str(dimension)] = 0
            total_runs_by_dimension[str(dimension)] = 0
            old_avg_mag_by_dim = 0
        total_runs_by_dimension[str(dimension)] = float(total_runs_by_dimension[str(dimension)]) + total_runs_one
        set_dict_csv("total_runs_by_dimension", total_runs_by_dimension)
        total_recurrent_runs_by_dimension = get_dict_csv("total_recurrent_runs_by_dimension")
        try:
            total_recurrent_runs_by_dimension[str(dimension)] = float(total_recurrent_runs_by_dimension[str(dimension)]) + total_recurrent_runs_one
        except KeyError:
            total_recurrent_runs_by_dimension[str(dimension)] = 0
            total_recurrent_runs_by_dimension[str(dimension)] = float(total_recurrent_runs_by_dimension[str(dimension)]) + total_recurrent_runs_one
        set_dict_csv("total_recurrent_runs_by_dimension", total_recurrent_runs_by_dimension)
        average_magnitude_by_dimension[str(dimension)] = (old_avg_mag_by_dim+new_magnitude)/total_runs_by_dimension[str(dimension)]
        set_dict_csv("average_magnitude_by_dimension", average_magnitude_by_dimension)


        average_magnitude_by_steps = get_dict_csv("average_magnitude_by_steps")
        total_runs_by_steps = get_dict_csv("total_runs_by_steps")
        #try:
        old_avg_mag_by_dim = float(average_magnitude_by_steps[str((dimension, steps))])*float(total_runs_by_steps[str((dimension, steps))])
        #except KeyError:
        #    average_magnitude_by_steps[str((dimension, steps))] = 0
        #    total_runs_by_steps[str((dimension, steps))] = 0
        #    old_avg_mag_by_dim = 0
        total_runs_by_steps[str((dimension, steps))] = float(total_runs_by_steps[str((dimension, steps))]) + total_runs_one
        set_dict_csv("total_runs_by_steps", total_runs_by_steps)
        total_recurrent_runs_by_steps = get_dict_csv("total_recurrent_runs_by_steps")
        try:
            total_recurrent_runs_by_steps[str((dimension, steps))] = float(total_recurrent_runs_by_steps[str((dimension, steps))]) + total_recurrent_runs_one
        except KeyError:
            total_recurrent_runs_by_steps[str((dimension, steps))] = 0
            total_recurrent_runs_by_steps[str((dimension, steps))] += total_recurrent_runs_one
        set_dict_csv("total_recurrent_runs_by_steps", total_recurrent_runs_by_steps)
        average_magnitude_by_steps[str((dimension, steps))] = (old_avg_mag_by_dim+new_magnitude)/total_runs_by_steps[str((dimension, steps))]
        set_dict_csv("average_magnitude_by_steps", average_magnitude_by_steps)

        
        for element in animation_steps:
            x.append(element[0])
            y.append(element[1])

        fig, ax = plt.subplots(figsize=(4, 3), dpi=800/4)

        if total_recurrent_runs_one:
            line, = ax.plot(x, y, color='g')
        elif not total_recurrent_runs_one:
            line, = ax.plot(x, y, color='r')
        
        line.axes.axis([min(x)-5, max(x)+5, min(y)-5, max(y)+5])

        plt.axhline(0, color='grey', alpha = 0.25, dashes = [0,0,1])
        plt.axvline(0, color='grey', alpha = 0.25, dashes = [0,0,1])
        plt.title("{} steps in {}-D Random Walk".format(steps, 2))
        
        blit = True
        interval = 25

        def update(num, x, y, line, jump):
                line.set_data(x[:num*jump], y[:num*jump])
                return line,

        if steps < 701: 
            ani = animation.FuncAnimation(fig, update, len(x)//3-1, fargs=[x, y, line, 3],
                                      interval=interval, blit=blit)
        elif steps < 2000:
            ani = animation.FuncAnimation(fig, update, len(x)//4-1, fargs=[x, y, line, 4],
                                      interval=interval, blit=blit)  
        elif steps < 4000:
            ani = animation.FuncAnimation(fig, update, len(x)//5-1, fargs=[x, y, line, 5],
                                      interval=interval, blit=blit)
        elif steps < 6000:
            ani = animation.FuncAnimation(fig, update, len(x)//6-1, fargs=[x, y, line, 6],
                                      interval=interval, blit=blit)
        elif steps < 8000:
            ani = animation.FuncAnimation(fig, update, len(x)//8-1, fargs=[x, y, line, 8],
                                      interval=interval, blit=blit)
        elif steps < 10000:
            ani = animation.FuncAnimation(fig, update, len(x)//10-1, fargs=[x, y, line, 10],
                                      interval=interval, blit=blit)
        else:
            ani = animation.FuncAnimation(fig, update, len(x)//12-1, fargs=[x, y, line, 12],
                                      interval=interval, blit=blit)
        

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
        total_runs_one, total_recurrent_runs_one, new_magnitude, animation_steps = run_walk(dimension, steps, animated = True)


        average_magnitude_by_dimension = get_dict_csv("average_magnitude_by_dimension")
        total_runs_by_dimension = get_dict_csv("total_runs_by_dimension")
        try:
            old_avg_mag_by_dim = average_magnitude_by_dimension[str(dimension)]*total_runs_by_dimension[str(dimension)]
        except KeyError:
            average_magnitude_by_dimension[str(dimension)] = 0
            total_runs_by_dimension[str(dimension)] = 0
            old_avg_mag_by_dim = 0
        total_runs_by_dimension[str(dimension)] += total_runs_one
        set_dict_csv("total_runs_by_dimension", total_runs_by_dimension)
        total_recurrent_runs_by_dimension = get_dict_csv("total_recurrent_runs_by_dimension")
        try:
            total_recurrent_runs_by_dimension[str(dimension)] += total_recurrent_runs_one
        except KeyError:
            total_recurrent_runs_by_dimension[str(dimension)] = 0
            total_recurrent_runs_by_dimension[str(dimension)] += total_recurrent_runs_one
        set_dict_csv("total_recurrent_runs_by_dimension", total_recurrent_runs_by_dimension)
        average_magnitude_by_dimension[str(dimension)] = (old_avg_mag_by_dim+new_magnitude)/total_runs_by_dimension[str(dimension)]
        set_dict_csv("average_magnitude_by_dimension", average_magnitude_by_dimension)
        
        for element in animation_steps:
            x.append(element[0])
            y.append(element[1])

        fig, ax = plt.subplots(figsize=(4, 3), dpi=800/4)

        if total_recurrent_runs_one:
            line, = ax.plot(x, y, color='g')
        elif not total_recurrent_runs_one:
            line, = ax.plot(x, y, color='r')
        
        line.axes.axis([min(x)-5, max(x)+5, min(y)-5, max(y)+5])

        plt.axhline(0, color='grey', alpha = 0.25, dashes = [0,0,1])
        plt.axvline(0, color='grey', alpha = 0.25, dashes = [0,0,1])
        plt.title("{} steps in {}-D Random Walk".format(steps, 2))
        
        def update(num, x, y, line):
            line.set_data(x[:num], y[:num])
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

            


 