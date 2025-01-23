from matrixbase import MatrixBase
import random

class TestingMatrix(MatrixBase):
    def __init__(self, *args, **kwargs):
        super(TestingMatrix, self).__init__(*args, **kwargs)

    
    def run(self):
        self.offscreen_canvas = self.matrix.CreateFrameCanvas()
        while True:
            self.usleep(5000)
            self.offscreen_canvas.Fill(random.randint(0,255), random.randint(0,255), random.randint(0,255))
            self.offscreen_canvas = self.matrix.SwapOnVSync(self.offscreen_canvas)
