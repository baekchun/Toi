import cv2

# img = cv2.imread('images/blood_in_stool_sample(2).jpg')

def get_type(count):
	if count < 10:
		return "Type II"
	elif count > 10:
		return "Type I" 
	else:
		return "None found"

def count_blobs(image):
	img = cv2.imread(image)
	
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

	# contour_info = sorted(contour_info, key=lambda x: x[2], reverse=True)
	count = 0
	
	# set the minimum contour area
	min_contour_area = 50

	for i in range(len(contour_info)):
		contour_area = contour_info[i][2]

		# count only if the area is greater than the min area
		if contour_area > 50:
			count += 1

	return count

# print (count)
# print (cv2.arcLength(contour_info[-1][0], True))
# print (len(contours))
# cv2.namedWindow("img", 0)
# cv2.imshow('img', img)
# cv2.resizeWindow('img', 600,600)
# cv2.waitKey(5000)