
# -*- coding: utf-8 -*-)
import numpy as np
import json
import matplotlib.pyplot as plt

def get_value(data, file):
    for line in open(file):
        js = json.loads(line)
        data.append(js['v1'])

lstm = []
lstm_cnn = []

get_value(lstm, 'infer')
#get_value(lstm_cnn, 'infer_cnn')

print 'lstm:',lstm
print 'type(lstm):',type(lstm)
print 'lstm_cnn:',lstm_cnn

x = np.arange(0, len(lstm), 1)
#plt.axis([x_min, x_max, y_min, y_max])
y = np.array(lstm)
y_cnn = np.array(lstm_cnn)
#plt.axis([-576, 576, -np.max(lstm), np.max(lstm)])
#plt.axis([0, 576,-2, 576])
plt.figure(figsize=(15, 5))
print 'type(x):',type(x)
plt.plot(x, y, color="r", linestyle="-", linewidth=1)

plt.grid(True, linestyle = "-.", color = 'g', linewidth = 1)
#plt.plot(x, y_cnn, color="b", linestyle="-", linewidth=1)
plt.show()


x = np.arange(-5, 5, 0.02)
print 'x:',type(x)
y = np.sin(x)

plt.axis([-np.pi, np.pi, -2, 2])

plt.plot(x, y, color="r", linestyle="-", linewidth=1)

#plt.show()

