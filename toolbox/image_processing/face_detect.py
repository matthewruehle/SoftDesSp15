"""
Implementing basic face detection & processing with OpenCV.
-Matt, March 2015
Note that the commented-out lines are mainly because I was mucking about with different types of faces. I was considering wrapping it into a function which would take the type of face (e.g. 'smile', 'joker', &c.) and then perform the corresponding actions, but i am very tired right now.
 """

import cv2
import numpy
kernel = numpy.ones((15,15), 'uint8')
kernel2 = numpy.ones((5,5), 'uint8')
kernel3 = numpy.ones((2,2), 'uint8')

video_capture = cv2.VideoCapture(0)
face_finder = cv2.CascadeClassifier('/usr/share/opencv/haarcascades/haarcascade_frontalface_alt.xml')
eye_finder = cv2.CascadeClassifier('/usr/share/opencv/haarcascades/haarcascade_eye.xml')
alt_eye_finder = cv2.CascadeClassifier('/usr/share/opencv/haarcascades/haarcascade_mcs_eyepair_big.xml')

while True:
	ret, frame = video_capture.read()
	faces = face_finder.detectMultiScale(frame, scaleFactor = 1.2, minSize = (20,20))
	# eyes = alt_eye_finder.detectMultiScale(frame, scaleFactor=1.2, minSize=(10,10))
	for (x, y, w, h) in faces:
		# cv2.ellipse(frame,(x + w/2, y + h/2),(w/3,int(h/2)),0,0,360,(255,255,255),-1)
		# frame[y:y+h, x:x+w] = cv2.dilate(frame[y:y+h, x:x+w,:], kernel)
		frame[y-.2*h:y+1.2*h, x-.2*w:x+1.2*w] = cv2.dilate(frame[y-.2*h:y+1.2*h, x-.2*w:x+1.2*w], kernel)
		# frame[y-.4*h:y+1.4*h, x-.4*w:x+1.4*w] = cv2.dilate(frame[y-.4*h:y+1.4*h, x-.4*w:x+1.4*w], kernel3)
		# cv2.rectangle(frame, (x,y), (x+w, y+h), (0, 255, 255))
		cv2.ellipse(frame,(x + w/2, y + 2*h/3),(w/4,h/6),0,0,180,(0,0,155),(h/20))
		cv2.ellipse(frame, (x + w/3, y+int(1.1*h/3)), (w/8, h/12),0,0,360,(10,10,10),-1)
		cv2.ellipse(frame, (x + w/3, y+int(1.15*h/3)), (w/8, h/12),0,0,110,(10,10,10),3)
		cv2.ellipse(frame, (x + w/3, y+int(1.1*h/3)), (w/10, h/15),0,0,360,(255,255,255),-1)
		cv2.ellipse(frame, (x + 2*w/3, y+int(1.1*h/3)), (w/8, h/12),0,0,360,(10,10,10),-1)
		cv2.ellipse(frame, (x + 2*w/3, y+int(1.1*h/3)), (w/10, h/15),0,0,360,(255,255,255),-1)
		cv2.ellipse(frame, (x + 2*w/3, y+int(1.15*h/3)), (w/8, h/12),0,70,180,(10,10,10),3)
		cv2.circle(frame, (x+w/3, y+int(1.1*h/3)),(w/25),(10,10,10),-1)
		cv2.circle(frame, (x+2*w/3, y+int(1.1*h/3)),(w/25),(10,10,10),-1)
		# cv2.ellipse(frame, (x + w/3, y+int(1.1*h/3)), (w/10, h/15),0,0,360,(10,10,10),3)
		# cv2.ellipse(frame, (x + 2*w/3, y+int(1.1*h/3)), (w/10, h/15),0,0,360,(10,10,10),3)
		# cv2.ellipse(frame,(x + w/2, y + int(1.8*h/3)),(w/4,h/6),0,30,150,(0,0,155),10)

	# eyes = eye_finder.detectMultiScale(frame, scaleFactor = 1.2, minSize = (5,5))
	# for (x, y, w, h) in eyes:
	# 	frame[y+(h/3.0):y+h - (h/3.0), x + (w/3.0) :x+w - (w/3.0)] = cv2.erode(frame[y+(h/3.0):y+h - (h/3.0), x + (w/3.0) :x+w - (w/3.0)], kernel)
		# cv2.rectangle(frame, (x, y), (x+w, y+h), (0,0,255))

	cv2.imshow('frame', frame)
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

video_capture.release()
cv2.destroyAllWindows()