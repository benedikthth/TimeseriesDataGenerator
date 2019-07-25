from scipy.fftpack import fft
import numpy as np 
import matplotlib.pyplot as plt

from TimeseriesDataGenerator import Generator 

generator = Generator(num_freqs=5, st_deviation = 0)
data, labels = generator.load(1)
# generator = generator.generator()
# labels, data = gen_dataset(1, num_freqs=3, amplitude_dropoff=0.7, st_deviation=2, variant_over_time=True)
data, labels = generator.load(1)
T = 1/100 #inverse of sampling rate
x = np.linspace(0.0, 1.0/(2.0*T), int(3000/2))

yr = fft(data[0]) 
y = 2/3000 * np.abs(yr[0:np.int(3000/2)]) # positive freqs only

print(labels[0])


plt.plot(x, y)
plt.title(f"{labels[0]}")
plt.show()
