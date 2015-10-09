from Classes.SUDBConnect import SUDBConnect
from Classes.CleanText import CleanText


class GetDatabaseInfoScholarshipsWithClassStatuses(object):
    def __init__(self, requirementNeeded=None, useNot=False):
        self.requirementNeeded = requirementNeeded
        self.formattedRequirementNeeded = '%' + self.requirementNeeded + '%'
        self.db = SUDBConnect()

        if self.requirementNeeded and useNot:
            self.rows = self.db.getRows(
                "select * from dbo.ScholarshipsWithClassStatuses where RequirementNeeded not like '" + self.formattedRequirementNeeded + "'")
        elif self.requirementNeeded:
            self.rows = self.db.getRows(
                "select * from dbo.ScholarshipsWithClassStatuses where RequirementNeeded like '" + self.formattedRequirementNeeded + "'")
        else:
            self.rows = self.db.getRows("select * from dbo.ScholarshipsWithClassStatuses")

    def getScholarshipDescriptionsList(self):
        scholarshipDescriptionsList = []

        for row in self.rows:
            scholarshipDescriptionsList.append(CleanText.cleanALLtheText(row.ScholarshipDescription))

        return scholarshipDescriptionsList

    def getEligibilitiesList(self):
        eligibilitiesList = []

        for row in self.rows:
            eligibilitiesList.append(CleanText.cleanALLtheText(row.Eligibility))

        return eligibilitiesList
