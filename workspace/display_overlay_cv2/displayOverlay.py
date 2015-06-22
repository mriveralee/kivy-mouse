""" Display Overlay using Open CV
""  An image serves as the microscope view port
"""

# NOTE cv2.LINE_AA is now cv2.CV_AA

import sys
import numpy as np
import cv2 as cv2
import uuid
import cv2drawable as cd
# from PIL import Image

def main(argv=sys.argv):
  paramLength = len(argv)
  # first argv is always the program name
  if argv is None or paramLength != 2:
    print "Please provide input a single string to encode"
    return
  # Image Name
  imgName = argv[1]
  # Load Image
  origImg = cv2.imread(imgName)
  # img = cv2.imread(imgName)

  # Resize for our purposes
  img = cv2.resize(origImg, (0,0), fx=0.5, fy=0.5)

  # Draw Sample circle
  #circle = cd.Circle()

  # Draw Sample Text
  font = cv2.FONT_HERSHEY_SIMPLEX
  cv2.putText(img,'Microscope Test',
             (10,600),
             font,
             2,
             (255,255,255),
             2,
             cv2.CV_AA)

  # Draw Display
  # Display image in window
  windowName = 'Display Overlay Test'
  windowHeight = 600
  windowWidth = 800
  cv2.namedWindow(windowName, cv2.WINDOW_NORMAL)
  cv2.imshow(windowName, img)
  cv2.resizeWindow(windowName, windowWidth, windowHeight)

  # Wait indefinitely for keyboard click
  cv2.waitKey(0)
  # Close all windows
  cv2.destroyAllWindows()

  # End main
  pass

if __name__ == '__main__':
    sys.exit(main())
