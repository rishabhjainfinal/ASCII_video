import cv2
import numpy as np
import os

# when saving in the fiel replace . from space
class image_to_ascii(object):
	def __init__(self,for_command_line = False,pbs=10):
		# pbs = pixle_block_size
		self.pbs = pbs # pixle_block_size
		# all the ascii characters used are here in the order of the darkness
		self.ascii_range_dictCHARS = [
			'.',
			',',
			"'",
			'"',
			':',
			";",
			'-',
			'*',
			'~',
			'+',
			'=',
			'?',
			'#',
			'%',
			'@'
			]
		# for the better visul of image use reverse 
		self.for_command_line = for_command_line
		if not self.for_command_line :
			self.ascii_range_dictCHARS.reverse()
		self.pixle_to_ascii_dict = {}
		# little help from https://github.com/sjqtentacles/Image-to-Ascii-Art-with-OpenCV/blob/master/image-to-ascii-art-a-demo-using-opencv.ipynb
		for index,key in enumerate(np.linspace(0,255,num=len(self.ascii_range_dictCHARS),endpoint=True)):
			key = round(key)
			if index == 0 :
				last = index
				continue
			for px in range(last,key+1) : 
				self.pixle_to_ascii_dict[px] = self.ascii_range_dictCHARS[index]
			last = key
		
		self.pixle_count_in_block = self.pbs**2
		self.ascii_art = "ascii_art.txt"
		self.img = []

	def image(self,image):
		# convert the image into black and white and read the pixles values  
		# also crate self.img for further processing with self.height and self.width for more computaion
		# read image 
		if not os.path.exists(image) : raise FileNotFoundError("File not found!!.")
		self.img = cv2.imread(image,0).transpose()
		self.width,self.height = self.img.shape
	
	def crate_ascii(self):
		# resonsible for the creation of ascii art from image and return a 2d list as the result  
		# average_pixle colour of each block 
		self.ascii_in_pixles = []
		for index_h,h in enumerate(range(0,self.height,self.pbs)) :
			temp_list = []
			for index_w,w in enumerate(range(0,self.width,self.pbs)) :
				try :
					sum_ = sum(self.img[w:w + self.pbs,h:h+self.pbs].flatten())
					average = round(float(sum_)/self.pixle_count_in_block)
					# print(average)
					temp_list.append(self.pixle_to_ascii_dict[average])
				except : pass # last some pixle less then pixle_count_in_block will be leaved because they may cause some irragularity in shades
			# print()
			self.ascii_in_pixles.append(temp_list)

		return self.ascii_in_pixles

	def save_in_file(self):
		# this will wirte all ascii in the fiel and update if the file exist
		af = open(self.ascii_art,'w')
		for a in self.ascii_in_pixles : 
			to_write = "".join(a)+'\n'
			if self.for_command_line : 
				# print("".join(a))
				to_write = to_write.replace(".",' ')
				to_write = to_write.replace(",",' ')
			af.writelines(to_write)
		af.close()
		print("file saved -> ",self.ascii_art)
	
	@classmethod
	def runner(cls,image,for_command_line,pbs = 10):
		ascii_ = cls(for_command_line=for_command_line,pbs=pbs)
		ascii_.image(image)
		ascii_.crate_ascii()
		ascii_.save_in_file()

if __name__ == "__main__":
	image_to_ascii.runner('abcd.jpg',False,3)
	# image_to_ascii.runner('Screenshot (228).png',False)