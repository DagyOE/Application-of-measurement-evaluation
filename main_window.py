import time
from PyQt6.QtWidgets import *
# from PyQt6.QtGui import *
from PyQt6.QtCore import *
import os

from controllers.load import Load
from controllers.datasets import Dataset
from controllers.tags import Tags
from controllers.render import Render
from controllers.protocols import Protocols
from controllers.edit import Edit

import sqlite3

con = sqlite3.connect(os.getcwd() + '/database.db')
cur = con.cursor()

class Main(QWidget):

    def __init__(self):
        super(Main, self).__init__()
        self.setWindowTitle("Skoda App")
        self.setGeometry(600, 150, 1024, 768)
        self.UI()
        self.show()
        self.load = Load()
        self.dataset = Dataset()
        self.tagcontroller = Tags()
        self.render = Render()
        self.protocols_show = Protocols()
        self.protocol_edit = Edit()

    def UI(self):
        self.design()
        self.layout()

    def design(self):
        # --> Title
        self.skoda = QLabel()
        self.skoda.setStyleSheet("image: url(img/skoda-logo.png);"
                                 "width: 50px;"
                                 "height: 50px;")

        self.foerster = QLabel()
        self.foerster.setStyleSheet("image: url(img/foerster-logo.png);"
                                    "width: 50px;"
                                    "height: 50px;")

        self.create = QPushButton("Create Project")
        self.create.setStyleSheet("QPushButton{background-color: #00800D;"
                                  "color: #F3FCF0;"
                                  "padding: 10px 10px 10px 10px;"
                                  "border-radius: 5px;"
                                  "font-size: 14px;}"
                                  "QPushButton:hover{background-color: #56BA4A;"
                                  "color: #3F4A3C;}")
        self.create.pressed.connect(self.CreateProtocol)

        # --> Navbar
        self.render = QPushButton("Create Protocol")
        self.render.setStyleSheet("QPushButton{background-color: transparent;"
                                  "color: #AA3600;"
                                  "padding: 10px 10px 10px 10px;"
                                  "border-radius: 0px;"
                                  "font-size: 14px;"
                                  "font-weight: bold;}"
                                  "QPushButton:hover{color: #DD4600;"
                                  "border-bottom: 2px solid #DD4600;}")
        self.render.pressed.connect(self.Render)

        self.mProtocols = QPushButton("Manage Protocols")
        self.mProtocols.setStyleSheet("QPushButton{background-color: transparent;"
                                      "color: #3F4A3C;"
                                      "padding: 10px 10px 10px 10px;"
                                      "border-radius: 0px;"
                                      "font-size: 14px;"
                                      "font-weight: bold;}"
                                      "QPushButton:hover{color: #00800D;"
                                      "border-bottom: 2px solid #00800D;}")
        self.mProtocols.pressed.connect(self.Protocols)

        self.aDataset = QPushButton("Add Dataset")
        self.aDataset.setStyleSheet("QPushButton{background-color: transparent;"
                                    "color: #3F4A3C;"
                                    "padding: 10px 10px 10px 10px;"
                                    "border-radius: 0px;"
                                    "font-size: 14px;"
                                    "font-weight: bold;}"
                                    "QPushButton:hover{color: #00800D;"
                                    "border-bottom: 2px solid #00800D;}")
        self.aDataset.pressed.connect(self.AddDataset)

        self.mDataset = QPushButton("Manage Dataset")
        self.mDataset.setStyleSheet("QPushButton{background-color: transparent;"
                                    "color: #3F4A3C;"
                                    "padding: 10px 10px 10px 10px;"
                                    "border-radius: 0px;"
                                    "font-size: 14px;"
                                    "font-weight: bold;}"
                                    "QPushButton:hover{color: #00800D;"
                                    "border-bottom: 2px solid #00800D;}")
        self.mDataset.pressed.connect(self.Datasets)

        self.tag = QPushButton("Manage Tags")
        self.tag.setStyleSheet("QPushButton{background-color: transparent;"
                               "color: #3F4A3C;"
                               "padding: 10px 10px 10px 10px;"
                               "border-radius: 0px;"
                               "font-size: 14px;"
                               "font-weight: bold;}"
                               "QPushButton:hover{color: #00800D;"
                               "border-bottom: 2px solid #00800D;}")
        self.tag.pressed.connect(self.Tag)

        # --> Body
        self.welcome = QLabel()
        self.welcome.setText("Welcome to the Foerster measurement results evaluation app")
        self.welcome.setStyleSheet("color: #00800D;"
                                   "font-size: 20px;")
        self.welcome.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # --> Creating protocol
        self.new = QLabel()
        self.new.setText("Creating new protocol")

        self.newResultsListTitle = QLabel()
        self.newResultsListTitle.setText("All Measurements")
        self.newResultsListTitle.setStyleSheet("background-color: rgba(255, 255, 255, 0);"
                                               "padding: 10px 0px 10px 10px;"
                                               "color: #123300;"
                                               "font-size: 16px;"
                                               "font-weight: bold;")

        self.newResultsList = QListWidget()
        self.newResultsList.setStyleSheet("QListWidget{background-color: rgba(255, 255, 255, 255);"
                                          "border-radius: 15px;"
                                          "padding: 15px 15px 15px 15px;}"
                                          "QListWidget::item{padding: 10px 0px 10px 0px;}"
                                          "QListWidget::item:hover{background-color: rgba(192, 229, 89, 255);"
                                          "border-radius: 10px;}"
                                          "QListWidget::item:selected{background-color: rgba(25, 201, 3, 255);"
                                          "border-radius: 10px;}")
        self.newResultsList.itemClicked.connect(self.SingleItem)

        self.newResultsSingleTitle = QLabel()
        self.newResultsSingleTitle.setText("Selected Measurement")
        self.newResultsSingleTitle.setStyleSheet("background-color: rgba(255, 255, 255, 0);"
                                                 "padding: 10px 0px 10px 10px;"
                                                 "color: #123300;"
                                                 "font-size: 16px;"
                                                 "font-weight: bold;")

        self.newResultsSingle = QLabel()
        self.newResultsSingle.setStyleSheet("background-color: rgba(255, 255, 255, 255);"
                                            "border-radius: 15px;"
                                            "padding: 15px;"
                                            "margin: 0px;"
                                            "font-size: 12px;")
        self.newResultsSingle.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.newResultsInfoTitle = QLabel()
        self.newResultsInfoTitle.setText("Selected Measurement")
        self.newResultsInfoTitle.setStyleSheet("background-color: rgba(255, 255, 255, 0);"
                                               "padding: 10px 0px 10px 10px;"
                                               "color: #123300;"
                                               "font-size: 16px;"
                                               "font-weight: bold;")

        self.newResultsInfo = QLabel()
        self.newResultsInfo.setStyleSheet("background-color: rgba(255, 255, 255, 255);"
                                          "border-radius: 15px;"
                                          "padding: 15px;"
                                          "margin: 0px;"
                                          "font-size: 14px;")
        self.newResultsInfo.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.userListTitle = QLabel()
        self.userListTitle.setText("Informations")
        self.userListTitle.setStyleSheet("background-color: rgba(255, 255, 255, 0);"
                                         "padding: 10px 0px 10px 10px;"
                                         "color: #123300;"
                                         "font-size: 16px;"
                                         "font-weight: bold;")

        self.userListTitle2 = QLabel()
        self.userListTitle2.setText("")
        self.userListTitle2.setStyleSheet("background-color: rgba(255, 255, 255, 0);"
                                          "padding: 10px 0px 10px 10px;"
                                          "color: #123300;"
                                          "font-size: 16px;"
                                          "font-weight: bold;")

        self.userList = QListWidget()
        self.userList.setStyleSheet("background-color: rgba(255, 255, 255, 255);"
                                    "border-radius: 15px;")

        self.nameTextBox = QLineEdit(self)
        self.nameTextBox.setPlaceholderText("First Name")
        self.nameTextBox.setStyleSheet("QLineEdit{padding: 10px;"
                                       "border-radius: 15px;"
                                       "color: #000000;}"
                                       "QLineEdit:focus{background-color: rgba(192, 229, 89, 255);}")
        # self.nameTextBox.setAttribute(Qt.WA_MacShowFocusRect, 0)

        self.surnameTextBox = QLineEdit(self)
        self.surnameTextBox.setPlaceholderText("Last Name")
        self.surnameTextBox.setStyleSheet("QLineEdit{padding: 10px;"
                                          "border-radius: 15px;"
                                          "color: #000000;}"
                                          "QLineEdit:focus{background-color: rgba(192, 229, 89, 255);}")
        # self.surnameTextBox.setAttribute(Qt.WA_MacShowFocusRect, 0)

        self.idTextBox = QLineEdit(self)
        self.idTextBox.setPlaceholderText("Employee Number")
        self.idTextBox.setStyleSheet("QLineEdit{padding: 10px;"
                                     "border-radius: 15px;"
                                     "color: #000000;}"
                                     "QLineEdit:focus{background-color: rgba(192, 229, 89, 255);}")
        # self.idTextBox.setAttribute(Qt.WA_MacShowFocusRect, 0)

        self.numberTextBox = QLineEdit(self)
        self.numberTextBox.setPlaceholderText("Part Number")
        self.numberTextBox.setStyleSheet("QLineEdit{padding: 10px;"
                                         "border-radius: 15px;"
                                         "color: #000000;}"
                                         "QLineEdit:focus{background-color: rgba(192, 229, 89, 255);}")
        # self.numberTextBox.setAttribute(Qt.WA_MacShowFocusRect, 0)

        self.furnanceTextBox = QLineEdit(self)
        self.furnanceTextBox.setPlaceholderText("Furnace")
        self.furnanceTextBox.setStyleSheet("QLineEdit{padding: 10px;"
                                           "border-radius: 15px;"
                                           "color: #000000;}"
                                           "QLineEdit:focus{background-color: rgba(192, 229, 89, 255);}")
        # self.furnanceTextBox.setAttribute(Qt.WA_MacShowFocusRect, 0)

        self.materialTextBox = QLineEdit(self)
        self.materialTextBox.setPlaceholderText("Material")
        self.materialTextBox.setStyleSheet("QLineEdit{padding: 10px;"
                                           "border-radius: 15px;"
                                           "color: #000000;}"
                                           "QLineEdit:focus{background-color: rgba(192, 229, 89, 255);}")
        # self.materialTextBox.setAttribute(Qt.WA_MacShowFocusRect, 0)

        self.batchTextBox = QLineEdit(self)
        self.batchTextBox.setPlaceholderText("Batch Number")
        self.batchTextBox.setStyleSheet("QLineEdit{padding: 10px;"
                                        "border-radius: 15px;"
                                        "color: #000000;}"
                                        "QLineEdit:focus{background-color: rgba(192, 229, 89, 255);}")
        # self.batchTextBox.setAttribute(Qt.WA_MacShowFocusRect, 0)

        self.gridTextBox = QLineEdit(self)
        self.gridTextBox.setPlaceholderText("Grid Number")
        self.gridTextBox.setStyleSheet("QLineEdit{padding: 10px;"
                                       "border-radius: 15px;"
                                       "color: #000000;}"
                                       "QLineEdit:focus{background-color: rgba(192, 229, 89, 255);}")
        # self.gridTextBox.setAttribute(Qt.WA_MacShowFocusRect, 0)

        self.meltTextBox = QLineEdit(self)
        self.meltTextBox.setPlaceholderText("Melt Number")
        self.meltTextBox.setStyleSheet("QLineEdit{padding: 10px;"
                                       "border-radius: 15px;"
                                       "color: #000000;}"
                                       "QLineEdit:focus{background-color: rgba(192, 229, 89, 255);}")
        # self.meltTextBox.setAttribute(Qt.WA_MacShowFocusRect, 0)

        self.noteTextBox = QLineEdit(self)
        self.noteTextBox.setPlaceholderText("Note")
        self.noteTextBox.setStyleSheet("QLineEdit{padding: 10px;"
                                       "border-radius: 15px;"
                                       "color: #000000;}"
                                       "QLineEdit:focus{background-color: rgba(192, 229, 89, 255);}")
        # self.noteTextBox.setAttribute(Qt.WA_MacShowFocusRect, 0)

        # --> Render making
        self.makerender = QLabel()

        # --> Editing/Open/Delete Protocols from DB
        self.protocols = QLabel()
        self.protocols.setText("Protocols stored in the database")
        self.protocols.setStyleSheet("background-color: rgba(255, 255, 255, 0);"
                                     "padding: 10px 0px 10px 10px;"
                                     "color: #123300;"
                                     "font-size: 16px;"
                                     "font-weight: bold;")

        self.protocolsGrid = QListWidget()
        self.protocolsGrid.setStyleSheet("QListWidget{background-color: rgba(255, 255, 255, 255);"
                                         "border-radius: 15px;"
                                         "padding: 15px 15px 15px 15px;}"
                                         "QListWidget::item{padding: 10px 0px 10px 0px;}"
                                         "QListWidget::item:hover{background-color: rgba(192, 229, 89, 255);"
                                         "border-radius: 10px;}"
                                         "QListWidget::item:selected{background-color: rgba(25, 201, 3, 255);")

        self.protocolEdit = QPushButton("Edit")
        self.protocolEdit.setStyleSheet("QPushButton{background-color: #0074F9;"
                                        "color: #F3FCF0;"
                                        "padding: 10px 25px 10px 25px;"
                                        "border-radius: 5px;"
                                        "font-size: 14px;}"
                                        "QPushButton:hover{background-color: #00BBFC;"
                                        "color: #3F4A3C;}")
        self.protocolEdit.pressed.connect(self.EditProtocol)

        self.protocolOpen = QPushButton("Open")
        self.protocolOpen.setStyleSheet("QPushButton{background-color: #00800D;"
                                        "color: #F3FCF0;"
                                        "padding: 10px 25px 10px 25px;"
                                        "border-radius: 5px;"
                                        "font-size: 14px;}"
                                        "QPushButton:hover{background-color: #56BA4A;"
                                        "color: #3F4A3C;}")
        self.protocolOpen.pressed.connect(self.OpenProtocol)

        self.protocolDelete = QPushButton("Delete")
        self.protocolDelete.setStyleSheet("QPushButton{background-color: #C63F00;"
                                          "color: #F3FCF0;"
                                          "padding: 10px 25px 10px 25px;"
                                          "border-radius: 5px;"
                                          "font-size: 14px;}"
                                          "QPushButton:hover{background-color: #F34D00;"
                                          "color: #F3FCF0;}")
        self.protocolDelete.pressed.connect(self.DeleteProtocol)

        # --> Protocol Editing
        self.editProtocolGridTitle = QLabel()
        self.editProtocolGridTitle.setText("Data from selected protocol")
        self.editProtocolGridTitle.setStyleSheet("background-color: rgba(255, 255, 255, 0);"
                                                 "padding: 10px 0px 10px 10px;"
                                                 "color: #123300;"
                                                 "font-size: 16px;"
                                                 "font-weight: bold;")
        self.editProtocolGrid = QListWidget()
        self.editProtocolGrid.setStyleSheet("QListWidget{background-color: rgba(255, 255, 255, 255);"
                                            "border-radius: 15px;"
                                            "padding: 15px 15px 15px 15px;}"
                                            "QListWidget::item{padding: 10px 0px 10px 0px;}"
                                            "QListWidget::item:hover{background-color: rgba(192, 229, 89, 255);"
                                            "border-radius: 10px;}"
                                            "QListWidget::item:selected{background-color: rgba(25, 201, 3, 255);")

        self.editProtocolCreate = QPushButton("Create new protocol")
        self.editProtocolCreate.setStyleSheet("QPushButton{background-color: #00800D;"
                                              "color: #F3FCF0;"
                                              "padding: 10px 25px 10px 25px;"
                                              "border-radius: 5px;"
                                              "font-size: 14px;}"
                                              "QPushButton:hover{background-color: #56BA4A;"
                                              "color: #3F4A3C;}")
        self.editProtocolCreate.pressed.connect(self.EditProtocolCreate)

        self.editProtocolEnd = QPushButton("End changes")
        self.editProtocolEnd.setStyleSheet("QPushButton{background-color: #C63F00;"
                                              "color: #F3FCF0;"
                                              "padding: 10px 25px 10px 25px;"
                                              "border-radius: 5px;"
                                              "font-size: 14px;}"
                                              "QPushButton:hover{background-color: #F34D00;"
                                              "color: #F3FCF0;}")
        self.editProtocolEnd.pressed.connect(self.EditProtocolEnd)

        # --> Add New Dataset to DB
        self.adddatasets = QLabel()

        # --> Delete Datasets from DB
        self.datasets = QLabel()
        self.datasets.setText("Datasets stored in the database")
        self.datasets.setStyleSheet("background-color: rgba(255, 255, 255, 0);"
                                    "padding: 10px 0px 10px 10px;"
                                    "color: #123300;"
                                    "font-size: 16px;"
                                    "font-weight: bold;")

        self.datasetsGrid = QListWidget()
        self.datasetsGrid.setStyleSheet("QListWidget{background-color: rgba(255, 255, 255, 255);"
                                        "border-radius: 15px;"
                                        "padding: 15px 15px 15px 15px;}"
                                        "QListWidget::item{padding: 10px 0px 10px 0px;}"
                                        "QListWidget::item:hover{background-color: rgba(192, 229, 89, 255);"
                                        "border-radius: 10px;}"
                                        "QListWidget::item:selected{background-color: rgba(25, 201, 3, 255);"
                                        "border-radius: 10px;}")

        self.datasetAdd = QPushButton("Add")
        self.datasetAdd.setStyleSheet("QPushButton{background-color: #00800D;"
                                      "color: #F3FCF0;"
                                      "padding: 10px 25px 10px 25px;"
                                      "border-radius: 5px;"
                                      "font-size: 14px;}"
                                      "QPushButton:hover{background-color: #56BA4A;"
                                      "color: #3F4A3C;}")
        self.datasetAdd.clicked.connect(self.AddDataset)

        self.datasetDelete = QPushButton("Delete")
        self.datasetDelete.setStyleSheet("QPushButton{background-color: #C63F00;"
                                         "color: #F3FCF0;"
                                         "padding: 10px 25px 10px 25px;"
                                         "border-radius: 5px;"
                                         "font-size: 14px;}"
                                         "QPushButton:hover{background-color: #F34D00;"
                                         "color: #F3FCF0;}")
        self.datasetDelete.clicked.connect(self.DeleteDataset)

        # --> Add/Delete Tag from DB
        self.tags = QLabel()
        self.tags = QLabel()
        self.tags.setText("Tags stored in the database")
        self.tags.setStyleSheet("background-color: rgba(255, 255, 255, 0);"
                                "padding: 10px 0px 10px 10px;"
                                "color: #123300;"
                                "font-size: 16px;"
                                "font-weight: bold;")

        self.tagsGrid = QListWidget()
        self.tagsGrid.setStyleSheet("QListWidget{background-color: rgba(255, 255, 255, 255);"
                                    "border-radius: 15px;"
                                    "padding: 15px 15px 15px 15px;}"
                                    "QListWidget::item{padding: 10px 0px 10px 0px;}"
                                    "QListWidget::item:hover{background-color: rgba(192, 229, 89, 255);"
                                    "border-radius: 10px;}"
                                    "QListWidget::item:selected{background-color: rgba(25, 201, 3, 255);")

        self.tagsAdd = QPushButton("Add")
        self.tagsAdd.setStyleSheet("QPushButton{background-color: #00800D;"
                                    "color: #F3FCF0;"
                                    "padding: 10px 25px 10px 25px;"
                                    "border-radius: 5px;"
                                    "font-size: 14px;}"
                                    "QPushButton:hover{background-color: #56BA4A;"
                                    "color: #3F4A3C;}")
        self.tagsAdd.clicked.connect(self.TagAdd)

        self.tagsDelete = QPushButton("Delete")
        self.tagsDelete.setStyleSheet("QPushButton{background-color: #C63F00;"
                                      "color: #F3FCF0;"
                                      "padding: 10px 25px 10px 25px;"
                                      "border-radius: 5px;"
                                      "font-size: 14px;}"
                                      "QPushButton:hover{background-color: #F34D00;"
                                      "color: #F3FCF0;}")
        self.tagsDelete.clicked.connect(self.TagDelete)

    def layout(self):
        self.main = QVBoxLayout()
        self.title = QHBoxLayout()
        self.navbar = QHBoxLayout()
        self.body = QVBoxLayout()
        # NEW PROTOCOL
        self.newProtocol = QWidget()
        self.newProtocolBody = QVBoxLayout()
        self.newProtocolLayout = QHBoxLayout()
        self.newProtocolLayoutTable = QVBoxLayout()
        self.newProtocolLayoutSingle = QVBoxLayout()
        self.newProtocolLayoutInfo = QVBoxLayout()
        self.user = QHBoxLayout()
        self.userL = QVBoxLayout()
        self.userR = QVBoxLayout()
        # PROTOCOLS
        self.dbProtocols = QWidget()
        self.dbProtocolsBody = QVBoxLayout()
        self.dbProtocolsLayoutTop = QVBoxLayout()
        self.dbProtocolsLayoutBottom = QHBoxLayout()
        # DATASETS
        self.dbDatasets = QWidget()
        self.dbDatasetsBody = QVBoxLayout()
        self.dbDatasetsLayoutTop = QVBoxLayout()
        self.dbDatasetsLayoutBottom = QHBoxLayout()
        # TAGS
        self.dbTags = QWidget()
        self.dbTagsBody = QVBoxLayout()
        self.dbTagsLayoutTop = QVBoxLayout()
        self.dbTagsLayoutBottom = QHBoxLayout()
        # EDIT PROTOCOL
        self.dbEdit = QWidget()
        self.dbEditBody = QVBoxLayout()
        self.dbEditLayoutTop = QVBoxLayout()
        self.dbEditLayoutBottom = QHBoxLayout()

        self.main.addLayout(self.title, 10)
        self.main.addLayout(self.navbar, 10)
        self.main.addLayout(self.body, 80)

        self.title.addWidget(self.skoda, 1)
        self.title.addWidget(self.foerster, 1)
        self.title.addStretch(15)
        self.title.addWidget(self.create, 2)

        self.navbar.addStretch()
        self.navbar.addWidget(self.render)
        self.navbar.addWidget(self.mProtocols)
        # self.navbar.addWidget(self.aDataset)
        self.navbar.addWidget(self.mDataset)
        self.navbar.addWidget(self.tag)
        self.navbar.addStretch()

        # NEW PROJECT
        self.newProtocolLayoutTable.addWidget(self.newResultsListTitle, 10)
        self.newProtocolLayoutTable.addWidget(self.newResultsList, 90)
        self.newProtocolLayoutSingle.addWidget(self.newResultsSingleTitle, 10)
        self.newProtocolLayoutSingle.addWidget(self.newResultsSingle, 90)
        self.newProtocolLayoutInfo.addWidget(self.newResultsInfoTitle, 10)
        self.newProtocolLayoutInfo.addWidget(self.newResultsInfo, 90)

        self.userL.addWidget(self.userListTitle, 10)
        self.userL.addWidget(self.nameTextBox, 18)
        self.userL.addWidget(self.surnameTextBox, 18)
        self.userL.addWidget(self.idTextBox, 18)
        self.userL.addWidget(self.numberTextBox, 18)
        self.userL.addWidget(self.furnanceTextBox, 18)

        self.userR.addWidget(self.userListTitle2, 10)
        self.userR.addWidget(self.materialTextBox, 18)
        self.userR.addWidget(self.batchTextBox, 18)
        self.userR.addWidget(self.gridTextBox, 18)
        self.userR.addWidget(self.meltTextBox, 18)
        self.userR.addWidget(self.noteTextBox, 18)

        self.user.addLayout(self.userL, 50)
        self.user.addLayout(self.userR, 50)

        self.newProtocolLayout.addLayout(self.newProtocolLayoutTable, 45)
        self.newProtocolLayout.addLayout(self.newProtocolLayoutSingle, 25)
        self.newProtocolLayout.addLayout(self.newProtocolLayoutInfo, 30)

        self.newProtocolBody.addLayout(self.newProtocolLayout, 60)
        self.newProtocolBody.addLayout(self.user, 40)

        self.newProtocol.setLayout(self.newProtocolBody)

        # PROTOCOLS
        self.dbProtocolsBody.addLayout(self.dbProtocolsLayoutTop, 90)
        self.dbProtocolsBody.addLayout(self.dbProtocolsLayoutBottom, 10)

        self.dbProtocolsLayoutTop.addWidget(self.protocols)
        self.dbProtocolsLayoutTop.addWidget(self.protocolsGrid)

        self.dbProtocolsLayoutBottom.addStretch()
        self.dbProtocolsLayoutBottom.addWidget(self.protocolEdit)
        self.dbProtocolsLayoutBottom.addWidget(self.protocolOpen)
        self.dbProtocolsLayoutBottom.addWidget(self.protocolDelete)
        self.dbProtocolsLayoutBottom.addStretch()

        self.dbProtocols.setLayout(self.dbProtocolsBody)

        # DATASETS
        self.dbDatasetsBody.addLayout(self.dbDatasetsLayoutTop, 90)
        self.dbDatasetsBody.addLayout(self.dbDatasetsLayoutBottom, 10)

        self.dbDatasetsLayoutTop.addWidget(self.datasets)
        self.dbDatasetsLayoutTop.addWidget(self.datasetsGrid)

        self.dbDatasetsLayoutBottom.addStretch()
        self.dbDatasetsLayoutBottom.addWidget(self.datasetAdd)
        self.dbDatasetsLayoutBottom.addWidget(self.datasetDelete)
        self.dbDatasetsLayoutBottom.addStretch()

        self.dbDatasets.setLayout(self.dbDatasetsBody)

        # TAGS
        self.dbTagsBody.addLayout(self.dbTagsLayoutTop, 90)
        self.dbTagsBody.addLayout(self.dbTagsLayoutBottom, 10)

        self.dbTagsLayoutTop.addWidget(self.tags)
        self.dbTagsLayoutTop.addWidget(self.tagsGrid)

        self.dbTagsLayoutBottom.addStretch()
        self.dbTagsLayoutBottom.addWidget(self.tagsAdd)
        self.dbTagsLayoutBottom.addWidget(self.tagsDelete)
        self.dbTagsLayoutBottom.addStretch()

        self.dbTags.setLayout(self.dbTagsBody)

        # PROTOCOLS EDIT
        self.dbEditBody.addLayout(self.dbEditLayoutTop, 90)
        self.dbEditBody.addLayout(self.dbEditLayoutBottom, 10)

        self.dbEditLayoutTop.addWidget(self.editProtocolGridTitle)
        self.dbEditLayoutTop.addWidget(self.editProtocolGrid)

        self.dbEditLayoutBottom.addStretch()
        self.dbEditLayoutBottom.addWidget(self.editProtocolCreate)
        self.dbEditLayoutBottom.addWidget(self.editProtocolEnd)
        self.dbEditLayoutBottom.addStretch()

        self.dbEdit.setLayout(self.dbEditBody)

        # STACKED
        self.stacked = QStackedWidget()

        self.body.addWidget(self.stacked)

        self.stacked.addWidget(self.welcome)
        self.stacked.addWidget(self.newProtocol)
        self.stacked.addWidget(self.makerender)
        self.stacked.addWidget(self.dbProtocols)
        self.stacked.addWidget(self.adddatasets)
        self.stacked.addWidget(self.dbDatasets)
        self.stacked.addWidget(self.dbTags)
        self.stacked.addWidget(self.dbEdit)

        self.setLayout(self.main)

    # ------------------------------------------------------------------------------------------------------------------
    # --- PROTOCOL DATA LOGIC ---

    def CreateProtocol(self):
        num, ok = QInputDialog.getInt(self, "Measurements of one product", "Insert the number of measurements of "
                                                                                "one product! \n\nThe number of "
                                                                                "measurements must be greater than 0! "
                                                                                "\n\nInsert number: \n")
        if num != 0:
            if ok:
                url, df = QFileDialog.getOpenFileName(self, "Open a file ...", "", "All Files(*);;*txt;;*csv;;*xsl")
                if len(url) != 0:
                    data = self.load.loadData(url, num)
                    for dat in data:
                        out = str(dat["id"]) + "# Product" + " - Average X: " + str(dat["x"]) + \
                              " - Average Y: " + str(dat["y"])
                        self.newResultsList.addItem(out)
                    query = "SELECT name FROM datasets"
                    datasets = cur.execute(query).fetchall()
                    items = ()
                    for dataset in datasets:
                        items += dataset
                    item, ok = QInputDialog.getItem(self, "Dataset selection",
                                                    "List of Datasets: ", items, 0, False)
                    if ok and item:
                        query = "SELECT name, link FROM datasets"
                        datasets = cur.execute(query).fetchall()
                        for dataset in datasets:
                            if dataset[0] == item:
                                self.border_link = dataset[1]
                                dataset_name = "Dataset name: " + str(dataset[0])
                    self.borders = self.load.border_points(self.border_link)
                    check = self.load.check_valid()
                    data = self.load.result(num)
                    if data == False:
                        QMessageBox.warning(self, "Warning", "Tag not found in the database!\n\n"
                                                             "Add tag to database")
                        self.Tag()
                    else:
                        self.newResultsInfo.clear()
                        self.newResultsInfo.setText(str(data['name']) + "\n\n" + "Measuring date: " + str(data['date'])
                                                    + "\n\n" + "Measuring time: " + str(data['time']) + "\n\n" +
                                                    "One piece measurement: " + str(data['onePiece']) + "\n\n" +
                                                    "Number of all pieces: " + str(data['all']) + "\n\n" + dataset_name
                                                    + "\n\n" + "Number of good pieces: " + str(data['ok']) + "\n\n" +
                                                    "Number of bad pieces: " + str(data['no']))
                        self.load.create = True
                        self.stacked.setCurrentIndex(1)
                else:
                    QMessageBox.warning(self, "Warning", "No generated output from the instrument was selected!")
                    self.stacked.setCurrentIndex(0)
        else:
            QMessageBox.warning(self, "Warning", "The number of measurements must be greater than 0!")
            self.stacked.setCurrentIndex(0)

    # --- PROTOCOL DATA LOGIC ---
    # ------------------------------------------------------------------------------------------------------------------
    # --- SINGLE ITEM LOGIC ---

    def SingleItem(self):
        id = self.newResultsList.currentItem().text().split("#")[0]
        data = self.load.single(id)
        self.newResultsSingle.clear()
        self.newResultsSingle.setText("\n\n".join([str(x[0]) + "# - X: " + str(x[1]) + " | Y: " + str(x[2])
                                                    for x in data]))

    # --- SINGLE ITEM LOGIC ---
    # ------------------------------------------------------------------------------------------------------------------
    # --- RENDER ITEM LOGIC ---

    def Render(self):
        print("Creating protocol")
        if self.load.data is False:
            self.makerender.setText("A measurement protocol has not been established.\n\n "
                                    "Repeat the creation of the protocol again.")
            self.makerender.setStyleSheet("color: #C63F00;"
                                          "font-size: 20px;")
            self.makerender.setAlignment(Qt.AlignmentFlag.AlignCenter)
        else:
            userData = {
                "name": self.nameTextBox.text(),
                "surname": self.surnameTextBox.text(),
                "id": self.idTextBox.text(),
                "number": self.numberTextBox.text(),
                "furnance": self.furnanceTextBox.text(),
                "material": self.materialTextBox.text(),
                "batch": self.batchTextBox.text(),
                "grid": self.gridTextBox.text(),
                "melt": self.meltTextBox.text(),
                "note": self.noteTextBox.text(),
            }
            protocol = self.render.ProtocolRender(self.load.data, self.load.url, self.load.num, userData, self.borders,
                                                  self.border_link)
            time.sleep(1)
            if protocol[0]:
                self.makerender.setText(f"The measurement protocol was successfully created created under "
                                        f"the name:\n\n {protocol[1]}\n\n "
                                        f"It was saved in the folder:\n\n {protocol[2]}")
                self.makerender.setStyleSheet("color: #00800D;"
                                              "font-size: 20px;")
                self.makerender.setAlignment(Qt.AlignmentFlag.AlignCenter)
            else:
                self.makerender.setText("A measurement protocol has not been established.\n\n "
                                        "Repeat the creation of the protocol again.")
                self.makerender.setStyleSheet("color: #C63F00;"
                                              "font-size: 20px;")
                self.makerender.setAlignment(Qt.AlignmentFlag.AlignCenter)

            self.load.create = False

        self.stacked.setCurrentIndex(2)

    # --- RENDER ITEM LOGIC ---
    # ------------------------------------------------------------------------------------------------------------------
    # --- PROTOCOLS STORAGE LOGIC ---

    def Protocols(self):
        self.protocolsGrid.clear()
        protocols = self.protocols_show.loadProtocols()
        for protocol in protocols:
            data = str(protocol[1])
            self.protocolsGrid.addItem(data)
        self.stacked.setCurrentIndex(3)

    def EditProtocol(self):
        self.editProtocolGrid.clear()
        name = self.protocolsGrid.currentItem().text()
        protocol = self.protocol_edit.OpenProtocolData(name)
        i = 0
        dataList = list(zip(protocol[0], protocol[1]))
        for row in dataList:
            i += 1
            item = QListWidgetItem("Measure #" + str(i) + " -> x: " + str(row[0]) + " - y: " + str(row[1]))
            item.setFlags(Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEnabled)
            item.setCheckState(Qt.CheckState.Unchecked)
            self.editProtocolGrid.addItem(item)
            self.editProtocolData = protocol[2]
        self.stacked.setCurrentIndex(7)

    def OpenProtocol(self):
        name = self.protocolsGrid.currentItem().text().split("#")[0]
        self.protocols_show.openProtocol(name)

    def DeleteProtocol(self):
        name = self.protocolsGrid.currentItem().text().split("#")[0]
        self.protocols_show.deleteProtocol(name)
        self.Protocols()

    def EditProtocolCreate(self):
        data = self.editProtocolGrid
        check = []
        for row in range(data.count()):
            item = self.editProtocolGrid.item(row)
            if item.checkState() == Qt.CheckState.Unchecked:
                check.append("1")
            else:
                check.append("0")
        self.protocol_edit.CreateNewData(check, self.editProtocolData)
        self.Protocols()

    def EditProtocolEnd(self):
        self.editProtocolGrid.clear()
        self.protocol_edit.ClearList()
        self.stacked.setCurrentIndex(3)

    # --- PROTOCOLS STORAGE LOGIC ---
    # ------------------------------------------------------------------------------------------------------------------
    # --- DATASETS LOGIC ---

    def Datasets(self):
        self.datasetsGrid.clear()
        datasets = self.dataset.loadDatasets()
        for dataset in datasets:
            data = str(dataset[1]) + " - " + str(dataset[2])
            self.datasetsGrid.addItem(data)
        self.stacked.setCurrentIndex(5)

    def AddDataset(self):
        name, ok = QInputDialog.getText(self, "Insert dataset name", "Insert dataset name: \n")
        if ok is True and len(name) != 0:
            url, df = QFileDialog.getOpenFileName(self, "Open a file ...", "", "All Files(*);;*txt;;*csv;;*xsl")
            if len(url) != 0:
                data = self.dataset.addDataset(url, name)
                if data == 0:
                    QMessageBox.warning(self, "Warning", "The name of the dataset is already in the database! \n\n"
                                                         "The dataset has not been added to the database.\n\n "
                                                         "Repeat the creation of the new dataset again.")
                elif data == 1:
                    QMessageBox.warning(self, "Warning", "The dataset has not been added to the database.\n\n "
                                                         "Repeat the creation of the new dataset again.")
                else:
                    QMessageBox.information(self, "Success", "The dataset has been successfully added "
                                                             "to the database. \n\n"
                                                             f"Dataset name: {name} \n"
                                                             f"Saved in folder: {data}\n")
                    self.Datasets()
            else:
                QMessageBox.warning(self, "Warning", "The correct file PATH is not selected! \n\n"
                                                     "The dataset has not been added to the database.\n\n "
                                                     "Repeat the creation of the new dataset again.")
        else:
            QMessageBox.warning(self, "Warning", "It is necessary to fill in the dataset name! \n\n"
                                                 "The dataset has not been added to the database.\n\n "
                                                 "Repeat the creation of the new dataset again.")

    def DeleteDataset(self):
        item = self.datasetsGrid.currentItem().text()
        self.dataset.deleteDataset(item)
        self.Datasets()

    # --- DATASETS LOGIC ---
    # ------------------------------------------------------------------------------------------------------------------
    # --- TAGS LOGIC ---

    def Tag(self):
        self.tagsGrid.clear()
        tags = self.tagcontroller.loadTags()
        for tag in tags:
            data = str(tag[2]) + " - " + str(tag[1])
            self.tagsGrid.addItem(data)
        self.stacked.setCurrentIndex(6)

    def TagAdd(self):
        tag_name, ok = QInputDialog.getText(self, "Insert tag name", "Insert tag name: \n")
        if ok is True and len(tag_name) != 0:
            tag_short, ok = QInputDialog.getText(self, "Insert tag shortcut", "Insert tag shortcut: \n")
            if ok is True and len(tag_short) != 0:
                if self.tagcontroller.addTag(tag_name, tag_short):
                    QMessageBox.information(self, "Success", "The tag has been successfully added to the database.")
                    self.Tag()
                else:
                    QMessageBox.warning(self, "Warning", "The tag has not been added to the database.")
            else:
                QMessageBox.warning(self, "Warning", "It is necessary to fill in the tag shortcut!")
        else:
            QMessageBox.warning(self, "Warning", "It is necessary to fill in the tag name!")
        self.stacked.setCurrentIndex(6)

    def TagDelete(self):
        item = self.tagsGrid.currentItem().text()
        self.tagcontroller.deleteTag(item)
        self.Tag()

    # --- TAGS LOGIC ---
    # ------------------------------------------------------------------------------------------------------------------
