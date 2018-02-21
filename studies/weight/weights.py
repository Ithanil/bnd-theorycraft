from pylab import *
from scipy.optimize import curve_fit

drain_weights = [250, 300, 350, 400, 500]
recovery_weights = [0, 50, 100, 125, 150]

def stamina_recovery(recovery_base, time):
    if recovery_base>0: # check needed for fitting
        return recovery_base * time
    else:
        return 0.0

def stamina_drain(weight, drain_base_1, drain_base_2, time):
    if weight<=100:
        return 0.0
    elif weight<=200:
        if drain_base_1>0: # check needed for fitting
            return drain_base_1 * time
        else:
            return 0.0
    else:
        if drain_base_2>0: # check needed for fitting
            return drain_base_2/255 * weight * time
        else:
            return 0.0


def stamina_drain_array(weights, drain_base_1, drain_base_2, time):
    result = zeros(len(weights))
    for it, weight in enumerate(weights):
        result[it] = stamina_drain(weight, drain_base_1, drain_base_2, time)
    return result        

def stamina_change(weight, recovery_base, drain_base_1, drain_base_2, time):
    return stamina_recovery(recovery_base, time) - stamina_drain(weight, drain_base_1, drain_base_2, time)

def stamina_change_array(weights, recovery_base, drain_base_1, drain_base_2, time):
    stamrec = stamina_recovery(recovery_base, time)
    stamdrain = stamina_drain_array(weights, drain_base_1, drain_base_2, time)    
    return stamrec - stamdrain

def stamina_rate(weight, recovery_base, drain_base_1, drain_base_2):
    return stamina_change(weight, recovery_base, drain_base_1, drain_base_2, 1.0)

def stamina_rate_array(weights, recovery_base, drain_base_1, drain_base_2):
    return stamina_change_array(weights, recovery_base, drain_base_1, drain_base_2, 1.0)

def stamina_rate_fit(weights, values, model_weights, ipars): # weight, value arrays + input for final model array + initial model parameters
    pars, covar = curve_fit(stamina_rate_array, weights, values, p0=ipars)
    model = stamina_rate_array(model_weights, pars[0], pars[1], pars[2])
    return pars, covar, model    

def rawToPlotData(raw_data, stamina_change):
    data_x = []
    data_y = []
    for x, y in raw_data.items():
        try:
            for yi in y:
                data_x.append(x)
                data_y.append(stamina_change/yi)
        except:
            data_x.append(x)
            data_y.append(stamina_change/y)

    data_x = array(data_x)
    data_y = array(data_y)

    return data_x, data_y


drain_data_raw = {}
for weight in drain_weights:
    drain_data_raw[weight] = array(genfromtxt("drain_data/weight_"+str(weight), comments = '#'))

recovery_data_raw = {}
for weight in recovery_weights:
    recovery_data_raw[weight] = genfromtxt("recovery_data/weight_"+str(weight)+"_move", comments = '#')

nomove_data = genfromtxt("recovery_data/nomove", comments = '#')

drain_data_x, drain_data_y = rawToPlotData(drain_data_raw, -255)
recovery_data_x, recovery_data_y = rawToPlotData(recovery_data_raw, 255)

comb_data_x = concatenate((recovery_data_x, drain_data_x))
comb_data_y = concatenate((recovery_data_y, drain_data_y))

avg_nomove_time = mean(nomove_data)
print('Avg standstill recovery time: ' + str(avg_nomove_time))
print('Avg standstill recovery rate: ' + str(255.0/avg_nomove_time))

init_vals = [3, 4, 8]

drain_model_data_x = arange(201, 500, 1)
drain_vals, covar_drain, drain_model = stamina_rate_fit(drain_data_x, drain_data_y, drain_model_data_x, init_vals)
print('drain vals', drain_vals)

rec_model_data_x = arange(0, 200, 1) 
rec_vals, covar_rec, rec_model = stamina_rate_fit(recovery_data_x, recovery_data_y, rec_model_data_x, init_vals)
print('rec_vals', rec_vals)

comb_model_data_x = arange(0, 500, 1)
comb_vals, covar_comb, comb_model = stamina_rate_fit(comb_data_x, comb_data_y, comb_model_data_x, init_vals)
print('comb_vals', comb_vals)

manual_model = stamina_rate_array(comb_model_data_x, 4, 3, 8)

figure(1)
plot(drain_data_x, drain_data_y, 'o')
plot(drain_model_data_x, drain_model)
title('Stamina drain test')
xlabel('Weight')
ylabel('Rate [1/s]')
savefig('plot_drain.pdf')

figure(2)
plot(recovery_data_x, recovery_data_y, 'o')
plot(rec_model_data_x, rec_model)
title('Stamina recovery test (moving)')
xlabel('Weight')
ylabel('Rate [1/s]')
savefig('plot_recovery.pdf')

figure(3)
plot(comb_data_x, comb_data_y, 'o')
plot(comb_model_data_x, comb_model)
title('Stamina drain+recovery test (moving)')
xlabel('Weight')
ylabel('Rate [1/s]')
savefig('plot_combined.pdf')

figure(4)
plot(comb_data_x, comb_data_y, 'o')
plot(comb_model_data_x, manual_model)
title('Stamina drain+recovery test (moving) \n Manually set model parameters')
xlabel('Weight')
ylabel('Rate [1/s]')
savefig('plot_manual.pdf')
show()
