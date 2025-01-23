from matrixbase import MatrixBase
import random
import time

class TestingMatrix(MatrixBase):
    def __init__(self, *args, **kwargs):
        super(TestingMatrix, self).__init__(*args, **kwargs)

    
    def run(self):
        self.offscreen_canvas = self.matrix.CreateFrameCanvas()
        while True:
            time.sleep(0.1)
            self.offscreen_canvas.Fill(random.randint(0,255), random.randint(0,255), random.randint(0,255))
            self.offscreen_canvas = self.matrix.SwapOnVSync(self.offscreen_canvas)


if __name__ == "__main__":
    test = TestingMatrix()
    if (not test.process()):
        test.print_help()