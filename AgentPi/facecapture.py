"""
This module is responsible for capturing a face for a users facerecognition.
"""

## Acknowledgement
## This code is adapted from:
## The tutorials and lectures in RMIT's Programming Internet of Things which further acknowledges
## https://www.hackster.io/mjrobot/real-time-face-recognition-an-end-to-end-project-a10826

import cv2
import os
import time
import shutil

# To consolidate logs into one location.
import logging
log = logging.getLogger(__name__)

# TODO If possible, update this to use the VideoStream class from imutils so
# that a usb or picamera can be used - it abstracts cv2.VideoCapture and picamera 
# in a threaded way which can improve performance.


# This class is responsible for capturing the faces for entry into the fac detection
# validation system. 
class FaceCapture:
    """
    If successful, it stores the set of faces in the passed in location. 
    The instantiation is passed in the following parameters
    name = (string) the name of the person intended to be added
    data_folder = (string) the folder to store face sets in.
    """

    # TODO this should be changed to a more appropriat name.
    # and it accepts the path for the files to be saved - this is the folder
    # structure passed in, so you can use 1 to many folders. Just use a single string. 
    def __init__ (self, name: str, data_folder: str):
        self.name = name
        self.data_folder = data_folder

    def capture_face(self) -> bool:
        """
        The only entry point for this class - attempts to record video and store
        the resulting images in a folder based on the name variable.
        """

        # # use name as folder name
        # TODO combine name and dataset to create the path...?
        user_folder = "./{}/{}".format(self.data_folder, self.name)

        # Create a new folder for the new name if one does not exist.
        if not os.path.exists(user_folder):
            os.makedirs(user_folder)

        # Create a VideoCapture object. Opens a camera for video capture - the parameter is 
        # the index of the camera to use. 
        # Could also be a video file (if someone sent in a video?)
        # TODO Handle if a camera is not connected/available?
        cam = cv2.VideoCapture(0)

        # Sets with width (3, 640) and the height (4, 480) of the video feed.
        # The higher the resolution, the more demanding this function will be on the CPU
        # Also, while these can return a boolean if the function was executed, there is no guarantee that the
        # change was accepted to the vidoo device - may be a problem with certain cameras.
        # The first value is the PropID (properties are a dict)
        cam.set(3, 640)
        cam.set(4, 480)
        # Get the pre-built classifier
        face_detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

        # A counter for the images, ensuring we don't spend too long collecting, but the function still exits after a period of time.
        image_counter = 0
        total_images = 10
        # Timeout in 10 seconds.
        timeout_time = time.time() + 10
        # Stop when 10 images are collected.
        # TODO Make a variable so that it can be more easily changed.
        while image_counter < total_images:
            # TODO break out of this in a different manner.
            # Allows the input to break the capturing if loop after each image is captured
            # key = input("Press q to quit or ENTER to continue: ")
            # if key == "q":
            #     break
            
            # Capture frame by frame, returns a bool (true if frame is read correctly)
            # and an image array vector captured based on the fps that was defined/default
            ret, frame = cam.read()
            # If an image is not succesfully captured, break the loop.
            # TODO this should be a continue...?
            if not ret:
                break
            
            # Convert the BRG that cv2 captures image to grayscale. 
            # This is necessary for the classifier.
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            
            # This calls the classifier function and returns a list of 
            # Rect(x, y, w, h) objects, the positions of the detections as 
            # a rectangle object where x and y are the top left corner coordinates 
            # and w and h the width and height respectively.
            # It is passed the following parameters:
            # gray - the inputted grayscale image.
            # scaleFactor - this parameter specifies how much the image size is 
            #     reduced at each image scale. It is used to create a scale pyramid
            #     where if the scale factor is 1.2, it reduces the image size by 20%.
            #     the smaller the scale factor (must be > 1), the more likely a match
            #     will be made, but it increases the computational cost.
            # minNeighbors - specifies how many neigbours each candidate rectangle
            #     should have to be retained. Higher values result in less detections
            #     but those that occur are of a higher quality.
            # minSize - unused the minimum possible object size. 
            #     Objects of a smaller size will be ignored. 
            # maxSize - unused in this test, but similar to minSize in nature.
            faces = face_detector.detectMultiScale(gray, 1.3, 5)
            # TODO it may be worth testing the faces list that is returned is 
            # only of length one, as we don't want more than one face to be analysed.
            # TODO it also may be worth exploring the use of a minimum size so that 
            # the user can't be too indistinct.

            # Break if taking too long.
            if time.time() > timeout_time:
                print("Face profiling unsuccessful (timeout).")
                print("Try again under later.")
                time.sleep(3)
                break

            if(len(faces) == 0):
                log.info("No face detected, retrying....")
                continue
            
            # for each rectangle tuple in the faces list, extracting the dimensions and 
            # coordinates using Numpy slicing
            for (x, y, w, h) in faces:
                # cv2.rectangle accepts the image, top-left corner tuple, 
                # bottom right corner tuple, colour tuple (Blue for BGR), 
                # and the thickness of the line. It then draws an outer rectangle from
                # the vertexes.
                # TODO is this necessary?
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                # Set the folder and filename, ensureing that there are leading zeros for
                # image_counter i.e., 0001
                img_name = "{}/{:04}.jpg".format(user_folder, image_counter)
                # imwrite(filename, image) saves the frame with just the face element
                # based on the coordiantes via a numpy index: img[left:right, top:bottom]
                # TODO Separate the cropping code into its own line?
                cv2.imwrite(img_name, frame[y : y + h, x : x + w])
                log.info("{} written!".format(img_name))
                image_counter += 1

        # Release the VideoCapture object. 
        # Return to calling function appropriately, deleting the files
        # if it was not successful so that they are not included in future
        # encodings.
        cam.release()
        if image_counter == total_images:
            # Update the pickle file upon returning.
            return True
        else:
            # Delete the folder.
            try: 
                shutil.rmtree(user_folder)
            except OSError as e:
                log.error("Error deleting {} folder: {}".format(user_folder, e))
            return False


# For Testing
if __name__ == "__main__":
    fc = FaceCapture("indy_test", "test_folder")
    fc.capture_face()
