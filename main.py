#  -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
#       Printerest Generator INDEV 1.0
#                by kolino
#  -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-


# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
import tkinter
import tkinter.messagebox
import customtkinter
import webbrowser
import sys
from tkinter import filedialog
from pinscrape import pinscrape
import time
import os
from PIL import Image
from moviepy.editor import *
from tkinter import messagebox
import shutil
import subprocess
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-


# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

# -=-=-=-=-=-=-=-[GUI]-=-=-=-=-=-=-=-=-=-
class App(customtkinter.CTk):

    WIDTH = 780
    HEIGHT = 520

    def __init__(self):
        super().__init__()

        self.title("Printerest generator")
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        # self.minsize(App.WIDTH, App.HEIGHT)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)  # call .on_closing() when app gets closed

        # ============ create two frames ============

        # configure grid layout (2x1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame_left = customtkinter.CTkFrame(master=self,
                                                 width=180,
                                                 corner_radius=0)
        self.frame_left.grid(row=0, column=0, sticky="nswe")

        self.frame_right = customtkinter.CTkFrame(master=self)
        self.frame_right.grid(row=0, column=1, sticky="nswe", padx=20, pady=20)

        # ============ frame_left ============

        # configure grid layout (1x11)
        self.frame_left.grid_rowconfigure(0, minsize=10)   # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(5, weight=1)  # empty row as spacing
        self.frame_left.grid_rowconfigure(8, minsize=20)    # empty row with minsize as spacing
        self.frame_left.grid_rowconfigure(11, minsize=10)  # empty row with minsize as spacing

        self.label_1 = customtkinter.CTkLabel(master=self.frame_left,
                                              text="Printerest Generator",
                                              font=("Roboto Medium", -16))  # font name and size in px
        self.label_1.grid(row=1, column=0, pady=1, padx=10)

        self.label_2 = customtkinter.CTkLabel(master=self.frame_left,
                                              text="INDEV",
                                              font=("Roboto Medium", -14))  # font name and size in px
        self.label_2.grid(row=2, column=0, columnspan=1, pady=(1, 1), padx=20)

        self.label_3 = customtkinter.CTkLabel(master=self.frame_left,
                                              text="by kolino",
                                              font=("Roboto Medium", -12))  # font name and size in px
        self.label_3.grid(row=3, column=0, pady=1, padx=10)

        self.button_3 = customtkinter.CTkButton(master=self.frame_left,
                                                text="How to use?",
                                                fg_color=("green", "green"),
                                                command=self.www)
        self.button_3.grid(row=8, column=0, pady=10, padx=20)

        self.switch_2 = customtkinter.CTkSwitch(master=self.frame_left,
                                                text="Dark Mode",
                                                command=self.change_mode)
        self.switch_2.grid(row=10, column=0, pady=10, padx=20, sticky="w")

        # ============ frame_right ============

        # configure grid layout (3x7)
        self.frame_right.rowconfigure((0, 1, 2, 3), weight=1)
        self.frame_right.rowconfigure(7, weight=10)
        self.frame_right.columnconfigure((0, 1), weight=1)
        self.frame_right.columnconfigure(2, weight=0)

        # Entry for subject of generation
        self.entry_subject = customtkinter.CTkEntry(master=self.frame_right,
                                            width=120,
                                            height=35,
                                            placeholder_text="Enter here the subject of generation")
        self.entry_subject.grid(row=0, column=0, columnspan=2, pady=5, padx=20, sticky="we")

        self.entry_num_images = customtkinter.CTkEntry(master=self.frame_right,
                                            width=120,
                                            height=35,
                                            placeholder_text="Number of images (max 15)")
        self.entry_num_images.grid(row=1, column=0, columnspan=2, pady=5, padx=20, sticky="we")

        self.entry_video_length = customtkinter.CTkEntry(master=self.frame_right,
                                            width=120,
                                            height=35,
                                            placeholder_text="Video length in seconds (max 320, min 4)")
        self.entry_video_length.grid(row=2, column=0, columnspan=2, pady=5, padx=20, sticky="we")

        self.mp3_path_entry = customtkinter.CTkEntry(master=self.frame_right,
                                                     width=120,
                                                     height=35,
                                                     placeholder_text="MP3 file path")
        self.mp3_path_entry.grid(row=3, column=0, columnspan=2, pady=0, padx=20, sticky="we")
        self.mp3_path_entry.bind("<Button-1>", self.open_file_dialog)



        self.radio_var = tkinter.IntVar(value=0)

        self.label_radio_group = customtkinter.CTkLabel(master=self.frame_right,
                                                        text="Resolution:")
        self.label_radio_group.grid(row=3, column=2, pady=(150, 10), padx=10, sticky="n")

        self.radio_button_1 = customtkinter.CTkRadioButton(master=self.frame_right,
                                                           variable=self.radio_var,
                                                           text="1920X1080",
                                                           value=0)
        self.radio_button_1.grid(row=4, column=2, pady=(0, 10), padx=0, sticky="n")

        self.radio_button_2 = customtkinter.CTkRadioButton(master=self.frame_right,
                                                           variable=self.radio_var,
                                                           text="1080X1920",
                                                           value=1)
        self.radio_button_2.grid(row=5, column=2, pady=(0, 10), padx=20, sticky="n")

        self.filename_entry = customtkinter.CTkEntry(master=self.frame_right,
                                               width=120,
                                               placeholder_text="File name without .mp4!")
        self.filename_entry.grid(row=8, column=0, columnspan=2, pady=20, padx=20, sticky="we")

        self.button_5 = customtkinter.CTkButton(master=self.frame_right,
                                                text="Generate!",
                                                fg_color=("green", "green"),
                                                command=self.button_event)
        self.button_5.grid(row=8, column=2, columnspan=1, pady=20, padx=20, sticky="we")

        # set default values
        self.radio_button_1.select()
        self.switch_2.select()

    def www(self):
        webbrowser.open('https://github.com/kolinov2/printerest_generator?tab=readme-ov-file#how-to-use')
    def button_event(self):
        print("Starting...")
        if self.radio_var.get() == 1:
            height = 1080
            width = 1920
            scrn = 'screen1080.png'
        else:
            height = 1920
            width = 1080
            scrn = 'screen1920.png'

        if self.filename_entry.get() == '':
            filename4 = 'brainrot-data'
        else:
            filename4 = self.filename_entry.get()

        if self.mp3_path_entry.get() == "":
            mp3_file = 'letgo.mp3'
        else:
            mp3_file = self.mp3_path_entry.get()

        if int(self.entry_video_length.get()) > 320 or int(self.entry_num_images.get()) > 15 or int(self.entry_video_length.get()) <= 3:
            print("error")
            show_error_window()
        else:
            pinlogic(self.entry_subject.get(), self.entry_num_images.get())
            cropping(height, width)
            cooking(height, width, scrn, self.entry_video_length.get(), self.entry_num_images.get(), mp3_file, filename4)
            clean()
            open()



    def slider_event(self, value):
        self.label_value.configure(text=f"{int(value)}")

    def change_mode(self):
        if self.switch_2.get() == 1:
            customtkinter.set_appearance_mode("dark")
        else:
            customtkinter.set_appearance_mode("light")

    def on_closing(self, event=0):
        self.destroy()

    def open_file_dialog(self, event):
        file_path = filedialog.askopenfilename(filetypes=[("MP3 files", "*.mp3")])
        if file_path:
            self.mp3_path_entry.delete(0, tkinter.END)
            self.mp3_path_entry.insert(0, file_path)
    def start(self):
        self.mainloop()
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-


# -=-=-=-=-=-=-=-=-=-=-=-=-[Logic]-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def pinlogic(topic, img):
    ilc = int(img)
    details = pinscrape.scraper.scrape(topic, "output", {}, 10, ilc)

    if details["isDownloaded"]:
        print("\nDownloading completed !!")
        print(f"\nTotal urls found: {len(details['extracted_urls'])}")
        print(f"\nTotal images downloaded (including duplicate images): {len(details['urls_list'])}")
        print(details)
    else:
        show_error_window_pinterest()
        print("\nNothing to download !!", details)

def cropping(target_width, target_height):
    if not os.path.exists('cropped'):
        os.makedirs('cropped')

    for filename in os.listdir('output'):
        if filename.endswith(('.png', '.jpg', '.jpeg')):
            img_path = os.path.join("output", filename)
            with Image.open(img_path) as img:

                scale = target_height / img.height
                new_width = int(img.width * scale)
                new_height = target_height

                resized_img = img.resize((new_width, new_height), Image.LANCZOS)

                left = (new_width - target_width) / 2
                right = left + target_width
                top = 0
                bottom = target_height

                # Przytnij obraz
                cropped_img = resized_img.crop((left, top, right, bottom))

                # Zapisz przycięty obraz w folderze docelowym
                output_path = os.path.join('cropped', filename)
                cropped_img.save(output_path)
                print(f'cropping done!: {filename}')

def cooking(target_width, target_height, screen, durt, img, audio, mp4name):
    resources_folder = "resources"
    cropped_images_folder = 'cropped'
    startscreen_path = os.path.join(resources_folder, screen)
    audio_path = os.path.join(resources_folder, audio)
    output_folder = "cooked"
    try:
        total_duration = float(durt)
    except ValueError:
        raise ValueError(f"Invalid duration value: {durt}")

    startscreen_duration = 3
    try:
        slide_duration = (total_duration - 3) / float(img)
    except ValueError:
        raise ValueError(f"Invalid number of images value: {img}")


    startscreen_clip = ImageClip(startscreen_path, duration=startscreen_duration)


    image_files = sorted([os.path.join(cropped_images_folder, img) for img in os.listdir(cropped_images_folder)])
    slides_clips = [ImageClip(img).set_duration(slide_duration) for img in image_files]


    final_clips = [startscreen_clip] + slides_clips
    video = concatenate_videoclips(final_clips)

    # Dodanie audio
    audio_clip = AudioFileClip(audio_path)
    audio_duration = audio_clip.duration

    # Sprawdzenie, czy długość audio jest mniejsza niż czas trwania filmu
    if audio_duration < total_duration:
        # Powtarzanie audio
        num_repeats = int(total_duration // audio_duration) + 1
        repeated_audio = concatenate_audioclips([audio_clip] * num_repeats)
        # Przycięcie do długości filmu
        audio_clip = repeated_audio.subclip(0, total_duration)
    else:
        # Przycięcie audio do długości filmu
        audio_clip = audio_clip.subclip(0, total_duration)

    # Dodanie audio do filmu
    video = video.set_audio(audio_clip)

    # Nazwa pliku wyjściowego
    output_filename = f"{mp4name}.mp4"
    output_path = os.path.join(output_folder, output_filename)

    # Tworzenie folderu docelowego, jeśli nie istnieje
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Zapisanie finalnego filmu
    video.write_videofile(output_path, codec="libx264", fps=24)

    print(f"Printerest file was create '{output_filename}' in folder '{output_folder}'")

def clean():
    print('cleaning...')
    folders_to_clear = ['cropped', 'output']

    for folder_name in folders_to_clear:
        folder_path = os.path.join(os.getcwd(), folder_name)
        if os.path.exists(folder_path):
            for item in os.listdir(folder_path):
                item_path = os.path.join(folder_path, item)
                if os.path.isdir(item_path):
                    shutil.rmtree(item_path)
                else:
                    os.remove(item_path)
            print(f"Folder '{folder_name}' został wyczyszczony.")
        else:
            print(f"Folder '{folder_name}' nie istnieje.")

def open():
    print('Opening folder../')
    folder_path = os.path.abspath('cooked')
    if os.path.exists(folder_path):
        subprocess.Popen(f'explorer "{folder_path}"')
    else:
        print(f"[ERROR] Folder cooked is not on the drive")


def show_error_window():
    root = tkinter.Tk()
    root.withdraw()  # Ukrywa główne okno
    messagebox.showerror("Error", "[ERROR] The values you have given are too high or wrong.")
    root.destroy()

def show_error_window_pinterest():
    root = tkinter.Tk()
    root.withdraw()  # Ukrywa główne okno
    messagebox.showerror("Error", "[ERROR] There is nothing to download!")
    root.destroy()
# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# -=-=-=-=-=-[START]-=-=-=-=-=-=-=-=-
if __name__ == "__main__":
    print("\033[1;31;40m [Warning!] you are now running the INDEV version you may encounter problems! good luck :) \033[0m")

    print('')
    print('-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-')
    print('         Welcome to the INDEV version of the printerest generator')
    print('When you encounter an error or want to propose a new function, create an issue')
    print('                    thanks for using from kolino!                 ')
    print('-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-')
    print('')
    app = App()
    app.start()

