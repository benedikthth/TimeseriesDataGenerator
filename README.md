```
.___________. __  .___  ___.  _______                                                             
|           ||  | |   \/   | |   ____|                                                            
`---|  |----`|  | |  \  /  | |  |__                                                               
    |  |     |  | |  |\/|  | |   __|                                                              
    |  |     |  | |  |  |  | |  |____                                                             
    |__|     |__| |__|  |__| |_______|                                                            
                                                                                                  
     _______. _______ .______       __   _______     _______.                                     
    /       ||   ____||   _  \     |  | |   ____|   /       |                                     
   |   (----`|  |__   |  |_)  |    |  | |  |__     |   (----`                                     
    \   \    |   __|  |      /     |  | |   __|     \   \                                         
.----)   |   |  |____ |  |\  \----.|  | |  |____.----)   |                                        
|_______/    |_______|| _| `._____||__| |_______|_______/                                         
                                                                                                  
 _______       ___   .___________.    ___                                                         
|       \     /   \  |           |   /   \                                                        
|  .--.  |   /  ^  \ `---|  |----`  /  ^  \                                                       
|  |  |  |  /  /_\  \    |  |      /  /_\  \                                                      
|  '--'  | /  _____  \   |  |     /  _____  \                                                     
|_______/ /__/     \__\  |__|    /__/     \__\                                                    
                                                                                                  
  _______  _______ .__   __.  _______ .______          ___   .___________.  ______   .______      
 /  _____||   ____||  \ |  | |   ____||   _  \        /   \  |           | /  __  \  |   _  \     
|  |  __  |  |__   |   \|  | |  |__   |  |_)  |      /  ^  \ `---|  |----`|  |  |  | |  |_)  |    
|  | |_ | |   __|  |  . `  | |   __|  |      /      /  /_\  \    |  |     |  |  |  | |      /     
|  |__| | |  |____ |  |\   | |  |____ |  |\  \----./  _____  \   |  |     |  `--'  | |  |\  \----.
 \______| |_______||__| \__| |_______|| _| `._____/__/     \__\  |__|      \______/  | _| `._____|
```
#  `Generate time series data for your machine learning models, you must.`


## Getting started
To be able to use this as a module run the following command inside the same folderr as the 
`setup.py` script

```
pip istall -e .
```
*you might need to sudo that*


## Importing 
Provided that you have used the above command,
you should be able to import the functions **gen_dataset** and **ThirdDimensionalize** like so:

`./Your_fantastic_script.py`:
```python
from TimeseriesDataGenerator import Generator
```


```python
generator = Generator(
    how_many=100, 
        #how many sequences in the dataset

    variant_over_time=True, 
        #should the noise level vary over time?
    
    return_not=False, 
        #If true: the noise level over time is 
        # returned with the dataset and the labels,
        # (useful for visualizing)
    
    num_freqs = 1, 
        #How many frequencies compose the signal 
    
    num_outputs=1, 
        #how many frequencies compose a label. 

    amplitude_dropoff=0.5, 
        #how much should each subsequent sine 
        # drop off in amplitude. 

    st_deviation=1, 
        #the strenght of the additive noise. 
        # pass 0 for no noise.

    freq_range=(2.5, 50),
        #Range of frequencies, the default is
        # the range of EEG frequencies.

    sampling_frequency=100, 
        #Sampling frequency, with sf=100, in 1
        # second recording there will be 100 
        # samples.

    sequence_length=30,
        #how many seconds of recording to generate.

    temporal=False,
        #The data returned from load will be 
        # multidimensional, where the dimensions 
        # are (batch, timestep, features).
 
    generator_settings=None
        #An object containing the above settings 
        # as key-value pairs. 
        # (useful for creating many generators with 
        # the same settings)
)

x, y = generator.load(3)
#x = [ [x1], [x2], [x3] ]
#y = [ [y1], [y2], [y3] ]
# where x_i is time series data, and y_i is a list of frequencies.
# x_i is an array of length (sequence_length * sampling_frequency)
# y_i is an array of length (num_outputs)
# x_i corresponds to y_i
```

## FFT_test.py
This file uses the generator to generate a single sequence and then 
shows a graph showing the frequencies that the signal is composed of.
