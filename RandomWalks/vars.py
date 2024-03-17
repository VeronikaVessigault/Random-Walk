# Tally
global valid_keys_by_steps
valid_keys_by_steps = [(i,j) for i in range(1,9) for j in range(200,7501,100)]
valid_keys_by_steps_1 = [(i,j) for i in range(1,9) for j in range(800,15001,500)]
valid_keys_by_steps.extend(valid_keys_by_steps_1) # (dimension, steps)
global valid_keys_by_dimension
valid_keys_by_dimension = [i for i in range(1,6)]

global total_runs_by_steps
total_runs_by_steps = {key : 0 for key in valid_keys_by_steps}
global total_recurrent_runs_by_steps
total_recurrent_runs_by_steps = {key : 0 for key in valid_keys_by_steps}
global average_magnitude_by_steps
average_magnitude_by_steps = {key : 0 for key in valid_keys_by_steps}

global total_runs_by_dimension
total_runs_by_dimension = {key : 0 for key in valid_keys_by_dimension}
global total_recurrent_runs_by_dimension
total_recurrent_runs_by_dimension = {key : 0 for key in valid_keys_by_dimension}
global average_magnitude_by_dimension
average_magnitude_by_dimension = {key : 0 for key in valid_keys_by_dimension}