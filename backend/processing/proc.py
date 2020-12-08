#github: https://github.com/opencv/opencv_contrib/tree/master/modules/dnn_superres
#article: https://towardsdatascience.com/deep-learning-based-super-resolution-with-opencv-4fd736678066


import cv2
from cv2 import dnn_superres

sr = dnn_superres.DnnSuperResImpl_create()

image = cv2.imread('./examples/butterfly.png')
print("read image")

model_path = "./models/EDSR_x3.pb"
sr.readModel(model_path)
print("read model")
#"edsr" or "fsrcnn"
sr.setModel("edsr", 3)

print("starting upsampling")
result = sr.upsample(image)
print("finished upsampling")

print("saving file...")
cv2.imwrite("./examples/output/input_scaled.jpg", result)
print("finished with program, exiting...")
