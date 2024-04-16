import tkinter as tk
from tkinter import filedialog
from tkinter.ttk import Progressbar
import os
import subprocess
import threading

def browse_input():
    selected_file = filedialog.askopenfilename(filetypes=[('Video Files', '*.mkv *.mp4 *.webm *.mov')])
    if selected_file:
        input_path.set(selected_file.replace('/', '\\'))

def browse_output():
    output_dir.set(filedialog.askdirectory())

def export(format_value):
    input_path_value = input_path.get()
    output_dir_value = output_dir.get()

    if not input_path_value or not output_dir_value:
        print("Please select an input and output path.")
        return

    output_filename = os.path.join(output_dir_value)
    output_filename = os.path.normpath(output_filename)

    if format_value == 'png':
        ffmpeg_command = f'ffmpeg -hide_banner -i "{input_path_value}" -sws_flags spline+accurate_rnd+full_chroma_int -color_trc 2 -colorspace 2 -color_primaries 2 -map 0:v -c:v png -pix_fmt rgb24 -start_number 0 "{output_filename}/%08d.png"'
    elif format_value == 'tiff':
        ffmpeg_command = f'ffmpeg -hide_banner -i "{input_path_value}" -sws_flags spline+accurate_rnd+full_chroma_int -color_trc 2 -colorspace 2 -color_primaries 2 -map 0:v -c:v tiff -compression_level 1 -start_number 0 "{output_filename}/%08d.tiff"'
    elif format_value == 'jpeg':
        ffmpeg_command = f'ffmpeg -hide_banner -i "{input_path_value}" -sws_flags spline+accurate_rnd+full_chroma_int -color_trc 2 -colorspace 2 -color_primaries 2 -map 0:v -c:v mjpeg -qscale:v 2 -start_number 0 "{output_filename}/%08d.jpeg"'
    else:
        print("Invalid format selected.")
        return

    def run_ffmpeg_command():
        subprocess.run(ffmpeg_command, shell=True)
        progress_bar['value'] = 100

    ffmpeg_thread = threading.Thread(target=run_ffmpeg_command)
    ffmpeg_thread.start()

root = tk.Tk()
root.title("Export Video Frames")

input_path = tk.StringVar()
output_dir = tk.StringVar()

tk.Label(root, text="Input Path:").pack()
tk.Entry(root, textvariable=input_path, width=50).pack()
tk.Button(root, text="Browse...", command=browse_input).pack()

tk.Label(root, text="Output Path:").pack()
tk.Entry(root, textvariable=output_dir, width=50).pack()
tk.Button(root, text="Browse...", command=browse_output).pack()

tk.Label(root, text="Format:").pack()

# Create buttons for each format choice
format_choices = ['png', 'tiff', 'jpeg']
for format_choice in format_choices:
    tk.Button(root, text=format_choice, command=lambda f=format_choice: export(f)).pack()

progress_bar = Progressbar(root, orient="horizontal", length=200, mode="determinate")
progress_bar.pack()

root.mainloop()
