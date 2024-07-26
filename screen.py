import mss
import mss.tools
import customtkinter as ctk
from PIL import Image, ImageTk

class ScreenViewerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Visualização em tempo real das telas")
        self.geometry("1400x800")

        self.sct = mss.mss()
        self.monitors = self.sct.monitors

        self.selected_monitors = []

        self.monitor_vars = [ctk.IntVar() for _ in self.monitors[1:]]

        self.create_widgets()

    def create_widgets(self):
        self.checkbuttons_frame = ctk.CTkFrame(self)
        self.checkbuttons_frame.pack(pady=10)

        for i, monitor in enumerate(self.monitors[1:], start=1):
            cb = ctk.CTkCheckBox(self.checkbuttons_frame, text=f'Monitor {i}', variable=self.monitor_vars[i-1])
            cb.pack(anchor="w")

        self.play_button = ctk.CTkButton(self, text="Play", command=self.start_viewing)
        self.play_button.pack(pady=10)

    def start_viewing(self):
        self.selected_monitors = [self.monitors[i+1] for i, var in enumerate(self.monitor_vars) if var.get() == 1]
        
        if not self.selected_monitors:
            ctk.CTkMessagebox.show_warning(title="Aviso", message="Selecione pelo menos um monitor para visualizar.")
            return

        self.viewer_frame = ctk.CTkFrame(self)
        self.viewer_frame.pack(pady=10)

        self.canvases = []
        for monitor in self.selected_monitors:
            canvas = ctk.CTkCanvas(self.viewer_frame, width=1280, height=720)
            canvas.pack(side="left", padx=10)
            self.canvases.append(canvas)

        self.update_images()

    def update_images(self):
        for canvas, monitor in zip(self.canvases, self.selected_monitors):
            screenshot = self.sct.grab(monitor)
            img = Image.frombytes('RGB', screenshot.size, screenshot.rgb)
            img.thumbnail((1280, 720))
            imgtk = ImageTk.PhotoImage(image=img)
            canvas.imgtk = imgtk
            canvas.create_image(0, 0, anchor="nw", image=imgtk)

        self.after(100, self.update_images)

if __name__ == "__main__":
    app = ScreenViewerApp()
    app.mainloop() 
