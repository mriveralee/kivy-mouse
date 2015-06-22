""" Track a QR Code"""

import sys
import qrcode as QR
import uuid
import zbar
from PIL import Image

def main(argv=sys.argv):
  paramLength = len(argv)
  # first argv is always the program name
  if argv is None or paramLength != 2:
    print "Please input a single string to encode"
    return
  # Message to encode is in second argv param
  msg = argv[1]
  # Create QR using image
  img = QR.make(msg)
  # Generate a UUID
  qrID = uuid.uuid4().hex
  # Create an image name using the unique ID
  imgName = "output/qr-%s.jpg" % qrID
  # Show the image
  img.show()
  # Save to a file
  img.save(imgName)

  print "Saved %s" % imgName
  pass

if __name__ == '__main__':
    sys.exit(main())
