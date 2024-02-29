import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageDraw, ImageFont

class WatermarkApp:
    """
    A class representing the Watermark Application GUI.

    Attributes:
        master (tk.Tk): The root Tkinter window.
        upload_button (tk.Button): Button to upload an image.
        canvas (tk.Canvas): Canvas to display the image.
        add_watermark_button (tk.Button): Button to add a watermark to the image.
        image_path (str): Path of the uploaded image.
    """
    def __init__(self, master):
        """
        Initialize the WatermarkApp.

        Args:
            master (tk.Tk): The root Tkinter window.
        """
        self.master = master
        self.master.title("Watermark App")

        self.upload_button = tk.Button(self.master, text="Upload Image", command=self.upload_image)
        self.upload_button.pack()

        self.canvas = tk.Canvas(self.master, width=400, height=400)
        self.canvas.pack()

        self.add_watermark_button = tk.Button(self.master, text="Add Watermark", command=self.add_watermark)
        self.add_watermark_button.pack()

    def upload_image(self):
        """
        Open a file dialog to upload an image.
        """
        file_path = filedialog.askopenfilename()
        if file_path:
            self.image_path = file_path
            self.display_image(file_path)

    def display_image(self, file_path):
        """
        Display the uploaded image on the canvas.

        Args:
            file_path (str): Path of the uploaded image.
        """
        image = Image.open(file_path)
        # Resize image to fit canvas if needed
        if image.width > 400 or image.height > 400:
            image.thumbnail((400, 400))
        self.photo = ImageTk.PhotoImage(image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.photo)

    def add_watermark(self):
        """
        Add a watermark to the uploaded image and save the watermarked image.
        """
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
    """
    Entry point of the application.
    """
    root = tk.Tk()
    app = WatermarkApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
