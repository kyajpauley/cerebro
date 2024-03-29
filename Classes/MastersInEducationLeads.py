from selenium import webdriver
from Classes.RipPage import RipPage
from Classes.CleanText import CleanText


class MastersInEducationLeads(object):
    def __init__(self):
        self.driver = webdriver.Chrome('C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')
        self.base_url = 'http://www.mastersineducation.net'
        self.driver.get(self.base_url + '/scholarships')
        self.driver.implicitly_wait(2)

        self.resultsArrays = []
        self.mastersInEducationLeadsArrays = []

    def getLeads(self):
        self.loopOverPages()

        for resultArray in self.resultsArrays:
            self.makeLeadArray(resultArray)

        self.driver.quit()

        return self.mastersInEducationLeadsArrays

    def loopOverPages(self):
        self.driver.find_element_by_xpath("//section[@class='scholarships']/ul[@class='tabs base']/li[2]").click()
        self.driver.implicitly_wait(2)
        self.getScholarshipsPicks()
        nextScholarshipPage = self.checkIfNextPage()
        while nextScholarshipPage:
            self.goToNextPage()
            self.getScholarshipsPicks()
            nextScholarshipPage = self.checkIfNextPage()

        self.getEditorsPicks()

    def makeLeadArray(self, resultArray):
        title = resultArray[0]
        amount = resultArray[1]
        deadline = resultArray[2]
        description = resultArray[3]
        sourceWebsite = resultArray[4]
        sourceText = RipPage.getPageSource(sourceWebsite)

        sourceText = CleanText.cleanALLtheText(sourceText)

        mastersInEducationLeadArray = [title, amount, deadline, description, sourceWebsite, sourceText]
        self.mastersInEducationLeadsArrays.append(mastersInEducationLeadArray)

    def getEditorsPicks(self):
        self.driver.get(self.base_url + '/scholarships')
        self.driver.implicitly_wait(2)

        visibleClickyDivs = self.driver.find_elements_by_xpath(
            "//section[@class='scholarships']/div[@class='tab h-results']/div[@class='h-result js-has-toggle']/div[@class='h-result-header js-toggle']")
        for clickyDiv in visibleClickyDivs:
            clickyDiv.click()

        titlesList = self.getTitlesListEditors()
        amountsList = self.getAmountsListEditors()
        deadlinesList = self.getDeadlinesListEditors()
        descriptionsList = self.getDescriptionsListEditors()
        sourceWebsitesList = self.getSourceWebsitesListEditors()

        for i in range(len(titlesList)):
            title = titlesList[i]
            amount = amountsList[i]
            deadline = deadlinesList[i]
            description = descriptionsList[i]
            sourceWebsite = sourceWebsitesList[i]

            resultArray = [title, amount, deadline, description, sourceWebsite]
            self.resultsArrays.append(resultArray)

    def getScholarshipsPicks(self):
        visibleClickyDivs = self.driver.find_elements_by_xpath(
            "//section[@class = 'scholarships']/div[@class = 'tab']/section/div/div[@class = 'h-result-header js-toggle']")
        for clickyDiv in visibleClickyDivs:
            clickyDiv.click()

        titlesList = self.getTitlesListScholarships()
        deadlinesList = self.getDeadlinesListScholarships()
        descriptionsList = self.getDescriptionsListScholarships()
        sourceWebsitesList = self.getSourceWebsitesListScholarships()

        for i in range(len(titlesList)):
            title = titlesList[i]
            amount = ''
            deadline = deadlinesList[i]
            description = descriptionsList[i]
            sourceWebsite = sourceWebsitesList[i]

            resultArray = [title, amount, deadline, description, sourceWebsite]
            self.resultsArrays.append(resultArray)

    def getTitlesListEditors(self):
        titlesList = []

        titlesDivs = self.driver.find_elements_by_xpath(
            "//section[@class='scholarships']/div[@class='tab h-results']/div[@class='h-result js-has-toggle active']/div[@class='h-result-header js-toggle active']/h3")
        for title in titlesDivs:
            titlesList.append(title.get_attribute('textContent'))

        titlesList = [CleanText.cleanALLtheText(title) for title in titlesList]

        return titlesList

    def getTitlesListScholarships(self):
        titlesList = []

        titlesDivs = self.driver.find_elements_by_xpath(
            "//section[@class='scholarships']/div[@class='tab']/section/div/div/h3")
        for title in titlesDivs:
            titlesList.append(title.get_attribute('textContent'))

        titlesList = [CleanText.cleanALLtheText(title) for title in titlesList]

        return titlesList

    def getAmountsListEditors(self):
        amountsList = []

        amountsDivs = self.driver.find_elements_by_xpath("//dt[text() = 'Amount']/following-sibling::dd[1]")
        for amount in amountsDivs:
            amountsList.append(amount.get_attribute('textContent'))

        amountsList = [CleanText.cleanALLtheText(amount) for amount in amountsList]

        return amountsList

    def getDeadlinesListEditors(self):
        deadlinesList = []

        deadlinesDivs = self.driver.find_elements_by_xpath(
            "//dt[text() = 'Amount']/following-sibling::dt[text() = 'Deadline']/following-sibling::dd[1]")
        for deadline in deadlinesDivs:
            deadlinesList.append(deadline.get_attribute('textContent'))

        deadlinesList = [CleanText.cleanALLtheText(deadline) for deadline in deadlinesList]

        return deadlinesList

    def getDeadlinesListScholarships(self):
        deadlinesList = []

        deadlinesDivs = self.driver.find_elements_by_xpath(
            "//dt[text() = 'Renewable']/preceding-sibling::dt[text() = 'Deadline']/following-sibling::dd[1]")
        for deadline in deadlinesDivs:
            deadlinesList.append(deadline.get_attribute('textContent'))

        deadlinesList = [CleanText.cleanALLtheText(deadline) for deadline in deadlinesList]

        return deadlinesList

    def getDescriptionsListEditors(self):
        descriptionsList = []

        descriptionsDivs = self.driver.find_elements_by_xpath(
            "//dt[text() = 'Amount']/following-sibling::dt[text() = 'Deadline']/following-sibling::dd[1]")
        for description in descriptionsDivs:
            descriptionsList.append(description.get_attribute('textContent'))

        descriptionsList = [CleanText.cleanALLtheText(description) for description in descriptionsList]

        return descriptionsList

    def getDescriptionsListScholarships(self):
        descriptionsList = []

        descriptionsDivs = self.driver.find_elements_by_xpath(
            "//section[@class = 'scholarships']/div[@class = 'tab']/section/div/div/p")
        for description in descriptionsDivs:
            descriptionsList.append(description.get_attribute('textContent'))

        descriptionsList = [CleanText.cleanALLtheText(description) for description in descriptionsList]

        return descriptionsList

    def getSourceWebsitesListEditors(self):
        sourceWebsitesList = []

        linksDivs = self.driver.find_elements_by_xpath(
            "//div[@class = 'h-result-header js-toggle active']/following-sibling::div[@class = 'js-target hide scholarship-content']/p/following-sibling::div[@class='text-center']/a[@class = 'btn']")
        for link in linksDivs:
            sourceWebsitesList.append(link.get_attribute('href'))

        return sourceWebsitesList

    def getSourceWebsitesListScholarships(self):
        sourceWebsitesList = []

        linksDivs = self.driver.find_elements_by_xpath(
            "//section[@class = 'scholarships']/div[@class = 'tab']/section/div/div/p/following-sibling::div[@class='text-center']/a[@class = 'btn']")
        for link in linksDivs:
            sourceWebsitesList.append(link.get_attribute('href'))

        return sourceWebsitesList

    def checkIfNextPage(self):
        checkNextPage = self.driver.find_elements_by_xpath("//a[@title = 'Next']")
        if checkNextPage != []:
            return True
        else:
            return False

    def goToNextPage(self):
        if self.checkIfNextPage():
            nextPageUrl = self.driver.find_element_by_xpath("//a[@title = 'Next']").get_attribute('href')
            self.driver.get(nextPageUrl)
            self.driver.implicitly_wait(2)

