from usefulfunction.colordescriptor import ColorDescriptor
from usefulfunction.searcher import Searcher
import argparse
import cv2
import os

# load the query image and describe it
query_path = 'queries/123600.png'
index_path = 'index.csv'
result_path = 'dataset'
# initialize the image descriptor
cd = ColorDescriptor((8, 12, 3))

  
#function for image search
def search_img(query_path, index_path,result_path):
        query = cv2.imread(query_path)
        features = cd.describe(query)

        # perform the search
        searcher = Searcher(index_path)
        results = searcher.search(features)

        result_img = []
        # loop over the results
        for (score, resultID) in results:
                # load the result image and display it
                
                result = cv2.imread(resultID)
                result_img.append(resultID)
                print(score)
        return result_img

results = search_img(query_path,index_path,result_path)
queryimg = cv2.imread(query_path,1)
cv2.imshow('Query Image' , queryimg)
cv2.waitKey(0)

for i in range(len(results)):
        print (results[i])
        img = cv2.imread(results[i],1)
        cv2.imshow('Result Similar Image',img)
        cv2.waitKey(0)

cv2.destroyAllWindows()

        
        
