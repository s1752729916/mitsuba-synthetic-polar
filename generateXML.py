# -*-coding:utf-8-*-
import xml.dom.minidom as xmldom
import numpy as np
import os

origXMLpath = '/media/smq/移动硬盘/blender/mesh_for_mitsuba/orig_pol.xml'
objectPath = '/media/smq/移动硬盘/blender/mesh_for_mitsuba/happy_vrip_front.ply'
outputRoot = '/media/smq/移动硬盘/Research/Synthetic-Polar/happy-vrip-front/xml'
outputNormalXml = '/media/smq/移动硬盘/Research/Synthetic-Polar/happy-vrip-front/normal-xml'

sample_count = 100
resolution_x = 500
resolution_y = 500
lookat_origin = '0.0000,   8.0000,    0.000'  # x,y,z    Y is the height of camera
lookat_target = '0.0,   0.0,   0.0'  # position of target
emitter_radiance = '1.0,  1.0,   1.0'

for theta in range(0,72):
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

    lookat_up = str(np.cos(np.deg2rad(theta*5))) + ',0,' + str(np.sin(np.deg2rad(theta*5)))
    lookat.setAttribute('origin',lookat_origin)
    lookat.setAttribute('target',lookat_target)
    lookat.setAttribute('up',lookat_up)

    #-- 3. set illumination
    emitter = elements.getElementsByTagName('emitter')[0]
    rgb = emitter.getElementsByTagName('rgb')[0]
    rgb.setAttribute('value',emitter_radiance)
    #-- 4. set object
    object = elements.getElementsByTagName('shape')[1]
    string = object.getElementsByTagName('string')[0]
    string.setAttribute('value',objectPath)

    #-- 5. save xml
    output_path = os.path.join(outputRoot,str(theta).zfill(3) + '-angles.xml')
    f = open(output_path, "w")
    f.write(dom.toprettyxml(indent=" "))
    f.close()
    print('processing file: %s' % output_path)

    #-- 6. save
    dom2 = dom
    elements = dom2.documentElement
    integrator = elements.getElementsByTagName('integrator')[0]
    elements.removeChild(integrator)
    integrator = dom2.createElement('integrator')
    integrator = elements.appendChild(integrator)
    integrator.setAttribute('type','aov')
    string = dom2.createElement('string')
    string = integrator.appendChild(string)
    string.setAttribute('name','aovs')
    string.setAttribute('value','dd.y:depth,nn:sh_normal')


    output_path = os.path.join(outputNormalXml, str(theta).zfill(3) + '-angles.xml')
    f = open(output_path, "w")
    f.write(dom2.toprettyxml(indent=" "))
    f.close()
    print('processing file: %s' % output_path)





