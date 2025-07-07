import tkinter as tk
from tkinter import messagebox
from google import genai
from google.genai import types
from PIL import Image, ImageTk
from io import BytesIO

# 🔐 Gemini API key
API_KEY = "AIzaSyDFVgqWD0FZBhVzmkpoY4QaNjnCt0Le_-Y"

# 🧠 Configure Gemini
client = genai.Client(api_key=API_KEY)

# 🖼️ GUI function to generate image
def generate_image():
    prompt = prompt_entry.get()

    if not prompt.strip():
        messagebox.showerror("Input Error", "Please enter a prompt.")
        return

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash-preview-image-generation",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_modalities=["TEXT", "IMAGE"]
            )
        )

        for part in response.candidates[0].content.parts:
            if part.inline_data is not None:
                image_data = part.inline_data.data
                image = Image.open(BytesIO(image_data))
                image.save("generated_gui_image.png")
                show_image(image)
                return

        messagebox.showinfo("No Image", "No image was generated.")
    except Exception as e:
        messagebox.showerror("Error", str(e))


# 🖼️ Show image in GUI
def show_image(img):
    img.thumbnail((400, 400))
    tk_img = ImageTk.PhotoImage(img)
    image_label.config(image=tk_img)
    image_label.image = tk_img


# 🖥️ GUI Setup
root = tk.Tk()
root.title("Gemini Image Generator")
root.geometry("500x600")
root.resizable(False, False)

prompt_label = tk.Label(root, text="Enter your prompt:")
prompt_label.pack(pady=10)

prompt_entry = tk.Entry(root, width=60)
prompt_entry.pack(pady=5)

generate_btn = tk.Button(root, text="Generate Image", command=generate_image)
generate_btn.pack(pady=10)

image_label = tk.Label(root)
image_label.pack(pady=20)

root.mainloop()
