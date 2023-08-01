class BaseDialog:
    def __init__(self, interface, on_result):
        self.interface = interface
        self.interface._impl = self
        self.on_result = on_result

    def simulate_result(self, result):
        self.on_result(None, result)
        self.interface.future.set_result(result)


class InfoDialog(BaseDialog):
    def __init__(self, interface, title, message, on_result=None):
        super().__init__(interface, on_result=on_result)
        interface.window._impl._action(
            "show info dialog",
            title=title,
            message=message,
        )


class QuestionDialog(BaseDialog):
    def __init__(self, interface, title, message, on_result=None):
        super().__init__(interface, on_result=on_result)
        interface.window._impl._action(
            "show question dialog",
            title=title,
            message=message,
        )


class ConfirmDialog(BaseDialog):
    def __init__(self, interface, title, message, on_result=None):
        super().__init__(interface, on_result=on_result)
        interface.window._impl._action(
            "show confirm dialog",
            title=title,
            message=message,
        )


class ErrorDialog(BaseDialog):
    def __init__(self, interface, title, message, on_result=None):
        super().__init__(interface, on_result=on_result)
        interface.window._impl._action(
            "show error dialog",
            title=title,
            message=message,
        )


class StackTraceDialog(BaseDialog):
    def __init__(self, interface, title, message, content, retry, on_result=None):
        super().__init__(interface, on_result=on_result)
        interface.window._impl._action(
            "show stack trace dialog",
            title=title,
            message=message,
            content=content,
            retry=retry,
        )


class SaveFileDialog(BaseDialog):
    def __init__(
        self,
        interface,
        title,
        filename,
        initial_directory,
        file_types=None,
        on_result=None,
    ):
        super().__init__(interface, on_result=on_result)
        interface.window._impl._action(
            "show save file dialog",
            title=title,
            filename=filename,
            initial_directory=initial_directory,
            file_types=file_types,
        )


class OpenFileDialog(BaseDialog):
    def __init__(
        self,
        interface,
        title,
        initial_directory,
        file_types,
        multiple_select,
        on_result=None,
    ):
        super().__init__(interface, on_result=on_result)
        interface.window._impl._action(
            "show open file dialog",
            title=title,
            initial_directory=initial_directory,
            file_types=file_types,
            multiple_select=multiple_select,
        )


class SelectFolderDialog(BaseDialog):
    def __init__(
        self,
        interface,
        title,
        initial_directory,
        multiple_select,
        on_result=None,
    ):
        super().__init__(interface, on_result=on_result)
        interface.window._impl._action(
            "show select folder dialog",
            title=title,
            initial_directory=initial_directory,
            multiple_select=multiple_select,
        )
