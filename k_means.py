from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import numpy as np
import cv2
import color_detection

def load():
    # load the image
    image = cv2.imread("images/blood_in_stool_sample(1).jpg")
    
    return image

def centroid_histogram(clt):
    # grab the number of different clusters and create a histogram
    # based on the number of pixels assigned to each cluster
    numLabels = np.arange(0, len(np.unique(clt.labels_)) + 1)
    hist, _ = np.histogram(clt.labels_, bins = numLabels)
 
    # normalize the histogram, such that it sums to one
    hist = hist.astype("float")
    hist /= hist.sum()
 
    # return the histogram
    return hist

def plot_colors(hist, centroids):
    # initialize the bar chart representing the relative frequency
    # of each of the colors
    bar = np.zeros((50, 300, 3), dtype = "uint8")
    startX = 0

    # loop over the percentage of each cluster and the color of
    # each cluster
    for percent, color in zip(hist, centroids):
        # plot the relative percentage of each cluster
        endX = startX + (percent * 300)
        cv2.rectangle(
            bar,
            (int(startX), 0),
            (int(endX), 50),
            color.astype("uint8").tolist(),
            -1
        )
        startX = endX
    
    # return the bar chart
    return bar

# loag image
image = load()

# balance the color of the image
image = color_detection.color_balance(image, 0.02)

# Convert image from BRG to RGB
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# convert the image from a matrix to a list of image RGB pixels
image = image.reshape((image.shape[0] * image.shape[1], 3))

# Instantiate a kmeans clustering object with 3 clusters
clt = KMeans(n_clusters = 3)

# Cluster colors (one 3D color vector per pixel) into 3 clusters
# based on the euclidean distance between the colors 
clt.fit(image)

# create a histogram with each color bar representing the color and its
# frequency in the given image
hist = centroid_histogram(clt)
bar = plot_colors(hist, clt.cluster_centers_)
 
plt.figure()
plt.axis("off")
plt.imshow(bar)
plt.show()
