
import scipy
import numpy as np

def import_cwru():
    mat_file = "data.mat"
    data = scipy.io.loadmat(mat_file) # Loads the .mat file data into a Python variable
    keys = data.keys() # Gets the keys of the loaded data
    # print(keys)
    De_key = next((key for key in keys if "DE" in key), None) # Finds the key that contains "DE"
    rpm_key = next((key for key in keys if "RPM" in key), None) # Finds the key that contains "rpm"
    rpm = data[rpm_key].flatten()[0] if rpm_key else None # Extracts the RPM value
    signal = data[De_key].flatten() if De_key else None # Extracts the signal data
    fs = 12e3 # Sampling frequency
    # rpm = 1797 # Rotational speed in RPM
    fr = rpm / 60 # Rotational frequency in Hz
    return signal, fs, fr

def import_polito():
    data2 = scipy.io.loadmat('523rpm_124.8kN_0kN.mat')
    signal1 = data2['Signal_2']
    start = signal1[0,0]["x_values"]["start_value"][0,0][0,0]
    increment = signal1[0,0]["x_values"]["increment"][0,0][0,0]
    N = signal1[0,0]["x_values"]["number_of_values"][0,0][0,0]
    fs = 1 / increment
    time = np.arange(start, start + N * increment, increment)
    unit = signal1[0,0]["y_values"]["quantity"][0,0]['label']
    print("acceleration unit:", unit)
    rpm_unit = data2["Signal_3"][0,0]["y_values"]["quantity"][0,0]['label']
    print("rpm unit:", rpm_unit)
    rpm = np.mean(data2["Signal_3"][0,0]["y_values"]["values"][0,0])
    
    factor = data2["Signal_3"][0,0]["y_values"]["quantity"][0,0]["unit_transformation"][0,0]["factor"][0,0][0,0]
    print(factor)
    
    
    fr = rpm * factor / 60
    signal = signal1[0,0]["y_values"]["values"][0,0][:,1]
    # print(unit)
    return signal, fs, fr

def import_cwru_133():
    mat_file = "133.mat"
    data = scipy.io.loadmat(mat_file) # Loads the .mat file data into a Python variable
    keys = data.keys() # Gets the keys of the loaded data
    # print(keys)
    De_key = next((key for key in keys if "DE" in key), None) # Finds the key that contains "DE"
    rpm_key = next((key for key in keys if "RPM" in key), None) # Finds the key that contains "rpm"
    rpm = data[rpm_key].flatten()[0] if rpm_key else None # Extracts the RPM value
    signal = data[De_key].flatten() if De_key else None # Extracts the signal data
    fs = 12e3 # Sampling frequency
    # rpm = 1797 # Rotational speed in RPM
    fr = rpm / 60 # Rotational frequency in Hz
    return signal, fs, fr

def import_cwru_200():
    mat_file = "200.mat"
    data = scipy.io.loadmat(mat_file) # Loads the .mat file data into a Python variable
    keys = data.keys() # Gets the keys of the loaded data
    # print(keys)
    De_key = next((key for key in keys if "DE" in key), None) # Finds the key that contains "DE"
    rpm_key = next((key for key in keys if "RPM" in key), None) # Finds the key that contains "rpm"
    rpm = data[rpm_key].flatten()[0] if rpm_key else None # Extracts the RPM value
    signal = data[De_key].flatten() if De_key else None # Extracts the signal data
    fs = 12e3 # Sampling frequency
    # rpm = 1797 # Rotational speed in RPM
    fr = rpm / 60 # Rotational frequency in Hz
    return signal, fs, fr
    
    
if __name__ == "__main__":
    print("This file contains functions to import data for the tutorial.ipynb notebook. It is not meant to be run directly.")