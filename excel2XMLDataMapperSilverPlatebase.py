# -*- coding: utf-8 -*-
# http://xlrd.readthedocs.io/en/latest/api.html#xlrd-sheet
from xlrd import open_workbook
import dms2wgs84 as latlong

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

def processStringByType(string, data_type):
    # Geo Reference
    if data_type == 'Geo reference' and string != '':
        dms = toUnicode(string)
        dms = dms.split(',')
        print dms[0]
        return ''.join(['\t\t\t\t<latitude>',str(latlong.wgs84(dms[0])),'</latitude>\n',
                       '\t\t\t\t<longitude>',str(latlong.wgs84(dms[1])),'</longitude>\n'])
    
    # Date Formatting

    # Dimension with Measurement Unit

    return processString(string)

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
                                    processStringByType(self.values[col],header[col]),
                                    '</',
                                    generateXMLTagName(header[col]),
                                    '>\n'])

        self.xml_object = self.xml_object + '</object>\n'

    def __str__(self):
        return self.xml_object


# Open Excel Spreadsheet
wb = open_workbook('data/SP_rawdata_master.xlsx')

# By adding the name of a specific sheet in the workbook as an item of the list below, 
# the script will not read its content and move to the next sheet like in the example
# wb_sheet_list_to_ignore = ['Sheet2','Sheet3'];
wb_sheet_list_to_ignore = ['RE - 200-300','RE - 300-400','Sasanian','Byzantine']
#wb_sheet_list_to_ignore = ['Provenance']

items = []

for sheet in wb.sheets():
    if sheet.name not in wb_sheet_list_to_ignore:
        number_of_rows = sheet.nrows
        number_of_columns = sheet.ncols

        rows = []

        # Set header of the sheet -- assuming it is the first row when set to 0
        header_row = 0
        header = []

        units_row = 1
        units = []

        for col in range(number_of_columns):
            header_item  = (sheet.cell(header_row,col).value)
            if not header_item:
                header_item = 'NoHeader'
            header.append(header_item)

            # 

        # Read rows starting from header_row+offset
        offset = 3
        for row in range(header_row+offset, number_of_rows):
            values = []
            for col in range(number_of_columns):
                print sheet.cell(row,col)
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
output = 'data/provenance.xml'
xml = open(output,'w')
xml.close()

# Writing into the .xml file
xml = open(output,'a')
xml.write('<?xml version="1.0" encoding="UTF-8"?>\n')
xml.write('<objects>\n')

for item in items:
    xml.write(str(item))

xml.write('</objects>\n')
xml.close()
