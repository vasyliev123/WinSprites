from src.Engine import Engine
import tkinter as tk
def main():

    root = tk.Tk()
    root.withdraw()

    engine = Engine()
    engine.add_sprite([100,100], [39, 51])

    while True:
        engine.update()
        root.update()
        root.after(10)

if __name__ == "__main__":
    main()