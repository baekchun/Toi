import cv2
import numpy as np

# parameters for canny, dilate, erode and mask color
BLUR = 21
CANNY_THRESH_1 = 20
CANNY_THRESH_2 = 20
MASK_DILATE_ITER = 10
MASK_ERODE_ITER = 10

# In BGR format
MASK_COLOR = (0.0,0.0,0.0)

# load image
img = cv2.imread('images/blood_in_stool_sample(2).jpg')

# convert image to greyscale
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

# Use Canny Edge Detection to detect edges in this image
edges = cv2.Canny(gray, CANNY_THRESH_1, CANNY_THRESH_2)
edges = cv2.dilate(edges, None)
edges = cv2.erode(edges, None)

# Find all contours among the dimage
contour_info = []
_, contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

# Iterate through contours and find the largest contour
for c in contours:
    contour_info.append((
        c,
        cv2.isContourConvex(c),
        cv2.contourArea(c),
    ))

contour_info = sorted(contour_info, key=lambda x: x[2], reverse=True)

# Draw a rectangle over the largest contour
print (contour_info[0][0], contour_info[0][0].shape)
x, y, width, height =cv2.boundingRect(contour_info[0][0])
print (x, y, width, height)

# crop the rectangle from the original image, i.e. zoom in
roi = img[y:y+height, x:x+width]
cv2.imwrite("images/masked(1).jpg", roi)
"""
# create empty mask, and fill the area with largest contour
mask = np.zeros(edges.shape)
cv2.fillConvexPoly(mask, contour_info[0][0], (255,) * img.shape[2])

# perform erosion and dilation to remove any small areas where noise are
# coming from
mask = cv2.dilate(mask, None, iterations=MASK_DILATE_ITER)
mask = cv2.erode(mask, None, iterations=MASK_ERODE_ITER)
mask = cv2.GaussianBlur(mask, (BLUR, BLUR), 0)
mask_stack = np.dstack([mask] * 3)

# Modify the masked area to be filled in with MASK_COLOR and combine with
# the original image
mask_stack = mask_stack.astype('float32') / 255.0
img = img.astype('float32') / 255.0
masked = (mask_stack * img) + ((1-mask_stack) * MASK_COLOR)
masked = (masked * 255).astype('uint8')

cv2.imwrite("images/masked(1).jpg", masked)

# show the image
# cv2.namedWindow("img", 0)
# cv2.imshow('img', masked)
# cv2.resizeWindow('img', 600,600)
# cv2.waitKey(4000)
"""