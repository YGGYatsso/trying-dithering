import numpy as np
import cv2 as cv
import torch 
import os
import copy
# what is dithering ??
#() error diffusion ) ,i.e discrepancy in the pixel value, 
# is passed onto the next pixel. 

#there are many versions of dethering ( ordered distribution of random noise.)

# one can use bayer matrix for ordered dithering. 
def bayer2x2(img,h,w):
    """
    Applying 2X2bayer thresholding.
    """
    img_copy=copy.deepcopy(img)
    img_copy=img_copy/255
    
    dither2X2=np.array([[0.2,0.8],[0.6,0.4]])
#    print(dither2X2)
    
    for i in range(0,h,2):
        for j in range(0,w,2):
            img_copy[i][j]=  (0 if img_copy[i][j]<dither2X2[0][0] else 255)
            
            if j+1<w :
                img_copy[i][j+1]=   (0 if img_copy[i][j+1] < dither2X2[0][1] else 255)
            
            if i+1 <h :
                img_copy[i+1][j]=(0 if img_copy[i+1][j] < dither2X2[1][0] else 255)
            
            if i+1 <h and j+1 <w :
                img_copy[i+1][j+1]=(0 if img_copy[i+1][j+1]<dither2X2[1][1] else 255)
                
    
    return img_copy

# https://en.wikipedia.org/wiki/Floyd%E2%80%93Steinberg_dithering
def floyd_steinberg_dither(img,h,w):
    """
    img : 2D grayscale image
    h,w   : Height and Width of the image, respectively.
    """
    
    img_copy=copy.deepcopy(img)
    # dither_img=np.zeros((h,w))
    
    for i in range(h):
        for j in range (w):
            # going from left to right and top to bottom. 
            #print(i,j,"\n")
            old_pixel=img_copy[i][j]
            new_pixel=find_closest_palette_color(old_pixel)
            img_copy[i][j]=new_pixel*255.0 # pixel value is updated. 
            
            quant_error=old_pixel-new_pixel
            
            if j+1<w:
                img_copy[i][j+1]=img_copy[i][j+1]+quant_error*(7/16) 
            
            if i+1<h and j+1 <w :
                img_copy[i+1][j+1]=img_copy[i+1][j+1]+(quant_error*(1/16))
      
            if i+1<h:
                img_copy[i+1][j]=img_copy[i+1][j]+(quant_error*(5/16))
 
            if i+1 <h and j-1 >=0 :
                img_copy[i+1][j-1]=img_copy[i+1][j-1]+(quant_error*(3/16))
            
    return img_copy

def find_closest_palette_color(pixel):
    return  round(pixel/255)


# we also need to try color dithering.

if __name__ == '__main__':
    dir_path="/Users/ygyatso/Documents/some pics/"
    images_list=os.listdir(dir_path)
    get_image_name=images_list[10]

    image_path=os.path.join(dir_path,get_image_name)
    
    color_img=cv.imread(image_path)
    img=cv.imread(image_path,cv.IMREAD_GRAYSCALE)
    img_tooperate=copy.deepcopy(img)
    
    # first get the height and width of the image. 
    h,w=img.shape
    

    FS_dither=floyd_steinberg_dither(img,h,w)
    bayer=bayer2x2(img,h,w)
    
    cv.imshow("FS_DITHER_NEG",255-FS_dither) 
    #Ques. Why i need to change the value of pixels in the output ?? to get expected output ??
    #cv.imshow("FS_DITHER",FS_dither)
    cv.imshow("bayerfilter",bayer)
    cv.imshow("image",img)

    
    cv.waitKey(0) 
    
    
    
    
    # using personal laptop camera for video feed.
    # cap = cv.VideoCapture(0)
    # if not cap.isOpened():
    #     print("Cannot open camera")
    #     exit()
    # while True:
    # # Capture frame-by-frame
    #     ret, frame = cap.read()
    
    #     # if frame is read correctly ret is True
    #     if not ret:
    #         print("Can't receive frame (stream end?). Exiting ...")
    #         break
    #     # Our operations on the frame come here
    #     #print(frame.shape)
    #     color_img=copy.deepcopy(frame)
    #     color_img=cv.resize(color_img,(480,480))
    #     gray = cv.cvtColor(color_img, cv.COLOR_BGR2GRAY)
    #     gray_copy=copy.deepcopy(gray)
    #     gray_blur=cv.GaussianBlur(gray_copy,(5,5),0)
        
    #     h,w=gray_blur.shape
        
    #     out=bayer2x2(gray_blur,h,w)
        
    #     cv.imshow("bayerfilter",out)
        
    #     cv.waitKey(0)