
"""BIL Camera feed """
import cv2 				# IP camera can be access in opencv by streaming URL of

# Using the video over IP network
cam = cv2.VideoCapture('rtsp://admin:BIL_2022@192.168.30.128')
					# connecting to camera username (admin) & password (BIL_2022) @ camera IP address
while True:
	ret, frame = cam.read()
	cv2.imshow('frame',frame)


	if cv2.waitKey(1) & 0xFF == ord('q'):
		cam.release()
		cv2.destroyAllWindows()
		break

