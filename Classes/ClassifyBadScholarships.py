#!/usr/bin/env python
# -*- coding: utf-8 -*-

import nltk
import re
from Classes.TokenizeOnWhitespacePunctuation import TokenizeOnWhitespacePunctuation
from Classes.TokenizeIntoSentences import TokenizeIntoSentences
from Classes.CleanText import CleanText
from Classes.SUDBConnect import SUDBConnect
from Classes.CleanText import CleanText


class ClassifyBadScholarships(object):
    def __init__(self, sponsorsList=[], infoTextList=[], test=None):
        self.test = test
        self.infoTextList = infoTextList
        self.sponsorsList = sponsorsList
        self.predictedBad = []
        self.db = SUDBConnect()

        self.educationKeywords = ['University', 'School', 'Institute', 'College', 'Conservatory']

        self.countriesList = self.getCountriesList()
        self.countryCapitalsList = self.getCountryCapitalsList()
        self.demonymsList = self.getDemonymsList()
        self.statesList = self.getStatesList()
        self.usCitiesList = self.getUSCitiesList()
        self.otherGPES = ['U.S.', 'U.S.A.', 'US', 'USA', 'UK', 'EU', 'European', 'African', 'Middle East', 'British',
                          'English', 'Europe', 'Soviet', 'Asian', 'New England', 'Tibetan', 'Tibet', 'Britain',
                          'South America', 'New York City', 'Florence', 'Milano', 'Korea', 'Korean', 'NYC', 'Barcelona',
                          'Balkan', 'Felician', 'Dubai', 'Sydney', 'South American', 'Asia', 'Eastern Europe',
                          'Central Eastern Europe', 'America', 'North America', 'Bethesda', 'Central America',
                          'Central American', 'Eurasia', 'Scandinavia', 'Scandinavian', 'Scandinavians', 'Africa',
                          'North American', 'Rhineland', 'Detroit', 'Bavaria', 'Bavarian', 'Latin America',
                          'Latin American']

    def loopThroughLeadsAndDoStuff(self):
        for i in range(len(self.infoTextList)):
            sponsor = ''
            if len(self.sponsorsList) > 0:
                sponsor = self.sponsorsList[i]
            infoText = self.infoTextList[i]
            predictBad = self.classifyOpportunity(sponsor, infoText)
            self.predictedBad.append(predictBad)

        return self.predictedBad

    def classifyOpportunity(self, sponsor, infoText):
        badScholarship = False

        if self.test == 'sponsorOnly':
            if self.checkBadSponsor(sponsor):
                badScholarship = True
        elif self.test == 'infoTextOnly':
            if self.checkBadText(infoText):
                badScholarship = True
        else:
            if self.checkBadSponsor(sponsor):
                badScholarship = True
            else:
                if self.checkBadText(infoText):
                    badScholarship = True

        if badScholarship:
            badScholarship = 'Yes'
        else:
            badScholarship = 'No'

        return badScholarship

    def checkBadSponsor(self, sponsor):
        sponsorUnigrams = TokenizeOnWhitespacePunctuation(sponsor).getUnigrams()
        educationKeywords = ['university', 'school', 'institute', 'college', 'schools', 'academy', 'universities',
                             'colleges']
        badSponsor = False

        for keyword in educationKeywords:
            if keyword in sponsorUnigrams:
                if sponsor != 'University of Arizona':
                    badSponsor = True

        if not badSponsor:
            findAcronymsRegex = re.search('[A-Z][A-Z][A-Z]+', sponsor)
            if findAcronymsRegex:
                badAcronyms = ['SWE']
                if findAcronymsRegex.group() in badAcronyms:
                    badSponsor = True
                else:
                    findParenthesesAcronym = re.search('\([A-Z][A-Z][A-Z]+\)', sponsor)
                    if not findParenthesesAcronym:
                        exceptionsList = ['LLC']
                        if findAcronymsRegex.group() not in exceptionsList:
                            badSponsor = True

        if not badSponsor:
            findUniversityOtherLanguage = re.search('[uU]niv', sponsor)
            if findUniversityOtherLanguage:
                badSponsor = True

        return badSponsor

    def checkBadText(self, infoText):
        infoTextSentences = TokenizeIntoSentences.doTokenize(infoText)

        organizations = []
        geoPoliticalEntities = []

        for sentence in infoTextSentences:
            sentenceOrganizations = self.parseOranizations(sentence)
            sentenceGPEs = self.parseGPEs(sentence)
            for organization in sentenceOrganizations:
                organizations.append(organization)

            for gpe in sentenceGPEs:
                gpe = gpe[0].upper() + gpe[1:]
                geoPoliticalEntities.append(gpe)

        misplacedGPEs = self.getMistaggedGPEsFromOrganizations(organizations)
        actualOrganizations = []
        for gpe in misplacedGPEs:
            geoPoliticalEntities.append(gpe)
        for organization in organizations:
            if organization not in misplacedGPEs:
                actualOrganizations.append(organization)

        organizations = actualOrganizations

        regexGPEsFromOrganizations = self.findGPEsWithRegex(organizations)
        for gpe in regexGPEsFromOrganizations:
            geoPoliticalEntities.append(gpe)

        badText = self.scanOrganizations(organizations)

        if badText != True:
            badText = self.scanGeoPoliticalEntities(geoPoliticalEntities, infoText)

        return badText

    def parseOranizations(self, sentence):
        unigrams = TokenizeOnWhitespacePunctuation(sentence, keepCaps=True).getUnigrams()
        for i in range(len(unigrams) - 1):
            if unigrams[i] in self.educationKeywords:
                if unigrams[i + 1] == 'of':
                    unigrams[i + 1] = unigrams[i + 1].title()

        posTagUnigrams = nltk.pos_tag(unigrams)

        chunkNamedEntities = nltk.ne_chunk(posTagUnigrams)

        organizations = []
        for treeBranch in chunkNamedEntities:
            if hasattr(treeBranch, 'label') and treeBranch.label() == 'ORGANIZATION':
                organizations.append(str(treeBranch))
        organizations = self.formatNamedEntities(organizations)

        return organizations

    def parseGPEs(self, sentence):
        sentence = self.cleanSentenceForGPEParsing(sentence)

        unigrams = TokenizeOnWhitespacePunctuation(sentence, keepCaps=True).getUnigrams()
        for i in range(len(unigrams) - 1):
            if unigrams[i] in self.educationKeywords:
                if unigrams[i + 1] == 'of':
                    unigrams[i + 1] = unigrams[i + 1].title()

        posTagUnigrams = nltk.pos_tag(unigrams)

        chunkNamedEntities = nltk.ne_chunk(posTagUnigrams)

        geoPoliticalEntities = []
        for treeBranch in chunkNamedEntities:
            if hasattr(treeBranch, 'label') and treeBranch.label() == 'GPE':
                geoPoliticalEntities.append(str(treeBranch))
        geoPoliticalEntities = self.formatNamedEntities(geoPoliticalEntities)

        return geoPoliticalEntities

    def formatNamedEntities(self, namedEntityList):
        formattedStrings = []

        for namedEntity in namedEntityList:
            result = re.sub('ORGANIZATION\s', '', namedEntity)
            result = re.sub('GPE\s', '', result)
            result = re.sub('/[A-Z]+', '', result)
            result = re.sub('\(', '', result)
            result = re.sub('\)', '', result)

            formattedStrings.append(result)

        return formattedStrings

    def uncapitalize(self, string):
        if len(string) > 0:
            string = string[0].lower() + string[1:]
        return string

    def replaceWithLowerCase(self, match):
        return match.lower()

    def cleanSentenceForGPEParsing(self, sentence):
        findFirstWordAfterAsterisk = re.findall('\*\s?(\w+)', sentence)
        if findFirstWordAfterAsterisk != []:
            for match in findFirstWordAfterAsterisk:
                sentence = re.sub(match, self.replaceWithLowerCase(match), sentence)

        findFirstWordAfterBullet = re.findall('•\s?(\w+)', sentence)
        if findFirstWordAfterBullet != []:
            for match in findFirstWordAfterBullet:
                sentence = re.sub(match, self.replaceWithLowerCase(match), sentence)

        sentence = re.sub('\*', '', sentence)
        sentence = re.sub('•', '', sentence)

        sentence = CleanText.cleanALLtheText(sentence)
        sentence = self.uncapitalize(sentence)

        return sentence

    def scanOrganizations(self, organizations):
        badTextOrganizations = False

        for organization in organizations:
            educationKeywordsForRegex = ['%s\s' % educationKeyword for educationKeyword in self.educationKeywords]
            educationRegex = '|'.join(educationKeywordsForRegex)
            if re.search(educationRegex, str(organization)):
                if organization != 'University Of Arizona':
                    badTextOrganizations = True
            else:
                educationKeywordsForRegex = ['%s$' % educationKeyword for educationKeyword in self.educationKeywords]
                educationRegex = '|'.join(educationKeywordsForRegex)
                if re.search(educationRegex, str(organization)):
                    badTextOrganizations = True

        return badTextOrganizations

    def scanGeoPoliticalEntities(self, geoPoliticalEntities, infoText):
        badTextGPEs = False

        allowedGPEs = ['United States', 'U.S.', 'America', 'Arizona', 'Tucson', 'US', 'American', 'North America',
                       'North American', 'USA']

        filteredGPEs = []
        badGPEs = []
        for gpe in geoPoliticalEntities:
            if gpe in self.countriesList:
                filteredGPEs.append(gpe)
            elif gpe in self.countryCapitalsList:
                filteredGPEs.append(gpe)
            elif gpe in self.demonymsList:
                filteredGPEs.append(gpe)
            elif gpe in self.statesList:
                filteredGPEs.append(gpe)
            elif gpe in self.usCitiesList:
                filteredGPEs.append(gpe)
            elif gpe in self.otherGPES:
                filteredGPEs.append(gpe)
            else:
                badGPEs.append(gpe)

        regexFoundGPEs = self.findGPEsWithRegex(badGPEs)
        for gpe in regexFoundGPEs:
            filteredGPEs.append(gpe)

        filteredGPEs = self.filterOutGPEsDemographicsPhrases(filteredGPEs, infoText)

        for gpe in filteredGPEs:
            if gpe not in allowedGPEs:
                if not re.search('study\sabroad', infoText.lower()) and not re.search('teach\sabroad',
                                                                                      infoText.lower()):
                    badTextGPEs = True
                elif re.search('study\sabroad', infoText.lower()) or re.search('teach\sabroad', infoText.lower()):
                    if gpe not in self.countriesList and gpe not in self.countryCapitalsList:
                        badTextGPEs = True

        return badTextGPEs

    def getCountriesList(self):
        countriesList = []

        rows = self.db.getRowsDB("select distinct Country from dbo.CountriesAndCapitals")
        for row in rows:
            countriesList.append(row.Country)

        return countriesList

    def getCountryCapitalsList(self):
        countryCapitalsList = []

        rows = self.db.getRowsDB("select distinct Capital from dbo.CountriesAndCapitals")
        for row in rows:
            countryCapitalsList.append(row.Capital)

        return countryCapitalsList

    def getStatesList(self):
        statesList = []

        rows = self.db.getRowsDB("select distinct State from dbo.USCitiesStates")
        for row in rows:
            statesList.append(row.State)

        return statesList

    def getUSCitiesList(self):
        usCitiesList = []

        rows = self.db.getRowsDB("select distinct City from dbo.USCitiesStates")
        for row in rows:
            usCitiesList.append(row.City)

        return usCitiesList

    def getDemonymsList(self):
        demonymsList = []

        rows = self.db.getRowsDB('select distinct Demonym from dbo.CountriesAndCapitals')
        for row in rows:
            demonymsList.append(row.Demonym)

        return demonymsList

    def getMistaggedGPEsFromOrganizations(self, organizations):
        isActuallyGPE = []

        for organization in organizations:
            if organization in self.countriesList:
                isActuallyGPE.append(organization)
            elif organization in self.countryCapitalsList:
                isActuallyGPE.append(organization)
            elif organization in self.demonymsList:
                isActuallyGPE.append(organization)
            elif organization in self.statesList:
                isActuallyGPE.append(organization)
            elif organization in self.usCitiesList:
                isActuallyGPE.append(organization)
            elif organization in self.otherGPES:
                isActuallyGPE.append(organization)

        return isActuallyGPE

    def findGPEsWithRegex(self, namedEntitiesList):
        countriesRegex = '|'.join(self.countriesList)
        countryCapitalsRegex = '|'.join(self.countryCapitalsList)
        statesRegex = '|'.join(self.statesList)
        usCitiesRegex = '|'.join(self.usCitiesList)

        foundGPEs = []

        for namedEntity in namedEntitiesList:
            findCountries = re.search(countriesRegex, namedEntity)
            findCountryCapitals = re.search(countryCapitalsRegex, namedEntity)
            findStates = re.search(statesRegex, namedEntity)
            findUSCities = re.search(usCitiesRegex, namedEntity)

            if findCountries:
                foundGPEs.append(findCountries.group())
            if findCountryCapitals:
                foundGPEs.append(findCountryCapitals.group())
            if findStates:
                foundGPEs.append(findStates.group())
            if findUSCities:
                foundGPEs.append(findUSCities.group())

        gpesAfterDemographicFiltering = self.checkRegexGPEsAgainstDemographicsList(foundGPEs, namedEntitiesList)
        foundGPEs = gpesAfterDemographicFiltering

        return foundGPEs

    def checkRegexGPEsAgainstDemographicsList(self, regexGPEs, namedEntityList):
        goodGPEs = regexGPEs

        for namedEntity in namedEntityList:
            if re.search('Alaskan', namedEntity):
                if 'Alaska' in goodGPEs:
                    goodGPEs.remove('Alaska')
            if re.search('American Indian', CleanText.cleanALLtheText(namedEntity)) or re.search('Native American',
                                                                                                 CleanText.cleanALLtheText(
                                                                                                         namedEntity)):
                if 'Indian' in goodGPEs:
                    goodGPEs.remove('Indian')
                if 'India' in goodGPEs:
                    goodGPEs.remove('India')

        return goodGPEs

    def filterOutGPEsDemographicsPhrases(self, gpesList, infoText):
        filteredGPEs = gpesList

        findAfricanAmerican = re.search('African American', CleanText.cleanALLtheText(infoText))
        if findAfricanAmerican:
            if 'African' in filteredGPEs:
                filteredGPEs.remove('African')

        findAsianAmerican = re.search('Asian American', CleanText.cleanALLtheText(infoText))
        if findAsianAmerican:
            if 'Asian' in filteredGPEs:
                filteredGPEs.remove('Asian')

        findDistrictOfColumbia = re.search('district of columbia', infoText.lower())
        if findDistrictOfColumbia:
            if 'Columbia' in filteredGPEs:
                filteredGPEs.remove('Columbia')
            if 'Washington' in filteredGPEs:
                filteredGPEs.remove('Washington')

        return filteredGPEs
