import uuid
from datetime import date
from decimal import Decimal
from collections import defaultdict

class DonorInfo():
    def __init__(self):
        self._filerId:str = ''
        self._amendmentInd:str = ''
        self._reportType:str = ''
        self._pgi:str = ''
        self._imageNbr:str = ''
        self._transactionType = ''
        self._entityType = ''
        self._name:str = ''
        self._firstname:str = ''
        self._lastname:str = ''
        self._city:str = ''
        self._state:str = ''
        self._zip:str = ''
        self._employer:str = ''
        self._transactionDate:date = date.min
        self._transactionAmount:Decimal = 0.00
        self._transactionId:str = ''
        self._rowkey = None
        self._originalRow = ''
        self._fecRecNumber = ''

    @property
    def name(self) -> str:
        return self._name
    @name.setter
    def name(self, value:str):
        if value != self._name:
            self._name = value
            self._rowkey = None

    @property
    def filerId(self) -> str:
        return self._filerId
    @filerId.setter
    def filerId(self, value:str):
        self._filerId = value

    @property
    def amendmentInd(self) -> str:
        return self._amendmentInd
    @amendmentInd.setter
    def amendmentInd(self, value:str):
        self._amendmentInd = value

    @property
    def reportType(self) -> str:
        return self._reportType
    @reportType.setter
    def reportType(self, value:str):
        self._reportType = value

    @property
    def pgi(self) -> str:
        return self._pgi
    @pgi.setter
    def pgi(self, value:str):
        self._pgi = value

    @property
    def imageNbr(self) -> str:
        return self._imageNbr
    @imageNbr.setter
    def imageNbr(self, value:str):
        self._imageNbr = value

    @property
    def transactionType(self) -> str:
        return self._transactionType
    @transactionType.setter
    def transactionType(self, value:str):
        self._transactionType = value

    @property
    def entityType(self) -> str:
        return self._entityType
    @entityType.setter
    def entityType(self, value:str):
        self._entityType = value

    @property
    def firstname(self) -> str:
        return self._firstname
    @firstname.setter
    def firstname(self, value:str):
        self._firstname = value

    @property
    def lastname(self) -> str:
        return self._lastname
    @lastname.setter
    def lastname(self, value:str):
        self._lastname = value
    
    @property
    def city(self) -> str:
        return self._city
    @city.setter
    def city(self, value:str):
        if value != self._city:
            self._city = value
            self._rowkey = None

    @property
    def state(self) -> str:
        return self._state
    @state.setter
    def state(self, value:str):
        if value != self._state:
            self._state = value
            self._rowkey = None

    @property
    def zip(self) -> str:
        return self._zip
    @zip.setter
    def zip(self, value:str):
        if value != self._zip:
            self._zip = value
            self._rowkey = None

    @property
    def employer(self) -> str:
        return self._employer
    @employer.setter
    def employer(self, a: str):
        self._employer = a

    @property
    def transactionDate(self) -> date:
        return self._transactionDate
    @transactionDate.setter
    def transactionDate(self, value:date):
        self._transactionDate = value

    @property
    def transactionAmount(self) -> Decimal:
        return self._transactionAmount
    @transactionAmount.setter
    def transactionAmount(self, value:Decimal):
        self._transactionAmount = value

    @property
    def transactionId(self) -> str:
        return self._transactionId
    @transactionId.setter
    def transactionId(self, value:str):
        self._transactionId = value

    @property
    def fecRecNumber(self) -> str:
        return self._fecRecNumber
    @fecRecNumber.setter
    def fecRecNumber(self, value:str):
        self._fecRecNumber = value
            
    @property
    def rowkey(self):
        if self._rowkey is None:
            self._rowkey = f'{self.name}{self.city}{self.state}{self.zip}'
        return self._rowkey
    
    @property
    def originalRow(self) -> str:
        return self._originalRow
    @originalRow.setter
    def originalRow(self, value:str):
        self._originalRow = value

def mapRowToClass(delimitedLine: str) -> DonorInfo:
    row = DonorInfo()
    fields = delimitedLine.split('|')
    row.filerId = parseSafeString(fields[0])
    row.amendmentInd = parseSafeString(fields[1])
    row.reportType = parseSafeString(fields[2])
    row.pgi = parseSafeString(fields[3])
    row.imageNbr = parseSafeString(fields[4])
    row.transactionType = parseSafeString(fields[5])
    row.entityType = parseSafeString(fields[6])
    row.name = parseSafeString(fields[7])
    firstNameLastName = parseName(fields[7])
    row.firstname = firstNameLastName[0]
    row.lastname = firstNameLastName[1]
    row.city = parseSafeString(fields[8])
    row.state = parseSafeString(fields[9])
    row.zip = parseSafeString(fields[10])
    row.employer = parseSafeString(fields[11])
    row.transactionDate = parseDate(fields[13])
    row.transactionAmount = Decimal(fields[14])
    row.transactionId = parseSafeString(fields[16])
    row.fecRecNumber = parseSafeString(fields[20])
    row.originalRow = delimitedLine
    return row

def parseDate(dateString: str | None) -> date:
    if dateString is None:
        return date.min
    if len(dateString.strip()) != 8:
        return date.min
    month = dateString[0] + dateString[1]
    day = dateString[2] + dateString[3]
    year = dateString[4] + dateString[5] + dateString[6] + dateString[7]
    newDate = date(int(year), int(month), int(day))
    return newDate

def parseSafeString(safeString: str) -> str:
    if safeString is None:
        safeString = ''
    return safeString.strip().upper()

def parseName(nameString: str) -> tuple[str, str]:
    nameParts = parseSafeString(nameString).split(',')
    if nameParts.__len__() == 2:
        lastname = nameParts[0].strip()
        firstname = nameParts[1].strip()
        return (firstname, lastname)
    else:
        return ('','')

def passesCriteria(row:DonorInfo) -> bool:
    includeRow = False
    if row.state == 'CA':
        includeRow = True
    return includeRow

def processFile(filePath) -> defaultdict:
    d = defaultdict(list)
    fileHandle = open(filePath, 'r')
    for line in fileHandle:
        row = mapRowToClass(line)
        if passesCriteria(row):
            rowKey = row.rowkey
            d[rowKey].append(row)
    fileHandle.close()
    # return rows
    return d

DONATION_THRESHOLD = 20
INPUT_FILE = 'itcont2023-2024.txt'
OUTPUT_FILE = f'outliers_{str(uuid.uuid4())}.txt'

myDict = processFile(INPUT_FILE)
sortedMultipleDonorsList: list = list()
donorCount = 0

for i in myDict:
    dictList = list(myDict[i])
    if len(dictList) >= DONATION_THRESHOLD:
        donorCount += 1
        for row in dictList:
            sortedMultipleDonorsList.append(row)

s = ''
f = open(OUTPUT_FILE, 'w')
f.write(f'Found {donorCount} donors with at least {DONATION_THRESHOLD} donations to ActBlue!\n')
f.write('\n')
f.write(f'{"FEC Record Number".ljust(19)} {"Name".ljust(200)} {"City".ljust(30)} State {"Zip".ljust(9)} {"Transaction Id".ljust(32)} Transaction Date Transaction Amount\n')
f.write(f'{s.ljust(19, "-")} {s.ljust(200, "-")} {s.ljust(30, "-")} {s.ljust(5, "-")} {s.ljust(9, "-")} {s.ljust(32, "-")} {s.ljust(16, "-")} {s.ljust(18, "-")}\n')
for row in sortedMultipleDonorsList:
    output = f'{row.fecRecNumber.ljust(19)} {row.name.ljust(200)} {row.city.ljust(30)} {row.state.ljust(5)} {row.zip.ljust(9)} {row.transactionId.ljust(32)} {str(row.transactionDate).ljust(16)} {row.transactionAmount}\n'
    f.write(output)
f.close()
