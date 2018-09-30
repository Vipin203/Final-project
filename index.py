from usefulfunction.colordescriptor import ColorDescriptor
import argparse
import glob
import cv2

# initialize the color descriptor
cd = ColorDescriptor((8, 12, 3))

# open the output index file for writing
output_file = 'index.csv'


dataset_path = 'dataset'

def create_index(dataset_path, output_file):
        output = open(output_file, "w")
        # use glob to grab the image paths and loop over them
        for imagePath in glob.glob(dataset_path + "/*.png"):
                # extract the image ID (i.e. the unique filename) from the image
                # path and load the image itself
                imageID = imagePath[imagePath.rfind("/") + 1:]
                image = cv2.imread(imagePath)

                # describe the image
                features = cd.describe(image)
                # write the features to file
                features = [str(f) for f in features]
                output.write("%s,%s\n" % (imageID, ",".join(features)))
        
        # close the index file
        output.close()
create_index(dataset_path,output_file)
