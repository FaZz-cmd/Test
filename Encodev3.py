import os
import customtkinter
import subprocess

class ImageEncoder:
    def __init__(self, master):
        self.master = master
        self.input_files = []
        master.title("Image Encoder")

        self.input_label = customtkinter.CTkLabel(master, text="Input Directory:")
        self.input_label.pack()

        self.input_entry = customtkinter.CTkEntry(master, width=50)
        self.input_entry.pack()

        self.input_button = customtkinter.CTkButton(master, text="Browse...", command=self.browse_input)
        self.input_button.pack()

        self.output_label = customtkinter.CTkLabel(master, text="Output File:")
        self.output_label.pack()

        self.output_entry = customtkinter.CTkEntry(master, width=50)
        self.output_entry.pack()

        self.output_button = customtkinter.CTkButton(master, text="Save As...", command=self.save_output)
        self.output_button.pack()

        self.render_button = customtkinter.CTkButton(master, text="Render", command=self.render)
        self.render_button.pack()

    def browse_input(self):
        directory = customtkinter.filedialog.askdirectory(title="Select Input Directory")
        self.input_entry.delete(0, 'end')
        self.input_entry.insert(0, directory)
        self.check_input_files(directory)

    def check_input_files(self, directory):
        self.input_files = []
        for filename in os.listdir(directory):
            if filename.lower().endswith(('.png', '.tif', '.tiff', '.jpg', '.jpeg')):
                self.input_files.append(os.path.join(directory, filename))
        if not self.input_files:
            print("Input directory contains no valid image files.")
            self.input_entry.delete(0, 'end')
        else:
            self.input_entry.insert(0, directory)

    def save_output(self):
        filename = customtkinter.filedialog.asksaveasfilename(title="Save Output File", defaultextension=".mkv")
        self.output_entry.insert(0, filename)

    def render(self):
        command = None
        input_directory = self.input_entry.get()
        output_file = self.output_entry.get()

        if not input_directory or not output_file:
            print("Please select both input and output files.")
            return

        self.check_input_files(input_directory)

        if not self.input_files:
            print("Input directory contains no valid image files.")
            return

        first_file = self.input_files[0]
        command = f"ffmpeg -framerate 48000/1001 -i {first_file} -i {self.input_files[1:]} -c:v ffv1 -coder 2 -context 1 -level 3 -slices 12 -g 1 {output_file}"

        try:
            subprocess.run(command, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"ffmpeg command failed with error code {e.returncode}: {e.output.decode()}")

root = customtkinter.CTk()
encoder = ImageEncoder(root)
root.mainloop()