from PyQt5.QtWidgets import QFrame, QStackedLayout

from app.gui.attributes_frame import AttributesFrame


class DataWidget(QFrame):

    def __init__(self, main_window, items):

        """
        Widget contains items with inputs.
        """

        super().__init__(main_window)

        stacked_layout = QStackedLayout()
        main_window.communication.item_selected.connect(stacked_layout.setCurrentIndex)
        self.setLayout(stacked_layout)

        self.showEvent = self._get_show_event(main_window)

        for item in items:
            frame = AttributesFrame(main_window=main_window, item=item)
            stacked_layout.addWidget(frame)

    @staticmethod
    def _get_show_event(main_window):
        """
        Emit signal to hide ActionButton.
        """
        def show_event(event):
            main_window.communication.action_button_toggle.emit(True, 'refresh', main_window.clean_input)

        return show_event
