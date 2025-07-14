import os
import sys
import time
import threading
import subprocess
import tkinter as tk
from tkinter import scrolledtext, messagebox
from PIL import Image, ImageTk
from pyfiglet import Figlet


ICON_FILE       = "ici.ico"
BASE_SCRIPT     = "Base.py"
APP_TITLE       = "Pannel Encre Noir"
ITEMS_PER_PAGE  = 3
VIOLET          = "#9c27b0"

TEXT_EXTS  = {".txt", ".py", ".js", ".java", ".c", ".cpp", ".cs", ".html", ".css", ".json", ".md", ".log", ".yaml", ".yml", ".sh"}
IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".bmp", ".gif"}


ROOT = os.path.dirname(os.path.abspath(__file__))


def list_entries(path, only_folders=False):
    items = sorted(os.listdir(path))
    if only_folders:
        return [i for i in items if os.path.isdir(os.path.join(path, i))]
    return items

def read_text(path):
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    except Exception as e:
        return f"[Erreur lecture] {e}"


def show_text(parent, path):
    win = tk.Toplevel(parent)
    win.title(os.path.basename(path))
    try:
        win.iconbitmap(os.path.join(ROOT, ICON_FILE))
    except:
        pass
    win.configure(bg="black")
    win.geometry("800x600")
    area = scrolledtext.ScrolledText(win, bg="black", fg=VIOLET, insertbackground=VIOLET, font=("Courier", 11))
    area.pack(expand=True, fill="both")
    area.insert("1.0", read_text(path))
    area.configure(state="disabled")

def show_image(parent, path):
    win = tk.Toplevel(parent)
    win.title(os.path.basename(path))
    win.configure(bg="black")
    img = Image.open(path)
    img.thumbnail((900, 700))
    photo = ImageTk.PhotoImage(img)
    lbl = tk.Label(win, image=photo, bg="black")
    lbl.image = photo
    lbl.pack(expand=True)


def ascii_title():
    fig = Figlet(font="ansi_shadow")
    return fig.renderText("Encre Noir")


class EncreNoirApp:
    def __init__(self, root):
        self.root = root
        root.title(APP_TITLE)
        try:
            root.iconbitmap(os.path.join(ROOT, ICON_FILE))
        except:
            pass
        root.configure(bg="black")
        root.attributes("-fullscreen", True)

        self.current = ROOT
        self.history = []
        self.page = 0

        self.build_ui()
        self.refresh()

    def build_ui(self):
        
        lbl = tk.Label(self.root, text=ascii_title(), fg=VIOLET, bg="black", font=("Courier", 12), justify="center")
        lbl.pack()

        
        tk.Label(self.root, text="Create by Celestia", fg=VIOLET, bg="black", font=("Courier", 10)).pack()

        
        self.anim = tk.Label(self.root, text="", fg=VIOLET, bg="black", font=("Courier", 10))
        self.anim.pack(pady=5)
        threading.Thread(target=self._animate, daemon=True).start()

        
        instr = "[T] Suivant   [R] Précédent   [0] Retour   [99] Base.py   [0000] Quitter"
        tk.Label(self.root, text=instr, fg=VIOLET, bg="black", font=("Courier", 10)).pack(pady=5)

        
        self.frame = tk.Frame(self.root, bg="black")
        self.frame.pack(pady=10)

        
        tf = tk.Frame(self.root, bg="black")
        tf.pack(fill="x", pady=(0,20))
        tk.Label(tf, text="Encre.Noir=", fg=VIOLET, bg="black", font=("Courier", 12)).pack(side="left")
        self.cmd = tk.StringVar()
        ent = tk.Entry(tf, textvariable=self.cmd, fg=VIOLET, bg="black", insertbackground=VIOLET, font=("Courier",12))
        ent.pack(side="left", fill="x", expand=True)
        ent.bind("<Return>", lambda e: self.execute(self.cmd.get().strip()))
        ent.focus_set()

    def _animate(self):
        import random, string
        while True:
            s = ''.join(random.choices(string.ascii_letters+string.digits, k=20))
            self.anim.config(text=s)
            time.sleep(0.1)

    def refresh(self):
        
        for w in self.frame.winfo_children():
            w.destroy()
        
        only_folders = (self.current == ROOT)
        items = list_entries(self.current, only_folders)
        
        start = self.page * ITEMS_PER_PAGE
        end = start + ITEMS_PER_PAGE
        page_items = items[start:end]

        self.map = {}
        for i, name in enumerate(page_items, start=1):
            path = os.path.join(self.current, name)
            lbl = tk.Label(self.frame, text=f"[{i}] {name}", fg=VIOLET, bg="black", font=("Courier", 11), anchor="w")
            lbl.pack(fill="x", padx=20, pady=2)
            self.map[str(i)] = path

        
        base_path = os.path.join(ROOT, BASE_SCRIPT)
        if os.path.isfile(base_path):
            lbl99 = tk.Label(self.frame, text="[99] Base.py", fg=VIOLET, bg="black", font=("Courier", 11), anchor="w")
            lbl99.pack(fill="x", padx=20, pady=2)
            self.map["99"] = base_path

        
        lblq = tk.Label(self.frame, text="[0000] Quitter", fg=VIOLET, bg="black", font=("Courier", 11), anchor="w")
        lblq.pack(fill="x", padx=20, pady=2)
        self.map["0000"] = "__QUIT__"

    def execute(self, cmd):
        self.cmd.set("")
        
        if cmd.upper() == "T":
            maxp = (len(list_entries(self.current, self.current==ROOT)) - 1) // ITEMS_PER_PAGE
            if self.page < maxp:
                self.page += 1
            self.refresh()
            return
        
        if cmd.upper() == "R":
            if self.page > 0:
                self.page -= 1
            self.refresh()
            return
        
        if cmd == "0":
            if self.history:
                self.current = self.history.pop()
                self.page = 0
            self.refresh()
            return
        
        tgt = self.map.get(cmd)
        if not tgt:
            return
        
        if tgt == "__QUIT__":
            self.root.destroy()
            return
        
        if tgt.endswith(BASE_SCRIPT):
            subprocess.Popen([sys.executable, tgt])
            return
        
        if os.path.isdir(tgt):
            self.history.append(self.current)
            self.current = tgt
            self.page = 0
            self.refresh()
            return
        
        ext = os.path.splitext(tgt)[1].lower()
        if ext in TEXT_EXTS:
            show_text(self.root, tgt)
        elif ext in IMAGE_EXTS:
            show_image(self.root, tgt)
        else:
            messagebox.showinfo("Non supporté", f"Extension non gérée : {ext}")


if __name__ == "__main__":
    if getattr(sys, "frozen", False):
        os.chdir(os.path.dirname(sys.executable))
    root = tk.Tk()
    EncreNoirApp(root)
    root.mainloop()
