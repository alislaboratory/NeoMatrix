from matrixbase import MatrixBase
import random
import time
from conway import Life

class TestingMatrix(MatrixBase):
    def __init__(self, *args, **kwargs):
        super(TestingMatrix, self).__init__(*args, **kwargs)
        self.life = Life(32,32)
        self.life.randomise_grid()

    
    def run(self):
        self.offscreen_canvas = self.matrix.CreateFrameCanvas()
        while True:
            time.sleep(0.1)
            self.life.tick()
            for i in range(32):
                for j in range(32):
                    if self.life.grid[i][j] == 1:
                        self.offscreen_canvas.SetPixel(i,j, 255,255,255)
                    else: self.offscreen_canvas.SetPixel(i,j,0,0,0)
            
            self.offscreen_canvas = self.matrix.SwapOnVSync(self.offscreen_canvas)


if __name__ == "__main__":
    test = TestingMatrix()
    if (not test.process()):
        test.print_help()