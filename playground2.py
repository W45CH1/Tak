import tkinter as tk

def on_resize(event):
    # Calculate scale factor based on window width/height
    scale = min(event.width / base_width, event.height / base_height)
    root.tk.call('tk', 'scaling', scale)

base_width, base_height = 400, 300

root = tk.Tk()
root.geometry(f"{base_width}x{base_height}")
root.bind("<Configure>", on_resize)

# Add your app's widgets here...

root.mainloop()