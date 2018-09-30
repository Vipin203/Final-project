from imutils import paths
import argparse
import time
import sys
import cv2
import os

def dhash(image, hashSize=8):
	# resize the input image, adding a single column (width) so we
	# can compute the horizontal gradient
	resized = cv2.resize(image, (hashSize + 1, hashSize))
 
	# compute the (relative) horizontal gradient between adjacent
	# column pixels
	diff = resized[:, 1:] > resized[:, :-1]
 
	# convert the difference image to a hash
	return sum([2 ** i for (i, v) in enumerate(diff.flatten()) if v])

def hashcompute(dataset_folder):
    print("computing hashes for dataset Images...")
    datasetPaths = list(paths.list_images(dataset_folder))

    if (sys.platform != "win32"):
        datasetPaths = [p.replace("\\", "") for p in datasetPaths]

    dataset = {}
    start = time.time()

    # loop over the dataset paths
    for p in datasetPaths:
        # load the image from disk
        image = cv2.imread(p)
        # if the image is None then we could not load it from disk (so skip it)
        if image is None:
            continue
        # convert the image to grayscale and compute the hash
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        imageHash = dhash(image)
        # update the dataset dictionary
        l = dataset.get(imageHash, [])
        l.append(p)
        dataset[imageHash] = l

    # show timing for hashing dataset images, then start computing the
    # hashes for needle images
    print("processed {} images in {:.2f} seconds".format(len(dataset), time.time() - start))
    return dataset

def match_hash(query_image,dataset):
    print("computing hashes for query...")
    query_path = query_image
    # load the image from disk
    image = cv2.imread(query_path)

    # convert the image to grayscale and compute the hash
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    imageHash = dhash(image)
    # grab all image paths that match the hash
    matchedPaths = dataset.get(imageHash, [])
    return matchedPaths
dataset_folder = 'dataset'
dataset = hashcompute(dataset_folder)


query_image = 'queries/105800.png'
#printing the query image
img = cv2.imread(query_image,1)
cv2.imshow('Query Image',img)
cv2.waitKey(0)


matchedPaths = match_hash(query_image,dataset)

print(matchedPaths)

if len(matchedPaths) != 0:
        img = cv2.imread(matchedPaths[0],1)
        cv2.imshow('Result Image',img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

else:
        print ('Image Not Found in database')
