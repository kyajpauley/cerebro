from Classes.SUDBConnect import SUDBConnect
import time
import re


class InsertScholarships360LeadArrayIntoScholarships360DB(object):
    def __init__(self, scholarships360LeadArray, fundingClassification, badScholarshipClassification):
        self.scholarships360LeadArray = scholarships360LeadArray
        self.fundingClassification = fundingClassification
        self.badScholarshipClassificaion = badScholarshipClassification
        self.db = SUDBConnect()
        self.fileSystemDB = SUDBConnect(destination='filesystem')

        self.name = self.scholarships360LeadArray[0]
        self.url = self.scholarships360LeadArray[1]
        self.description = self.scholarships360LeadArray[2]
        self.eligibility = self.scholarships360LeadArray[3]
        self.amount = self.scholarships360LeadArray[4]
        self.amountInfo = self.scholarships360LeadArray[5]
        self.deadline = self.scholarships360LeadArray[6]
        self.deadlineInfo = self.scholarships360LeadArray[7]
        self.sourceWebsite = self.scholarships360LeadArray[8]
        self.sourceText = self.scholarships360LeadArray[9]
        self.date = time.strftime('%Y%m%d')

    def checkIfAlreadyInDB(self):
        matchingRow = self.db.getRowsDB(
                "select * from dbo.Scholarships360Leads where Name='" + self.name + "' and Url='" + self.url + "'")
        if matchingRow != []:
            return True
        else:
            return False

    def writeFileToDisk(self):
        tableName = 'Scholarships360Leads'
        user = 'Kya'
        website = re.sub('Leads', '', tableName)
        columns = self.db.getColumnNamesFromTable(tableName)
        currentRow = self.db.getRowsDB(
                "select * from dbo.Scholarships360Leads where Name='" + self.name + "' and Url='" + self.url + "'")[0]
        self.fileSystemDB.writeFile(columns, currentRow, user, website, self.url, self.date)

    def insertUpdateLead(self):
        if not self.checkIfAlreadyInDB():
            self.db.insertUpdateOrDeleteDB(
                    "INSERT INTO dbo.Scholarships360Leads (Name, Url, Description, Eligibility, Amount, AmountInfo, Deadline, DeadlineInfo, SourceWebsite, SourceText, Tag, BadScholarship, Date) VALUES (N'" + self.name + "', N'" + self.url + "', N'" + self.description + "', N'" + self.eligibility + "', N'" + self.amount + "', N'" + self.amountInfo + "', N'" + self.deadline + "', N'" + self.deadlineInfo + "', N'" + self.sourceWebsite + "', N'" + self.sourceText + "', '" + self.fundingClassification + "', '" + self.badScholarshipClassificaion + "', '" + self.date + "')")
            self.writeFileToDisk()
            return True
        else:
            self.db.insertUpdateOrDeleteDB(
                    "update dbo.Scholarships360Leads set Description=N'" + self.description + "', Eligibility=N'" + self.eligibility + "', Amount=N'" + self.amount + "', AmountInfo=N'" + self.amountInfo + "', Deadline=N'" + self.deadline + "', DeadlineInfo=N'" + self.deadlineInfo + "', SourceWebsite='" + self.sourceWebsite + "', SourceText=N'" + self.sourceText + "', Tag='" + self.fundingClassification + "', BadScholarship='" + self.badScholarshipClassificaion + "', Date='" + self.date + "' where Name='" + self.name + "' and Url='" + self.url + "'")
            self.writeFileToDisk()
            return False
