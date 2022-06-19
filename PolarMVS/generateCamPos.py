# -*-coding:utf-8-*-
import numpy as np
import random
def sphere_surface(R,phi,theta,center):
    # defaut center is (0,0,0)
    c_x,c_z,c_y = center
    x = R * np.sin(theta) * np.cos(phi) + c_x
    y = R * np.sin(theta) * np.sin(phi) + c_y
    z = R * np.cos(theta) + c_z

    return x,z,y # return point coordinates in mitsuba2
def generatePostions(phi_min,phi_max,theta_min,theta_max,num,R,center):
    # generate camera positions randomly
    positions = []
    for i in range(0,num):
        phi = random.randint(phi_min,phi_max)
        theta = random.randint(theta_min,theta_max)
        phi = phi*np.pi/180
        theta = theta*np.pi/180
        x,y,z = sphere_surface(R,phi,theta,center)
        positions.append([x,y,z])
    return positions
def generatePositionsUniform(phi_min,phi_max,phi_interval,theta,R,center):
    positions = []
    theta = theta * np.pi / 180

    num = int((phi_max-phi_min)/phi_interval)
    for i in range(0,num):
        phi = phi_min + i*phi_interval
        phi = phi*np.pi/180
        x,y,z = sphere_surface(R,phi,theta,center)
        positions.append([x,y,z])
    return positions


if __name__ =='__main__':
    theta_min = 20
    theta_max = 80
    phi_min = 0
    phi_max = 360
    R = 5
    center = [0,5,0]

    positions = generatePostions(0,360,0,80,20,R,center)
    print(positions)

