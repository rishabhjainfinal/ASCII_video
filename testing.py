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


create_save_image()