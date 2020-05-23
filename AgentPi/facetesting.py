# See module description in agenttesting.py
# In addition, this module tests the modules responsible for interacting
# with the camera and the intermediate encoding file. Other face recognition
# tests such as validation of the token are conducted in other modules
# such as agenttesting.py

# These tests operate on test data, not actual data and as such can be 
# initiated without modifying or affecting any core data such as the 
# customer face profiles.
# However because of the order of testing, it is necessary to ensure that
# that the tester's face is included in the valid file. To achieve this
# it may be neccessary to run these tests with fails first, and then
# test properly afterwards.

import unittest
import time

# Modules to be tested.
import faceencoder
import facecapture
import facerecognition


# This class tests a face capture event - it requires tester interaction, active 
# hardware, and takes approximately two minutes.

# This testing class is structured in such a way as to test a non-working face database
# actively without compromising the existing face profiles. If it does however, it
# avoids collisions with the existing user base to maintain integrity by 
# using different file structures that the primary software ignores. Modification of
# this is NOT RECOMMENDED.
# It is necessary for a face to be present to test. Also note that tests are
# order dependant and names as such. As such note that this test is monolithic 
# in nature - Fail early, fail fast.
class TestFaceRecognition(unittest.TestCase):

    # Define all the variables for consistent testing across all functions.
    def setUp(self):
        # Random named objects are for faces that are unintentionally captured.
        self.dataset_valid = "testing/dataset"
        self.dataset_invalid = "testing/dataset_inv"
        self.dataset_random = "testing/dataset_rand"
        # face files - mimicks user names.
        self.face_random = "random_face"
        self.face_valid = "valid_face"
        # self.invalid_face = "testing/invalid_face"
        self.pickle_file_valid = "testing/testpickle.pickle"
        self.pickle_file_invalid = "testing/testpickle_inv.pickle"

    # This will add the face to the test database.
    # Test that a face is present and that adequate files are captured.
    def test_01_face_is_present(self):
        face_capture_valid = facecapture.FaceCapture(self.face_valid, self.dataset_valid)
        print("LOOK AT CAMERA FOR 15 SECONDS!")
        capture_valid = face_capture_valid.capture_face()
        self.assertEqual(capture_valid, True)
        print("Done - Keep paying attention though...")
        time.sleep(1)

    # Test the timeout and graceful return of a missing face.
    def test_02_face_is_not_present(self):
        face_capture_random = facecapture.FaceCapture(self.face_random, self.dataset_random)
        print("NO FACES IN VIEW OF CAMERA FOR 15 SECONDS!")
        capture_invalid = face_capture_random.capture_face()
        print("Done - Keep paying attention though....")
        self.assertEquals(capture_invalid, False)
        time.sleep(1)

    # Encode the test faces just captured.
    def test_03_encode_valid(self):
        encoder_valid = faceencoder.FaceEncoder(self.dataset_valid, self.pickle_file_valid)
        encoding_valid = encoder_valid.encode_faces()
        self.assertEquals(encoding_valid, True)

    # Encode the database of pre-existing faces
    # We reencode this each time incase the encoding library changes.
    def test_04_encode_invalid(self):
        encoder_invalid = faceencoder.FaceEncoder(self.dataset_invalid, self.pickle_file_invalid)
        encoding_invalid = encoder_invalid.encode_faces()
        self.assertEquals(encoding_invalid, True)

    # Test face against database it does exist in.
    def test_05_recog_valid(self):
        print("LOOK AT CAMERA for 30 seconds!")
        recogniser_valid = facerecognition.FaceRecognition(self.pickle_file_valid)
        recognition_valid = recogniser_valid.recognise_face()
        self.assertEquals(recognition_valid, self.face_valid)

    # Test face against a database that it does not exist in, and the graveful return.
    def test_06_unrecog_valid(self):
        recogniser_invalid = facerecognition.FaceRecognition(self.pickle_file_invalid)
        recognition_invalid = recogniser_invalid.recognise_face()
        self.assertEquals(recognition_valid, None)
    

"""
Okay so what are we doing here - In this test, we first capture a face
to test against the pickle file. There exists files for creating a 
false database to test the tester's face against. So we capture faces,
and also test the absense of a face. Then we create a real and a 
false database (based on preexisting files) and test the tester's 
face against them confirming the return.
"""
if __name__ == '__main__':
    unittest.main()