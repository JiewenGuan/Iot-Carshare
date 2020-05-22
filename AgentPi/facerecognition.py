# This class is responsible for recognising the face captured by the device. It does
# so by checking the presented face against the locally stored encodings, returning
# the encoded name which should be the user token to be sent to the MasterPi for 
# validation.


## Acknowledgement
## This code is adapted from:
## https://www.pyimagesearch.com/2018/06/18/face-recognition-with-opencv-python-and-deep-learning/

# import the necessary packages
from imutils.video import VideoStream
import face_recognition
import argparse
import imutils
import pickle
import time
import cv2
import os
# To consolidate logs into one location.
import logging
log = logging.getLogger(__name__)

# This class is instantiated and the recognise_face() method called to recognise a face
# if it is stored in the pickle encoding. It accepts a path to the pickle file the 
# resolution of the video feed.
class FaceRecognition:
    def __init__(self, pickle_file: str):
        self.pickle_file = pickle_file

        # USAGE
        # With default parameters
        #     python3 03_recognise.py
        # OR specifying the encodings, screen resolution
        #     python3 03_recognise.py -e encodings.pickle -r 240

    def recognise_face(self) -> str:
        # The detection method is set as hog due to device limitations. See faceencoder.py
        # for further details.

        print("\nPlease look at the camera....")
        detection_method = "hog"
        detection_resolution = 240

        # # construct the argument parser and parse the arguments
        # ap = argparse.ArgumentParser()
        # ap.add_argument("-e", "--encodings", default="encodings.pickle",
        # help="path to serialized db of facial encodings")
        # ap.add_argument("-r", "--resolution", type=int, default=240,
        #     help="Resolution of the video feed")
        # ap.add_argument("-d", "--detection-method", type=str, default="hog",
        #     help="face detection model to use: either `hog` or `cnn`")
        # args = vars(ap.parse_args())

        # load the known faces and embeddings
        log.info("Loading encodings...")
        # data = pickle.loads(open(args["encodings"], "rb").read())

        # Load the pickly file and deserialise it. Also handles the event of 
        # no pickle file existing.
        # TODO can remove the printing of err after testing. There may be other errors!
        data = None
        try:
            with open(self.pickle_file, "rb") as f:
                file = f.read()
                data = pickle.loads(file)
        except IOError as err:
            log.error(err)
            print("Error opening or decoding pickle file!")
            return None
        except Exception as e: 
            print("Some other error when operating with pickle file!")
            log.error(e)
            return None

        # initialize the video stream and then allow the camera sensor to warm up
        log.info("Starting video stream...")
        # Initialise VideoStream from imutila (in capture we used cv2.videocapture)
        # where the src parameter is the camera as before. Sleep for camera warmup.
        vs = VideoStream(src = 0).start()
        time.sleep(2.0)

        # Set a timeout time in case no faces are ever found.
        timeout_time = time.time() + 10

        # loop over frames from the video file stream
        # TODO The loop should have a timeout if it can't return a match.
        # This timeout should take into consideration that the threading of 
        # VideoStream results in dropped frames as it only reads the most 
        # recent frame - it may take some time for a frame to have a readable
        # face in it, and many frames may be dropped during the face recognition.
        while True:
            # Check the time elapsed
            if time.time() > timeout_time: 
                print("No valid faces found.")
                time.sleep(2)
                break

            # Extract a frame from the video stream. Remember this is 
            # threaded so it is the most recent frame.
            frame = vs.read()
            log.info("Frame read")

            # Convert the frame from BRG to RGB and resize it to the
            # specified width while maintaining aspect ratio.
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # TODO FIXED This seems problematic - above we are setting rgb to the
            # colour adjusted version of frame, but in the line below we are
            # overwritting the rgb object from before with a new one, which 
            # is not colour corrected, but the original frame. Should frame
            # be rgb in the line below?
            # rgb = imutils.resize(frame, width = args["resolution"])
            # rgb = imutils.resize(frame, width = detection_resolution)
            resized_rgb_frame = imutils.resize(rgb_frame, width = detection_resolution)

            # detect the (x, y)-coordinates of the bounding boxes
            # corresponding to each face in the input frame, then compute
            # the facial embeddings for each face
            # boxes = face_recognition.face_locations(rgb, model = args["detection_method"])
            # Detects faces and returns an array of bounding boxes in css (top, right, 
            # bottom, left) order (like padding).
            boxes = face_recognition.face_locations(resized_rgb_frame, model = detection_method)
            # Computes a 128-dimensional face encoding (technically called an embedding 
            # which is actually a 128 float numpy array of underfined meaning) for each face 
            # in the image, returning a list of these encodings. 
            # Passed in the image and the bounding box. Also accepts a model parameter 
            # (large (default) or small - small is faster but only returns 5 points), 
            # and a num_jitters which randomly distorts the image before encoding. 
            encodings = face_recognition.face_encodings(resized_rgb_frame, boxes)
            names = []

            # loop over the facial embeddings
            for encoding in encodings:
                # attempt to match each face in the input image to our known
                # encodings
                # Compares the list of face encodings to the encoding captured.
                # Returns a bool list (ordered) of True/False values (since there may be more
                # than one face in an image.) based on the data list.
                # Also accepts a tolerance paramter (default 0.6), lower is more strict.
                matches = face_recognition.compare_faces(data["encodings"], encoding)
                name = None

                # check to see if we have found a match
                # This takes O(n) memory which if the list is large would take 
                # up considerable memory, so use if any instead.
                #if True in matches:
                if any(matches):
                    # find the indexes of all matched faces then initialize a
                    # dictionary to count the total number of times each face
                    # was matched
                    # List comprehension
                    # The matches list is returned as an iterable object inside the function.
                    # It returns the a list of each index of the matches iterable (a) based on the boolean
                    # in matches (b) (technically matches[0] == enumerate(matches[][0])).
                    matched_id_index = [
                        index 
                        for (index, matches_boolean) 
                        in enumerate(matches) 
                        if matches_boolean
                        ]
                    # Dictionary for names matched to be counted and incrememted with key name
                    counts = {}

                    # loop over the matched indexes and maintain a count for
                    # each recognized face face
                    # Loop through the matched_id_index and extract the name from the 
                    # associated data dictionary value - the name the encoding matched.
                    # Append the count to the appropriate name in the dictionary name
                    for index in matched_id_index:
                        name = data["names"][index]
                        counts[name] = counts.get(name, 0) + 1

                    # determine the recognized face with the largest number
                    # of votes (note: in the event of an unlikely tie Python
                    # will select first entry in the dictionary)
                    # Returns the name with the highest count, the statistically most
                    # correct match.
                    name = max(counts, key = counts.get)

                # Adds the most popular name to the list.
                names.append(name)

        # Loop over the names (again hopefully just one) and return it to the
        # calling function.
            for name in names:
                if name is not None:
                    # print to console, identified person
                    log.info("Person found: {}".format(name))
                    # Set a flag to sleep the cam for fixed time
                    # time.sleep(3.0)
                    vs.stop()
                    return name

        # Stop the thread that the VideoStream is operating on.
        vs.stop()


# Testing
if __name__ == "__main__":
    face_recogniser = FaceRecognition("testpickle.pickle")
    face_recogniser.recognise_face()