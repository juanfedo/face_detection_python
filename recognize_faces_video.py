from imutils.video import VideoStream
import face_recognition
import argparse
import imutils
import pickle
import time
import cv2

class Camera_Singleton:
    __camera = None

    @staticmethod
    def getCamera():
        if Camera_Singleton.__camera == None:
            Camera_Singleton.__camera = VideoStream(src=0).start()
        return Camera_Singleton.__camera 

class VideoCamera():

    def __init__(self):
		self.encodings = '/home/usuario/Codigo/face_detection_python/encodings.pickle'
		print("[INFO] loading encodings...")
		self.data = pickle.loads(open(self.encodings, "rb").read())
		self.vs = Camera_Singleton.getCamera()
		time.sleep(2.0)

    def __del__(self):
        self.vs.stop()

    def frames(self):
		detection_method=''
		print("[INFO] starting video stream...")		
		while True:
			frame = self.vs.read()
			
			# convert the input frame from BGR to RGB then resize it to have
			# a width of 750px (to speedup processing)
			rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
			rgb = imutils.resize(frame, width=750)
			r = frame.shape[1] / float(rgb.shape[1])

			# detect the (x, y)-coordinates of the bounding boxes
			# corresponding to each face in the input frame, then compute
			# the facial embeddings for each face
			boxes = face_recognition.face_locations(rgb,
				model=detection_method)
			encodings = face_recognition.face_encodings(rgb, boxes)
			names = []

			# loop over the facial embeddings
			for encoding in encodings:
				# attempt to match each face in the input image to our known
				# encodings
				matches = face_recognition.compare_faces(self.data["encodings"],
					encoding)
				name = "Unknown"

				# check to see if we have found a match
				if True in matches:
					# find the indexes of all matched faces then initialize a
					# dictionary to count the total number of times each face
					# was matched
					matchedIdxs = [i for (i, b) in enumerate(matches) if b]
					counts = {}

					# loop over the matched indexes and maintain a count for
					# each recognized face face
					for i in matchedIdxs:
						name = self.data["names"][i]
						counts[name] = counts.get(name, 0) + 1

					# determine the recognized face with the largest number
					# of votes (note: in the event of an unlikely tie Python
					# will select first entry in the dictionary)
					name = max(counts, key=counts.get)
				
				# update the list of names
				names.append(name)

			# loop over the recognized faces
			for ((top, right, bottom, left), name) in zip(boxes, names):
				# rescale the face coordinates
				top = int(top * r)
				right = int(right * r)
				bottom = int(bottom * r)
				left = int(left * r)

				# draw the predicted face name on the image
				cv2.rectangle(frame, (left, top), (right, bottom),
					(0, 255, 0), 2)
				y = top - 15 if top - 15 > 15 else top + 15
				cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
					0.75, (0, 255, 0), 2)

			#print ('FRAME ENTREGADO')
			#return cv2.imencode('.jpg', frame)[1].tobytes()
			yield cv2.imencode('.jpg', frame)[1].tobytes()
