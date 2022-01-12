import matplotlib.pyplot as plt
import sys

sys.path.append('/home/smq/mitsuba2/build/dist/python')
import os
import enoki as ek
import mitsuba
import  numpy as np
# Set the desired mitsuba variant
mitsuba.set_variant('packet_spectral')

from mitsuba.core import Float, Vector3f, Thread, xml
from mitsuba.core.xml import load_file
from mitsuba.render import (BSDF, BSDFContext, BSDFFlags,
                            DirectionSample3f, Emitter, ImageBlock,
                            SamplingIntegrator, has_flag,
                            register_integrator)
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





    # nums = [float(s) for s in re.findall(r'-?\d+', m_out._buff)]

    transform = np.array(nums).reshape([4,4])[0:3,0:3]
    return transform


# Load an XML file which specifies "mydirectintegrator" as the scene's integrator
filename = '/media/smq/移动硬盘/Research/Synthetic-Polar/plastic-cup/normal-xml/000-angles.xml'
Thread.thread().file_resolver().append(os.path.dirname(filename))
scene = load_file(filename)
print(scene.sensors()[0])

# R_0 = getSensorTransform(scene.sensors()[0])
# a = [0,1,0,0,0,-1,-1,0,0]
# R_0 = np.array(a).reshape([3,3])
# a = [1,0,0,0,0,-1,0,1,0]
# R_90 = np.array(a).reshape([3,3])
# a = [0.707,0.707,0,0,0,-1,-0.707,0.707,0]
# R_45 = np.array(a).reshape([3,3])

transform =getSensorTransform(sensor=scene.sensors()[0])
print('camera to world transform:\n',transform)
scene.integrator().render(scene, scene.sensors()[0])

film = scene.sensors()[0].film()
img = film.bitmap(raw = False)
img_np = np.array(img).astype(np.float32)
depth = img_np[:,:,4]
x = img_np[:, :, 5]
y = img_np[:, :, 6]
z = img_np[:, :, 7]
temp = np.ndarray([3,x.shape[0], x.shape[1]])
temp[0,:,:] = x
temp[1,:,:] = y
temp[2,:,:] = z

for row in range(0,x.shape[0]):
    for col in range(0,x.shape[1]):
        temp[:,row,col] = np.matmul(np.linalg.inv(transform),temp[:,row,col])

print(temp.shape)
x = temp[0,:,:]
y = temp[1,:,:]
z = temp[2,:,:]


normals = np.ndarray([x.shape[0], x.shape[1], 3])
normals[:, :, 0] = -x
normals[:, :, 1] = y
normals[:, :, 2] = -z
normals[np.where((x == -1) & (z == -1) & (y == 1))] = -1
# m_transform = np.ndarray([[1.22465e-16, -1, 0],
#                    [0, 0, -1],
#                    [1, 1.22465e-16,0 ]])
normal_uint8 = ((normals + 1) * 127.5).astype(np.uint8)
normal_uint8[np.where((normal_uint8[:,:,0] == 127) & (normal_uint8[:,:,1] == 255) & (normal_uint8[:,:,0] == 127))] = 0

plt.imshow(normal_uint8)
plt.show()


