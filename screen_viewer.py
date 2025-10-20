import mss
import customtkinter as ctk
from PIL import Image, ImageTk, ImageDraw
import tkinter as tk
from tkinter import messagebox
import pyautogui  # para pegar posição do mouse

REFRESH_MS = 100  # ~10 fps

class SelectionWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")

        self.title("Seleção de Monitores")
        self.geometry("600x320")

        self.sct = mss.mss()
        self.monitors = self.sct.monitors  # [0]=todos; [1..]=monitores individuais
        self.monitor_vars = [ctk.IntVar() for _ in self.monitors[1:]]
        self.create_widgets()

    def create_widgets(self):
        ctk.CTkLabel(self, text="Screen Viewer", font=("Montserrat", 30)).pack(side="top", pady=10)

        wrapper = ctk.CTkFrame(self)
        wrapper.pack(pady=10, padx=12, fill="x")

        inner = ctk.CTkFrame(wrapper)
        inner.pack(padx=10, pady=10, side="left", expand=True)

        for i, _ in enumerate(self.monitors[1:], start=1):
            ctk.CTkCheckBox(inner, text=f"Monitor {i}", variable=self.monitor_vars[i-1]).pack(anchor="w", pady=5)

        ctk.CTkButton(self, text="Play", command=self.start_viewing).pack(pady=10)
        ctk.CTkLabel(self, text="Desenvolvido por Rial", font=("Montserrat", 10)).pack(side="bottom", pady=10)

    def start_viewing(self):
        selected = [self.monitors[i+1] for i, var in enumerate(self.monitor_vars) if var.get() == 1]
        if not selected:
            messagebox.showwarning("Aviso", "Selecione pelo menos um monitor para visualizar.")
            return

        # Esconde a seleção e abre a janela de visualização (redimensionável)
        self.withdraw()
        viewer = ScreenViewerWindow(self, selected)
        viewer.protocol("WM_DELETE_WINDOW", lambda: (viewer.safe_close(), self.deiconify()))


class ScreenViewerWindow(ctk.CTkToplevel):
    def __init__(self, master, selected_monitors):
        super().__init__(master)
        ctk.set_appearance_mode("dark")

        self.title("Visualização em Tempo Real das Telas")
        self.geometry("1200x700")      # janela “caixinha” inicial
        self.minsize(800, 450)         # tamanho mínimo
        self.resizable(True, True)     # permite redimensionar
        # atalhos úteis
        self.bind("<Escape>", lambda e: self.safe_close())

        self.sct = mss.mss()
        self.selected_monitors = selected_monitors

        # topo com controles (opcional: “Sempre no topo”)
        topbar = ctk.CTkFrame(self)
        topbar.pack(side="top", fill="x")
        self.always_on_top = tk.BooleanVar(value=False)
        ctk.CTkCheckBox(topbar, text="Sempre no topo", variable=self.always_on_top,
                        command=self._toggle_ontop).pack(side="left", padx=10, pady=6)

        # área dos canvases (um por monitor)
        self.viewer_frame = ctk.CTkFrame(self)
        self.viewer_frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.canvases = []
        for _ in self.selected_monitors:
            c = tk.Canvas(self.viewer_frame, bg="black", highlightthickness=0)
            c.pack(side="left", padx=10, pady=10, fill="both", expand=True)
            self.canvases.append(c)

        self._after_id = None
        self.running = True
        self.update_images()

    def _toggle_ontop(self):
        self.attributes("-topmost", self.always_on_top.get())

    def safe_close(self):
        self.running = False
        if self._after_id is not None:
            try:
                self.after_cancel(self._after_id)
            except Exception:
                pass
            self._after_id = None
        self.destroy()

    def update_images(self):
        if not self.running:
            return

        # posição global do mouse (para desenhar cursor)
        try:
            mx, my = pyautogui.position()
        except Exception:
            mx, my = None, None

        for canvas, mon in zip(self.canvases, self.selected_monitors):
            shot = self.sct.grab(mon)
            img = Image.frombytes("RGB", shot.size, shot.rgb)

            # desenha cursor “círculo” se o mouse estiver dentro desse monitor
            if mx is not None and my is not None:
                left, top = mon["left"], mon["top"]
                right, bottom = left + mon["width"], top + mon["height"]
                if left <= mx < right and top <= my < bottom:
                    relx, rely = mx - left, my - top
                    draw = ImageDraw.Draw(img, "RGBA")
                    r = 10
                    draw.ellipse((relx - r - 1, rely - r - 1, relx + r + 1, rely + r + 1),
                                 outline=(0, 0, 0, 200), width=3)
                    draw.ellipse((relx - r, rely - r, relx + r, rely + r),
                                 outline=(255, 255, 255, 220), width=2)

            # redimensiona para o tamanho atual do canvas (a janela pode mudar)
            cw = max(canvas.winfo_width(), 1)
            ch = max(canvas.winfo_height(), 1)
            img = img.resize((cw, ch), Image.LANCZOS)

            imgtk = ImageTk.PhotoImage(img)
            canvas.imgtk = imgtk
            canvas.create_image(0, 0, anchor="nw", image=imgtk)

        self._after_id = self.after(REFRESH_MS, self.update_images)


if __name__ == "__main__":
    app = SelectionWindow()
    app.mainloop()
