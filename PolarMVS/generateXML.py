# -*-coding:utf-8-*-
import xml.dom.minidom as xmldom
import numpy as np
import os
from PolarMVS.generateCamPos import generatePostions
# params setup
origXMLpath = '/media/disk2/smq_data/blender/mesh_for_mitsuba_mvs/orig-polar-server.xml'
objectPath = '/media/disk2/smq_data/blender/mesh_for_mitsuba_mvs/meshes/cow.ply'
outputRoot = '/media/disk2/smq_data/samples/TransMVS/synthetic/cow-3/xml'
outputNormalXml = '/media/disk2/smq_data/samples/TransMVS/synthetic/cow-3/normal-xml'

sample_count = 512
resolution_x = 1232
resolution_y = 1028
lookat_origin = '0.0000,   8.0000,    0.000'  # x,y,z    Y is the height of camera
lookat_target = '0.0,   5.0,   0.0'  # position of target
lookat_up = '0.0,    1.0,    0.0'


# generate camera positions
theta_min = 40
theta_max = 80
phi_min = 0
phi_max = 360
R = 7
center = [0, 5, 0]
numOfPositions = 40
positions = generatePostions(theta_min=theta_min,theta_max=theta_max,phi_min=phi_min,phi_max=phi_max,R=R,center=center,num=numOfPositions)
# positions = generatePositionsUniform(phi_min,phi_max,20,80,R,center)
# generate xml files
for i in range(0,len(positions)):
    lookat_origin = str(positions[i][0]) +','+ str(positions[i][1]) +','+ str(positions[i][2])

    dom = xmldom.parse(origXMLpath)
    elements = dom.documentElement

    #-- 1. set render params(sample count,resolution)
    spp = elements.getElementsByTagName('default')[0]
    resx = elements.getElementsByTagName('default')[1]
    resy = elements.getElementsByTagName('default')[2]
    spp.setAttribute('value',str(sample_count))
    resx.setAttribute('value',str(resolution_x))
    resy.setAttribute('value',str(resolution_y))

    #-- 2. sensor setting: rotate camera
    lookat = elements.getElementsByTagName('lookat')[0]
    lookat.setAttribute('origin',lookat_origin)
    lookat.setAttribute('target',lookat_target)
    lookat.setAttribute('up',lookat_up)

    #-- 3. set object
    object = elements.getElementsByTagName('shape')[1]
    string = object.getElementsByTagName('string')[0]
    string.setAttribute('value',objectPath)

    #-- 5. save xml
    output_path = os.path.join(outputRoot,str(i).zfill(3) + '-view.xml')
    f = open(output_path, "w")
    f.write(dom.toprettyxml(indent=" "))
    f.close()
    print('processing file: %s' % output_path)

    #-- 6. save normal-xml
    dom2 = dom
    elements = dom2.documentElement
    integrator = elements.getElementsByTagName('integrator')[0]
    elements.removeChild(integrator)
    # change integrator to aov
    integrator = dom2.createElement('integrator')
    integrator = elements.appendChild(integrator)
    integrator.setAttribute('type','aov')
    string = dom2.createElement('string')
    string = integrator.appendChild(string)
    string.setAttribute('name','aovs')
    string.setAttribute('value','dd.y:depth,nn:sh_normal')

    # delete other models
    cube = elements.getElementsByTagName('shape')[0]
    elements.removeChild(cube)


    output_path = os.path.join(outputNormalXml,str(i).zfill(3) + '-view.xml')
    f = open(output_path, "w")
    f.write(dom2.toprettyxml(indent=""))
    f.close()
    print('processing file: %s' % output_path)