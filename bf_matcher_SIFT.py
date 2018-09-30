import numpy as np
import cv2
import os

# collecting name of all images from folder
def load_images_from_folder(folder):
    images = []
    for filename in os.listdir(folder):
        images.append(os.path.join(folder,filename))
    return images


#function for image match using python
def sift_matcher(query_image, dataset_images):
    # Initiate SIFT detector
    sift = cv2.SIFT()
    # find the keypoints and descriptors with SIFT
    query_img = cv2.imread(query_image)
    kp1, des1 = sift.detectAndCompute(query_img,None)
    flag = 0;
    for i in range (len(dataset_images)):
        db_image_path = dataset_images[i]
        db_image =  cv2.imread(db_image_path)
        print(dataset_images[i])
        kp2, des2 = sift.detectAndCompute(db_image,None)
        # BFMatcher with default params
        bf = cv2.BFMatcher()
        matches = bf.knnMatch(des1,des2, k=2)
        # Apply ratio test
        good = []
        for m,n in matches:
            if m.distance < 0.75*n.distance:
                good.append([m])
        per = (len(good)/len(matches))*100
        print(per)
        #set flag =1 if match found else set 0
        if per :
            flag = 1
            break
        else:
            flag = 0;
    if flag == 1:
        return 1 , db_image_path
    else:
        return 0 , ''

#calling functions
folder = 'dataset'
dataset_images = load_images_from_folder(folder)

#query image
query_img = 'queries/abc.png'
queryimg = cv2.imread(query_img,1)
cv2.imshow('Query Image',queryimg)
cv2.waitKey(0)
percentage_match ,  path = sift_matcher(query_img,dataset_images)
if percentage_match==1:
    print('Found')
    print(path)
    resultimg = cv2.imread(path,1)
    cv2.imshow('Result Image' ,resultimg)
    cv2.waitKey(0)
else:
    print('NOT Found in Database')
cv2.destroyAllWindows()
