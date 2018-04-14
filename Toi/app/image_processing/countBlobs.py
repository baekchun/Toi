import cv2

img = cv2.imread('images/stool_sample(2).jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

ret, thresh = cv2.threshold(gray, 100, 255, 1)
_, contours,h = cv2.findContours(
    thresh,
    cv2.RETR_EXTERNAL,
    cv2.CHAIN_APPROX_SIMPLE
)

total_len_contours = 0
contour_info = []

for cnt in contours:
    cv2.drawContours(img,[cnt],0,(0,0,255),1)

    contour_info.append((
        cnt,
        cv2.isContourConvex(cnt),
        cv2.contourArea(cnt),
    ))

contour_info = sorted(contour_info, key=lambda x: x[2], reverse=True)
print (cv2.arcLength(contour_info[0][0], True))
print (len(contours))
cv2.namedWindow("img", 0)
cv2.imshow('img', img)
cv2.resizeWindow('img', 600,600)
cv2.waitKey(4000)