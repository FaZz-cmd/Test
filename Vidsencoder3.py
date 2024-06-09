import customtkinter as ctk
from tkinter import filedialog
import tkinter.messagebox as tkmb
import os
import subprocess
import threading

def browse_video_file():
    file_path = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4 *.mkv *.mov")])
    if file_path:
        input_path.set(file_path.replace('/', '\\'))
        video_name_entry.delete(0, ctk.END)
        video_name_entry.insert(0, os.path.splitext(os.path.basename(file_path))[0])

def browse_output_folder():
    folder_path = filedialog.askdirectory()
    if folder_path:
        output_path.set(folder_path.replace('/', '\\'))

def keep_video_name():
    video_name_entry.delete(0, ctk.END)
    video_name_entry.insert(0, os.path.splitext(os.path.basename(input_path.get()))[0])

def encode_video():
    input_value = input_path.get()
    output_folder = output_path.get()
    video_name = video_name_entry.get()
    encoder = encoder_var.get()
    format = format_var.get()
    resolution_display = resolution_var.get()

    if not input_value or not output_folder or not video_name:
        tkmb.showerror("Error", "Please select the video file, output folder, and specify the video name.")
        return

    output_file = os.path.join(output_folder, f"{video_name}.{format}")

    if (encoder in ['ProRes', 'ffv1'] and format not in ['mov', 'mkv']) or \
       (encoder not in ['ProRes', 'ffv1'] and format not in ['mp4', 'mkv']):
        tkmb.showerror("Error", "Codec and format are incompatible.")
        return

    resolution_command = "" if resolution_display == "Keep" else resolution_mapping[resolution_display]

    audio_format_command = f'ffprobe -v error -show_entries stream=codec_name -of default=noprint_wrappers=1:nokey=1 "{input_value}"'
    result = subprocess.run(audio_format_command, shell=True, capture_output=True, text=True)
    audio_format = result.stdout.strip()

    compatible_audio_formats = {
        "mp4": ["aac"],
        "mov": ["aac", "flac"],
        "mkv": ["aac", "flac", "mp3", "wav", "opus"]
    }

    if audio_format not in compatible_audio_formats[format]:
        temp_audio_file = os.path.join(output_folder, "temp_audio.aac")
        reencode_audio_command = f'ffmpeg -hide_banner -y -i "{input_value}" -c:a aac -b:a 614k "{temp_audio_file}"'
        subprocess.run(reencode_audio_command, shell=True)
        audio_copy_command = f'-i "{temp_audio_file}" -c:a copy'
    else:
        audio_copy_command = '-c:a copy'

    ffmpeg_command = f'ffmpeg -hide_banner -y -i "{input_value}" {audio_copy_command} {resolution_command} {encoder_command[encoder]} "{output_file}"'

    def run_ffmpeg_command():
        subprocess.run(ffmpeg_command, shell=True)
        tkmb.showinfo("Success", "Video encoded successfully!")

    threading.Thread(target=run_ffmpeg_command).start()

app = ctk.CTk()
app.title("Video Encoder")
app.geometry("517x330")

input_path = ctk.StringVar()
output_path = ctk.StringVar()
encoder_var = ctk.StringVar(value="x264")
format_var = ctk.StringVar(value="mp4")
resolution_var = ctk.StringVar(value="Keep")

encoder_command = {
    "x264": "-c:v libx264 -crf 16 -preset slow -x264-params direct=spatial:me=umh -pix_fmt yuv420p",
    "x265": "-c:v libx265 -crf 18 -preset medium -pix_fmt yuv420p",
    "AV1": "-c:v libsvtav1 -qp 20 -preset 7 -svtav1-params tune=0:enable-tf=0:enable-overlays=1:enable-qm=1 -pix_fmt yuv420p10le",
    "VP9": "-c:v libvpx-vp9 -b:v 0 -crf 18 -cpu-used 3 -aq-mode 1 -pix_fmt yuv420p",
    "ProRes": "-c:v prores_ks -profile:v 4 -vendor apl0 -bits_per_mb 8000 -pix_fmt yuva444p10le",
    "ffv1": "-c:v ffv1 -coder 2 -context 1 -level 3 -slices 12 -g 1",
    "h264_nvenc": "-c:v h264_nvenc -preset p6 -b_adapt 1 -rc-lookahead 30 -qp 18 -qp_cb_offset -2 -qp_cr_offset -2 -pix_fmt nv12",
    "hevc_nvenc": "-c:v hevc_nvenc -preset p6 -b_adapt 1 -rc-lookahead 30 -qp 18 -qp_cb_offset -2 -qp_cr_offset -2 -pix_fmt nv12",
    "Av1_nvenc": "-c:v av1_nvenc -preset p7 -tune:v hq -rc:v vbr -cq:v 12 -b:v 250M -pix_fmt nv12",
    "h264_amf": "-c:v h264_amf -quality balanced -profile high -rc cqp -qp 20 -pix_fmt nv12",
    "hevc_amf": "-c:v hevc_amf -quality balanced -profile main -rc cqp -qp 20 -pix_fmt nv12",
    "av1_amf": "-c:v av1_amf -quality balanced -profile main -rc cqp -qp 20 -pix_fmt nv12",
    "h264_qsv": "-c:v h264_qsv -preset slow -q 25 -pix_fmt nv12",
    "hevc_qsv": "-c:v hevc_qsv -preset slow -q 25 -pix_fmt nv12",
    "av1_qsv": "-c:v av1_qsv -preset slow -q 25 -pix_fmt nv12",
    "av1-youtube": "-c:v libsvtav1 -b:v 30M -g 120 -keyint_min 120 -sc_threshold 0 -pix_fmt yuv420p -color_primaries bt709 -color_trc bt709 -colorspace bt709 -rc:v cbr",
    "h264-youtube": "-c:v libx264 -b:v 35M -g 120 -keyint_min 120 -sc_threshold 0 -pix_fmt yuv420p -color_primaries bt709 -color_trc bt709 -colorspace bt709 -profile:v high -bf 2 -b_strategy 2",
    "h265-youtube": "-c:v libx265 -b:v 30M -g 120 -keyint_min 120 -sc_threshold 0 -pix_fmt yuv420p10le -color_primaries bt709 -color_trc bt709 -colorspace bt709 -rc:v cbr"
}

resolution_mapping = {
    "Keep": "",
    "720p": "-vf scale=1280:720",
    "1080p": "-vf scale=1920:1080",
    "2k": "-vf scale=2560:1440",
    "4k": "-vf scale=3840:2160"
}

# Frame for input and output selection
frame_select = ctk.CTkFrame(app)
frame_select.grid(row=0, column=0, padx=10, pady=10, sticky="nswe")

ctk.CTkLabel(frame_select, text="Input File:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
input_entry = ctk.CTkEntry(frame_select, textvariable=input_path, width=250, state="disabled")
input_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")
browse_input_button = ctk.CTkButton(frame_select, text="Browse...", command=browse_video_file)
browse_input_button.grid(row=0, column=2, padx=5, pady=5, sticky="w")

ctk.CTkLabel(frame_select, text="Output Folder:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
output_entry = ctk.CTkEntry(frame_select, textvariable=output_path, width=250, state="disabled")
output_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")
ctk.CTkButton(frame_select, text="Browse...", command=browse_output_folder).grid(row=1, column=2, padx=5, pady=5, sticky="w")

ctk.CTkLabel(frame_select, text="Video Name:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
video_name_entry = ctk.CTkEntry(frame_select, width=250)
video_name_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")
keep_name_button = ctk.CTkButton(frame_select, text="Keep Video Name", command=keep_video_name)
keep_name_button.grid(row=2, column=2, padx=5, pady=5, sticky="w")

# Frame for encoding settings
frame_settings = ctk.CTkFrame(app)
frame_settings.grid(row=1, column=0, padx=10, pady=10, sticky="nswe")

frame_settings.columnconfigure(0, weight=1)
frame_settings.columnconfigure(1, weight=1)

ctk.CTkLabel(frame_settings, text="Codec:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
encoder_combobox = ctk.CTkOptionMenu(frame_settings, variable=encoder_var, values=list(encoder_command.keys()))
encoder_combobox.grid(row=0, column=1, padx=5, pady=5, sticky="w")

ctk.CTkLabel(frame_settings, text="Format:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
format_combobox = ctk.CTkOptionMenu(frame_settings, variable=format_var, values=["mp4", "mkv", "mov"])
format_combobox.grid(row=1, column=1, padx=5, pady=5, sticky="w")

ctk.CTkLabel(frame_settings, text="Resolution:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
resolution_combobox = ctk.CTkOptionMenu(frame_settings, variable=resolution_var, values=["Keep", "720p", "1080p", "2k", "4k"])
resolution_combobox.grid(row=2, column=1, padx=5, pady=5, sticky="w")

# Button to start encoding
ctk.CTkButton(app, text="Encode", command=encode_video).grid(row=2, column=0, padx=10, pady=20, sticky="n")

app.mainloop()
