#!/usr/bin/env python
"""Segmentation skeleton code for Lab 6
Course: EECS C106A, Fall 2019
Author: Grant Wang

This Python file is the skeleton code for Lab 3. You are expected to fill in
the body of the incomplete functions below to complete the lab. The 'test_..'
functions are already defined for you for allowing you to check your 
implementations.

When you believe you have completed implementations of all the incompeleted
functions, you can test your code by running python segmentation.py at the
command line and step through test images
"""

import os
import numpy as np
import cv2
import matplotlib.pyplot as plt

from scipy import ndimage
from scipy.misc import imresize
from skimage import filters

from skimage.measure import block_reduce
import time
import pdb
from trans_new import calibration

IMG_DIR = os.path.dirname(os.path.abspath(__file__))

class imgProcess:
    def __init__(self):
        self.lower_thresh = 0
        self.upper_thresh = 145

    @staticmethod
    def read_image(img_name, grayscale=False):
        """ reads an image

        Parameters
        ----------
        img_name : str
            name of image
        grayscale : boolean
            true if image is in grayscale, false o/w
        
        Returns
        -------
        ndarray
            an array representing the image read (w/ extension)
        """

        if not grayscale:
            img = cv2.imread(img_name)
        else:
            img = cv2.imread(img_name, 0)

        return img

    @staticmethod
    def write_image(img, img_name):
        """writes the image as a file
        
        Parameters
        ----------
        img : ndarray
            an array representing an image
        img_name : str
            name of file to write as (make sure to put extension)
        """

        cv2.imwrite(img_name, img)

    @staticmethod
    def show_image(img_name, title='Fig', grayscale=False):
        """show as a matplotlib figure
        
        Parameters
        ----------
        img_name : str
            name of image
        tile : str
            title to give the figure shown
        grayscale : boolean
            true if image is in grayscale, false o/w
        """
        if not grayscale:
            plt.imshow(img_name)
            plt.title(title)
            plt.show()
        else:
            plt.imshow(img_name, cmap='gray')
            plt.title(title)
            plt.show()

    @staticmethod
    def threshold_segment_naive(gray_img, lower_thresh, upper_thresh):
        """perform grayscale thresholding using a lower and upper threshold by
        blacking the background lying between the threholds and whitening the
        foreground

        Parameter
        ---------
        gray_img : ndarray
            grayscale image array
        lower_thresh : float or int
            lowerbound to threshold (an intensity value between 0-255)
        upper_thresh : float or int
            upperbound to threshold (an intensity value between 0-255)

        Returns
        -------
        ndarray
            thresholded version of gray_img
        """
        # TODO: Implement threshold segmentation by setting pixels of gray_img inside the 
        # lower_thresh and upper_thresh parameters to 0
        # Then set any value that is outside the range to be 1 
        # Hints: make a copy of gray_img so that we don't alter the original image
        # Boolean array indexing, or masking will come in handy. 
        # See https://docs.scipy.org/doc/numpy-1.13.0/user/basics.indexing.html
        [n, m] = gray_img.shape
        newImage = np.zeros((n, m))
        for i in range(n):
            for j in range(m):
                if lower_thresh <= gray_img[i][j] <= upper_thresh:
                    newImage[i][j] = 0  # black
                else:
                    newImage[i][j] = 1  # white
        return newImage

    @staticmethod
    def edge_detect_naive(gray_img):
        """perform edge detection using first two steps of Canny (Gaussian blurring and Sobel
        filtering)

        Parameter
        ---------
        gray_img : ndarray
            grayscale image array

        Returns
        -------
        ndarray
            gray_img with edges outlined
        """

        img = gray_img.astype('int16') # convert to int16 for better img quality 
        # TODO: Blur gray_s using Gaussian blurring, convole the blurred image with
        # Sobel filters, and combine to compute the intensity gradient image (image with edges highlighted)
        # Hints: open-cv GaussianBlur will be helpful https://medium.com/analytics-vidhya/gaussian-blurring-with-python-and-opencv-ba8429eb879b 
        # the scipy.ndimage.filters class (imported already) has a useful convolve function

        # Steps
        # 1. apply a gaussian blur with a 5x5 kernel.
        # 2. define the convolution kernel Kx and Ky as defined in the doc.
        # 3. compute Gx and Gy by convolving Kx and Ky respectively with the blurred image.
        # 4. compute G = sqrt(Gx ** 2 + Gy ** 2)
        # 5. Return G
        
        # if our edge is bold, we need to blur first
        img_blur = img
        # img_blur = cv2.GaussianBlur(img, (5, 5), cv2.BORDER_DEFAULT)  # need to tune here
        
        Kx = np.array([[-1,0,1], [-2,0,2], [-1,0,1]])
        Ky = np.array([[-1,-2,-1], [0,0,0], [1,2,1]])

        Gx = ndimage.convolve(img_blur, Kx, mode='constant', cval=0.0)
        Gy = ndimage.convolve(img_blur, Ky, mode='constant', cval=0.0)

        G = np.sqrt(Gx ** 2 + Gy ** 2)

        return G

    @staticmethod
    def edge_detect_canny(gray_img):
        """perform Canny edge detection

        Parameter
        ---------
        gray_img : ndarray
            grayscale image array

        Returns
        -------
        ndarray
            gray_img with edges outlined
        """

        edges = cv2.Canny(gray_img, 100, 200)

        return edges

    @staticmethod
    def to_grayscale(rgb_img):
        return np.dot(rgb_img[... , :3] , [0.299 , 0.587, 0.114])

    @staticmethod
    def thresh_naive(img, lower_thresh, upper_thresh):
        thresh = imgProcess.threshold_segment_naive(img, lower_thresh, upper_thresh)
        imgProcess.show_image(thresh, title='thresh_naive', grayscale=True)
        cv2.imwrite(IMG_DIR + "/thresh.jpg", thresh.astype('uint8') * 255)
        return thresh  # 0, balck; 1, white

    @staticmethod
    def test_edge_naive(thresh):
        edges = imgProcess.edge_detect_naive(thresh)
        # write edgdes numpy array to file
        # np.savetxt(IMG_DIR + '/edge_naive', edges, fmt="%3f", delimiter=" ", newline='\n')

        # blur again, avoid hollow edge
        edges = cv2.GaussianBlur(edges, (5, 5), cv2.BORDER_DEFAULT)  # need to tune here
        # imgProcess.show_image(edges, title='edge blur', grayscale=True)
        # np.savetxt(IMG_DIR + '/edge_blur', edges, fmt="%3f", delimiter=" ", newline='\n')
        
        # first flip the image
        imgProcess.flip(edges)  # now black -> edge; white -> space
        # imgProcess.show_image(edges, title='edge flip', grayscale=True)
        # np.savetxt(IMG_DIR + '/edge_flip', edges, fmt="%3f", delimiter=" ", newline='\n')

        # then assign each area number
        count = imgProcess.assignAreaNumber(edges)
        print(count)
        imgProcess.show_image(edges, title='edge naive', grayscale=True)
        # np.savetxt(IMG_DIR + '/edge_naive_assigned', edges, fmt="%3f", delimiter=" ", newline='\n')

        # save the processed image
        cv2.imwrite(IMG_DIR + "/test_naive.jpg", edges)
        return edges

    @staticmethod
    def test_edge_canny(img):
        edges = edge_detect_canny(img)
        # np.savetxt(IMG_DIR + '/edge_canny', edges, fmt="%3f", delimiter=" ", newline='\n')
        # first maximize the edge
        boldEdge(edges)
        show_image(edges, title='edge canny bold', grayscale=True)
        # then assign the numbers
        count = assignAreaNumber(edges)
        print(count)
        # np.savetxt(IMG_DIR + '/edge_canny_assigned', edges, fmt="%3f", delimiter=" ", newline='\n')
        show_image(edges, title='edge canny', grayscale=True)
        cv2.imwrite(IMG_DIR + "/test_canny.jpg", edges)

    @staticmethod
    def flip(img):
        """flip the color of the image. 0 -> black -> edge; 1 -> white -> space.
        
        Parameters
        ----------
        img_name : ndarray
            image matrix
        """
        (m, n) = img.shape
        for i in range(m):
            for j in range(n):
                if img[i, j] != 0:  # white -> edge
                    img[i, j] = 0  # black -> edge
                else:  # original black space
                    img[i, j] = 1  # withe -> space
        return

    @staticmethod
    def assignAreaNumber(img):
        """This function will devide graph into several areas. Finally, 0 edge, >0 space.
        
        Parameters
        ----------
        img_name : ndarray
            image matrix

        Returns
        -------
        count : int
            number of areas
        """
        def DFS(i, j, count):
            stack = [(i, j)]
            while stack:
                (x, y) = stack[-1]  # top of the stack
                # up
                if x-1 >= 0 and img[x-1, y] == 1 and (x-1, y) not in visited:
                    stack.append((x-1, y))
                    visited.add((x-1, y))
                    continue
                # down
                if x+1 < m and img[x+1, y] == 1 and (x+1, y) not in visited:
                    stack.append((x+1, y))
                    visited.add((x+1, y))
                    continue
                # left
                if y-1 >= 0 and img[x, y-1] == 1 and (x, y-1) not in visited:
                    stack.append((x, y-1))
                    visited.add((x, y-1))
                    continue
                # right
                if y+1 < n and img[x, y+1] == 1 and (x, y+1) not in visited:
                    stack.append((x, y+1))
                    visited.add((x, y+1))
                    continue
                stack.pop()
                img[x, y] = (255-count)
            return  # stack empty
                    
        count = 0
        (m, n) = img.shape
        visited = set()  # keep all seen index
        for i in range(m):
            for j in range(n):
                if (i, j) not in visited and img[i, j] == 1:
                    DFS(i, j, count)  # assign white area number
                    count += 1
        return count

    @staticmethod
    def findStartandEnd(img):
        """This function will put all (start index, end index for each row) tuple in a dict.
        
        Parameters
        ----------
        img_name : ndarray
            image matrix

        Returns
        -------
        result : dict
            each element is a list of (start, end) tuples for a specific area number; each list is sorted
        """

        # circle test
        # (n, m) = img.shape
        # result = {
        #     1: [[(0, 0), (0, m-1), (n-1, m-1), (n-1, 0), (0, 0)]]
        # }        
        # result = {
        #     1: [[(50, 50), (60, 50), (60, 60), (50, 60), (50, 50)]]
        # }

        # center = [100, 100]
        # radius = 100

        # circle_stroke = []
        # for x in np.linspace(0, np.pi * 4, num=30):
        #     circle_stroke.append((radius * np.cos(x) + center[0], center[1] + radius * np.sin(x)))
        # result[1].append(circle_stroke[:])

        # circle_stroke = []
        # for x in np.linspace(0, np.pi * 4, num=30):
        #     circle_stroke.append((radius * np.cos(x) + center[0], center[1] + radius * np.sin(x)))
        # result[1].append(circle_stroke[:])

        # circle_stroke = []
        # for x in np.linspace(0, np.pi * 4, num=30):
        #     circle_stroke.append((radius * np.cos(x) + center[0], center[1] + radius * np.sin(x)))
        # result[1].append(circle_stroke[:])



        # for area_number in range(count)
        # while True:
        #     sti = -1
        #     stj = -1
        #     # find 0
        #     for i in range(0, n):
        #         for j in range(0, m):
        #             if img[i][j] == 0:
        #                 sti = i
        #                 stj = j
        #                 break
        #         if sti != -1:
        #             break

        #     if sti == -1 and stj == -1:
        #         break


        #     fd = [(-1, 0), (-1, 1), (0, 1), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1)]
        #     current_d = 0
        #     while True:
        #         if 


        (m, n) = img.shape
        result = {}  # {area number: [(starts, ends)]}
        for i in range(0, m, 3):  # skip 3 rows
            start = 0  # column index of start points
            prev = None
            for j in range(n):
                if img[i][j] != prev or j == n-1:  # new start or end of the row
                    end = j
                    if img[i][j] != prev:
                        end = j-1
                    # TODO: find a way to not hardcode the outerspace number here
                    if prev != None and prev != 0 and prev != 255:  # 0 edge; 255 outer space
                        if end - start < 7:  # less than 7 pixel, then ignore
                            prev = img[i][j]  # update prev and start
                            start = j
                            continue
                        # if end - start > 500 * 0.75:  # probably outer space

                        if prev not in result:  # new area
                            result[prev] = [[(i, start), (i, end)]]
                        else:
                            result[prev][0].append((i, start))
                            result[prev][0].append((i, end))       
                    prev = img[i][j]  # update prev and start
                    start = j
        # # print(result[254])

        return result

    @ staticmethod
    def pixel2World(cali, areaPoints):
        worldPoints = {}  # {area number: [(starts in world frame, ends in world frame)]}
        for area in areaPoints:
            worldPoints[area] = []
            for stroke in areaPoints[area]:
                temp = []  # [(starts in world frame, ends in world frame)]
                for (x, y) in stroke:
                    # startWorld = cali.transform_to_3d(np.array([start[0], start[1]]))
                    p = cali.transform_to_3d(np.array([x, y]))
                    temp.append(p)  # (np.array(2,), np.array(2))
                worldPoints[area].append(temp[:])
        # worldPoints[1] = [0]
        # worldPoints[1][0] = [cali.transform_to_3d(np.array([50, 50])),cali.transform_to_3d(np.array([50, 50]))]
        return worldPoints

    @ staticmethod
    def getPoints():
        # get th webcame image
        original_image = imgProcess.read_image(IMG_DIR + '/test.jpg', grayscale=True)
        
        # transform webcame image to standard image
        cali = calibration(original_image, (345, 500))
        standard_img = cali.calibrate()

        # first, threshold the original image
        thresh = imgProcess.thresh_naive(standard_img, 0, 180)

        # then do the naive edge detection; also do area segmentation underlyingly
        thresh = imgProcess.test_edge_naive(thresh)
        # imgProcess.test_edge_canny(test_img)

        # get start points and corresponding end points
        areaPoints = imgProcess.findStartandEnd(thresh)  # {area number: [(starts, ends)]}

        # transfer index of the matrix to the coordinate in the world frame
        worldPoints = imgProcess.pixel2World(cali, areaPoints)
        # print(worldPoints)
        return worldPoints
        
if __name__ == '__main__':
    # TODO: to poptimize, no space allocation

    # get the webcame image
    original_image = imgProcess.read_image(IMG_DIR + '/test.jpg', grayscale=True)
    
    # transform webcame image to standard image
    cali = calibration(original_image, (345, 500))
    standard_img = cali.calibrate()

    # first, threshold the original image
    thresh = imgProcess.thresh_naive(standard_img, 0, 200)  # may need to tune the thresh hold

    # then do the naive edge detection; also do area segmentation underlyingly
    thresh = imgProcess.test_edge_naive(thresh)
    # imgProcess.test_edge_canny(test_img)

    # get start points and corresponding end points
    areaPoints = imgProcess.findStartandEnd(thresh)  # {area number: [(starts, ends)]}

    # transfer index of the matrix to the coordinate in the world frame
    worldPoints = imgProcess.pixel2World(cali, areaPoints)
    # print(worldPoints)