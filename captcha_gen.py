import os
import random
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageDraw

# Configuration
IMAGE_DIR = "THIS_FOLDER"  # Folder containing images
GRID_SIZE = 3  # 3x3 grid

# Load images from the directory
def load_images():
    correct_files = [f"correct/{f}" for f in os.listdir(os.path.join(IMAGE_DIR, "correct")) if f.endswith((".png", ".jpg", ".jpeg"))]
    incorrect_files = [f"incorrect/{f}" for f in os.listdir(os.path.join(IMAGE_DIR, "incorrect")) if f.endswith((".png", ".jpg", ".jpeg"))]

    # Select a few correct images and fill the rest with incorrect ones
    num_correct = 3
    selected_correct = random.sample(correct_files, num_correct)
    selected_incorrect = random.sample(incorrect_files, GRID_SIZE * GRID_SIZE - num_correct)

    selected_files = selected_correct + selected_incorrect
    random.shuffle(selected_files)  # Shuffle images so correct ones aren't always first

    correct_indices = {selected_files.index(f) for f in selected_correct}  # Indices of correct images

    return selected_files, correct_indices

# Handle user selection
def check_solution():
    if set(selected) == set(correct_indices):
        messagebox.showinfo("CAPTCHA", "Correct! Folder unlocked.")
        root.quit()  # Closes the Tkinter window
    else:
        messagebox.showerror("CAPTCHA", "Incorrect selection. Try again.")

# Toggle selection and overlay
def select_image(idx):
    if idx in selected:
        selected.remove(idx)
        buttons[idx].config(image=tk_images[idx])
    else:
        selected.add(idx)
        # Create an overlay with a checkmark
        overlay = images[idx].copy()
        draw = ImageDraw.Draw(overlay)
        draw.rectangle([(0, 0), (100, 100)], outline="red", width=5)
        overlay_tk = ImageTk.PhotoImage(overlay)
        buttons[idx].config(image=overlay_tk)
        overlays[idx] = overlay_tk  # Store reference to avoid garbage collection

# Setup Tkinter UI
root = tk.Tk()
root.title("CAPTCHA Challenge")

# Instruction label
instruction_label = tk.Label(root, text="Select all the rick images to verify you are human.", font=("Arial", 12))
instruction_label.pack()

# Load random images
image_files, correct_indices = load_images()
images = [Image.open(os.path.join(IMAGE_DIR, f)).resize((100, 100)) for f in image_files]
tk_images = [ImageTk.PhotoImage(img) for img in images]

overlays = {}  # Store overlay images to prevent garbage collection
selected = set()

# Create buttons for images
buttons = []
frame = tk.Frame(root)
frame.pack()
for i in range(GRID_SIZE):
    for j in range(GRID_SIZE):
        idx = i * GRID_SIZE + j
        btn = tk.Button(frame, image=tk_images[idx], command=lambda i=idx: select_image(i))
        btn.grid(row=i, column=j)
        buttons.append(btn)

# Submit button
submit_btn = tk.Button(root, text="Submit", command=check_solution)
submit_btn.pack()

root.mainloop()

