import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageDraw, ImageFont

class WatermarkApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Watermark App")

        self.upload_button = tk.Button(self.master, text="Upload Image", command=self.upload_image)
        self.upload_button.pack()

        self.canvas = tk.Canvas(self.master, width=400, height=400)
        self.canvas.pack()

        self.add_watermark_button = tk.Button(self.master, text="Add Watermark", command=self.add_watermark)
        self.add_watermark_button.pack()

    def upload_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.image_path = file_path
            self.display_image(file_path)

    def display_image(self, file_path):
        image = Image.open(file_path)
        # Resize image to fit canvas if needed
        if image.width > 400 or image.height > 400:
            image.thumbnail((400, 400))
        self.photo = ImageTk.PhotoImage(image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)

    def add_watermark(self):
        if not hasattr(self, 'image_path'):
            messagebox.showerror("Error", "Please upload an image first.")
            return

        watermark_text = "© rogertxe"
        image = Image.open(self.image_path)
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype("arial.ttf", 20)  # Adjust font size here
        text_bbox = draw.textbbox((0, 0), watermark_text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        image_width, image_height = image.size
        x = (image_width - text_width) / 2
        y = (image_height - text_height) / 2
        draw.text((x, y), watermark_text, fill=(255, 255, 255, 128), font=font)
        
        # Save watermarked image
        original_filename, original_extension = os.path.splitext(self.image_path)
        watermarked_filename = original_filename + "_watermark" + original_extension
        image.save(watermarked_filename)
        messagebox.showinfo("Success", f"Watermarked image saved as {watermarked_filename}")

def main():
    root = tk.Tk()
    app = WatermarkApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
