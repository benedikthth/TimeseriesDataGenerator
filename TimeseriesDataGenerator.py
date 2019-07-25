import math
from operator import add, mul
import numpy as np
import random
from noise._perlin import noise1 as perlin
from timeit import default_timer as timer



 

class Generator:


    def __init__(self, variant_over_time=False , num_freqs = 1, num_outputs=1, amplitude_dropoff=0.5, st_deviation=1, freq_range=(2.5, 50), sampling_frequency=100, sequence_length=30, temporal=False, settings=None, verbose=False):
        
        """Create dataset containing how_many synthesized signals of length {recording_length} 
        with sampling rate {sampling_rate}. The signal has zero mean normally distrubuted noise

        Parameters:
            num_freqs: how many frequencies are overlaid on eachother.\n
            num_outputs: how many predictions to make. First prediction will be sine of stronges amplitude.\n
            variant_over_time (bool): Should the noise strength change over time?\n
            amplitude_dropoff: how much less amplitude the subsequent sine waves will have. (sine_i * amplitude_dropoff^i)\n
            temporal: (bool) is the data in 3 dimensions? (useful for lstms etc.)
            generator_settings: Object containing all these settings. Must contain all settings, will overwrite all other settings.\n
            st_deviation: standard deviation of additive zero mean noise  
            sampling_frequency: how many measurements are made each second.
            sequence_length: length of each segment loaded by `load`
        Returns:
            triple contining labels(list of numbers), data (list of lists of data points)
        """



        defaults =  {
            'num_freqs': 1,
            'num_outputs': 1,
            'variant_over_time': False,
            'amplitude_dropoff': 0.5,
            'st_deviation': 1,
            'sequence_length': 30,
            'freq_range': (2.5, 50), 
            'sampling_frequency':100,
            'temporal':False,
        }

        if settings:
            for i in defaults:
                if i not in settings: 
                    if verbose:
                        print(f'no setting for parameter {i}, default is {defaults[i]}')
                    settings[f'{i}'] = defaults[i]

            num_freqs = settings['num_freqs']
            num_outputs = settings['num_outputs']
            variant_over_time = settings['variant_over_time']
            amplitude_dropoff = settings['amplitude_dropoff'] 
            st_deviation = settings['st_deviation']
            sequence_length = settings['sequence_length']
            freq_range = settings['freq_range']
            sampling_frequency = settings['sampling_frequency']
            temporal = settings['temporal']

        if num_freqs < num_outputs: 
            raise Exception(f'Num freqs should not be less than num_outputs. ({num_freqs} < {num_outputs})')

        self.num_freqs = num_freqs
        self.num_outputs = num_outputs
        self.variant_over_time = variant_over_time
        self.amplitude_dropoff = amplitude_dropoff 
        self.st_deviation = st_deviation
        self.sequence_length = sequence_length
        self.freq_range = freq_range
        self._frange = self.freq_range[1] - self.freq_range[0]
        self.sampling_frequency = sampling_frequency
        self.temporal = temporal


    def load(self, how_many, return_noise_over_time=False):  
        
        """
        Create X and Y from the settings supplied in the constructor.

        Returns:
        ---
            tuple contining labels(list of numbers), data (list of lists of data points) 
        """
        #A sine wave has a cycle freq. of 2PI
        hz = 2 * math.pi # one cycle

        perlin_scale_range = (0.001, 0.005)
        _psrange = perlin_scale_range[1] - perlin_scale_range[0]

        offset_range = (0, 2*math.pi)
        _orange = offset_range[1] - offset_range[0]

        if return_noise_over_time: 
            noise_ots = []

        samples = self.sequence_length * self.sampling_frequency 

        labels = []

        dataset = []

        for i in range(how_many):
            #create perlin noise from 0 - 1 for gradually changing noise levels. 
            if self.variant_over_time:
                randbase = random.randint(1, 250)
                noise_ot = range(samples)
                pscale = (random.random() * _psrange) + perlin_scale_range[0]
                noise_ot = list(map(lambda i: (perlin(i*pscale, base=randbase)+1)/2, noise_ot))
            else:
                noise_ot = np.ones(samples)

            if return_noise_over_time:
                noise_ots.append(noise_ot)

            #create a x range.
            y = np.arange(self.sequence_length, step=1/self.sampling_frequency)
            #generate a frequency in the range of freq_range[0] - freq_range[1]
            freqs  = [(self._frange*random.random() ) + self.freq_range[0] for i in range(self.num_freqs)]
            if self.num_freqs != 1:
                labels.append(freqs[:self.num_freqs])
            else:
                labels.append(freqs[0])
            # the frequency of a normal sine is 1/2pi, so to get the 
            # sine wave to a frequency that we want we must multiply 2pi by our desired frequency

            freqs = [ f * hz for f in freqs ]
            # Generate a random offset.
            offsets = [( _orange*random.random() ) + offset_range[0] for i in range(self.num_freqs)]

            # Function that finds a value of sine wave with frequency f, offset o, at time 
            f = (
                lambda t, f, o: math.sin( ( (t) *  f ) + o  )
            )

            #precompute amplitude dropoffs.
            ads = [pow(self.amplitude_dropoff, i) for i in range(self.num_freqs)]
            # create base sine. 
            x = [f(p, freqs[0], offsets[0]) for p in y]
            # add sines.
            if self.num_freqs != 1:
                for i in range(1, self.num_freqs):
                    #create timeseries with this frequency, 
                    f2 = [f(p, freqs[i], offsets[i])* ads[i] for p in y ]
                    # add sine to base sine.
                    x = list(map(add, x, f2))
                    
            #create random numbers normally distributed with 0 mean.
            rands = np.random.normal(0, self.st_deviation, len(x))
            #multiply random noise by the perlin noise to gradually decrease, increase noise
            rands = list(map(mul, noise_ot, rands))
            #add the new nosie to the measurements.
            x = np.array(list(map(add, x, rands)) )
            dataset.append(x)

        dataset = np.array(dataset)
        if self.temporal :
            dataset = self.ThirdDimensionalize(dataset)

        labels = np.array(labels)


        if return_noise_over_time:
            return dataset, labels, noise_ots

        return dataset, labels

    
        
    def ThirdDimensionalize(self, data):
        '''Turn 2d data into a 3d data where the shape is (batch, time, feateures)
        '''
        data = np.array(
            list(map( lambda ds: np.array(list(map(lambda d: [d], ds))
            ), data))
        )
        return data






if __name__ == '__main__':

    from matplotlib import pyplot as plt


    
    gs = {
        'variant_over_time':True, 
        'num_freqs' : 1, 
        'num_outputs':1, 
        'amplitude_dropoff':0.5, 
        'st_deviation':0, 
        'freq_range':(2.5, 10), 
        'sampling_frequency':100, 
    }

    generator = Generator(settings=gs, verbose=True)

    # start = timer()
    # data, labels = generator.load(200)
    # end = timer()
    # print(f'Generated 200 sequences in {end-start} seconds.')

    x, y, n = generator.load(4, return_noise_over_time=True)
    
     
    fig, ax = plt.subplots(2, 2)
    if type(y[0]) == np.float64:
       y = [[t] for t in y]

    ax[0, 0].plot(x[0]) 
    ax[0,0].title.set_text(f"""Frequencies {
        [round(f, 2) for f in y[0]]}""") 

    ax[0, 1].plot(x[1])
    ax[0,1].title.set_text(f"""Frequencies {
        [round(f, 2) for f in y[1]]}""") 

    ax[1, 0].plot(x[2])
    ax[1,0].title.set_text(f"""Frequencies {
        [round(f, 2) for f in y[2]]}""") 

    ax[1, 1].plot(x[3])
    ax[1,1].title.set_text(f"""Frequencies {
        [round(f, 2) for f in y[3]]}""")

    ax[0,0].plot(n[0])
    ax[0,1].plot(n[1])
    ax[1,0].plot(n[2])
    ax[1,1].plot(n[3])
    plt.show()