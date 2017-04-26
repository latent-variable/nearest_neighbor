import sys
import math
from math import sqrt
import re
import time


pointRE=re.compile("(-?\\d+.?\\d*)\\s(-?\\d+.?\\d*)")

def dist(p1 , p2 ):
    return sqrt(pow(p1[0]-p2[0],2) + pow(p1[1]-p2[1],2))

#Run the divide-and-conquor nearest neighbor 
def nearest_neighbor(points):
    return nearest_neighbor_recursion(points)

#function used in nearest_reighbor_recursion
def split_list(alist):
    half = len(alist)/2
    return alist[:half], alist[half:]
#Brute force version of the nearest neighbor algorithm, O(n**2)
#returns shordest distance and the two points 
def brute_force_nearest_neighbor(points):       #Naive implementation 
    min_distance = 9e999
    for i  in range(0,len(points)):
        for j in range(i+1,len(points)):
            if points[i] != points[j]:
                tmp_distance = dist(points[i],points[j])
            if tmp_distance < min_distance:
                min_distance = tmp_distance
                tmp_point1 = points[i]
                tmp_point2 = points[j]
    return  tmp_point1, tmp_point2, min_distance

#only returns the shorthes distance to be used in with the divide andconquere implementation  
def brute_force_nearest_neighbor2(points):        
    min_distance = 9e999
    for i  in range(0,len(points)):
        for j in range(i+1,len(points)):
            if points[i] != points[j]:
                tmp_distance = dist(points[i],points[j])
            if tmp_distance < min_distance:
                min_distance = tmp_distance
    return  min_distance

#divide and conquere implementaion 
def nearest_neighbor_recursion(points):
    min_distance=9e999
    
    if len(points) <= 3:
        return brute_force_nearest_neighbor2(points)
    
    
    mid = len(points)/2
    midpoint = points[mid]
    B , A = split_list(points)
   
    #2 recursive calls to itself one for the left and one for the right logn
    distance_left = nearest_neighbor_recursion(B)
    distance_right = nearest_neighbor_recursion(A)
    
    #print(distance_left,distance_right)
    distance_temp = min(distance_left,distance_right)
    if min_distance > distance_temp:
        min_distance = distance_temp
    
    #check all the points in middle that have a distance less then  the min distance
    mid_set = []
    for i in range(0,len(points)):
        if (abs(points[i][0]-midpoint[0]) < min_distance ):
            mid_set.append(points[i]) 
    '''        
    print("mid point: ", midpoint)
    print("mid set: ", mid_set)
    print("min distance: ", min_distance)
    '''
    return min(min_distance,brute_force_nearest_neighbor2(mid_set))

def read_file(filename):
    points=[]
    # File format
    # x1 y1
    # x2 y2
    # ...
    in_file=open(filename,'r')
    for line in in_file.readlines():
        line = line.strip()
        point_match=pointRE.match(line)
        if point_match:
            x = point_match.group(1)
            y = point_match.group(2)
            points.append((float(x),float(y))) #much easier to add float types
    #print(points)
    return points

def main(filename,algorithm):
    algorithm=algorithm
    points=read_file(filename)
    #print("Before sort", points)
    #sorted(points, key=getKey)
    points.sort()
    #print("after sort", points)
    name,w = filename.split('.')
    f = open( name +'_distance.txt', 'w')
    f.write("Shortes distance found between the points ")
    if algorithm =="dc":
        d = nearest_neighbor(points)
        print("Divide and Conquer: "+  str(d) )
        f.write(str(d))
    elif algorithm == "bf":
        point1,point2,d = brute_force_nearest_neighbor(points)
        print("Brute Force: "+ str(d) )
        f.write(str(point1)+" and "+str(point2) + "\n")
        f.write("Brute Force: "+ str(d))
        
    elif algorithm == "both":
        d1 = nearest_neighbor(points)
        point1,point2,d2 = brute_force_nearest_neighbor(points)
        print("Divide and Conquer: "+ str(d1) )
        print("Brute Force: "+ str(d2) )
        f.write(str(point1)+" and "+str(point2) + "\n")
        f.write("Divide and Conquer: "+ str(d1)+"\n")
        f.write("Brute Force: "+ str(d2))
    else: 
        print("Does not apply")
    f.close()
   
if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("python assignment1.py -<dc|bf|both> <input_file>")
        quit(1)
    if len(sys.argv[1]) < 2:
        print("python assignment1.py -<dc|bf|both> <input_file>")
        quit(1)
    main(sys.argv[2],sys.argv[1])
