import base64
import sys
import cv2
import numpy as np
def to_base64(img):

    _, buf = cv2.imencode(".png", img)



    return base64.b64encode(buf)





def from_base64(buf):

    buf_decode = base64.b64decode(buf)



    buf_arr = np.frombuffer(bytearray(buf_decode), dtype=np.uint8)



    return cv2.imdecode(buf_arr, cv2.IMREAD_UNCHANGED)





img = cv2.imread("examples/butterfly.png")

img_base64 = to_base64(img)

img_decoded = from_base64(img_base64)

with open('examples/output.png', 'w') as f:
    f.write(img_decoded)

print(img_decoded.shape)
