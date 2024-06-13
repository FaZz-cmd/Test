import customtkinter as ctk
import subprocess
import tkinter.messagebox as tkmb
from tkinter import filedialog
import threading

def export_video():
    url = url_entry.get()
    resolution = resolution_var.get()
    output_path = output_entry.get()
    
    if not output_path:
        tkmb.showerror("Error", "Please select an output folder.")
        return
    
    command = f'.\\yt-dlp.exe -S "res:{resolution},vcodec:av01,vcodec:vp9,vcodec:h264" -o "{output_path}\\%(title)s.%(ext)s" {url} --merge-output-format "mkv"'
    
    try:
        subprocess.run(command, check=True, shell=True)
        tkmb.showinfo("Success", "Video exported successfully")
    except subprocess.CalledProcessError:
        tkmb.showerror("Error", "Error exporting the video. Check the URL and resolution.")
    except Exception as e:
        tkmb.showerror("Error", f"An error occurred: {str(e)}")

def start_export():
    export_thread = threading.Thread(target=export_video)
    export_thread.start()

def select_output_folder():
    folder_path = filedialog.askdirectory()
    output_entry.delete(0, ctk.END)
    output_entry.insert(0, folder_path)

app = ctk.CTk()
app.title("YTDownloader v1.0.0")
app.geometry("500x415")

url_label = ctk.CTkLabel(app, text="YouTube video URL:")
url_label.pack(pady=10)
url_entry = ctk.CTkEntry(app, width=400)
url_entry.pack(pady=10)

resolution_label = ctk.CTkLabel(app, text="Quality:")
resolution_label.pack(pady=10)
resolution_var = ctk.StringVar(value="1080")
resolution_options = ctk.CTkOptionMenu(app, variable=resolution_var, values=["1080", "1440", "2160"])
resolution_options.pack(pady=10)

output_label = ctk.CTkLabel(app, text="Output Folder:")
output_label.pack(pady=10)
output_entry = ctk.CTkEntry(app, width=400)
output_entry.pack(pady=10)

output_button = ctk.CTkButton(app, text="Select output folder", command=select_output_folder)
output_button.pack(pady=10)

export_button = ctk.CTkButton(app, text="Export", command=start_export)
export_button.pack(pady=20)

app.mainloop()
