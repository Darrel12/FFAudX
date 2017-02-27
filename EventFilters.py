from PyQt4.QtCore import QEvent, QObject, pyqtSignal


# Implement a custom event filter to allow non-clickable objects to have a signal for a click event #
def clickable(widget):
    class Filter(QObject):

        clicked = pyqtSignal()

        def eventFilter(self, obj, event):

            if obj == widget:
                if event.type() == QEvent.MouseButtonDblClick: #  QEvent.MouseButtonRelease:
                    if obj.rect().contains(event.pos()):
                        self.clicked.emit()
                        # The developer can opt for .emit(obj) to get the object within the slot.
                        return True

            return False

    # apply the filter to the widget the user is applying clickable() to
    clickFilter = Filter(widget)
    widget.installEventFilter(clickFilter)
    return clickFilter.clicked
