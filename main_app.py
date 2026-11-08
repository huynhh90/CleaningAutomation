from PyQt5.QtCore import QTimer, QSize, Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QSplitter, QLCDNumber, QFrame
from PyQt5.QtGui import QFont, QIcon
import sys
from datetime import datetime

from app_css import style_sheet

# Global variables
START_TIME = 60000

class CleaningAutomation(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.initializeUI()


    def initializeUI(self) -> None:
        self.setWindowTitle("CapsoClean Automation")
        self.setFixedSize(QSize(700, 600))


        # Method to setup buttons and widgets
        self.setupWidgets()

        # Variables
        self.clean_cycle_enable = True
        self.current_cycle_time = START_TIME

        # Create timer object
        self.timer: QTimer = QTimer()
        self.timer.timeout.connect(self.updateTimer)
        self.timer.start(1000)


    def setupWidgets(self) -> None:

        splitter: QSplitter = QSplitter()
        splitter.setOrientation(Qt.Horizontal)
        #splitter.resize

        information_box: QVBoxLayout = QVBoxLayout()
        information_box.setObjectName('information_box')

        temperature_box: QHBoxLayout = QHBoxLayout()
        temp_label: QLabel = QLabel()
        temp_label.setText('Temperature (°C): ')
        temp_label.setObjectName('temp_label')
        temp_label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        self.temp_display: QLabel = QLabel()
        self.temp_display.setText('------')
        self.temp_display.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        self.temp_display.setObjectName('temp_display')
        temperature_box.addWidget(temp_label)
        temperature_box.addWidget(self.temp_display)

        humidity_box: QHBoxLayout = QHBoxLayout()
        humid_label: QLabel = QLabel()
        humid_label.setText("Humidity (%): ")
        humid_label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        humid_label.setObjectName('humid_label')
        self.humid_display: QLabel = QLabel()
        self.humid_display.setText('------')
        self.humid_display.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        self.humid_display.setObjectName('humid_display')
        humidity_box.addWidget(humid_label)
        humidity_box.addWidget(self.humid_display)

        hydrogen_peroxide_box: QHBoxLayout = QHBoxLayout()
        hydro_perox_label: QLabel = QLabel()
        hydro_perox_label.setText('H2O2 (PPM):')
        hydro_perox_label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        hydro_perox_label.setObjectName('hydro_perox_label')
        hydro_perox_display: QLabel = QLabel()
        hydro_perox_display.setText('------')
        hydro_perox_display.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        hydro_perox_display.setObjectName('hydro_perox_display')
        hydrogen_peroxide_box.addWidget(hydro_perox_label)
        hydrogen_peroxide_box.addWidget(hydro_perox_display)

        pressure_box: QHBoxLayout = QHBoxLayout()
        pressure_label: QLabel = QLabel()
        pressure_label.setText('Pressure (psi):')
        pressure_label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        pressure_label.setObjectName('pressure_label')
        pressure_display: QLabel = QLabel()
        pressure_display.setText('------')
        pressure_display.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)
        pressure_display.setObjectName('pressure_display')
        pressure_box.addWidget(pressure_label)
        pressure_box.addWidget(pressure_display)

        # Add all information layout
        information_box.addLayout(temperature_box)
        information_box.addLayout(humidity_box)
        information_box.addLayout(hydrogen_peroxide_box)
        information_box.addLayout(pressure_box)

        information_container: QWidget = QWidget()
        information_container.setObjectName('information_box')
        information_container.setFixedSize(QSize(int(self.width()/2), int(self.height()/4)))
        information_container.setLayout(information_box)

        label2 = QLabel()
        label2.setText('jfkajoi2043')
        label2.setObjectName('L2')

        button_frame: QFrame = QFrame()

        start_button: QPushButton = QPushButton()
        start_button.setText('Start Clean Cycle')
        start_button.setFixedHeight(80)
        start_button.clicked.connect(self.toggleCleaningEnable)

        cancel_button: QPushButton = QPushButton()
        cancel_button.setText('Cancel')

        cycle_button_box: QHBoxLayout = QHBoxLayout()
        cycle_button_box.addWidget(start_button)
        cycle_button_box.addWidget(cancel_button)

        button_frame.setLayout(cycle_button_box)


        connect_button: QPushButton = QPushButton()
        connect_button.setText('Connect to ESP32')


        splitter.addWidget(button_frame)
        splitter.addWidget(information_container)





        # Create QCLD Widget
        self.timer_lcd: QLCDNumber = QLCDNumber()
        self.timer_lcd.setObjectName("timer_lcd")
        self.timer_lcd.setSegmentStyle(QLCDNumber.Filled)
        self.timer_lcd.display(self.calculateDisplayTime(START_TIME))

        label3 = QLabel()
        label3.setText('VBOX')
        label3.setObjectName('L3')


        # Add Widgets to layout
        h_box = QVBoxLayout()

        h_box.addWidget(splitter)
        h_box.addWidget(self.timer_lcd)

        main_container = QWidget()
        main_container.setLayout(h_box)

        self.setCentralWidget(main_container)
        #self.show()

    def startCleanCycle(self) -> None:
        pass



    def toggleCleaningEnable(self) -> None:
        self.clean_cycle_enable = not self.clean_cycle_enable

    def updateTimer(self):
        current_time = datetime.now().time()
        #self.temp_display.clear()
        self.temp_display.setText(f'{current_time:%H:%M:%S}')

        if self.clean_cycle_enable:
            print(f'{self.clean_cycle_enable=}')
            if self.current_cycle_time != 0:
                self.current_cycle_time -= 1000
                self.timer_lcd.display(self.calculateDisplayTime(self.current_cycle_time))
            else:
                print('Clean cycle disabled.')
                self.clean_cycle_enable = False


    def calculateDisplayTime(self, time:int) -> str:
        """ Calculate time that should be displayed in the QLCDNumber Widget."""
        minutes, seconds = self.convertMilliseconds(time)
        amount_of_time = f'{minutes:02d}:{seconds:02d}'
        return amount_of_time

    @staticmethod
    def convertMilliseconds(time_in_ms: int) -> tuple[int, int]:
        minute = time_in_ms/(1000 * 60)
        second = (time_in_ms/1000) % 60
        return int(minute), int(second)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(style_sheet)
    main_window = CleaningAutomation()
    main_window.show()
    sys.exit(app.exec_())