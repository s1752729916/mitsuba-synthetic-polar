# -*-coding:utf-8-*-
import xml.dom.minidom as xmldom
import numpy as np
import os
import glob
import json
import sys
from PolarMVS.generateCamPos import generatePostions

# 先用generateXML生成初始的XML文件，再generateNormals生成json文件，再用这个脚本生成新的xml
root = '/media/disk2/smq_data/samples/TransMVS/synthetic/cow-3'
origXml = '/media/disk2/smq_data/blender/mesh_for_mitsuba_mvs_reflection/orig_pol.xml'
objectPath = '/media/disk2/smq_data/blender/mesh_for_mitsuba_mvs_reflection/cow.ply'
outputNormalXml = '/media/disk2/smq_data/samples/TransMVS/synthetic/cow-3/normal-xml-2'

inputJson = os.path.join(root,'json')

outputRoot = os.path.join(root,'xml-2')
outputNormalRoot = os.path.join(root,'normal-xml-2')

Tc = np.linalg.inv(np.array([[0.141421,0.98995,0,0],[0,0,-1,5],[-0.98995,0.141421,0,0],[0,0,0,1]])) # 初始相机外参
print('Tc:',Tc)
searchStr = os.path.join(inputJson, '*.json')
jsonLists = sorted(glob.glob(searchStr))
num = len(jsonLists)
# 读取json文件

# 参数设置
sample_count = 512
resolution_x = 1232
resolution_y = 1028
for i in range(0,num):
    with open(jsonLists[i], 'r') as f:
        data = json.load(f)

    # 计算物体的外参
    extrinsic = (np.array(data[0]['extrinsic']))

    print('extrinsic:',extrinsic)
    To_ = np.matmul(extrinsic,Tc)
    To_ = np.linalg.inv(To_) # mitsuba2里的to_wolrd是local2world的
    print('To_',To_)
    # 保存新的xml文件
    dom = xmldom.parse(origXml)
    elements = dom.documentElement
    #-- 1. set render params(sample count,resolution)
    spp = elements.getElementsByTagName('default')[0]
    resx = elements.getElementsByTagName('default')[1]
    resy = elements.getElementsByTagName('default')[2]
    spp.setAttribute('value',str(sample_count))
    resx.setAttribute('value',str(resolution_x))
    resy.setAttribute('value',str(resolution_y))

    #-- 2. set object rotation

    object = elements.getElementsByTagName('shape')[1]
    to_world_element = dom.createElement("transform")
    to_world_element.setAttribute('name','to_world')
    matrix_element = dom.createElement('matrix')
    matrix_element.setAttribute('value',','.join(str(k) for k in To_.reshape(-1)))
    to_world_element.appendChild(matrix_element)
    object.appendChild(to_world_element)

    #-- 3. set object
    string = object.getElementsByTagName('string')[0]
    string.setAttribute('value',objectPath)

    #-- save xml file
    output_path = os.path.join(outputRoot,str(i).zfill(3) + '-view.xml')
    # output_path = '/media/disk2/smq_data/samples/TransMVS/test-output.xml'
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
    ball = elements.getElementsByTagName('shape')[2]

    elements.removeChild(cube)
    elements.removeChild(ball)

    output_path = os.path.join(outputNormalXml,str(i).zfill(3) + '-view.xml')
    f = open(output_path, "w")
    f.write(dom2.toprettyxml(indent=""))
    f.close()
    print('processing file: %s' % output_path)


