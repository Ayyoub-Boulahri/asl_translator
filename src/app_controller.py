from sign_model import SignModel

class AppController:
    def __init__(self, view):
        self.model = SignModel("../nn_model/asl_nn_model.h5", "../nn_model/label_encoder.pkl")
        self.view = view
        self.model.attach(self.view)

    def start_camera(self):
        self.model.start_camera()

    def stop_camera(self):
        self.model.stop_camera()

    def clear_text(self):
        self.model.clear_text()
    
    def set_voice(self, voice_name):
        self.model.set_voice(voice_name)

