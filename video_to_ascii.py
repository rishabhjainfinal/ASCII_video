from image_to_ascii import image_to_ascii
import cv2,os,numpy as np
from threading import Thread
from multiprocessing import Process
# may add sound later .

class ascii_video(image_to_ascii) :
    """ working of class 
            extract image and yield  
            convert into ascii image 
            save in the video  
    """
    def __init__(self,video,output_video,fps,pbs):
        self.pbs = pbs
        super().__init__(for_command_line = False,pbs = self.pbs)
        self.video_name = video
        self.video_output_name = output_video
        self.fps = fps
        if not os.path.exists(self.video_name): 
            raise Exception("File not found!!!")

        self.thread_list = []

    def __enter__(self):
        # this will start reading and writting the frames 
        print("starting the functions ...")
        # reading video stuff
        self.vidcap = cv2.VideoCapture(self.video_name)
        # fps set for reading and saving file 
        default_fps = round(self.vidcap.get(cv2.CAP_PROP_FPS))
        print("default fps of video is --> ",default_fps)
        if self.fps < default_fps : steps = round(default_fps/self.fps)
        else : steps = 1
        self.fps =int(default_fps/steps)
        print("new fps of video is --> ",self.fps)
        # extracting first frame for the setup 
        success,frame = self.vidcap.read()

        # writting video stuff
        self.writer = cv2.VideoWriter(self.video_output_name, cv2.VideoWriter_fourcc(*"mp4v"), self.fps,tuple(list(frame.shape)[0:2][::-1]) )
        return self
    
    def __exit__(self,a,b,c):
        self.vidcap.release() # print(self.vidcap.isOpened())
        print(f"Saving video as - { self.video_output_name }")
        self.writer.release()
    
    def read_video(self):
        success = True
        while success:
            count = int(self.vidcap.get(1))
            success,frame = self.vidcap.read()
            # print(success,frame)
            if count%steps == 0 and success :
                try : 
                    self.current_frame = frame 
                    # print(self.current_frame)
                    if success : print(f"Working on frame -> '{str(count).zfill(5)}'",end=" - ")
                    yield True
                except GeneratorExit : break  #"Need to do some clean up."
                except : pass # last frame is none =.=
            else : pass
        
        yield False

    def convert_to_ascii_image(self,current_frame):
        # this will convert the black and white frame to ascii letter and creat a image from that letter
        print('converting to ASCII images' ,end = " - ")
        # need only b&w images
        self.img = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
        self.img = self.img.transpose()
        self.width,self.height = self.img.shape
        ascii_list = self.crate_ascii()
        # creat image 
        return self.ascii_to_image(ascii_list,self.pbs)
    
    def add_ascii_frame(self):
        # size of the first frames in videos is default   
        ascii_frame = self.convert_to_ascii_image(self.current_frame)
        print('Saving image in video.')  
        self.writer.write(ascii_frame)

    def ascii_to_image(self,ascii_data,pbs):
        # print(ascii_data)
        # ascii_data = ascii_data.split('\n')
        width,height = len(ascii_data)*pbs,len(ascii_data[0])*pbs
        # creating black image
        image = np.zeros((width,height,3), np.uint8)
        # updating the text in it 
        for index_r,row in enumerate(ascii_data) :
            for index_c,ascii_val in enumerate(row) :
                image = cv2.putText(image,ascii_val,(index_c*pbs,(index_r+1)*pbs),cv2.FONT_HERSHEY_PLAIN,0.9,(255,255,255),1)
        return image
    
    @classmethod
    def testing(cls):
        with cls('a.mp4',"Ascii_video.mp4",1,20) as ascii_video :



    
    @classmethod
    def runner(cls,video,output_video,fps,pbs):
        class_runner = cls(video,output_video,fps,pbs) # for testing only
        # readiing each image
        reader_gen = class_runner.read_video()
        # saving each convterted image in video with given fps
        cretor_gen = class_runner.add_ascii_frame()
        to_iter = True # for first time
        while to_iter:
            to_iter = next(reader_gen)
            if to_iter : 
                Thread(target=lambda :next(cretor_gen)).start()
                # next(cretor_gen)
            else :
                print("")
                break
        
        class_runner.close()
        
if __name__ == "__main__":
    ascii_video.runner('ab.mp4',"Ascii_video.mp4",1,20)



# updates needed :
    # video creator make it simple not generator 
    # pass argument to the funcion to do its work
    # crate function to which thread submit his work and function save the result in order