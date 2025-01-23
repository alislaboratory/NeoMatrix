from matrixbase import MatrixBase
from conway import Life
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import threading
import time

# Flask setup
app = Flask(__name__)
socketio = SocketIO(app)

# Game of Life matrix class
class NeoMatrix(MatrixBase):
    def __init__(self, *args, **kwargs):
        super(NeoMatrix, self).__init__(*args, **kwargs)
        self.life = Life(32, 16)
        self.life.randomise_grid()
        self.running = False
        self.speed = 0.1  # Default speed

    def run_game_loop(self):
        self.offscreen_canvas = self.matrix.CreateFrameCanvas()
        print("At the top")
        while True:
            print("I mean we're hereee")
            if self.running:
                print("Game is running")  # Debug statement
                self.life.grid = self.life.tick()
                for i in range(16):
                    for j in range(32):
                        if self.life.grid[i][j] == 1:
                            self.offscreen_canvas.SetPixel(j, i, 125, 125, 125)
                        else:
                            self.offscreen_canvas.SetPixel(j, i, 0, 0, 0)
                self.offscreen_canvas = self.matrix.SwapOnVSync(self.offscreen_canvas)

                # Emit the updated grid to the web interface
                socketio.emit("update_grid", {"grid": self.life.grid})

                time.sleep(self.speed)
            else:
                print("Game is paused")  # Debug statement
                time.sleep(0.1)


    def start_game(self):
        self.running = True
        self.run_game_loop()

    def stop_game(self):
        self.running = False

    def randomize_grid(self):
        self.life.randomise_grid()

    def clear_grid(self):
        self.life.clear_grid()

    def set_speed(self, speed):
        self.speed = speed


# Create an instance of TestingMatrix
matrix = NeoMatrix()

# Flask routes and SocketIO events
@app.route("/")
def index():
    return render_template("index.html")


@socketio.on("start")
def start_game():
    print("Start button pressed")
    matrix.process()
    matrix.start_game()


@socketio.on("stop")
def stop_game():
    matrix.stop_game()


@socketio.on("randomize")
def randomize_grid():
    matrix.randomize_grid()
    emit("update_grid", {"grid": matrix.life.grid})


@socketio.on("clear")
def clear_grid():
    matrix.clear_grid()
    emit("update_grid", {"grid": matrix.life.grid})


@socketio.on("set_speed")
def set_speed(data):
    speed = data.get("speed", 0.1)
    matrix.set_speed(speed)


def matrix_thread():
    matrix.run_game_loop()


if __name__ == "__main__":
    # Run the matrix logic in a separate thread
    # game_thread = threading.Thread(target=matrix.run_game_loop, daemon=True)
    # game_thread.start()
    

    # Run the Flask web server
    socketio.run(app, host="0.0.0.0", port=5000)