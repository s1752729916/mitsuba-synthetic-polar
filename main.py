

import sys

import matplotlib.pyplot as plt

sys.path.append('/home/smq/mitsuba2/build/dist/python')
import mitsuba
import numpy as np
import enoki as ek
mitsuba.set_variant('scalar_rgb')

from mitsuba.core.xml import load_file
scene = load_file('/media/smq/移动硬盘/blender/transparent3.xml')

# Get the scene's sensor (if many, can pick one by specifying the index)
sensor = scene.sensors()[0]


# Call the scene's integrator to render the loaded scene with the desired sensor
scene.integrator().render(scene, sensor)

film = sensor.film()

from mitsuba.core import Bitmap, Struct
img = film.bitmap(raw=True).convert(Bitmap.PixelFormat.RGB, Struct.Type.UInt8, srgb_gamma=True)
img_np = np.array(img)
import matplotlib.pyplot as plt
plt.imshow(img_np)
plt.show()

