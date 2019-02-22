import csv
import os

class Ingestor:
    def __init__(self,fileLocation):
        self.filename = fileLocation
        self.rows = []
        self.headers = []


    def listToDict(self,list,defaultVal):
        """
        Takes an array of strings and maps it to an
        dictionary with a specified default val
        """
        dict = {}
        for item in list:
            dict[item] = -1
        return dict

    def readCSV(self):
        """
        Reads the csv from the file specified in the constructor. It reads in
        the first row as the row if column headers. Then it reads in the
        reamining rows into a 2d array
        """
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as csvfile:
                    #Created csv reader object
                    csvreader = csv.reader(csvfile)
                    #Reads in first row
                    #next(csvreader) reads in the next row
                    self.headers = next(csvreader)
                    for row in csvreader:
                        #Loops through all rows in csvreader adding it to and array
                        self.rows.append(row)
                return True
            except IOERROR:
                #If there is an io error return a false
                return False
            else:
                return False


    def getHeaderIndex(self,headerDic,fieldsList):
        """
        Takes the header dictionary and finds each element in the column
        headers from the fields list. It then updates the integer values
        for each element to match what column it is
        """
        for header in headerDic:
            #Loops through each item in the dictionary
            count = 0
            for field in fieldsList:
                #Loops through each column header in the column header array
                if field.upper() == header.upper():
                    #If the current column header is the same as the header in
                    #the header dictionary then save that index value
                    headerDic[header] = count
                    break
                else:
                    count = count + 1
        return headerDic

    def searchRow(self,headerDic, unfilteredRow):
        """
        Takes the header dictionary and an unfiltered row of data and sorts
        it. Using the int value in the dictionary for each element it take
        it from the unfiltered row. The values from the unfiltered row are saved
        in a new array and returned
        """
        filteredRow = []
        for header in headerDic:
            filteredRow.append(unfilteredRow[headerDic[header]])

        return filteredRow

    def searchRows(self,headerDic,unfilteredRows):
        """
        Iderates over all the rows in unfiltered rows and sorts them using
        the dictionary
        """
        newRows = []
        for row in unfilteredRows:
            newRows.append(self.searchRow(headerDic,row))
        self.rows = newRows

    def getCritera(self):
        return self.searchCritera

    def getRows(self):
        return self.rows

    def getRowAt(self, index):
        return self.rows[index]

    def getNumberOfRows(self):
        return len(self.rows)

    def getNumberOfHeaders(self):
        return len(self.headers)

    def getCSVHeaders(self):
        return self.headers

    def getFileLoc(self):
        return self.filename

    def updateFileLoc(self,newLocation):
        if newLocation and os.path.exists(newLocation):
            self.filename = newLocation
            return True
        else:
            return False
