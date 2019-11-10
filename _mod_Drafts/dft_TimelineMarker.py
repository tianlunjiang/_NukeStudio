from Qt import QtWidgets, QtGui, QtCore
import sys, time


class MarkerAdd(QtWidgets.QDialog):
    '''
    GUI for adding markers
    data to be stored:frame, tooltip, id(<SHOW>-<timestamp>, PHX-12345678)
    '''
    def __init__(ma, layout_obj):
        super(MarkerAdd, ma).__init__()

        # cur_frame = nuke.frame()
        cur_frame = 1001
        ma.thisLayout = layout_obj
        ma.m_frame = QtWidgets.QSpinBox()
        ma.m_frame.setMaximum(3000)
        ma.m_frame.setPrefix('x')
        ma.m_frame.setValue(cur_frame)
        ma.m_frame.selectAll()
        ma.m_label = QtWidgets.QLineEdit()
        ma.m_label.setPlaceholderText("Keep it short")
        ma.m_add = QtWidgets.QPushButton('Add Marker')
        ma.m_add.clicked.connect(ma.add)

        ma.layout = QtWidgets.QVBoxLayout()
        ma.layout.addWidget(ma.m_frame)
        ma.layout.addWidget(ma.m_label)
        ma.layout.addWidget(ma.m_add)
        ma.setLayout(ma.layout)


    def add(ma):
        '''add button'''
        thisFrame = int(ma.m_frame.text().replace('x', ''))
        thisId = int(time.time())
        thisLabel = ma.m_label.text()
        thisMarker = MarkerButton(thisId, thisFrame, thisLabel)
        # thisMarker.customContextMenuRequested.connect(Core_TimelineMarker.removeMarker)

        label_button = ma.m_label.text() if len(ma.m_label.text())<=10 else ma.m_label.text()[:10]+'...'
        thisMarker.setText(label_button)
        thisMarker.setToolTip( "<b>x%s:</b><br>%s<br>(id: %s)" % (thisMarker.frame, thisMarker.label, thisMarker.id) )
        ma.thisLayout.addWidget(thisMarker)

        ma.close()

        #self.onSave()


    def onSave(self):
        '''save buttons when clicked'''
        num_widget = layout_obj.count()
        self.saveMarkers()


class MarkerButton(QtWidgets.QPushButton):
    def __init__(self, id, frame, label):
        super(MarkerButton, self).__init__()

        self.id = id
        self.frame = frame
        self.label = label



class Core_TimelineMarker(QtWidgets.QWidget):
    def __init__(self):
        super(Core_TimelineMarker, self).__init__()

        self.bt_add = QtWidgets.QPushButton('+')
        self.bt_add.clicked.connect(self.addMarker)
        self.bt_add.setStyle(QtGui.QFont().setBold(True))
        self.bt_remove = QtWidgets.QPushButton('-')
        self.bt_remove.clicked.connect(self.removeMarker)
        self.bt_reload = QtWidgets.QPushButton('reload')
        self.bt_reload.clicked.connect(self.reloadMarkers)
        self.bt_reloadFile = QtWidgets.QPushButton('reload from file')
        self.bt_reloadFile.clicked.connect(self.loadFromFile)

        self.layout_master = QtWidgets.QHBoxLayout()
        self.layout_editMarkers = QtWidgets.QVBoxLayout()
        self.layout_editMarkers.setAlignment(QtCore.Qt.AlignLeft)
        self.layout_editMarkers.setContentsMargins(0,0,0,0)

        self.layout_markers = QtWidgets.QHBoxLayout()
        self.group_markers = QtWidgets.QGroupBox('Markers')
        self.group_markers.setLayout(self.layout_markers)
        self.group_markers.setAlignment(QtCore.Qt.AlignLeft)

        self.layout_reload = QtWidgets.QVBoxLayout()
        self.layout_reload.setAlignment(QtCore.Qt.AlignRight)
        self.layout_reload.setContentsMargins(0,0,0,0)

        self.layout_editMarkers.addWidget(self.bt_add)
        self.layout_editMarkers.addWidget(self.bt_remove)
        self.layout_editMarkers.setSpacing(0)
        self.layout_reload.addWidget(self.bt_reload)
        self.layout_reload.addWidget(self.bt_reloadFile)

        self.layout_master.addLayout(self.layout_editMarkers)
        self.layout_master.addWidget(self.group_markers)
        self.layout_master.addStretch()
        self.layout_master.addLayout(self.layout_reload)
        self.setLayout(self.layout_master)
        self.setMinimumWidth(1000)
        self.setContentsMargins(0,0,0,0)


    def saveMarkers(self):
        '''save marker into json files'''
        layout_markers = self.layout_markers
        num_widget = layout_markers.count()
        json_marker = {}

        for w in range(0,num_widget):
            thisWidget = layout_markers.itemAt(w).widget()



    def addMarker(self):
        '''add MarkerButton widget'''
        self.p = MarkerAdd(self.layout_markers)
        self.p.exec_()
        # add connect signal to the last widgets
        self.layout_markers.itemAt(self.layout_markers.count()-1).widget().clicked.connect(self.setFrame)


    def removeMarker(self):
        '''remove MarkerButton widget'''
        try:
            num_widget = self.layout_markers.count()-1
            thisWidget = self.layout_markers.itemAt(num_widget).widget()
            thisWidget.setParent(None)
            self.saveMarkers()
        except:
            print "no markers to be removed"



    def reloadMarkers(self):
        '''reload from json file and rebuild MarkerButtons'''


    def loadFromFile(self):
        '''load buttons from a json file'''


    def setFrame(self):
        '''set the frame in nuke when marker is clicked'''
        thisSender = self.sender()
        print "%s | %s | %s" % (thisSender.id, thisSender.frame, thisSender.label)



app = QtWidgets.QApplication(sys.argv)
p = Core_TimelineMarker()
p.show()
p.raise_()
app.exec_()