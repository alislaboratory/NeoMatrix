import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from conway import Life  # Import your Life class

def update(frame, life, img):
    """
    Update function for the animation.

    Args:
        frame: The current frame of the animation.
        life: An instance of the Life class.
        img: The Matplotlib image object to update.
    """
    life.grid = life.tick()  # Advance the grid by one generation
    img.set_array(life.grid)  # Update the image data
    return img,

def main():
    # Initialize your Life instance with grid dimensions
    rows, cols = 16, 32  # Adjust grid size as needed
    life = Life(cols, rows)
    life.randomise_grid()  # Randomize the initial grid

    # Setup Matplotlib figure and axis
    fig, ax = plt.subplots()
    img = ax.imshow(life.grid, cmap="binary", interpolation="nearest")
    ax.axis("off")  # Hide axes for a clean look

    # Create the animation
    ani = FuncAnimation(
        fig, update, fargs=(life, img), frames=1000, interval=50, blit=False
    )

    # Show the animation
    plt.show()

if __name__ == "__main__":
    main()
