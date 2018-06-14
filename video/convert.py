import ffmpeg

class VideoConvert(object):
    def __init__(self, thing_id, fps):
        self.thing_id = thing_id
        self.stream = ffmpeg.input("downloads/" + str(thing_id) + "/%09d.png", framerate=fps)
        self.stream = ffmpeg.filter_(self.stream, "fps", fps=30) # I'm not sure this is the right way of doing fps but whatever
    def run(self):
        self.stream = ffmpeg.output(self.stream, "dist/videos/"+ str(self.thing_id) + ".mp4")
        print(ffmpeg.compile(self.stream))
        self.stream.run()

if __name__ == "__main__":
    convert = VideoConvert("test", 10)
    convert.run()
