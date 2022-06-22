# -*-coding:utf-8-*-
import os
import sys
import matplotlib.pyplot as plt
sys.path.append('/media/disk2/smq_data/mitsuba2/build/dist/python/')
import glob
import mitsuba
mitsuba.set_variant('scalar_spectral')
mitsuba.core.set_thread_count(32)

import numpy as np
import enoki as ek
from mitsuba.core.xml import load_file
import xml.dom.minidom as xmldom
from mitsuba.core import Bitmap, Struct
import json
import imageio
import re
class __Autonomy__(object):
    def __init__(self):
        """
         init
         """
        self._buff = ""
    def write(self, out_stream):
        """
         :param out_stream: :
         return: """
        self._buff += out_stream

def getSensorTransform(sensor):
    current = sys.stdout
    m_out = __Autonomy__()
    sys.stdout = m_out
    print(sensor.world_transform())
    sys.stdout = current
    A = m_out._buff[37:].split(',')
    nums = []
    for a in A:
        m = re.search(r'[-+]?\d+\.\d+([Ee]-?\d+)?', a)
        if(m is not None):
            nums.append(float(m.group()))
        else:
            m = re.findall(r'-?\d+',a)
            if(len(m)==1):
                nums.append(float(m[0]))
    transform = np.array(nums).reshape([4,4])
    return transform

root = '/media/disk2/smq_data/samples/TransMVS/synthetic/cow-3'
normal_xml_path = os.path.join(root,'normal-xml')
#-- 1. get all xml files
xml_list = glob.glob(os.path.join(normal_xml_path,'*.xml'))
print('found %d xml files.' % len(xml_list))

#-- 2. process files
for i in range(0,len(xml_list)):
    #-- (1). render polarization
    xml_file = os.path.join(normal_xml_path,str(i).zfill(3)+'-view.xml')
    scene = load_file(xml_file)
    sensor = scene.sensors()[0]
    transform = getSensorTransform(sensor)
    print('world_transform',sensor.world_transform())
    print('transform:\n',transform)



    #-- 4. get intrinsic/extrinsic matrix
    dom = xmldom.parse(xml_file)
    elements = dom.documentElement
    resx_dom = elements.getElementsByTagName('default')[1]
    resy_dom = elements.getElementsByTagName('default')[2]
    fov_dom = elements.getElementsByTagName('float')[0]
    lookat = elements.getElementsByTagName('lookat')[0]
    lookat_origin = lookat.getAttribute('origin')
    lookat_target = lookat.getAttribute('target')
    lookat_up = lookat.getAttribute('up')

    resx = resx_dom.getAttribute('value')
    resy = resy_dom.getAttribute('value')
    fov = fov_dom.getAttribute('value')

    transform = transform.tolist()   # local to world transform(cam to world)
    data = [{'intrinsic':[{'fov':fov,'resx':resx,'resy':resy}],'extrinsic':transform,'extrinsic_lookat':[{'origin':lookat_origin,'target':lookat_target,'up':lookat_up}]}]
    jsonData = json.dumps(data,indent=1)
    #-- 5. save json files
    json_output_path = os.path.join(os.path.join(root,'json'),str(i).zfill(3)+'-view.json')
    file = open(json_output_path,'w')
    file.write(jsonData)
    file.close()











# -*-coding:utf-8-*-
