import cv2
import numpy as np

image = cv2.imread("images/blood_in_stool_sample.jpg")

# make the image smaller for viewing purpose
image = cv2.resize(image, (500, 375))

# set range of color RED
# Note: numpy takes the values in the order of BGR, not RGB
lower = np.array([17, 15, 100], dtype = "uint8")
upper = np.array([50, 56, 200], dtype = "uint8")

# mask the non-red parts of an image
mask = cv2.inRange(image, lower, upper)
output = cv2.bitwise_and(image, image, mask=mask)

# show the image
cv2.imshow("image", np.hstack([image, output]))





# open for 13 seconds and close
cv2.waitKey(13000)
cv2.destroyAllWindows()
