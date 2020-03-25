from tkinter import *
from PyDictionary import PyDictionary
import ctypes
from tkinter import filedialog
from tkinter.filedialog import askopenfilename
    
class Example(Frame):
        
    def __init__(self, *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
        scrollbar = Scrollbar(Frame.__init__(self, *args, **kwargs))
        self.text = Text(self, wrap="none",yscrollcommand=scrollbar.set)
        self.text.pack(fill="both", expand=True)
        self.text.bind("<ButtonRelease-1>", self._on_click)
        self.text.tag_configure("tag", background="green", foreground="black")
        scrollbar.config(command=self.text.yview)
        scrollbar.pack(side="right", fill="y")
        name = askopenfilename( initialdir="C:/Users/Niranjan P. patil/Desktop/" ,filetypes =( ('All files','*.*'),("Text File", "*.txt")), title = "Choose a file." )
        with open(name, "r", encoding="utf8") as f:
            data = f.read()
            self.text.insert("1.0", data)
            
        
    def _on_click(self, event):
        self.text.tag_remove("tag", "1.0", "end")
        self.text.tag_add("tag", "insert wordstart", "insert wordend")
        dictionary=PyDictionary()
        index = event.widget.index("@%s,%s" % (event.x, event.y))

        # get the indices of all "adj" tags
        tag_indices = list(event.widget.tag_ranges('tag'))

        # iterate them pairwise (start and end index)
        for start, end in zip(tag_indices[0::2], tag_indices[1::2]):
            # check if the tag matches the mouse click index
            if event.widget.compare(start, '<=', index) and event.widget.compare(index, '<', end):
                # return string between tag start and end
                word = event.widget.get(start, end)

        ctypes.windll.user32.MessageBoxW(0, str(dictionary.meaning(word)), "Meaning of "+ word, 1)

if __name__ == "__main__":
    root = Tk()
    #scrollbar = Scrollbar(root)
   # scrollbar.pack( side = RIGHT, fill = Y )
   # scrollbar.config( command = root.yview)
    Example(root).pack(fill="both", expand=True)
    root.mainloop()

