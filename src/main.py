import cv2
from camera import Camera, tone_map
from primitives import point, Box
from utils import timed
from datetime import datetime
from bvh import BoundingVolumeHierarchy, triangles_for_box
from load import load_obj
from bidirectional import bidirectional_screen_sample
from unidirectional import unidirectional_screen_sample
from constants import Material

WINDOW_WIDTH = 320
WINDOW_HEIGHT = 180
SAMPLE_COUNT = 100


if __name__ == '__main__':
    camera = Camera(center=point(0, 2, 5), direction=point(0, 0, -1), pixel_height=WINDOW_HEIGHT,
                    pixel_width=WINDOW_WIDTH, phys_width=WINDOW_WIDTH / WINDOW_HEIGHT, phys_height=1.)
    # + load_obj('../resources/teapot.obj', material=Material.SPECULAR.value)
    bvh = BoundingVolumeHierarchy(
        triangles_for_box(Box(point(-10, -3, -10), point(10, 17, 10))) )#+ load_obj('../resources/teapot.obj', material=Material.DIFFUSE.value))

    try:
        for n in range(SAMPLE_COUNT):
            bidirectional_screen_sample(camera, bvh.root.box, 1)
            print('sample', n, 'done')
            cv2.imshow('render', tone_map(camera))
            cv2.waitKey(1)
    except KeyboardInterrupt:
        print('stopped early')
    else:
        print('done')
    cv2.imwrite('../renders/%s.jpg' % datetime.now(), tone_map(camera))


# performance test unidirectional 200x200 10 samples
# parallel_pixel_capture - 33.9686
# parallel_capture - 33.8465
# single_threaded_capture - 44.5569

# todo: Feature Schedule
#  - Bidirectional largely implemented, just need to understand the 1/N 1/Nk stuff and correct geometry term issues
#  - I made a lot of changes. i should revert to unidirectional and make sure everything still works at a basic level

#  - normal smoothing
#  - textures

# todo: Tech Debt
#  - Automated tests
#  - jit OBJ loading and bvh construction, eliminate TreeBox class

# todo: Known Bugs
#  - sample 0 does not display properly
