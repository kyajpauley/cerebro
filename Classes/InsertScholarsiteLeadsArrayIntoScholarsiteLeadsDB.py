from Classes.SUDBConnect import SUDBConnect


class InsertScholarsiteLeadsArrayIntoScholarsiteLeadsDB(object):
    def __init__(self, scholarsiteLeadArray):
        self.scholarsiteLeadArray = scholarsiteLeadArray
        self.db = SUDBConnect()
        self.name = self.scholarsiteLeadArray[0]
        self.amount = self.scholarsiteLeadArray[1]
        self.deadline = self.scholarsiteLeadArray[2]
        self.requirements = self.scholarsiteLeadArray[3]
        self.annualAwards = self.scholarsiteLeadArray[4]
        self.major = self.scholarsiteLeadArray[5]
        self.academicLevel = self.scholarsiteLeadArray[6]
        self.qualifiedMinorities = self.scholarsiteLeadArray[7]
        self.eligibleInstitution = self.scholarsiteLeadArray[8]
        self.eligibleRegion = self.scholarsiteLeadArray[9]
        self.usCitizen = self.scholarsiteLeadArray[10]
        self.usResident = self.scholarsiteLeadArray[11]
        self.foreignNational = self.scholarsiteLeadArray[12]
        self.minimumAge = self.scholarsiteLeadArray[13]
        self.maximumAge = self.scholarsiteLeadArray[14]
        self.classRank = self.scholarsiteLeadArray[15]
        self.minimumGPA = self.scholarsiteLeadArray[16]
        self.minimumACT = self.scholarsiteLeadArray[17]
        self.minimumSAT = self.scholarsiteLeadArray[18]
        self.tag = 'Scholarship'

        self.db.insertUpdateOrDelete(
            "insert into dbo.ScholarsiteLeads (Name, Amount, Deadline, Requirements, AnnualAwards, Major, AcademicLevel, QualifiedMinorities, EligibleInstitution, EligibleRegion, USCitizen, USResident, ForeignNational, MinimumAge, MaximumAge, ClassRank, MinimumGPA, MinimumACT, MinimumSAT, Tag) values (N'" + self.name + "', N'" + self.amount + "', '" + self.deadline + "', N'" + self.requirements + "', N'" + self.annualAwards + "', N'" + self.major + "', N'" + self.academicLevel + "', N'" + self.qualifiedMinorities + "', N'" + self.eligibleInstitution + "', N'" + self.eligibleRegion + "', N'" + self.usCitizen + "', N'" + self.usResident + "', N'" + self.foreignNational + "', '" + self.minimumAge + "', '" + self.maximumAge + "', N'" + self.classRank + "', N'" + self.minimumGPA + "', N'" + self.minimumACT + "', N'" + self.minimumSAT + "', N'" + self.tag + "')")
