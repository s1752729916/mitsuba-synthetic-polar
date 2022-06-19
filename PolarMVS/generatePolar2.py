# -*-coding:utf-8-*-
# -*-coding:utf-8-*-
import os
import sys
import matplotlib.pyplot as plt
sys.path.append('/media/disk2/smq_data/mitsuba2/build/dist/python/')
import glob
import mitsuba
mitsuba.set_variant('scalar_spectral_polarized')
mitsuba.core.set_thread_count(32)
import numpy as np
import enoki as ek
from mitsuba.core.xml import load_file
import xml.dom.minidom as xmldom
from mitsuba.core import Bitmap, Struct
import imageio
root = '/media/disk2/smq_data/samples/TransMVS/synthetic/hemi-sphere-big'
xml_path = os.path.join(root,'xml')
#-- 1. get all xml files
xml_list = glob.glob(os.path.join(xml_path,'*.xml'))
print('found %d xml files.' % len(xml_list))

#-- 2. process files
for i in range(0,len(xml_list)):
    #-- (1). render polarization
    xml_file = os.path.join(xml_path,str(i).zfill(3)+'-view.xml')
    dom = xmldom.parse(xml_file)
    scene = load_file(xml_file)
    sensor = scene.sensors()[0]
    scene.integrator().render(scene, sensor)
    film = sensor.film()
    img = film.bitmap()
    img_np = np.array(img).astype(np.float32)
    s0 = img_np[:, :, 4]
    s1 = img_np[:, :, 7]
    s2 = img_np[:, :, 10]
    s3 = img_np[:, :, 13]
    DoLP = np.sqrt(s1 ** 2 + s2 ** 2) / s0
    DoLP[np.where(np.isnan(DoLP))] = 0
    AoLP = 1 / 2.0 * np.arctan2(s2, s1)
    dolp_uint8 = (DoLP*255).astype(np.uint8)
    aolp_uint8 = (((np.round(AoLP*180/np.pi)%180)/180.0)*255).astype(np.uint8)

    #-- (2). get I_0,I_45,I_90,I_135

    I_sum = s0

    I_0 = I_sum/2.0 + DoLP * I_sum * np.cos(2*(AoLP-0))
    I_45 = I_sum/2.0 + DoLP * I_sum * np.cos(2*(AoLP-np.pi/4.0))
    I_90 = I_sum/2.0 + DoLP * I_sum * np.cos(2*(AoLP-np.pi/2.0))
    I_135 = I_sum/2.0 + DoLP * I_sum * np.cos(2*(AoLP-3*np.pi/4.0))

    I_sum_uint8 = np.round(I_sum*255).astype(np.uint8)
    I_0_uint8 = np.round(I_0*255).astype(np.uint8)
    I_45_uint8 = np.round(I_45*255).astype(np.uint8)
    I_90_uint8 = np.round(I_90*255).astype(np.uint8)
    I_135_uint8 = np.round(I_135*255).astype(np.uint8)

    #-- (3). save pictures
    I_0_output_path = os.path.join(os.path.join(root,'I-0'),str(i).zfill(3)+'-view.png')
    I_45_output_path = os.path.join(os.path.join(root,'I-45'),str(i).zfill(3)+'-view.png')
    I_90_output_path = os.path.join(os.path.join(root,'I-90'),str(i).zfill(3)+'-view.png')
    I_135_output_path = os.path.join(os.path.join(root,'I-135'),str(i).zfill(3)+'-view.png')
    I_sum_output_path = os.path.join(os.path.join(root,'I-sum'),str(i).zfill(3)+'-view.png')
    DoLP_output_path = os.path.join(os.path.join(os.path.join(root,'params'),'DoLP'),str(i).zfill(3)+'-view.png')
    AoLP_output_path = os.path.join(os.path.join(os.path.join(root,'params'),'AoLP'),str(i).zfill(3)+'-view.png')

    imageio.imwrite(I_0_output_path,I_0_uint8)
    imageio.imwrite(I_45_output_path,I_45_uint8)
    imageio.imwrite(I_90_output_path,I_90_uint8)
    imageio.imwrite(I_135_output_path,I_135_uint8)
    imageio.imwrite(I_sum_output_path,I_sum_uint8)
    imageio.imwrite(DoLP_output_path,dolp_uint8)
    imageio.imwrite(AoLP_output_path,aolp_uint8)










