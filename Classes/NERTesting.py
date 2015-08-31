#!/usr/bin/env python
# -*- coding: utf-8 -*-

import nltk
import re
from Classes.TokenizeOnWhitespacePunctuation import TokenizeOnWhitespacePunctuation
from Classes.TokenizeIntoSentences import TokenizeIntoSentences
from Classes.CleanText import CleanText


class NERTesting(object):
    def __init__(self, sponsorsList, infoTextList, test=None):
        self.test = test
        self.infoTextList = infoTextList
        self.sponsorsList = sponsorsList
        self.predictedBad = []

        self.educationKeywords = ['University', 'School', 'Institute', 'College']

    def loopThroughLeadsAndDoStuff(self):
        for i in range(len(self.sponsorsList)):
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
        badText = False

        organizations = []
        geoPoliticalEntities = []

        for sentence in infoTextSentences:
            sentenceOrganizations = self.parseOranizations(sentence)
            sentenceGPEs = self.parseGPEs(sentence)
            for organization in sentenceOrganizations:
                organizations.append(organization)

                # for gpe in sentenceGeoPoliticalEntities:
                #    geoPoliticalEntities.append(gpe)

        filteredGPEs = []
        for geoPoliticalEntity in geoPoliticalEntities:
            if geoPoliticalEntity not in organizations:
                filteredGPEs.append(geoPoliticalEntity)
        '''
        if len(organizations) > 0:
            print('Organizations: %s' % organizations)
        if len(filteredGPEs) > 0:
            print('GPEs: %s' % filteredGPEs)
        '''

        for organization in organizations:
            educationKeywordsForRegex = ['%s\s' % educationKeyword for educationKeyword in self.educationKeywords]
            educationRegex = '|'.join(educationKeywordsForRegex)
            if re.search(educationRegex, str(organization)):
                if organization != 'University Of Arizona':
                    badText = True

        if badText != True:
            for gpe in geoPoliticalEntities:
                allowedLocations = ['United States', 'U.S.', 'America', 'Arizona', 'Tucson', 'US']
                locationsRegex = '|'.join(allowedLocations)
                if not re.search(locationsRegex, str(gpe)):
                    badText = True
                else:
                    badText = False

        print(badText)
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
        print(sentence)

        sentence = self.cleanSentenceForGPEParsing(sentence)

        print(sentence)

    '''
    def parseNamedEntities(self, posTagUnigrams):
        chunkNamedEntities = nltk.ne_chunk(posTagUnigrams)

        organizations = []
        for treeBranch in chunkNamedEntities:
            if hasattr(treeBranch, 'label') and treeBranch.label() == 'ORGANIZATION':
                organizations.append(str(treeBranch))
        organizations = self.formatNamedEntities(organizations)

        geoPoliticalEntities = []
        for treeBranch in chunkNamedEntities:
            if hasattr(treeBranch, 'label') and treeBranch.label() == 'GPE':
                geoPoliticalEntities.append(str(treeBranch))
        geoPoliticalEntities = self.formatNamedEntities(geoPoliticalEntities)

        namedEntitiesOrgGPEList = [organizations, geoPoliticalEntities]
        return namedEntitiesOrgGPEList
    '''

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
        # sentence = CleanText.cleanALLtheText(sentence)
        # sentence = self.uncapitalize(sentence)

        # sentence = re.sub('\*\s?(\w+)', self.replaceWithLowerCase(match), sentence)




        # findFirstWordAfterAsterisk = re.search('\*\s?(\w+)', sentence)
        # if findFirstWordAfterAsterisk:
        #    sentence = re.sub('\*\s?(\w+)', self.replaceWithLowerCase(findFirstWordAfterAsterisk), sentence)

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

        return sentence
