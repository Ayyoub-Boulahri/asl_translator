class Subject:
    def __init__(self):
        self._observers = []

    def attach(self, observer):
        if observer is not None and observer not in self._observers:
            self._observers.append(observer)

    def detach(self, observer):
        if observer in self._observers:
            self._observers.remove(observer)

    def notify(self):
        for observer in list(self._observers): 
            if observer is not None:
                observer.update(self)
