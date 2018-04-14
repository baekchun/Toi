import cv2
import numpy as np
import math


def read_image():
    """
    read in an image as an array
    """
    image = cv2.imread("images/blood_in_stool_sample.jpg")
    
    # make the image smaller for viewing purpose
    image = cv2.resize(image, (500, 375))

    return image

def saturate(matrix, v_min, v_max):
    """
    the pixels are updated to v_min if the pixel is lower than v_min and
    similarly they are updated to v_max if the pixel is higher than v_max
    """
    min_mask = matrix < v_min
    matrix = np.ma.array(matrix, mask=min_mask, fill_value=v_min)

    max_mask = matrix > v_max
    matrix = np.ma.array(matrix, mask=max_mask, fill_value=v_max)

    return matrix

def color_balance(img, saturation_level):
    """
    The goal is to scale each color channel(red, green blue) to make each of them
    span from 0 to 255 range.
    Reference used: http://web.stanford.edu/~sujason/ColorBalancing/simplestcb.html
    and http://www.ipol.im/pub/art/2011/llmps-scb/article.pdf
    """

    # split the image into B, G, R channels
    channels = cv2.split(img)

    new_channels = []

    # for each channel find the low and high percentile values 
    for channel in channels:

        # vector size = width * height
        vector_size = channel.shape[1] * channel.shape[0]

        # flatten the channel vector
        flattened = channel.reshape(vector_size)

        # sort the pixel values
        flattened = np.sort(flattened)

        # get the number of columns of flattened vector
        columns = len(flattened)
        
        # find lower and upper bound that correspond to our desired saturation level 
        # v_min and v_max are essentially the saturation extrema
        v_min  = flattened[math.floor(columns * saturation_level)]
        v_max = flattened[math.ceil(columns * (1.0 - saturation_level) - 1)]

        print ("v_min: ", v_min)
        print ("v_max: ", v_max)

        # saturate the pixels based on the quantiles of the pixel values distribution
        saturated = saturate(channel, v_min, v_max)

        # normalize each channel to span the full 0 to 255 range
        normalized = cv2.normalize(saturated, saturated.copy(), 0, 255, cv2.NORM_MINMAX)
        new_channels.append(normalized)

    # combine the channels back together
    return cv2.merge(new_channels)

def detect_color(image):

    # set range of color RED
    # Note: numpy takes the values in the order of BGR, not RGB
    lower = np.array([7, 5, 90], dtype = "uint8")
    upper = np.array([60, 66, 210], dtype = "uint8")

    # mask the non-red parts of an image
    mask = cv2.inRange(image, lower, upper)
    output = cv2.bitwise_and(image, image, mask=mask)
    print (output.shape)

    no_red = cv2.countNonZero(mask)
    print('The number of red pixels is: ' + str(no_red))

    # display the image
    cv2.imshow("image", np.hstack([image, output]))

    # open window for 10 seconds and close
    cv2.waitKey(10000)
    cv2.destroyAllWindows()

def main():
    # read image
    img = read_image()

    # balance the color of the image
    img = color_balance(img, 0.02)

    # detect the color of image
    detect_color(img)

if __name__ == "__main__":
    main()
    