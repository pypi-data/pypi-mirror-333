from logging import getLogger
from phystool.config import config
from requests import get as download
from requests.exceptions import SSLError

from PySide6.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QTextEdit,
    QVBoxLayout,
)

logger = getLogger(__name__)


class MarkDownDialog(QDialog):
    def __init__(self, markdown: str, title: str):
        super().__init__()
        self.setWindowTitle(title)
        self.setSizeGripEnabled(True)
        self.setGeometry(100, 100, 600, 800)
        self.setMinimumSize(80, 100)
        self.setMaximumSize(800, 1000)
        self._text_edit = QTextEdit(
            markdown=markdown,
            readOnly=True
        )

        btn_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        btn_box.accepted.connect(self.accept)

        layout = QVBoxLayout(self)
        layout.addWidget(self._text_edit)
        layout.addWidget(btn_box)


class ReadmeDialog(MarkDownDialog):
    def __init__(self):
        with (config.get_static_path() / "README.md").open() as md:
            super().__init__(md.read(), "Readme")


class ChangelogDialog(MarkDownDialog):
    CHANGELOG = ""

    def __init__(self):
        if not ChangelogDialog.CHANGELOG:
            user = "jdufour"
            key = "ATBB3LvDXYexfRER3TYawSeLDJRXD1D30A27"
            url = "https://api.bitbucket.org/2.0/repositories/jdufour/phystool/src/master/CHANGELOG.md"
            try:
                response = download(url, auth=(user, key))
                ok = response.ok
            except SSLError:
                logger.error("SSLError: probably a faulty internet connection")
                ok = False

            if not ok:
                msg = f"Can't download 'CHANGELOG.md': {response}"
                logger.error(msg)
                super().__init__(msg, "CHANGELOG")
                return
            ChangelogDialog.CHANGELOG = response.content.decode()
        super().__init__(ChangelogDialog.CHANGELOG, "CHANGELOG")
