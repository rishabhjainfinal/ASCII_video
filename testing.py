from PIL import Image, ImageDraw, ImageFont

# size is 15 X 15 pixles 
def create_save_image():
	image = Image.new(mode = "RGB", size = (1920,1080) ,color = "black")
	draw = ImageDraw.Draw(image)
	fnt = ImageFont.truetype('arial.ttf',encoding="unic")
	with open('ascii_art.txt') as f:
		data = f.readlines()

	for row_index,j in enumerate(data) :
		for col_index,i in enumerate(j) :
			print(row_index*15,col_index*15)
			try:
				draw.text((row_index*15,col_index*15),text=data,font=fnt, fill=(255,255,255))
			except :
				pass
	
	
	image.save("image_name.jpg") # save file


# create_save_image()
# import numpy as np, cv2

# with open('ascii_art.txt') as f:data = f.read()

def ascii_to_image(ascii_data,pbs):
	ascii_data = ascii_data.split('\n')
	width,height = len(ascii_data)*pbs,len(ascii_data[0])*pbs
	# creating black image
	image = np.zeros((width,height,3), np.uint8)
	# updating the text in it 
	for index_r,row in enumerate(data) :
		for index_c,ascii_val in enumerate(row) :
			image = cv2.putText(image,ascii_val,(index_c*pbs,(index_r+1)*pbs),cv2.FONT_HERSHEY_PLAIN,0.9,(255,255,255),1)
	return image

# cv2.imshow("a",func(data))
# cv2.waitKey(0)


# def extract_image(video,fps):
#     # 1. get videos frames 
#     vidcap = cv2.VideoCapture('a.mp4')
#     default_fps = round(vidcap.get(cv2.CAP_PROP_FPS))
#     print("default fps of video is --> ",default_fps)
#     if fps < default_fps : steps = round(default_fps/fps)
#     else : steps = 1
#     print("new fps of video is --> ",int(default_fps/steps))
#     success = True
#     while success:
#         count = int(vidcap.get(1))
#         success,frame = vidcap.read()
#         if count>100 and count%steps == 0 :
#             # save txt here here     
#             grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#             a = image_to_ascii(False,pbs=5)
#             a.img = grayFrame.transpose()
#             a.width, a.height = a.img.shape
#             a.crate_assci()
#             a.save_in_file()
#             break


a = [0,1,2,3,4,5,6]

a1 = iter(a)


for i in a1:
	a.append(10)
	print(i)