# -*-coding:utf-8-*-
import os
import sys
import matplotlib.pyplot as plt
sys.path.append('/home/smq/mitsuba2/build/dist/python')
import glob
import mitsuba
mitsuba.set_variant('scalar_spectral')
import numpy as np
import enoki as ek
from mitsuba.core.xml import load_file
import xml.dom.minidom as xmldom
from mitsuba.core import Bitmap, Struct
import json
import imageio
import re
class __Autonomy__(object):
    """ 自定义变量的write方法 """
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

root = '/media/smq/移动硬盘/Research/TransMVS/synthetic/bear'
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
    # print('transform:\n',transform)
    scene.integrator().render(scene, sensor)
    film = sensor.film()

    from mitsuba.core import Bitmap, Struct

    img = film.bitmap(raw = False)
    img_np = np.array(img).astype(np.float32)
    import matplotlib.pyplot as plt

    x = img_np[:, :, 5]  # world space
    y = img_np[:, :, 6]
    z = img_np[:, :, 7]
    temp = np.ndarray([3, x.shape[0], x.shape[1]])
    temp[0, :, :] = x
    temp[1, :, :] = y
    temp[2, :, :] = z
    temp = temp.reshape([3,-1])
    temp = np.matmul(np.linalg.inv(transform[0:3,0:3]),temp)  # to camera space
    temp = temp.reshape([3,x.shape[0],-1])
    # for row in range(0, x.shape[0]):
    #     for col in range(0, x.shape[1]):
    #         temp[:, row, col] = np.matmul(np.linalg.inv(transform), temp[:, row, col])
    normals = np.ndarray([x.shape[0], x.shape[1], 3])
    x = temp[0, :, :]
    y = temp[1, :, :]
    z = temp[2, :, :]
    normals[:, :, 0] = -x
    normals[:, :, 1] = y
    normals[:, :, 2] = -z

    normal_uint8 = ((normals + 1)*127.5).astype(np.uint8)
    mask = np.ndarray(x.shape,dtype=np.uint8)
    mask[:,:] = 255
    mask[np.where((x==0) & (y==0) &(z==0))] = 0



    #-- (3). save pictures
    normal_output_path = os.path.join(os.path.join(root,'normals-png'),str(i).zfill(3)+'-view.png')
    exr_output_path = os.path.join(os.path.join(root,'normals-exr'),str(i).zfill(3)+'-angles.exr')
    mask_output_path = os.path.join(os.path.join(root,'masks'),str(i).zfill(3)+'-view.png')

    imageio.imwrite(normal_output_path,normal_uint8)
    imageio.imwrite(mask_output_path,mask)
    film.set_destination_file(exr_output_path)
    film.develop()

    #-- 4. get intrinsic/extrinsic matrix
    dom = xmldom.parse(xml_file)
    elements = dom.documentElement
    resx_dom = elements.getElementsByTagName('default')[1]
    resy_dom = elements.getElementsByTagName('default')[2]
    fov_dom = elements.getElementsByTagName('float')[0]
    resx = resx_dom.getAttribute('value')
    resy = resy_dom.getAttribute('value')
    fov = fov_dom.getAttribute('value')

    transform = transform.tolist()   # local to world transform(cam to world)
    data = [{'intrinsic':[{'fov':fov,'resx':resx,'resy':resy}],'extrinsic':transform}]
    jsonData = json.dumps(data,indent=1)
    #-- 5. save json files
    json_output_path = os.path.join(os.path.join(root,'json'),str(i).zfill(3)+'-view.json')
    file = open(json_output_path,'w')
    file.write(jsonData)
    file.close()











# -*-coding:utf-8-*-
