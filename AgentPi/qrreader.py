
"""
This module performs the functions associated with QR code
reading. It has one class QRReader that consists of two 
functions - read_qr_code which uses the camera to search
for QR codes, and validate_qr_code which ensures the QR Code
is of the correct format before been returned.
"""
##########################################################################################
# Does not work with the version of CV2 that the face detection has been tested with,
# as the this module was not introduced until a later version of opencv.
#
# import cv2
#
# cap = cv2.VideoCapture(0)
#
# detector = cv2.QRCodeDetector()
#
# while True:
#     _, img = cap.read()
#     data, bbox, _ = detector.detectAndDecode(img)
#   
#     if(bbox is not None):
#         for i in range(len(bbox)):
#             cv2.line(img, tuple(bbox[i][0]), tuple(bbox[(i+1) % len(bbox)][0]), color=(255,
#                      0, 255), thickness=2)
#         cv2.putText(img, data, (int(bbox[0][0][0]), int(bbox[0][0][1]) - 10), cv2.FONT_HERSHEY_SIMPLEX,
#                     0.5, (0, 255, 0), 2)
#         if data:
#             print("data found: ", data)
#     cv2.imshow("code detector", img)
#     if(cv2.waitKey(1) == ord("q")):
#         break
# cap.release()
# cv2.destroyAllWindows()
##########################################################################################

# This code is adapted from the RMIT Programming of
# Internet Things 2020 Semester One undergraduate course
# and their referenced 
# https://www.pyimagesearch.com/2018/05/21/an-opencv-barcode-and-qr-code-scanner-with-zbar/

# TODO Dependencies
# python3 -m pip install pyzbar

# Only import appropriate packages to reduce loading time.
from imutils.video import VideoStream
from pyzbar import pyzbar
import datetime
import imutils
import time
import cv2

# To consolidate logs into one location.
import logging
log = logging.getLogger(__name__)


class QRReader():
    """
    The QRReader class consists of two functions, read_qr_code which is publicly
    callable read_qr_code, and validate_qr_code which is called to validate
    any codes that are found.
    """

    def read_qr_code(self):
        """
        This functions initialises the camera and then searches for QR codes. 
        Any codes that are found are incrementally passed to validate_qr_code 
        which returns the code to be returned to the calling function,
        or False if the code is invalid.        
        """

        # Initialise the VideoStream and sleep for adequate time
        # for the camera to be initialised.
        log.info("Starting video stream...")
        video_stream = VideoStream(src=0).start()
        time.sleep(2)

        # Defines a timeout time for video, and the return
        # valid_code 
        timeout_time = time.time() + 10
        # found = set()
        valid_code = False
        print("1")

        # Extract frames from the video_stream and process them for potential barcodes.
        # Breaks after the set time.
        while True:
            # Check the time elapsed and break if it exceeds the set time.
            if time.time() > timeout_time: 
                # print("No valid codes identified.")
                # time.sleep(2)
                break

            # grab the frame from the threaded video stream and resize it to
            # have a maximum width of 400 pixels
            # Extract a fream from the stream and resize it to a processor
            # efficient size.
            extracted_frame = video_stream.read()
            extracted_frame = imutils.resize(extracted_frame, width=400)

            # Extract any barcodes from the frame.
            found_barcodes = pyzbar.decode(extracted_frame)

            # Assess all the barcodes found by looping through .
            for extracted_barcode in found_barcodes:
                # Determine the type, and if of type QRCODE then continue.
                # Is instance does not work as the type function returns a string.
                if extracted_barcode.type == "QRCODE":
                    # Convert the barcode from a byte array to a string,
                    # pass the string to the validation function and if valid,
                    # break out of the loop and return.
                    extracted_qrcode = extracted_barcode.data.decode("utf-8")
                    log.info("QRCODE Found: {}".format(extracted_qrcode))
                    valid_code = self.validate_qr_code(extracted_qrcode)
                    if valid_code:
                        log.info("Most recent code is of valid format.")
                        break

                # the barcode data is a bytes object so we convert it to a string
                # Convert the barcode from a byte array to a string.
                # barcodeData = barcode.data.decode("utf-8")


                # if the barcode text has not been seen before print it and update the set
                # if barcodeData not in found:
                #     print("[FOUND] Type: {}, Data: {}".format(barcodeType, barcodeData))
                #     found.add(barcodeData)
            
            # Delay the scan of the next frame to reduce the chance of reading an 
            # undesired barcode again.
            # time.sleep(1)

        # Close the videostream (all video streams), and return
        # the found code.
        video_stream.stop()
        return valid_code

    
    def validate_qr_code(self, qr_code: str):
        """
        This function validates a QR code that has been passed to it
        by checking if the code has the correct structure and if needed,
        extracts the relevant data and returns the data, or returns 
        False if the code is invalid.
        """

        extracted_code = qr_code.split()
        if extracted_code[0] == "PIOT":
            return qr_code
        return False


if __name__ == "__main__":
    qr_read_test = QRReader()
    qr_read_test.read_qr_code()