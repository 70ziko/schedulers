import numpy as np
from scipy.stats import truncnorm
import random

def normal(number, mean=30, scale=5, low=0, upp=50, arr_up=100, arr_low=0):

    # obiekt generujący dane
    norm = truncnorm((low-mean)/scale,(upp-mean)/scale,loc=mean,scale=scale)

    arrivals = np.array([])
    for i in range(number):
        arrivals = np.append(arrivals, random.randrange(arr_low, arr_up))

    executions = norm.rvs(number)

    data_2d = np.vstack((arrivals, executions)).T

    # przedstawianie danych w postaci tabeli dwuwymiarowej
    # data_2d = np.reshape(data_2d,(number,2))
    data_2d = data_2d.astype(int)

    # zapisywanie danych do pliku
    with open("generated.txt",'w', encoding='utf-8') as f:
        data_str = '\n'.join(map(str,data_2d))
        data_str = data_str.replace("[","")
        data_str = data_str.replace("]","")
        f.write(data_str)
    
    return data_2d

def normal_all(number, mean=20, scale=10, low=0, upp=50):

    # obiekt generujący dane
    norm = truncnorm((low-mean)/scale,(upp-mean)/scale,loc=mean,scale=scale)

    # przedstawianie danych w postaci tabeli dwuwymiarowej
    data_2d = np.reshape(norm(2*number),(number,2))
    data_2d = data_2d.astype(int)

    # zapisywanie danych do pliku
    with open("generated.txt",'w', encoding='utf-8') as f:
        data_str = '\n'.join(map(str,data_2d))
        data_str = data_str.replace("[","")
        data_str = data_str.replace("]","")
        f.write(data_str)
    
    return data_2d

def rand(number,  low=0, upp=50):

    data = np.array([])
    # generowanie danych
    for i in range(2*number):
        data = np.append(data, random.randrange(low, upp))

    # przedstawianie danych w postaci tabeli dwuwymiarowej
    data_2d = np.reshape(data,(number,2))
    data_2d = data_2d.astype(int)

    # zapisywanie danych do pliku
    with open("generated.txt",'w', encoding='utf-8') as f:
        data_str = '\n'.join(map(str,data_2d))
        data_str = data_str.replace("[","")
        data_str = data_str.replace("]","")
        f.write(data_str) 
    
    return data_2d

def zeroes(number, mean=30, scale=5, low=0, upp=50):

    # obiekt generujący dane
    norm = truncnorm((low-mean)/scale,(upp-mean)/scale,loc=mean,scale=scale)

    arrivals = np.array([])
    for i in range(number):
        arrivals = np.append(arrivals, 0)

    executions = norm.rvs(number)

    data_2d = np.vstack((arrivals, executions)).T

    # przedstawianie danych w postaci tabeli dwuwymiarowej
    # data_2d = np.reshape(data_2d,(number,2))
    data_2d = data_2d.astype(int)

    # zapisywanie danych do pliku
    with open("generated.txt",'w', encoding='utf-8') as f:
        data_str = '\n'.join(map(str,data_2d))
        data_str = data_str.replace("[","")
        data_str = data_str.replace("]","")
        f.write(data_str)
    
    return data_2d