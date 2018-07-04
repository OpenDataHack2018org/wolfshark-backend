import subprocess

class VideoConvert(object):
    def __init__(self, thing_id, fps):
        self.thing_id = thing_id
        self.fps = fps

    def run(self):
        subprocess.run([
            "ffmpeg",
            "-framerate", str(self.fps),
            "-f", "image2",
            "-pattern_type", "glob",
            "-i", "downloads/%d/*.png" % self.thing_id,
            "-vcodec", "libx264",
            "-crf", "25",
            "-pix_fmt", "yuv420p",
            "-y", # overwrite existing file
            "dist/static/videos/%d.mp4" % self.thing_id
        ])

if __name__ == "__main__":
    convert = VideoConvert("test", 10)
    convert.run()
