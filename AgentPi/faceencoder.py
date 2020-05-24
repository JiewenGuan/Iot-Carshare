"""
This module is responsible for encoding the dataset of face captures.
It should be called either after a user has been added to the face collection,
or if the database becomes large, periodically whenever processing time is available.
"""
# Acknowledgement
# This code is adapted from:
# The tutorials and lectures in RMIT's Programming Internet of Things which further acknowledges
# https://www.pyimagesearch.com/2018/06/18/face-recognition-with-opencv-python-and-deep-learning/


from imutils import paths
import face_recognition
import argparse
import pickle
import cv2
import os
# To consolidate logs into one location.
import logging
log = logging.getLogger(__name__)


class FaceEncoder:
    """
    Accepts the dataset file location, and the name of the output file.
    """

    def __init__(self, dataset: str, encoding_file: str):
        self.dataset = dataset
        self.encoding_file = encoding_file

    def encode_faces(self) -> bool:
        """
        Instantiating method - accepts nothing and returns a bool based on the outcome of encoding.
        This method has a significant time cost factor.
        """
        # hog - less accurate but fast on CPU
        # cnn - more accurate but slower, but GPU/CUDA accelerated if available.
        detection_method = str("hog")
        # grab the paths to the input images in our dataset
        log.info("Quantifying faces...")
        # imagePaths = list(paths.list_images(args["dataset"]))
        # Returns the paths of all images (including subdirectories) as a list, 
        # based on the root directory provided.
        image_paths = list(paths.list_images(self.dataset))

        # TODO TESTING TO DELETE.
        log.info(image_paths)
        log.info(image_paths[0].split(os.path.sep)[-2])
        log.info("TEST {}/{}".format(1, len(image_paths)))
        #sys.exit()

        # initialize the lists to contain the encodings and names
        image_encodings = []
        image_names = []

        # Loop over the list of image_paths, with a counter i for updating the user...?
        # TODO Do we need the counter?
        for (i, image_path) in enumerate(image_paths):
            # extract the person name from the image path
            log.info("Processing image {}/{}".format(i + 1, len(image_paths)))
            # Extract the username by extracting the folder name (second element from end)
            name = image_path.split(os.path.sep)[-2]

            # Loads the image based on the path, and convert it from BRG (OpenCV ordering)
            # to RGB (dlib ordering)
            brg_image = cv2.imread(image_path)
            rgb_image = cv2.cvtColor(brg_image, cv2.COLOR_BGR2RGB)

            # detect the (x, y)-coordinates of the bounding boxes
            # corresponding to each face in the input image
            # boxes = face_recognition.face_locations(rgb_image, model = args["detection_method"])
            # Detects faces and returns an array of bounding boxes in css (top, right, 
            # bottom, left) order (like padding).
            # TODO As per a comment in facecapture.py, it may not be necessary to draw a box
            # in facecapture.py as this detects the face implicitly.
            face_boundaries = face_recognition.face_locations(rgb_image, model = detection_method)

            # Computes a 128-dimensional face encoding (technically called an embedding 
            # which is actually a 128 float numpy array of underfined meaning) for each face 
            # in the image, returning a list of these encodings. 
            # Passed in the image and the bounding box. Also accepts a model parameter 
            # (large (default) or small - small is faster but only returns 5 points), 
            # and a num_jitters which randomly distorts the image before encoding. 
            encodings = face_recognition.face_encodings(rgb_image, face_boundaries)
            
            # Loop over the encodings returned for the image (ideally just one).
            # TODO there should only be one of these, so is it necessary to loop?
            # TODO Although we are using different algorithms, so it is possible that 
            # more than once face will be detected here vs previously found. 
            log.info("Length of encodings: {}".format(len(encodings)))
            for encoding in encodings:
                # Each encoding from the image is appended to the list, with the 
                # relevant name also appended to its relevant list.
                image_encodings.append(encoding)
                image_names.append(name)

        # Construct a dictionary with two keys, and each list as the values.
        log.info("Serializing encodings...")
        encoding_data = {"encodings": image_encodings, "names": image_names}

        # Convert this to a pickled object.
        encoding_pickle = pickle.dumps(encoding_data)

        # Open file writing only in binary format, overwritting existing file. 
        # with open() closes the file automatically, and includes error handling.
        # pickle.dumps() serialises the data into a byte stream, known as "pickling".
        # with open(args["encodings"], "wb") as f:
        #     f.write(pickle.dumps(data))
        with open(self.encoding_file, "wb") as f:
            f.write(encoding_pickle)

        return True


# For testing when calling this module directly.
if __name__ == "__main__":
    face_encoder = FaceEncoder("dataset", "test_pickle.pickle")
    face_encoder.encode_faces()