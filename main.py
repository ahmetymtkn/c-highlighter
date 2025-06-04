from tkinter import Tk
from gui.highlighter_gui import CSyntaxHighlighterGUI

def main():
    root = Tk()
    app = CSyntaxHighlighterGUI(root)
    root.mainloop()

if __name__ == '__main__':
    main()
