from image_to_ascii import image_to_ascii
import cv2,os,numpy as np
import concurrent.futures
from threading import Thread
from time import perf_counter,sleep as nap
from numba import jit, cuda 
# may add sound later .

@jit
class ascii_video :
    """ working of class 
            extract image and yield  
            convert into ascii image 
            save in the video  
    """
    ascii_range_dictCHARS = [
        ' ','.',
        ',',"'",
        '"',':',
        ";",'-',
        '*','~',
        '+','=',
        '?','/',
        '|','#',
        '%','₹',
        '$','@']
    def __init__(self,video,output_video,fps,pbs):
        self.pbs = pbs
        self.video_name = video
        self.video_output_name = output_video
        self.fps = fps
        if not os.path.exists(self.video_name) : raise Exception("File not found!!!")

        self.ascii_range_dictCHARS.reverse()
        self.pixle_to_ascii_dict = {}
        for index,key in enumerate(np.linspace(0,255,num=len(self.ascii_range_dictCHARS),endpoint=True)):
            key = round(key)
            if index == 0 :
                last = index
                continue
            for px in range(last,key+1) : 
                self.pixle_to_ascii_dict[px] = self.ascii_range_dictCHARS[index]
            last = key

        self.pixle_count_in_block = self.pbs**2

        self.frame_list = []

    def __enter__(self):
        # this will start reading and writting the frames 
        print("starting the functions ...")
        # reading video stuff
        self.vidcap = cv2.VideoCapture(self.video_name)
        # fps set for reading and saving file 
        self.total_frames = int(self.vidcap.get(cv2.CAP_PROP_FRAME_COUNT)) 
        print("Total frame count is --> ",self.total_frames)
        default_fps = round(self.vidcap.get(cv2.CAP_PROP_FPS))
        print("default fps of video is --> ",default_fps)
        if self.fps < default_fps : self.steps = round(default_fps/self.fps)
        else : self.steps = 1
        self.fps =int(default_fps/self.steps)
        print("new fps of video is --> ",self.fps)
        self.reader_completed = False
        # extracting first frame for the setup 
        success,frame = self.vidcap.read()
        self.width,self.height = tuple(list(frame.shape)[0:2][::-1]) # for creating ascii from the image
        
        # blank black image
        self.blank_black = np.zeros((self.height,self.width,3), np.uint8)
        
        # for ascii conversion
        self.ascii_in_pixles = np.full([self.height//self.pbs,self.width//self.pbs], "", dtype=np.object)


        # writting video stuff
        self.writer = cv2.VideoWriter(self.video_output_name, cv2.VideoWriter_fourcc(*"mp4v"), self.fps,tuple(list(frame.shape)[0:2][::-1]) )
        return self
    
    def __exit__(self,a,b,c):
        self.vidcap.release() # print(self.vidcap.isOpened())
        print(f"\nSaving video as - { self.video_output_name }")
        self.writer.release()
    
    @jit
    def iter_each_frame(self):  
        success = True
        t1 = Thread(target = lambda : None )
        t1.start()
        while success:
            count = int(self.vidcap.get(1))
            success,frame = self.vidcap.read()
            if count%self.steps == 0 and success :
                if success and self.total_frames > count : 
                    print(f"Working on frame -> '{str(count).zfill(5)}'")
                    t1.join()
                    t1 = Thread(target = lambda : self.frame_list.append(frame))
                    t1.start()
                    # make it save frames in thread  in frame list
        self.reader_completed = True

    @jit
    def image_to_ascii_convertor(self,image):
        # read the image in the b&w format transpose it and return the ascii nested list for that 
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY).transpose()
        ascii_in_pixles  = np.copy(self.ascii_in_pixles)

        # use numpy for fast working here
        for index_h,h in enumerate(range(0,self.height,self.pbs)) :
            for index_w,w in enumerate(range(0,self.width,self.pbs)) :
                try :
                    sum_ = sum(image[w:w + self.pbs,h:h+self.pbs].flatten())
                    average = round(float(sum_)/self.pixle_count_in_block)
                    ascii_in_pixles[index_h][index_w] = self.pixle_to_ascii_dict[average]
                except : pass # last some pixle less then pixle_count_in_block will be leaved because they may cause some irragularity in shades
		
        return ascii_in_pixles

    @jit
    def frame_to_ascii_to_ascii_image(self,current_frame):
        # take frame extract ascii data and return the ascii image
        # print('converting to ASCII images' ,end = " - ")
        ascii_data = self.image_to_ascii_convertor(current_frame)
        # copy that blank image here black image 
        image = np.copy(self.blank_black)
        # np.zeros((self.height,self.width,3), np.uint8)
        # updating the text in it 
        for index_r,row in enumerate(ascii_data) :
            for index_c,ascii_val in enumerate(row) :
                if ascii_val.strip() != "" :
                    image = cv2.putText(image,ascii_val,(index_c*self.pbs,(index_r+1)*self.pbs),cv2.FONT_HERSHEY_PLAIN,0.9,(255,255,255),1)
        return image
    
    @jit
    def add_ascii_frame(self,frame):
        # convert the frame into ascii then convert the ascii to ascii frame 
        ascii_frame = self.frame_to_ascii_to_ascii_image(frame)
        self.writer.write(ascii_frame) # save the frame 

    @jit
    def frame_thread_superviser(self):
        print("working on image computing")
        while not self.reader_completed :
            with concurrent.futures.ThreadPoolExecutor() as executor:
                new_frames = executor.map(self.frame_to_ascii_to_ascii_image , self.frame_list )
                for new_frame in new_frames:
                    Thread(target= lambda : self.frame_list.pop(0)).start()
                    self.writer.write(new_frame) # save the frame 
        
        print('Done. 😎')

    @classmethod
    def runner(cls,video,output_video,fps,pbs):
        with cls(video,output_video,fps,pbs) as ascii_video :
            reader = Thread(target= ascii_video.iter_each_frame )
            reader.start()

            # start the frame saving thread
            saver = Thread(target = ascii_video.frame_thread_superviser)
            saver.start()

            # waiting for complete all the reading frames
            reader.join()
            print('waiting for the results...')
            saver.join()

if __name__ == "__main__" : 
    start = perf_counter()
    ascii_video.runner('ab.mp4',"Ascii_video2.mp4",30,10)
    finish = perf_counter()

    print(f"Total time Taken {finish - start} ")