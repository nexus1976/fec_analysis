from datetime import date
from decimal import Decimal
from collections import defaultdict

class DonorInfo():
    def __init__(self):
        self._name:str = ''
        self._firstname:str = ''
        self._lastname:str = ''
        self._city:str = ''
        self._state:str = ''
        self._zip:str = ''
        self._employer:str = ''
        self._transactionDate:date = date.min
        self._transactionAmount:Decimal = 0.00
        self._rowkey = None

    @property
    def name(self) -> str:
        return self._name
    @name.setter
    def name(self, value:str):
        if value != self._name:
            self._name = value
            self._rowkey = None

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
    def rowkey(self):
        if self._rowkey is None:
            self._rowkey = f'{self.name}{self.city}{self.state}{self.zip}'
        return self._rowkey

def mapRowToClass(delimitedLine: str) -> DonorInfo:
    row = DonorInfo()
    fields = delimitedLine.split('|')
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

def processFile(filePath) -> defaultdict:
    d = defaultdict(list)
    fileHandle = open(filePath, 'r')
    for line in fileHandle:
        row = mapRowToClass(line)
        rowKey = row.rowkey
        d[rowKey].append(row)
    fileHandle.close()
    # return rows
    return d

myDict = processFile('itcont2023-2024.txt')
