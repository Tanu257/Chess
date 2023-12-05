import tkinter as tk
import CONSTANTS
class Swind:
    statistics = None
    def on_selectionBUttonClicked(self,button_id):
        self.statistics["pretransformation"] = button_id
        self.tra_label.config(text="Selected Pretransformation - "+CONSTANTS.IDS_2_KEY[self.statistics["pretransformation"]])
        
                 
    def __init__(self,stats) -> None:
        self.statistics = stats
        self.statistics["pretransformation"] = 1

    def runSwind(self):
        root = tk.Tk()
        root.title(self .statistics["side"])
        self.tra_label = tk.Label(root, text="Selected Pretransformation - "+CONSTANTS.IDS_2_KEY[self.statistics["pretransformation"]] )
        self.tra_label.grid(row=2,column=2)
        button = tk.Button(root, text=f"Queen", command=lambda: self.on_selectionBUttonClicked(1))
        button.grid(row=3,column=1)
        button = tk.Button(root, text=f"Rook", command=lambda: self.on_selectionBUttonClicked(4))
        button.grid(row=3,column=2)

        button = tk.Button(root, text=f"Bishop", command=lambda: self.on_selectionBUttonClicked(2))
        button.grid(row=3,column=3)

        button = tk.Button(root, text=f"Knight", command=lambda: self.on_selectionBUttonClicked(3))
        button.grid(row=3,column=4)


        root.mainloop()
