from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QCheckBox
from PyQt5.QtWidgets import QGroupBox, QVBoxLayout,QScrollArea, QPushButton
from PyQt5.QtWidgets import QRadioButton, QButtonGroup
from Ingestor import Ingestor
from DatabaseManager import DatabaseManager

ABSENTEE_DEFAULT_LIST=['Site Address','Site City','Site Zip Code','County',"1st Owner's First Name","1st Owner's Last Name"]
DIVORCE_DEFAULT_LIST=['Site Address','Site City','Site Zip Code','County',"1st Owner's First Name","1st Owner's Last Name"]
LISTPENDENT_DEFAULT_LIST=['Site Address','Site City','Site Zip Code','County',"1st Owner's First Name","1st Owner's Last Name"]
PROBATE_DEFAULT_LIST=['Site Address','Site City','Site Zip Code','County',"1st Owner's First Name","1st Owner's Last Name"]
DEFAULT_LISTS=[ABSENTEE_DEFAULT_LIST,DIVORCE_DEFAULT_LIST,LISTPENDENT_DEFAULT_LIST,PROBATE_DEFAULT_LIST]

class csv_importer_popup(QWidget):
    def __init__(self,window_title,file_loc,tables,db_file_loc,debug=False):
        super().__init__()
        self.title = window_title
        self.setWindowTitle(self.title)


        self.commonFileTypes = ['Absentee', 'Divorce', 'Lis Pendents','Probate']
        self.tablesInDB = tables

        #CSV file stuff
        self.ingestor = Ingestor(file_loc)
        self.ingestor.readCSV()

        #Database manager stuff
        self.db = DatabaseManager(db_file_loc)

        #Create the check box window
        #Create a group of buttons
        header_button_group = QButtonGroup()
        header_button_group.setExclusive(False)
        header_button_group_box = QGroupBox('Select which headers you want to import')
        #Make the layout display the buttons vertically
        header_button_group_layout = QVBoxLayout()
        for header in self.ingestor.getCSVHeaders():
            #Add each button to the layout from the csv file
            checkbox = QCheckBox(header)
            header_button_group.addButton(checkbox)
            header_button_group_layout.addWidget(header_button_group.buttons()[-1])

        #Make the window fit the longest word
        header_button_group_layout.addStretch(1)
        #set the button group's layout to the layout with the vertically
        #alligned button layout
        header_button_group_box.setLayout(header_button_group_layout)

        #Create a area that has a scroll bar
        scrollArea = QScrollArea()
        scrollArea.setWidget(header_button_group_box)
        scrollArea.horizontalScrollBar().setEnabled(False)

        commonHeaderGroup = QButtonGroup()
        #Create a group of common headers buttons
        commonHeaderGroupBox = QGroupBox('Select a default header setup')
        #Make the layout display the buttons vertically
        commonHeaderGroupLayout = QVBoxLayout()
        #For each common file types make a radio button
        count = 0
        for fileType in self.commonFileTypes:
            radioButton = QRadioButton(fileType)
            commonHeaderGroup.addButton(radioButton,count)
            commonHeaderGroupLayout.addWidget(commonHeaderGroup.buttons()[-1])
            count += 1
        #Allow window to stretch to longest word
        commonHeaderGroupLayout.addStretch(1)
        #Set the groups layout to the one with the added buttons
        commonHeaderGroupBox.setLayout(commonHeaderGroupLayout)

        #List of button groups
        self.buttonGroups = [commonHeaderGroup,header_button_group]

        #Create the master layout which is a grid
        layout = QGridLayout()
        #Add widgets
        #format of addWidget(widget,row,col,row span, col span)

        cancelButton = QPushButton('Cancel')
        importButton = QPushButton('Import')

        cancelButton.clicked.connect(self.closeWindow)
        importButton.clicked.connect(self.importCSV)

        layout.addWidget(scrollArea,1,1,1,2)
        layout.addWidget(commonHeaderGroupBox,2,1,1,2)
        layout.addWidget(cancelButton,3,1)
        layout.addWidget(importButton,3,2)
        self.setLayout(layout)
        self.resize(self.sizeHint())

        if debug:
            #Only here so if you run this class something shows up
            self.show()

    def closeWindow(self):
        #Closes the window
        self.close()

    def importCSV(self):
        self.closeWindow()

        #If any of the radio buttons are check it will return a number > -1
        if self.buttonGroups[0].checkedId() > -1:
            print("Radio button pressed")
            buttonID = self.buttonGroups[0].checkedId()
            print('Button id %i' % buttonID)
            #Use a default list for importing
            searchCritera = self.ingestor.getHeaderIndex(DEFAULT_LISTS[buttonID],self.ingestor.getCSVHeaders())
            print(searchCritera)

            buttonText = self.buttonGroups[0].buttons()[buttonID].text()
            #buttonText = self.buttonGroups[0].id(self.buttonGroups[0].checkedId()).text()

            #Check which table coresponds with the button pressed
            for tableName in self.tablesInDB:
                if buttonText == tableName:
                    print(tableName)
                    #print(self.ingestor.getRowAt(0))
                    #Uses the ingestor to search the unfiltered rows using
                    #this search critera list
                    self.ingestor.searchRows(searchCritera,self.ingestor.getRows())
                    rows = self.ingestor.getRows()

                    #Check if tables exists already
                    if not self.db.doesTableExist(tableName):
                        #If not the create it with the table name
                        self.db.create_table_list(tableName,self.db.remove_spaces(DEFAULT_LISTS[buttonID]),'string')

                    #Add the searched rows to the table that was clicked
                    #The seach critera list has to have spaces removed so the db
                    #doesn't get confused
                    self.db.add_list_of_rows(tableName,self.db.remove_spaces(DEFAULT_LISTS[buttonID]),rows)
                    print(self.db.get_table(tableName))


        else:
            #default header option not choosen, so custom lists
            for item in self.buttonGroups[1].buttons():
                if item.isChecked():
                    print(item.text())


#Running this file with run this part of the code
#Makes a pop up window
if __name__ == '__main__':
    file = "/home/anthonym/Documents/SchoolWork/SoftwareEngineering/Divorce_list_08.20.18_FIXED.csv"
    tables = ['Absentee','Divorce','Lis Pendent','Probate']
    app = QApplication([])
    ex = csv_importer_popup('Test',file,tables,'test.db',True)
    app.exec_()
