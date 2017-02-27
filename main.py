from xlrd import open_workbook

def toUnicode(string):
    return string.encode('utf-8').strip()

def escapeAmpersandCharacter(string):
    return string.replace('&','&amp;')

def escapeBracketCharacter(string):
    string = string.replace('(','')
    string = string.replace(')', '')
    return string

def escapeApostropheCharacter(string):
    return string.replace('\'','_')

def escapeForwardSlashCharacter(string):
    return string.replace('/','_')

def processString(string):
    string = escapeAmpersandCharacter(string)
    string = toUnicode(string)
    return string

def generateXMLTagName(string):
    string = toUnicode(string)
    string = escapeBracketCharacter(string)
    string = escapeApostropheCharacter(string)
    string = escapeForwardSlashCharacter(string)
    return (string.lower()).replace(' ','_')

class XMLObject(object):
    def __init__(self, header, values = None):  
        self.xml_object = '<object>\n'
        self.values = values
        for col in range(0,len(header)):
            if (header[col] != 'NoHeader'):
                self.xml_object = ''.join([self.xml_object,
                                    '\t\t<',
                                    generateXMLTagName(header[col]),
                                    '>',
                                    processString(self.values[col]),
                                    '</',
                                    generateXMLTagName(header[col]),
                                    '>\n'])
            
        self.xml_object = self.xml_object + '</object>\n'

    def __str__(self):
        return self.xml_object

# Open Excel Spreadsheet
wb = open_workbook('AR_Platebase_sample.xlsx')

items = []

for sheet in wb.sheets():
    number_of_rows = sheet.nrows
    number_of_columns = sheet.ncols   
    
    rows = []

    # Set header of the sheet -- assuming it is the first row when set to 0
    header_row = 0
    header = []
    for col in range(number_of_columns):
        header_item  = (sheet.cell(header_row,col).value)
        if not header_item:
            header_item = 'NoHeader'
        header.append(header_item)

    # Read rows starting from header_row+offset
    offset = 2
    for row in range(header_row+offset, number_of_rows):
        values = []
        for col in range(number_of_columns):
            value  = (sheet.cell(row,col).value)
            try:
                value = str(int(value))
            except ValueError:
                pass
            finally:
                values.append(value)
        item = XMLObject(header,values)
        items.append(item)



# Creating an empty output file
xml = open('output.xml','w')
xml.close()

# Writing into the .xml file
xml = open('output.xml','a')
xml.write('<?xml version="1.0" encoding="UTF-8"?>\n')
xml.write('<objects>\n')

for item in items:
    xml.write(str(item))

xml.write('</objects>\n')
xml.close()