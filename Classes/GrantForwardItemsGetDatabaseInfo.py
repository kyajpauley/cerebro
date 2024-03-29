from Classes.SUDBConnect import SUDBConnect
from Classes.CleanText import CleanText


class GrantForwardItemsGetDatabaseInfo(object):
    def __init__(self, keyword=None, tag=None):
        self.tag = tag
        self.keyword = keyword
        self.db = SUDBConnect()

    def getTitles(self):
        titles = []

        if self.keyword and self.tag:
            rows = self.db.getRowsDB(
                "select Name from dbo.GrantForwardItems where Keyword='" + self.keyword + "' and Tag='" + self.tag + "'")
            for row in rows:
                titles.append(row.Name)
        elif self.keyword:
            rows = self.db.getRowsDB("select Name from dbo.GrantForwardItems where Keyword='" + self.keyword + "'")
            for row in rows:
                titles.append(row.Name)
        elif self.tag:
            rows = self.db.getRowsDB("select * from dbo.GrantForwardItems where Tag='" + self.tag + "'")
            for row in rows:
                titles.append(row.Name)
        else:
            rows = self.db.getRowsDB("select * from dbo.GrantForwardItems")
            for row in rows:
                titles.append(row.Name)

        return titles

    def getDescriptions(self):
        descriptions = []

        if self.tag and self.keyword:
            rows = self.db.getRowsDB(
                "select Description from dbo.GrantForwardItems where Keyword='" + self.keyword + "' and Tag='" + self.tag + "'")
            for row in rows:
                descriptions.append(row.Description)
        elif self.keyword:
            rows = self.db.getRowsDB(
                "select Description from dbo.GrantForwardItems where Keyword='" + self.keyword + "'")
            for row in rows:
                descriptions.append(row.Description)
        elif self.tag:
            rows = self.db.getRowsDB("select * from dbo.GrantForwardItems where Tag='" + self.tag + "'")
            for row in rows:
                descriptions.append(row.Description)
        else:
            rows = self.db.getRowsDB("select * from dbo.GrantForwardItems")
            for row in rows:
                descriptions.append(row.Description)

        return descriptions

    def getEligibilities(self):
        eligibilities = []

        if self.tag and self.keyword:
            rows = self.db.getRowsDB(
                "select Eligibility from dbo.GrantForwardItems where Keyword='" + self.keyword + "' and Tag='" + self.tag + "'")
            for row in rows:
                eligibilities.append(row.Eligibility)
        elif self.keyword:
            rows = self.db.getRowsDB(
                "select Eligibility from dbo.GrantForwardItems where Keyword='" + self.keyword + "'")
            for row in rows:
                eligibilities.append(row.Eligibility)
        elif self.tag:
            rows = self.db.getRowsDB("select * from dbo.GrantForwardItems where Tag='" + self.tag + "'")
            for row in rows:
                eligibilities.append(row.Eligibility)
        else:
            rows = self.db.getRowsDB("select * from dbo.GrantForwardItems")
            for row in rows:
                eligibilities.append(row.Eligibility)

        return eligibilities

    def getGrantForwardItemIds(self):
        grantForwardItemIds = []

        if self.tag and self.keyword:
            rows = self.db.getRowsDB(
                "select GrantForwardItemId from dbo.GrantForwardItems where Keyword='" + self.keyword + "' and Tag='" + self.tag + "'")
            for row in rows:
                grantForwardItemIds.append(str(row.GrantForwardItemId))
        elif self.keyword:
            rows = self.db.getRowsDB(
                "select GrantForwardItemId from dbo.GrantForwardItems where Keyword='" + self.keyword + "'")
            for row in rows:
                grantForwardItemIds.append(str(row.GrantForwardItemId))
        elif self.tag:
            rows = self.db.getRowsDB("select * from dbo.GrantForwardItems where Tag='" + self.tag + "'")
            for row in rows:
                grantForwardItemIds.append(row.GrantForwardItemId)
        else:
            rows = self.db.getRowsDB("select * from dbo.GrantForwardItems")
            for row in rows:
                grantForwardItemIds.append(row.GrantForwardItemId)

        return grantForwardItemIds

    def getSourceTexts(self):
        sourceTexts = []

        if self.tag and self.keyword:
            rows = self.db.getRowsDB(
                "select OpportunitySourceText from dbo.GrantForwardItems where Keyword='" + self.keyword + "' and Tag='" + self.tag + "'")
            for row in rows:
                sourceTexts.append(row.OpportunitySourceText)
        elif self.keyword:
            rows = self.db.getRowsDB(
                "select OpportunitySourceText from dbo.GrantForwardItems where Keyword='" + self.keyword + "'")
            for row in rows:
                sourceTexts.append(row.OpportunitySourceText)
        elif self.tag:
            rows = self.db.getRowsDB("select *from dbo.GrantForwardItems where Tag='" + self.tag + "'")
            for row in rows:
                sourceTexts.append(row.OpportunitySourceText)
        else:
            rows = self.db.getRowsDB("select * from dbo.GrantForwardItems")
            for row in rows:
                sourceTexts.append(row.OpportunitySourceText)

        return sourceTexts

    def getSponsors(self):
        sponsors = []

        if self.tag and self.keyword:
            rows = self.db.getRowsDB(
                "select * from dbo.GrantForwardItems where Keyword='" + self.keyword + "' and Tag='" + self.tag + "'")
            for row in rows:
                sponsors.append(row.Sponsor)
        elif self.keyword:
            rows = self.db.getRowsDB("select * from dbo.GrantForwrdItems where Keyword='" + self.keyword + "'")
            for row in rows:
                sponsors.append(row.Sponsor)
        elif self.tag:
            rows = self.db.getRowsDB("select * from dbo.GrantForwardItems where Tag='" + self.tag + "'")
            for row in rows:
                sponsors.append(row.Sponsor)
        else:
            rows = self.db.getRowsDB("select * from dbo.GrantForwardItems")
            for row in rows:
                sponsors.append(row.Sponsor)

        return sponsors

    def getListStringConcatenatedDescriptionEligibility(self):
        listComboDescriptionsEligibilities = []

        descriptions = self.getDescriptions()
        eligibilities = self.getEligibilities()

        for i in range(len(descriptions)):
            description = descriptions[i]
            eligibility = eligibilities[i]

            comboDescriptionEligibility = '%s %s' % (description, eligibility)
            comboDescriptionEligibility = CleanText.cleanALLtheText(comboDescriptionEligibility)
            listComboDescriptionsEligibilities.append(comboDescriptionEligibility)

        return listComboDescriptionsEligibilities

    def getTitleDescriptionList(self):
        wholeList = []

        titles = self.getTitles()
        descriptions = self.getDescriptions()

        for i in range(len(titles)):
            title = titles[i]
            description = descriptions[i]

            listOfItems = [title, description]
            wholeList.append(listOfItems)

        return wholeList

    @staticmethod
    def getKeywords(tag=None):
        db = SUDBConnect()
        keywords = []

        if tag:
            rows = db.getRowsDB("select distinct Keyword from dbo.GrantForwardItems where Tag='" + tag + "'")
            for row in rows:
                keywords.append(row.Keyword)
        else:
            rows = db.getRowsDB("select distinct Keyword from dbo.GrantForwardItems")
            for row in rows:
                keywords.append(row.Keyword)

        return keywords
