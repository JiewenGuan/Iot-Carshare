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
        print("[INFO] loading encodings...")
        # data = pickle.loads(open(args["encodings"], "rb").read())

        # Load the pickly file and deserialise it. Also handles the event of 
        # no pickle file existing.
        # TODO can remove the printing of err after testing. There may be other errors!
        data = None
        try:
            with open(pickle_file, "rb").read() as f:
                data = pickle.loads(f)
        Except IOError as err:
            print(err)
            print("Error opening or decoding pickle file!")
            return None
        except: 
            print("Some other error when operating with pickle file!")
            return None

        # initialize the video stream and then allow the camera sensor to warm up
        print("[INFO] starting video stream...")
        # Initialise VideoStream from imutila (in capture we used cv2.videocapture)
        # where the src parameter is the camera as before. Sleep for camera warmup.
        vs = VideoStream(src = 0).start()
        time.sleep(2.0)

        # loop over frames from the video file stream
        # TODO The loop should have a timeout if it can't return a match.
        # This timeout should take into consideration that the threading of 
        # VideoStream results in dropped frames as it only reads the most 
        # recent frame - it may take some time for a frame to have a readable
        # face in it, and many frames may be dropped during the face recognition.
        while True:
            # Extract a frame from the video stream. Remember this is 
            # threaded so it is the most recent frame.
            frame = vs.read()

            # convert the input frame from BGR to RGB then resize it to have
            # a width of 750px (to speedup processing)
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # TODO This seems problematic - above we are setting rgb to the
            # colour adjusted version of frame, but in the line below we are
            # overwritting the rgb object from before with a new one, which 
            # is not colour corrected, but the original frame. Should frame
            # be rgb in the line below?
            # rgb = imutils.resize(frame, width = args["resolution"])
            rgb = imutils.resize(frame, width = detection_resolution)

            # detect the (x, y)-coordinates of the bounding boxes
            # corresponding to each face in the input frame, then compute
            # the facial embeddings for each face
            # boxes = face_recognition.face_locations(rgb, model = args["detection_method"])
            # Detects faces and returns an array of bounding boxes in css (top, right, 
            # bottom, left) order (like padding).
            boxes = face_recognition.face_locations(rgb, model = detection_method)
            # Computes a 128-dimensional face encoding (technically called an embedding 
            # which is actually a 128 float numpy array of underfined meaning) for each face 
            # in the image, returning a list of these encodings. 
            # Passed in the image and the bounding box. Also accepts a model parameter 
            # (large (default) or small - small is faster but only returns 5 points), 
            # and a num_jitters which randomly distorts the image before encoding. 
            encodings = face_recognition.face_encodings(rgb, boxes)
            names = []

            # loop over the facial embeddings
            for encoding in encodings:
                # attempt to match each face in the input image to our known
                # encodings
                matches = face_recognition.compare_faces(data["encodings"], encoding)
                name = "Unknown"

                # check to see if we have found a match
                if True in matches:
                    # find the indexes of all matched faces then initialize a
                    # dictionary to count the total number of times each face
                    # was matched
                    # The 
                    matchedIdxs = [i for (i, b) in enumerate(matches) if b]
                    counts = {}

                    # loop over the matched indexes and maintain a count for
                    # each recognized face face
                    for i in matchedIdxs:
                        name = data["names"][i]
                        counts[name] = counts.get(name, 0) + 1

                    # determine the recognized face with the largest number
                    # of votes (note: in the event of an unlikely tie Python
                    # will select first entry in the dictionary)
                    name = max(counts, key = counts.get)

                # update the list of names
                names.append(name)

        # loop over the recognized faces
            for name in names:
                # print to console, identified person
                print("Person found: {}".format(name))
                # Set a flag to sleep the cam for fixed time
                time.sleep(3.0)

        # Stop the thread that the VideoStream is operating on.
        vs.stop()


# Testing
if __init__ = "__main__":
    face_recogniser = FaceRecognition("testpickle.pickle")
    face_recogniser.recognise_face()