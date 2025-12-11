from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QComboBox, QPushButton, QMessageBox
)
from PyQt5.QtCore import Qt


class DeleteFriendDialog(QDialog):
    def __init__(self, graph):
        super().__init__()
        self.graph = graph

        self.setWindowTitle("❌ Delete Friendship")
        self.setMinimumWidth(360)

        layout = QVBoxLayout()
        layout.setSpacing(15)

        label = QLabel("Select two users to remove their friendship:")
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(label)

        # User A dropdown
        self.user1 = QComboBox()
        self.user1.addItems(sorted(graph.get_all_users()))
        layout.addWidget(self.user1)

        # User B dropdown
        self.user2 = QComboBox()
        self.user2.addItems(sorted(graph.get_all_users()))
        layout.addWidget(self.user2)

        # Delete button
        btn_delete = QPushButton("❌ Remove Friendship")
        btn_delete.setStyleSheet("font-size: 15px; padding: 8px; font-weight: bold;")
        btn_delete.clicked.connect(self.delete_friendship)
        layout.addWidget(btn_delete)

        self.setLayout(layout)

    def delete_friendship(self):
        u = self.user1.currentText()
        v = self.user2.currentText()

        if u == v:
            QMessageBox.warning(self, "Invalid", "Cannot remove friendship with the same user.")
            return

        if not self.graph.are_friends(u, v):
            QMessageBox.warning(self, "Not friends", f"{u} and {v} are not friends.")
            return

        reply = QMessageBox.question(
            self,
            "Confirm deletion",
            f"Remove friendship between {u} and {v}?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply != QMessageBox.Yes:
            return

        # Backend deletion
        self.graph.remove_friendship(u, v)

        QMessageBox.information(
            self,
            "Friendship removed",
            f"{u} and {v} are no longer friends."
        )

        self.accept()
