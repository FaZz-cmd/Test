import customtkinter as ctk
import subprocess
import tkinter.messagebox as tkmb

# Fonction pour exécuter la commande yt-dlp
def export_video():
    url = url_entry.get()
    resolution = resolution_var.get()
    command = f'C:\\Users\\matth\\Videos\\timelens\\yt-dlp\\yt-dlp.exe -S "res:{resolution},vcodec:av01,vcodec:vp9,vcodec:h264" -o "%(title)s.%(ext)s" {url} --merge-output-format "mkv"'
    
    try:
        subprocess.run(command, check=True, shell=True)
        tkmb.showinfo("Succès", "Vidéo exportée avec succès!")
    except subprocess.CalledProcessError:
        tkmb.showerror("Erreur", "Erreur lors de l'exportation de la vidéo. Vérifiez l'URL et la résolution.")

# Initialisation de l'application
app = ctk.CTk()
app.title("Exporteur de Vidéo YouTube")
app.geometry("500x300")

# Label et champ pour l'URL
url_label = ctk.CTkLabel(app, text="URL de la vidéo YouTube:")
url_label.pack(pady=10)
url_entry = ctk.CTkEntry(app, width=400)
url_entry.pack(pady=10)

# Label et options de qualité
resolution_label = ctk.CTkLabel(app, text="Qualité:")
resolution_label.pack(pady=10)
resolution_var = ctk.StringVar(value="1080")
resolution_options = ctk.CTkOptionMenu(app, variable=resolution_var, values=["1080", "1440", "2160"])
resolution_options.pack(pady=10)

# Bouton pour exporter
export_button = ctk.CTkButton(app, text="Exporter", command=export_video)
export_button.pack(pady=20)

# Boucle principale de l'application
app.mainloop()
