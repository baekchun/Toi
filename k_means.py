from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import numpy as np
import cv2
import color_detection
import json
import math

def load():
    # load the image
    image = cv2.imread("images/blood_in_stool_sample(1).jpg")
    
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

def create_histogram(k_means):
    # grab the number of different clusters and create a histogram
    # based on the number of pixels assigned to each cluster
    numLabels = np.arange(0, len(np.unique(k_means.labels_)) + 1)
    hist, _ = np.histogram(k_means.labels_, bins = numLabels)
 
    # normalize the histogram so that it sums to one
    hist = hist.astype("float")
    hist /= hist.sum()

    # return the histogram
    return hist

def plot_colors(hist, colors):
    # initialize the bar chart representing the relative frequency
    # of each of the colors
    bar = np.zeros((50, 300, 3), dtype = "uint8")
    startX = 0

    # loop over the percentage of each cluster and the color of
    # each cluster
    for percent, color in zip(hist, colors):
        # plot the relative percentage of each cluster
        endX = startX + (percent * 300)
        cv2.rectangle(
            bar,
            (int(startX), 0),
            (int(endX), 50),
            # set pixels in uint8: [0, 255]
            color.astype("uint8").tolist(), 
            -1
        )
        startX = endX
    
    # return the bar chart
    print ("bar", bar, bar.shape)

    return bar

def main():

    # read image
    image = load()

    # balance the color of the image, i.e. scale each color channel to fully
    # span [0, 255] range
    image = color_balance(image, 0.02)

    # Convert image from BRG to RGB
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # convert the image from a matrix to a 1D array of image RGB pixels
    image = image.reshape((image.shape[0] * image.shape[1], 3))

    # Instantiate a k_means clustering object with 4 clusters
    k_means = KMeans(n_clusters = 8)

    # Cluster colors (one 3D color vector per pixel) into 4 clusters
    # based on the euclidean distance between the colors 
    k_means.fit(image)

    # get the most dominant colors found in the image
    dominant_colors = k_means.cluster_centers_

    # create a histogram with each color bar representing the color and its
    # frequency in the given image
    hist = create_histogram(k_means)

    # create a dictionary of probability mapped to the dominant RGB values
    color_dist = {}
    for p, rgb in zip(hist, dominant_colors):
        color_dist[p] = rgb.tolist()

    print ("distribution:", json.dumps(color_dist, indent=4))

    bar = plot_colors(hist, dominant_colors)

    plt.figure()
    plt.axis("off")
    plt.imshow(bar)
    plt.show()


if __name__ == "__main__":
    main()
