import cv2

image = cv2.imread("valid/syn_0.jpg")

image = cv2.resize(image, dsize=None, fx = 0.2, fy = 0.2)

image = cv2.resize(image, dsize=None, fx=5, fy=5)

cv2.imwrite("test.jpg", image)