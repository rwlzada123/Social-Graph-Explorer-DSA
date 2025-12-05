# from PyQt5.QtWidgets import (
#     QDialog, QVBoxLayout, QLabel, QPushButton, QTextEdit
# )
# from PyQt5.QtCore import Qt

# from social_graph.graph import Graph

# # Import DSU if it exists — optional
# try:
#     from social_graph.dsu import DSU
#     DSU_AVAILABLE = True
# except ImportError:
#     DSU_AVAILABLE = False


# class CommunityWindow(QDialog):
#     def __init__(self, graph: Graph):
#         super().__init__()
#         self.graph = graph

#         self.setWindowTitle("Community Detection")
#         self.setMinimumWidth(450)

#         # ------------ Pastel Theme ------------
#         self.setStyleSheet("""
#             QDialog {
#                 background-color: #fff9f9;
#             }
#             QLabel {
#                 font-size: 15px;
#                 color: #4b4b4b;
#             }
#             QPushButton {
#                 background-color: #ffd4d4;
#                 padding: 10px;
#                 border-radius: 10px;
#                 font-size: 14px;
#             }
#             QPushButton:hover {
#                 background-color: #ffbcbc;
#             }
#             QTextEdit {
#                 background-color: white;
#                 border: 1px solid #ffcccc;
#                 border-radius: 8px;
#                 padding: 8px;
#                 color: #4b4b4b;
#                 font-size: 14px;
#             }
#         """)

#         # ------------ Layout ------------
#         layout = QVBoxLayout()

#         title = QLabel("Detected Communities")
#         title.setAlignment(Qt.AlignCenter)
#         title.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 10px;")

#         layout.addWidget(title)

#         btn_find = QPushButton("Find Communities")
#         btn_find.clicked.connect(self.find_communities)
#         layout.addWidget(btn_find)

#         self.output = QTextEdit()
#         self.output.setReadOnly(True)
#         layout.addWidget(self.output)

#         self.setLayout(layout)

#     # ------------ Community Detection Logic ------------
#     def find_communities(self):
#         if not self.graph.get_all_users():
#             self.output.setText("No users in graph.")
#             return

#         if DSU_AVAILABLE:
#             result = self._find_components_dsu()
#         else:
#             result = self._find_components_dfs()

#         # Format output
#         text = ""
#         for i, group in enumerate(result, 1):
#             users_str = ", ".join(group)
#             text += f"Group {i}: {users_str}\n"

#         self.output.setText(text.strip())

#     # ------------ DFS-Based Community Detection ------------
#     def _find_components_dfs(self):
#         users = self.graph.get_all_users()
#         visited = set()
#         components = []

#         def dfs(user):
#             stack = [user]
#             group = []

#             while stack:
#                 u = stack.pop()
#                 if u in visited:
#                     continue
#                 visited.add(u)
#                 group.append(u)

#                 for friend in self.graph.get_friends(u):
#                     if friend not in visited:
#                         stack.append(friend)

#             return group

#         for user in users:
#             if user not in visited:
#                 components.append(dfs(user))

#         return components

#     # ------------ DSU-Based Community Detection ------------
#     def _find_components_dsu(self):
#         users = self.graph.get_all_users()
#         n = len(users)

#         # Create DSU with n elements
#         dsu = DSU(n)

#         # Union all friendships
#         for u in users:
#             for v in self.graph.get_friends(u):
#                 dsu.union(self.graph._user_to_id[u], self.graph._user_to_id[v])

#         # Build groups by root
#         groups = {}

#         for user in users:
#             root = dsu.find(self.graph._user_to_id[user])
#             groups.setdefault(root, []).append(user)

#         return list(groups.values())















'''

# gui/community_window.py

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QTextEdit, QPushButton, QHBoxLayout
)
from PyQt5.QtCore import Qt
from social_graph.dsu import DSU
from social_graph.graph import Graph
from gui.graph_canvas import GraphCanvas
from PyQt5.QtGui import QColor


class CommunityWindow(QDialog):
    def __init__(self, graph: Graph):
        super().__init__()
        self.graph = graph

        self.setWindowTitle("🌐 Community Detection (Connected Components)")
        self.setMinimumSize(1100, 600)

        # -------------------------------------------------------
        # Style
        # -------------------------------------------------------
        self.setStyleSheet("""
            QDialog {
                background-color: #f8f5ff;
            }
            QLabel {
                font-size: 18px;
                color: #333;
            }
            QTextEdit {
                background-color: #ffffff;
                border: 1px solid #dcd2ff;
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
                color: #333;
            }
            QPushButton {
                background-color: #c8e9ff;
                padding: 10px;
                border-radius: 10px;
                font-size: 15px;
            }
            QPushButton:hover {
                background-color: #b2ddff;
            }
        """)

        # -------------------------------------------------------
        # Layout (Left = summary, Right = GraphCanvas)
        # -------------------------------------------------------
        root = QHBoxLayout()

        left = QVBoxLayout()
        left.setSpacing(10)

        title = QLabel("Community Detection Using DSU")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 22px; font-weight: bold;")
        left.addWidget(title)

        # Summary output box
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        left.addWidget(self.output)

        # Button to refresh communities
        btn_refresh = QPushButton("Refresh Communities")
        btn_refresh.clicked.connect(self.show_communities)
        left.addWidget(btn_refresh)

        left.addStretch()
        root.addLayout(left, 1)

        # Graph Canvas (color communities)
        self.canvas = GraphCanvas(graph)
        root.addWidget(self.canvas, 2)

        self.setLayout(root)

        # Compute and display communities
        self.show_communities()

    # -------------------------------------------------------
    # Community detection logic (DSU)
    # -------------------------------------------------------
    def show_communities(self):
        users = self.graph.get_all_users()
        n = len(users)
        user_to_id = {u: self.graph.get_user_id(u) for u in users}

        # Run DSU over all friendships
        dsu = DSU(n)

        for u in users:
            for v in self.graph.get_friends(u):
                dsu.union(user_to_id[u], user_to_id[v])

        # Group users by root
        communities = {}
        for u in users:
            root = dsu.find(user_to_id[u])
            communities.setdefault(root, []).append(u)

        # ---------------------------------------------------
        # Display community info (left panel)
        # ---------------------------------------------------
        self.output.clear()

        self.output.append(f"Total Users: {n}")
        self.output.append(f"Total Communities: {len(communities)}\n")

        sorted_comms = sorted(communities.values(), key=lambda x: -len(x))

        for i, group in enumerate(sorted_comms, 1):
            self.output.append(f"Community {i}  (size = {len(group)})")
            self.output.append("Members: " + ", ".join(sorted(group)))
            self.output.append("")

        # ---------------------------------------------------
        # Color communities on GraphCanvas (right panel)
        # ---------------------------------------------------
        self._color_communities(sorted_comms)

    # -------------------------------------------------------
    # Color nodes by community group
    # -------------------------------------------------------
    def _color_communities(self, communities):
        # soft pastel colors
        palette = [
            QColor("#b8e1ff"), QColor("#ffd580"), QColor("#d4ffb2"),
            QColor("#ffb2d8"), QColor("#e3b2ff"), QColor("#b2ffc8"),
            QColor("#ffdfba"), QColor("#bae1ff")
        ]

        self.canvas.reset_colors()

        for idx, group in enumerate(communities):
            color = palette[idx % len(palette)]

            for username in group:
                uid = self.graph.get_user_id(username)
                self.canvas.nodes[uid].item.setBrush(color)
'''



# gui/community_window.py

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QTextEdit, QPushButton,
    QHBoxLayout, QWidget, QScrollArea
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QGraphicsDropShadowEffect

from social_graph.dsu import DSU
from social_graph.graph import Graph
from gui.graph_canvas import GraphCanvas


class CommunityWindow(QDialog):
    def __init__(self, graph: Graph):
        super().__init__()
        self.graph = graph

        # Window size (more compact like BFS/DFS)
        self.setWindowTitle("🌐 Community Detection (DSU)")
        self.resize(1080, 600)
        self.setMinimumSize(900, 540)

        self._build_ui()
        self.show_communities()
        self._apply_theme()

    # -------------------------------------------------------
    # UI BUILD
    # -------------------------------------------------------
    def _build_ui(self):
        root = QHBoxLayout()
        root.setContentsMargins(15, 15, 15, 15)
        root.setSpacing(20)

        # LEFT PANEL inside scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setFixedWidth(330)          # Same width as BFS/DFS theme

        left_container = QWidget()
        left_layout = QVBoxLayout(left_container)
        left_layout.setSpacing(18)
        left_layout.setContentsMargins(10, 10, 10, 10)

        scroll_area.setWidget(left_container)

        # Title
        title = QLabel("🌐 Community Detection (DSU)")
        title.setObjectName("Title")
        title.setAlignment(Qt.AlignCenter)
        left_layout.addWidget(title)

        # Details box
        lbl_details = QLabel("Communities:")
        lbl_details.setObjectName("SectionLabel")
        left_layout.addWidget(lbl_details)

        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.output.setMinimumHeight(260)
        left_layout.addWidget(self.output)

        # Refresh button
        self.btn_refresh = QPushButton("🔄 Refresh Communities")
        self.btn_refresh.setObjectName("runButton")
        self._style_button(self.btn_refresh)
        self.btn_refresh.clicked.connect(self.show_communities)
        left_layout.addWidget(self.btn_refresh)

        left_layout.addStretch()

        # RIGHT PANEL — Graph Canvas
        self.canvas = GraphCanvas(self.graph)
        self.canvas.setMaximumHeight(450) 

        root.addWidget(scroll_area, 0)
        root.addWidget(self.canvas, 1)

        self.setLayout(root)

    # -------------------------------------------------------
    # Button styling
    # -------------------------------------------------------
    def _style_button(self, btn):
        btn.setMinimumHeight(48)
        btn.setStyleSheet("font-size: 15px; font-weight: bold; padding: 6px;")

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(18)
        shadow.setXOffset(1)
        shadow.setYOffset(3)
        btn.setGraphicsEffect(shadow)

    # -------------------------------------------------------
    # Apply theme stylesheet
    # -------------------------------------------------------
    def _apply_theme(self):
        self.setStyleSheet("""
            QDialog {
                background-color: #f3eaff;
            }

            /* TITLE */
            QLabel#Title {
                font-size: 18px;
                font-weight: bold;
                color: #3b2a66;
            }

            /* Section label: "Communities:" etc */
            QLabel {
                font-size: 15px;
                color: #3b2a66;
                font-weight: bold;
            }

            /* Output box */
            QTextEdit {
                background-color: #ffffff;
                border: 2px solid #d9ceff;
                border-radius: 10px;
                padding: 8px;
                font-size: 13px;
                color: #2a2240;
            }

            /* Refresh button */
            QPushButton {
                background-color: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 #dec0ff,
                    stop:1 #caa2ff
                );
                padding: 10px;
                border-radius: 14px;
                font-size: 14px;
                font-weight: bold;
                color: #2d1c48;
                border: 2px solid #b28aff;
            }

            QPushButton:hover {
                background-color: qlineargradient(
                    x1:0, y1:0, x2:0, y2:1,
                    stop:0 #e9d1ff,
                    stop:1 #d7b8ff
                );
            }
        """)

            
    # -------------------------------------------------------
    # COMMUNITY DETECTION LOGIC
    # -------------------------------------------------------
    def show_communities(self):
        users = self.graph.get_all_users()
        n = len(users)
        user_to_id = {u: self.graph.get_user_id(u) for u in users}

        # DSU over friendships
        dsu = DSU(n)
        for u in users:
            for v in self.graph.get_friends(u):
                dsu.union(user_to_id[u], user_to_id[v])

        # Group users by root
        communities = {}
        for u in users:
            root = dsu.find(user_to_id[u])
            communities.setdefault(root, []).append(u)

        sorted_groups = sorted(communities.values(), key=lambda g: -len(g))

        # Display info
        self.output.clear()
        self.output.append(f"Total Users: {n}")
        self.output.append(f"Total Communities: {len(sorted_groups)}\n")

        for i, group in enumerate(sorted_groups, 1):
            self.output.append(f"🔸 Community {i} (size {len(group)})")
            self.output.append("Members: " + ", ".join(sorted(group)))
            self.output.append("")

        # Color communities visually
        self._color_communities(sorted_groups)

    # -------------------------------------------------------
    # COLOR COMMUNITIES
    # -------------------------------------------------------
    def _color_communities(self, communities):
        pastel_palette = [
            QColor("#dec0ff"), QColor("#ffd6a5"), QColor("#bde0fe"),
            QColor("#ffc8dd"), QColor("#caffbf"), QColor("#a0c4ff"),
            QColor("#fdffb6"), QColor("#e4c1f9")
        ]

        self.canvas.reset_colors()

        for idx, group in enumerate(communities):
            color = pastel_palette[idx % len(pastel_palette)]
            for username in group:
                uid = self.graph.get_user_id(username)
                self.canvas.nodes[uid].item.setBrush(color)
