
from myapp.views.base import BaseView
from carta import ReMarkable, Widget

class NoInternetView(BaseView):
    def __init__(self, reMarkable: ReMarkable, current_view: list[callable], additional_args: dict = {}) -> None:
        super().__init__(reMarkable, current_view, additional_args)
    

    def display(self):
        self.rm.add(
            Widget(
                id="no_internet",
                typ="label",
                value="No Internet",
                justify="center",
                x="50%",
                y="10",
                
                fontsize="50",
            )
        )
        self.rm.add(
            Widget(
                id="no_internet_message",
                typ="label",
                value="Please check your internet connection",
                justify="center",
                x="50%",
                y="70",
                fontsize="30",
            )
        )
        self.rm.add(
            Widget(
                id="no_internet_back",
                typ="button",
                value="Back",
                justify="left",
                x="0",
                y="100%",
            )
        )