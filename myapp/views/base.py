from carta import ReMarkable

class BaseView(object):
    def __init__(self, reMarkable: ReMarkable, current_view: list[callable], additional_args: dict = {}) -> None:
        self.current_view = current_view
        self.rm = reMarkable
        self.hooks = []
        self.additional_args = additional_args
        pass

    def display(self):
        pass
    
    def handle_buttons(self, clicked: tuple):
        for hook in self.hooks:
            hook(clicked)
            