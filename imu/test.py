#!/usr/bin/python3
from operator import eq
import numpy as np

# tp = (1,2,3)
# a, b, c = tp

# lst=[]
# lst.append([a,b,c])
# print(lst)

# lst.append([a,b,c])
# print(lst)

# arr = np.array(lst)
# print(arr)
# mean = np.mean(arr, axis=0)
# print(np.mean(arr, axis=0))
# print(np.var(arr, axis=0))


#################################
## test write to file function
f = open("test.txt","a")
data1 = np.array([ 0.09672119, -0.02568009])
data2 = np.array([0.09938804, -0.02498509])
data3 = np.array([0.10093812, -0.06810719])
list = [data1, data2, data3]
print(type(list))
#for row in mean:
#	np.savetxt(f, row)
np.savetxt(f, list, fmt="%s")
f.write("\n")
np.savetxt(f, np.array(list), fmt="%s")
f.write("\n")
f.close()
print(type(np.array(list)))

a = np.arange(6).reshape(2,3)
#print(np.shape(a))
#print(a)

b = a[:,1]
#print(b)

list = [[],[],[]]
list[0] = a[:,0]
list[1] = a[:,1]
list[2] = a[:,2]
#print(list)

# import time
#print(time.time())

a = ["a","b","c"]

#for index, item in enumerate(a):
    #print(index)
    #print(item)

###############################
## check numpy version
# print(np.version.version)

###############################
## try out curve fit
# from scipy.optimize import curve_fit

# def eqn(x, a, b):
#     return (a*x) + b 


# arr = np.append(np.ones((1,3)), np.zeros((1,3)))

# popt, pcov = curve_fit(eqn, arr, arr)
# print(popt)
# print(pcov)
# a=1
# if a==1 :
#     print(1)

# str = "list"

# if str=="list":
#     print(str)