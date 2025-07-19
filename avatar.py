import tkinter as tk
from PIL import Image, ImageTk, ImageDraw, ImageFilter
import threading, time, math

class SciFiAvatar:
    def __init__(self, size=220):
        self.size = size
        self.root = tk.Tk()
        self.root.overrideredirect(True)
        self.root.attributes('-topmost', True)
        self.root.configure(bg='black')
        self.root.attributes('-transparentcolor', 'black')

        w, h = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        self.root.geometry(f"{size}x{size}+{w-size-30}+{h-size-120}")

        self.canvas = tk.Canvas(self.root, width=size, height=size,
                                bg='black', highlightthickness=0)
        self.canvas.pack()

        # pre-render the ring artwork once
        self.base_img = self._make_rings()
        self.tk_img = ImageTk.PhotoImage(self.base_img)
        self.item = self.canvas.create_image(size//2, size//2, image=self.tk_img)

        self.is_talking = False
        threading.Thread(target=self._pulse_loop, daemon=True).start()

    # ---------- RING ART ----------
    def _make_rings(self):
        img = Image.new('RGBA', (self.size, self.size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        cx = self.size // 2
        for i in range(8, 0, -1):
            radius = cx - 10 - 2*i
            alpha = int(80 + 20*i)          # fade outward
            draw.ellipse([cx-radius, cx-radius, cx+radius, cx+radius],
                         outline=(0, 255, 255, alpha), width=2)
        # inner solid disc
        draw.ellipse([cx-35, cx-35, cx+35, cx+35], fill=(0, 20, 40))
        return img

    # ---------- PULSE LOOP ----------
    def _pulse_loop(self):
        angle = 0
        while True:
            scale = 1 + 0.06 * math.sin(angle) if self.is_talking else 1
            angle += 0.25
            self.root.after(0, self._scale_image, scale)
            time.sleep(0.05)

    def _scale_image(self, scale):
        s = int(self.size * scale)
        img = self.base_img.resize((s, s), Image.LANCZOS)
        self.tk_img = ImageTk.PhotoImage(img)
        self.canvas.itemconfig(self.item, image=self.tk_img)

    # ---------- PUBLIC ----------
    def start_talking(self):
        self.is_talking = True

    def stop_talking(self):
        self.is_talking = False

    def run(self):
        self.root.mainloop()