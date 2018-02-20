from pylab import *

drain_weights = [250, 300, 350, 400, 500]
recovery_weights = [0, 50, 100, 125, 150]
drain_data = {}
for weight in drain_weights:
    drain_data[weight] = genfromtxt("drain_data/weight_"+str(weight))

print(drain_data)

