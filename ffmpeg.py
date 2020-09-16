import cv2
import subprocess as sp
import numpy

try:
	IMG_W = 640
	IMG_H = 480

	FFMPEG_BIN = "ffmpeg"
	ffmpeg_cmd = [ FFMPEG_BIN,
				'-f', 'dshow',
				'-i', 'video=USB2.0 HD UVC WebCam',
				'-r', '30',					# FPS
				'-pix_fmt', 'bgr24',      	# opencv requires bgr24 pixel format.
				'-vcodec', 'rawvideo',
				'-video_size', '640x480'
				'-an','-sn',              	# disable audio processing
				'-f', 'image2pipe', '-']    
	pipe = sp.Popen(ffmpeg_cmd, stdout = sp.PIPE, bufsize=10)
	# pipe = sp.Popen(ffmpeg_cmd, stdout=sp.PIPE, stderr=sp.STDOUT, universal_newlines=True)
	# ffmpeg_output, _ = pipe.communicate()
	while True:
		raw_image = pipe.stdout.read(IMG_W*IMG_H*3)
		image =  numpy.fromstring(raw_image, dtype='uint8')		# convert read bytes to np
		image = image.reshape((IMG_H,IMG_W,3))

		cv2.imshow('Video', image)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break

	pipe.stdout.flush()
	cv2.destroyAllWindows()

except Exception as e:
	print(e)