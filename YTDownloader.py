import customtkinter as ctk
import subprocess
import tkinter.messagebox as tkmb
from tkinter import filedialog
import threading

# Function to run the yt-dlp command in a separate thread
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

# Function to start the thread
def start_export():
    export_thread = threading.Thread(target=export_video)
    export_thread.start()

# Function to select the output folder
def select_output_folder():
    folder_path = filedialog.askdirectory()
    output_entry.delete(0, ctk.END)
    output_entry.insert(0, folder_path)

# Initialize the application
app = ctk.CTk()
app.title("YTDownloader")
app.geometry("500x415")

# Label and entry for the URL
url_label = ctk.CTkLabel(app, text="YouTube video URL:")
url_label.pack(pady=10)
url_entry = ctk.CTkEntry(app, width=400)
url_entry.pack(pady=10)

# Label and quality options
resolution_label = ctk.CTkLabel(app, text="Quality:")
resolution_label.pack(pady=10)
resolution_var = ctk.StringVar(value="1080")
resolution_options = ctk.CTkOptionMenu(app, variable=resolution_var, values=["1080", "1440", "2160"])
resolution_options.pack(pady=10)

# Label and entry for the output folder
output_label = ctk.CTkLabel(app, text="Output Folder:")
output_label.pack(pady=10)
output_entry = ctk.CTkEntry(app, width=400)
output_entry.pack(pady=10)

# Button to select the output folder
output_button = ctk.CTkButton(app, text="Select output folder", command=select_output_folder)
output_button.pack(pady=10)

# Button to export
export_button = ctk.CTkButton(app, text="Export", command=start_export)
export_button.pack(pady=20)

app.mainloop()
