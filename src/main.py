import customtkinter as ctk
from app_view import AppView
from app_controller import AppController

if __name__ == "__main__":
    root = ctk.CTk()
    controller = AppController(None)
    view = AppView(root, controller)
    controller.view = view
    controller.model.attach(view)  
    root.mainloop()