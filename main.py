import sys
import cv2
import numpy as np
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QGridLayout, QComboBox, QSizePolicy
)
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QImage, QPixmap


class CricketOverlay(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Cricket Overlay App")
        self.setGeometry(100, 100, 1280, 720)

        self.label = QLabel("Camera feed here")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.cap = None

        self.theme = "Dark"
        self.team_name = "IND"
        self.runs = 0
        self.wickets = 0
        self.overs = "0.0"
        self.striker = "Kohli"
        self.striker_runs = 0
        self.striker_balls = 0
        self.non_striker = "Gill"
        self.non_striker_runs = 0
        self.non_striker_balls = 0
        self.bowler = "Bumrah"
        self.bowler_wickets = 0
        self.bowler_runs = 0
        self.bowler_overs = "0.0"

        # Inputs
        self.cam_input = QLineEdit()
        self.cam_input.setPlaceholderText("http://192.168.1.4:8080/video")
        self.connect_button = QPushButton("Connect")
        self.connect_button.clicked.connect(self.connect_camera)

        self.theme_box = QComboBox()
        self.theme_box.addItems(["Dark", "IPL", "Classic", "Blood"])
        self.theme_box.currentIndexChanged.connect(self.set_theme)

        self.input_team = QLineEdit("IND")
        self.input_runs = QLineEdit("0")
        self.input_wickets = QLineEdit("0")
        self.input_overs = QLineEdit("0.0")
        self.input_striker = QLineEdit("Kohli")
        self.input_striker_runs = QLineEdit("0")
        self.input_striker_balls = QLineEdit("0")
        self.input_non_striker = QLineEdit("Gill")
        self.input_non_striker_runs = QLineEdit("0")
        self.input_non_striker_balls = QLineEdit("0")
        self.input_bowler = QLineEdit("Bumrah")
        self.input_bowler_wickets = QLineEdit("0")
        self.input_bowler_runs = QLineEdit("0")
        self.input_bowler_overs = QLineEdit("0.0")

        self.update_button = QPushButton("Update Stats")
        self.update_button.clicked.connect(self.update_stats)

        layout = QVBoxLayout()
        layout.addWidget(self.label)

        controls = QHBoxLayout()
        cam_layout = QVBoxLayout()
        cam_layout.addWidget(self.cam_input)
        cam_layout.addWidget(self.connect_button)
        cam_layout.addWidget(QLabel("Theme:"))
        cam_layout.addWidget(self.theme_box)

        score_layout = QGridLayout()
        score_layout.addWidget(QLabel("Team:"), 0, 0)
        score_layout.addWidget(self.input_team, 0, 1)
        score_layout.addWidget(QLabel("Runs:"), 0, 2)
        score_layout.addWidget(self.input_runs, 0, 3)
        score_layout.addWidget(QLabel("Wickets:"), 1, 0)
        score_layout.addWidget(self.input_wickets, 1, 1)
        score_layout.addWidget(QLabel("Overs:"), 1, 2)
        score_layout.addWidget(self.input_overs, 1, 3)

        player_layout = QGridLayout()
        player_layout.addWidget(QLabel("Striker:"), 0, 0)
        player_layout.addWidget(self.input_striker, 0, 1)
        player_layout.addWidget(QLabel("R:"), 0, 2)
        player_layout.addWidget(self.input_striker_runs, 0, 3)
        player_layout.addWidget(QLabel("B:"), 0, 4)
        player_layout.addWidget(self.input_striker_balls, 0, 5)
        player_layout.addWidget(QLabel("Non-Striker:"), 1, 0)
        player_layout.addWidget(self.input_non_striker, 1, 1)
        player_layout.addWidget(QLabel("R:"), 1, 2)
        player_layout.addWidget(self.input_non_striker_runs, 1, 3)
        player_layout.addWidget(QLabel("B:"), 1, 4)
        player_layout.addWidget(self.input_non_striker_balls, 1, 5)
        player_layout.addWidget(QLabel("Bowler:"), 2, 0)
        player_layout.addWidget(self.input_bowler, 2, 1)
        player_layout.addWidget(QLabel("W:"), 2, 2)
        player_layout.addWidget(self.input_bowler_wickets, 2, 3)
        player_layout.addWidget(QLabel("R:"), 2, 4)
        player_layout.addWidget(self.input_bowler_runs, 2, 5)
        player_layout.addWidget(QLabel("O:"), 2, 6)
        player_layout.addWidget(self.input_bowler_overs, 2, 7)
        player_layout.addWidget(self.update_button, 3, 0, 1, 8)

        controls.addLayout(cam_layout)
        controls.addLayout(score_layout)
        controls.addLayout(player_layout)
        layout.addLayout(controls)

        self.setLayout(layout)

    def connect_camera(self):
        url = self.cam_input.text().strip()
        self.cap = cv2.VideoCapture(url)
        if not self.cap.isOpened():
            self.label.setText("❌ Could not open camera.")
            return
        self.timer.start(30)

    def set_theme(self):
        self.theme = self.theme_box.currentText()

    def update_stats(self):
        self.team_name = self.input_team.text()
        self.runs = int(self.input_runs.text())
        self.wickets = int(self.input_wickets.text())
        self.overs = self.input_overs.text()
        self.striker = self.input_striker.text()
        self.striker_runs = int(self.input_striker_runs.text())
        self.striker_balls = int(self.input_striker_balls.text())
        self.non_striker = self.input_non_striker.text()
        self.non_striker_runs = int(self.input_non_striker_runs.text())
        self.non_striker_balls = int(self.input_non_striker_balls.text())
        self.bowler = self.input_bowler.text()
        self.bowler_wickets = int(self.input_bowler_wickets.text())
        self.bowler_runs = int(self.input_bowler_runs.text())
        self.bowler_overs = self.input_bowler_overs.text()

    def draw_overlay(self, frame):
        h, w, _ = frame.shape
        font_scale = w / 1600.0
        thickness = int(font_scale * 2)

        themes = {
            "Dark": ((0, 0, 0), (255, 255, 255)),
            "IPL": ((0, 102, 204), (255, 255, 0)),
            "Classic": ((255, 255, 255), (0, 0, 0)),
            "Blood": ((30, 0, 0), (255, 0, 0))
        }

        bg, fg = themes.get(self.theme, ((0, 0, 0), (255, 255, 255)))

        # Scorecard bottom bar
        overlay_height = 90
        y_pos = h - overlay_height - 10
        cv2.rectangle(frame, (10, y_pos), (w - 10, y_pos + overlay_height), bg, -1)

        main_text = f"{self.team_name} {self.runs}/{self.wickets} ({self.overs})"
        player_text = f"{self.striker} {self.striker_runs}({self.striker_balls}) | {self.non_striker} {self.non_striker_runs}({self.non_striker_balls}) | {self.bowler} {self.bowler_wickets}/{self.bowler_runs} ({self.bowler_overs})"

        # Use better fonts
        cv2.putText(frame, main_text, (20, y_pos + 30), cv2.FONT_HERSHEY_DUPLEX, font_scale * 1.2, fg, thickness + 1, cv2.LINE_AA)
        cv2.putText(frame, player_text, (20, y_pos + 65), cv2.FONT_HERSHEY_TRIPLEX, font_scale * 1.0, fg, 1, cv2.LINE_AA)

    def update_frame(self):
        if self.cap and self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret or frame is None:
                return
            if len(frame.shape) == 3 and frame.shape[2] == 3:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            self.draw_overlay(frame)
            image = QImage(frame.data, frame.shape[1], frame.shape[0], frame.strides[0], QImage.Format_RGB888)
            pix = QPixmap.fromImage(image)
            self.label.setPixmap(pix.scaled(self.label.width(), self.label.height(), Qt.KeepAspectRatio))

    def closeEvent(self, event):
        self.timer.stop()
        if self.cap:
            self.cap.release()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = CricketOverlay()
    win.showMaximized()
    sys.exit(app.exec_())
