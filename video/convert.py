import ffmpeg

class VideoConvert(object):
    def __init__(self, id, fps):
        self.stream = ffmpeg.input(str(id) + "/%09d.png")
    def run(self):
        self.stream = ffmpeg.output(self.stream, "out.mp4")
        print(ffmpeg.compile(self.stream))
        self.stream.run()

if __name__ == "__main__":
    convert = VideoConvert("test", 1)
    convert.run()
