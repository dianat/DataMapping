
from TurtleStatement import TurtleStatement
from xlrd import open_workbook

# Open Excel Spreadsheet
wb = open_workbook('data/excel2skos.xlsx')

# By adding the name of a specific sheet in the workbook as an item of the list below, 
# the script will not read its content and move to the next sheet like in the example
# wb_sheet_list_to_ignore = ['Sheet2','Sheet3'];
wb_sheet_list_to_ignore = []
items = []

for sheet in wb.sheets():
    if sheet.name not in wb_sheet_list_to_ignore:
        number_of_rows = sheet.nrows
        number_of_columns = sheet.ncols   
        
        rows = []

        # Set header of the sheet -- assuming it is the first row when set to 0
        skos_predicates_row = 6
        skos_predicates = []
        for col in range(number_of_columns):
            skos_relation  = (sheet.cell(skos_predicates_row,col).value)
            if not skos_relation:
                skos_relation = ''
            skos_predicates.append(skos_relation)

        # Read rows starting from header_row+offset
        offset = 1
        for row in range(skos_predicates_row+offset, number_of_rows):
            values = []
            for col in range(number_of_columns):
                value  = (sheet.cell(row,col).value)
                try:
                    value = str(int(value))
                except ValueError:
                    pass
                finally:
                    values.append(value)
            item = TurtleStatement(skos_predicates,values)
            items.append(item)



# Creating an empty output file
xml = open('output.ttl','w',encoding='utf-8')
xml.close()

# Writing into the .xml file
xml = open('output.ttl','a',encoding='utf-8')
xml.write('')
xml.write('')

#for item in items:
#    xml.write(str(item))

xml.write('')
xml.close()