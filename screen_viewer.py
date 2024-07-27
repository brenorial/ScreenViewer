import mss
import mss.tools
import customtkinter as ctk
from PIL import Image, ImageTk
import tkinter as tk

class SelectionWindow(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Definir o tema para "Screen Viewer"
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        
        self.title("Seleção de Monitores")
        self.geometry("600x300")

        self.sct = mss.mss()
        self.monitors = self.sct.monitors

        self.monitor_vars = [ctk.IntVar() for _ in self.monitors[1:]]

        self.create_widgets()

    def create_widgets(self):

        self.title_label = ctk.CTkLabel(self, text="Screen Viewer", font=("Montserrat", 30))
        self.title_label.pack(side="top", pady=10)

        # Frame para os checkbuttons
        self.checkbuttons_frame = ctk.CTkFrame(self)
        self.checkbuttons_frame.pack(pady=10, fill="x")  # Preencher horizontalmente

        # Frame para centralizar os checkbuttons
        self.checkbuttons_inner_frame = ctk.CTkFrame(self.checkbuttons_frame)
        self.checkbuttons_inner_frame.pack(padx=10, pady=10, side="left", expand=True)  # Centraliza o frame

        for i, monitor in enumerate(self.monitors[1:], start=1):
            cb = ctk.CTkCheckBox(self.checkbuttons_inner_frame, text=f'Monitor {i}', variable=self.monitor_vars[i-1])
            cb.pack(anchor="w", pady=5)  # Ajustar espaçamento vertical

        self.play_button = ctk.CTkButton(self, text="Play", command=self.start_viewing)
        self.play_button.pack(pady=10)

        # Adicionar o texto "Desenvolvido por Rial" na parte inferior
        self.footer_label = ctk.CTkLabel(self, text="Desenvolvido por Rial", font=("Montserrat", 10))
        self.footer_label.pack(side="bottom", pady=10)

        # Aplicar a cor de fundo da janela
    def start_viewing(self):
        self.selected_monitors = [self.monitors[i+1] for i, var in enumerate(self.monitor_vars) if var.get() == 1]
        
        if not self.selected_monitors:
            ctk.CTkMessagebox.show_warning(title="Aviso", message="Selecione pelo menos um monitor para visualizar.")
            return
        
        # Fechar a janela de seleção
        self.destroy()

        # Abrir a janela de visualização
        app = ScreenViewerWindow(self.selected_monitors)
        app.mainloop()

class ScreenViewerWindow(ctk.CTk):
    def __init__(self, selected_monitors):
        super().__init__()

        # Definir o tema para preto
        ctk.set_appearance_mode("dark")

        self.title("Visualização em Tempo Real das Telas")
        self.geometry("1200x600")  # Ajuste o tamanho da janela conforme necessário

        self.sct = mss.mss()
        self.selected_monitors = selected_monitors

        self.create_widgets()

    def create_widgets(self):
        self.viewer_frame = ctk.CTkFrame(self)
        self.viewer_frame.pack(pady=10, fill="both", expand=True)

        self.canvases = []
        num_monitors = len(self.selected_monitors)

        for i, monitor in enumerate(self.selected_monitors):
            # Ajustar o tamanho do canvas para se ajustar ao número de monitores
            canvas_width = (self.winfo_width() - 20 * (num_monitors - 1)) // num_monitors  # Ajustar a largura para todos os canvases
            canvas_height = self.winfo_height() - 60  # Ajustar a altura para se ajustar ao tamanho da janela
            canvas = ctk.CTkCanvas(self.viewer_frame, width=canvas_width, height=canvas_height, bg='black')
            canvas.pack(side="left", padx=10, pady=10, fill="both", expand=True)
            self.canvases.append(canvas)

        self.update_images()

    def update_images(self):
        for canvas, monitor in zip(self.canvases, self.selected_monitors):
            screenshot = self.sct.grab(monitor)
            img = Image.frombytes('RGB', screenshot.size, screenshot.rgb)

            # Ajustar o tamanho da imagem para caber no canvas
            canvas_width = canvas.winfo_width()
            canvas_height = canvas.winfo_height()
            img.thumbnail((canvas_width, canvas_height))
            imgtk = ImageTk.PhotoImage(image=img)

            canvas.imgtk = imgtk
            canvas.create_image(0, 0, anchor="nw", image=imgtk)

        self.after(100, self.update_images)

if __name__ == "__main__":
    app = SelectionWindow()
    app.mainloop()
