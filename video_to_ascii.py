from image_to_ascii import image_to_ascii
import cv2

# steps for the working
# 1. extract images 
# 2. convert to ascii 
# 3. create a images of ascii 
# 4. ascii  to image
# 5. save the image in video in the same frame 
# 6. (optional) extract and add sound to the videos 

class ascii_video:
    """ working of class 
            extract image and yield  
            convert into ascii image 
            save in the video  
    """
    def __init__(self,video,fps):
        self.video_name = video
        self.video_output_name = "Ascii_video.mp4"
        self.fps = fps
    
    def read_video(self):
        vidcap = cv2.VideoCapture(self.video_name)
        
        # fps set for reading and saving file 
        default_fps = round(vidcap.get(cv2.CAP_PROP_FPS))
        print("default fps of video is --> ",default_fps)
        if self.fps < default_fps : steps = round(default_fps/self.fps)
        else : steps = 1
        self.fps =int(default_fps/steps)
        print("new fps of video is --> ",self.fps)
        
        success = True
        while success:
            count = int(vidcap.get(1))
            success,frame = vidcap.read()
            if count%steps == 0 :
                try : 
                    self.current_frame = frame 
                    yield True
                except GeneratorExit : break  #"Need to do some clean up."
                except : pass # last frame is none =.=
                else:
                    if success : print(f"Working on frame -> '{str(count).zfill(5)}'",end=" - ")


        vidcap.release() # print(vidcap.isOpened())
        yield False

    def convert_to_ascii_image(self,current_frame):
        # this will convert the black and white frame to ascii letter and creat a image from that letter
        print('converting to ASCII images' ,end = " - ")
        # need only b&w images
        # cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        return current_frame

    def create_video(self):
        # size of the first frames in videos is default   
        # print(list(self.current_frame.shape)[0:2][::-1])
        writer = cv2.VideoWriter(self.video_output_name, cv2.VideoWriter_fourcc(*"mp4v"), self.fps,tuple(list(self.current_frame.shape)[0:2][::-1]) )
        while True :
            try : 
                ascii_frame = self.convert_to_ascii_image(self.current_frame)
                writer.write(ascii_frame)
                print('Saving image in video.')  
                yield
            except GeneratorExit : break  #"Need to do some clean up."
            except : pass # last frame is none =.=

        print(f"Saving video as - {self.video_output_name}")
        writer.release()
        return

    @classmethod
    def runner(cls):
        class_runner = cls('a.mp4',30) # for testing only
        # readiing each image
        reader_gen = class_runner.read_video()
        # saving each convterted image in video with given fps
        cretor_gen = class_runner.create_video()
        # testign loop
        to_iter = True # for first time
        while to_iter:
            to_iter = next(reader_gen)
            if to_iter : 
                next(cretor_gen)
            else :
                print("")
                break
            # break
            # print(type(a.current_frame))
        
def extract_image(video,fps):
    # 1. get videos frames 
    vidcap = cv2.VideoCapture('a.mp4')
    default_fps = round(vidcap.get(cv2.CAP_PROP_FPS))
    print("default fps of video is --> ",default_fps)
    if fps < default_fps : steps = round(default_fps/fps)
    else : steps = 1
    print("new fps of video is --> ",int(default_fps/steps))
    success = True
    while success:
        count = int(vidcap.get(1))
        success,frame = vidcap.read()
        if count>100 and count%steps == 0 :
            # save txt here here     
            grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            a = image_to_ascii(False,pbs=5)
            a.img = grayFrame.transpose()
            a.width, a.height = a.img.shape
            a.crate_assci()
            a.save_in_file()
            break

if __name__ == "__main__":
    ascii_video.runner()