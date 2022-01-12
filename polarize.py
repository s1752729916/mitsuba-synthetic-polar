# -*-coding:utf-8-*-

import sys

import matplotlib.pyplot as plt

sys.path.append('/home/smq/mitsuba2/build/dist/python')
import mitsuba
import numpy as np
import enoki as ek
mitsuba.set_variant('scalar_spectral_polarized')

from mitsuba.core.xml import load_file
scene = load_file('/media/smq/移动硬盘/Research/Synthetic-Polar/tiny-white-cup-edges/xml/angle-0.xml')

# Get the scene's sensor (if many, can pick one by specifying the index)
sensor = scene.sensors()[0]

# Call the scene's integrator to render the loaded scene with the desired sensor
scene.integrator().render(scene, sensor)

film = sensor.film()

from mitsuba.core import Bitmap, Struct
img = film.bitmap()
img_np = np.array(img).astype(np.float32)
print(img)
# 5，6，7 is s0, 8 9 10 is s1
s0 = img_np[:,:,4]
s1 = img_np[:,:,7]
s2 = img_np[:,:,10]
s3 = img_np[:,:,13]

# lculate dolp and aolp
DoLP = np.sqrt(s1**2 + s2**2)/s0
DoLP[np.where(np.isnan(DoLP))] = 0
AoLP = 1/2.0*np.arctan2(s2,s1)
fig = plt.figure()
ax0 = plt.subplot(121)
ax0.imshow(DoLP,cmap='gray')
ax1 = plt.subplot(122)
ax1.imshow(AoLP,cmap='gray')


plt.figure(figsize=(5, 5))
plt.imshow(s0, cmap='gray', vmin=0, vmax=1) # TODO: correct linear -> sRGB conversion
plt.colorbar()
plt.xticks([]); plt.yticks([])
plt.xlabel("S0: Intensity", size=14, weight='bold')

def plot_stokes_component(ax, data):
    plot_minmax = 0.05*max(np.max(data), np.max(-data)) # Arbitrary scale for colormap
    img = ax.imshow(data, cmap='coolwarm', vmin=-plot_minmax, vmax=+plot_minmax)
    ax.set_xticks([]); ax.set_yticks([])
    return img
fig, ax = plt.subplots(ncols=3, figsize=(18, 5))
img = plot_stokes_component(ax[0], s1)
plt.colorbar(img, ax=ax[0])
img = plot_stokes_component(ax[1], s2)
plt.colorbar(img, ax=ax[1])
img = plot_stokes_component(ax[2], s3)
plt.colorbar(img, ax=ax[2])

ax[0].set_xlabel("S1: Horizontal vs. vertical", size=14, weight='bold')
ax[1].set_xlabel("S2: Diagonal", size=14, weight='bold')
ax[2].set_xlabel("S3: Circular", size=14, weight='bold')

plt.show()



