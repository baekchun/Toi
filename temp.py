import numpy as np
import cv2

img = cv2.imread("images/stool_sample(1).jpg", 0)

_, contours, _ = cv2.findContours(img, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
contour_info = []
# The index of the contour that surrounds your object
for c in contours:
    contour_info.append((
        c,
        cv2.isContourConvex(c),
        cv2.contourArea(c),
    ))

contour_info = sorted(contour_info, key=lambda x: x[2], reverse=True)

mask = np.zeros_like(img) # Create mask where white is what we want, black otherwise
cv2.drawContours(mask, contours, 0, 255, -1) # Draw filled contour in mask
out = np.zeros_like(img) # Extract out the object and place into output image
out[mask == 255] = img[mask == 255]

# Now crop
(x, y) = np.where(mask == 255)
(topx, topy) = (np.min(x), np.min(y))
(bottomx, bottomy) = (np.max(x), np.max(y))
out = out[topx:bottomx+1, topy:bottomy+1]

# Show the output image
cv2.imshow('Output', out)
cv2.waitKey(5000)