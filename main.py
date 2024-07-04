from tkinter import *
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageDraw, ImageFont

MAX_WIDTH = 800
MAX_HEIGHT = 600


class WaterMarkerApp:
    def __init__(self, window):
        self.window = window
        self.window.title("WaterMarker")
        self.window.minsize(width=300, height=150)
        self.window.config(padx=20, pady=20)

        self.tk_image = None
        self.image = None

        # Button
        self.upload_btn = Button(window, text="Upload image", command=self.upload_image, width=12)
        self.upload_btn.grid(column=0, row=0)

        self.add_text_btn = Button(window, text="Add text", command=self.add_text, width=12)
        self.add_text_btn.grid(column=0, row=1)

        self.add_logo_btn = Button(window, text="Add logo", command=self.add_logo, width=12)
        self.add_logo_btn.grid(column=0, row=2)

        self.save_btn = Button(window, text="Save image", command=self.save_image, width=12)
        self.save_btn.grid(column=0, row=3)

        # Canvas
        self.canvas = Canvas(window)
        self.canvas.grid(column=0, row=4)

    def upload_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.image = Image.open(file_path)
            self.display_image(self.image)

    def add_text(self):
        if self.image:
            text = "Your Watermark"
            font = ImageFont.truetype("arial.ttf", 100)
            draw = ImageDraw.Draw(self.image)

            # テキストのサイズを取得
            _, _, text_width, text_height = draw.textbbox((0, 0), text=text, font=font)

            width, height = self.image.size
            x = width - text_width - 10
            y = height - text_height - 10

            draw.text((x, y), text, font=font, fill=(255, 255, 255, 128))
            self.display_image(self.image)
        else:
            messagebox.showwarning("警告", "まず画像をアップロードしてください。")

    def add_logo(self):
        if self.image:
            logo_path = filedialog.askopenfilename()
            if logo_path:
                logo = Image.open(logo_path).convert("RGBA")
                width, height = self.image.size
                logo = logo.resize((int(height * 0.2), int(height * 0.2)))
                logo_width, logo_height = logo.size
                position = (width - logo_width - 10, height - logo_height - 10)
                self.image.paste(logo, position, logo)
                self.display_image(self.image)
        else:
            messagebox.showwarning("警告", "まず画像をアップロードしてください。")

    def display_image(self, local_image):
        # 画像のサイズを取得
        width, height = local_image.size

        # 画像のリサイズが必要か確認
        if width > MAX_WIDTH or height > MAX_HEIGHT:
            ratio = min(MAX_WIDTH/width, MAX_HEIGHT/height)
            new_size = (int(width*ratio), int(height*ratio))
            local_image = local_image.resize(new_size)

        self.tk_image = ImageTk.PhotoImage(local_image)
        self.canvas.config(width=self.tk_image.width(), height=self.tk_image.height())
        self.canvas.create_image(self.tk_image.width()/2, self.tk_image.height()/2, image=self.tk_image)

    def save_image(self):
        if self.image:
            save_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("All files", "*.*")])
            if save_path:
                self.image.save(save_path)
                messagebox.showinfo("情報", "画像が保存されました。")
        else:
            messagebox.showwarning("警告", "まず画像をアップロードしてください。")


window = Tk()
app = WaterMarkerApp(window)
window.mainloop()
