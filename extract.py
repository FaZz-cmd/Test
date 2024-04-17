import tkinter as tk
from tkinter import filedialog
from tkinter.ttk import Progressbar, Combobox, Style
import os
import subprocess
import threading
import shutil

def browse_input():
    selected_file = filedialog.askopenfilename(filetypes=[('Video Files', '*.mkv *.mp4 *.webm *.mov')])
    if selected_file:
        input_path.set(selected_file.replace('/', '\\'))

def browse_output():
    output_dir_value = filedialog.askdirectory()
    if not os.path.exists(output_dir_value):
        os.makedirs(output_dir_value)
    output_dir.set(output_dir_value)

def export():
    input_path_value = input_path.get()
    output_dir_value = output_dir.get()

    if not input_path_value or not output_dir_value:
        print("Please select an input and output path.")
        return

    output_filename = os.path.join(output_dir_value)
    output_filename = os.path.normpath(output_filename)

    format = format_var.get()

    if format == 'PNG':
        ffmpeg_command = f'ffmpeg -hide_banner -i "{input_path_value}" -sws_flags spline+accurate_rnd+full_chroma_int -color_trc 2 -colorspace 2 -color_primaries 2 -map 0:v -c:v png -pix_fmt rgb24 -start_number 0 "{output_filename}/%08d.png"'
    elif format == 'TIFF':
        ffmpeg_command = f'ffmpeg -hide_banner -i "{input_path_value}" -sws_flags spline+accurate_rnd+full_chroma_int -color_trc 2 -colorspace 2 -color_primaries 2 -map 0:v -c:v tiff -pix_fmt rgb24 -start_number 0 "{output_filename}/%08d.tiff"'
    elif format == 'JPEG':
        ffmpeg_command = f'ffmpeg -hide_banner -i "{input_path_value}" -sws_flags spline+accurate_rnd+full_chroma_int -color_trc 2 -colorspace 2 -color_primaries 2 -map 0:v -c:v mjpeg -pix_fmt yuvj420p -q:v 1 -start_number 0 "{output_filename}/%08d.jpg"'

    def run_ffmpeg_command():
        subprocess.run(ffmpeg_command, shell=True)

    ffmpeg_thread = threading.Thread(target=run_ffmpeg_command)
    ffmpeg_thread.start()

root = tk.Tk()
root.title("Export Video Frames to Image")

input_path = tk.StringVar()
output_dir = tk.StringVar()

tk.Label(root, text="Input Path:").pack()
tk.Entry(root, textvariable=input_path, width=50).pack()
tk.Button(root, text="Browse...", command=browse_input).pack()

tk.Label(root, text="Output Path:").pack()
tk.Entry(root, textvariable=output_dir, width=50).pack()
tk.Button(root, text="Browse...", command=browse_output).pack()

style = Style()
style.theme_use('default')
style.configure('TCombobox', width=15)

format_var = tk.StringVar()

format_combobox = Combobox(root, textvariable=format_var, state='readonly')
format_combobox['values'] = ('PNG', 'TIFF', 'JPEG')
format_combobox.current(0)
format_combobox.pack()

tk.Button(root, text="Export", command=export).pack()

root.mainloop()
