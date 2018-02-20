from pylab import *

drain_weights = [250, 300, 350, 400, 500]
recovery_weights = [0, 50, 100, 125, 150]

def rawToPlotData(raw_data):
    data_x = []
    data_y = []
    for x, y in raw_data.items():
        try:
            for yi in y:
                data_x.append(x)
                data_y.append(yi)
        except:
            data_x.append(x)
            data_y.append(y)

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

drain_data_x, drain_data_y = rawToPlotData(drain_data_raw)
recovery_data_x, recovery_data_y = rawToPlotData(recovery_data_raw)


print(drain_data_raw)
print(recovery_data_raw)
print(nomove_data)

avg_nomove_time = mean(nomove_data)
print('Avg standstill recovery time: ' + str(avg_nomove_time))

figure(1)
plot(drain_data_x, drain_data_y, 'o')
title('Stamina drain test')
xlabel('Weight')
ylabel('Time [s]')
savefig('plot_drain.pdf')

figure(2)
plot(recovery_data_x, recovery_data_y, 'o')
title('Stamina recovery test (moving)')
xlabel('Weight')
ylabel('Time [s]')
savefig('plot_recovery.pdf')

show()
