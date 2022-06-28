import cv2
#useing the vdieo over IP network (
cam = cv2.VideoCapture('rtsp://admin:BIL_2022@192.168.30.128')

while True:
	ret, frame = cam.read()
	cv2.imshow('frame',frame)


	if cv2.waitKey(1) & 0xFF == ord('q'):
		cam.release()
		cv2.destroyAllWindows()
		break

