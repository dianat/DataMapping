import string_utilities as su
from TurtleStatement import TurtleStatement
from xlrd import open_workbook

# Open Excel Spreadsheet
wb = open_workbook('data/Japanese_format_impression_SKOS_vocab.xlsx')

# Specifying the concept scheme definition section
concept_scheme_sheet = wb.sheet_by_name('Sheet1')

# modify the range to include all rows describing the concept scheme
concept_sheme_rows = 3
concept_scheme_tuple = ''
concept_scheme_URI = ''

for row in range(3):
    predicate = (concept_scheme_sheet.cell(row,0).value)
    value = (concept_scheme_sheet.cell(row,1).value)
    
    if predicate.find('ConceptScheme URI')==0:
        concept_scheme_URI = su.enclose(value)
        concept_scheme_tuple = ''.join([concept_scheme_URI, ' ',
                                    'rdf:type ',
                                    'skos:ConceptScheme .\n'])
    else:  
        concept_scheme_tuple = ''.join([concept_scheme_tuple, concept_scheme_URI, ' ',predicate,' ',su.langString(value),'.\n'])

print concept_scheme_tuple

# By adding the name of a specific sheet in the workbook as an item of the list below, 
# the script will not read its content and move to the next sheet like in the example
# wb_sheet_list_to_ignore = ['Sheet2','Sheet3'];
wb_sheet_list_to_ignore = ['Sheet2','Sheet3']
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

prefixes = ''.join(['@prefix owl: <http://www.w3.org/2002/07/owl#> .\n',
            '@prefix lexvo: <http://lexvo.org/id/iso639-3/> .\n',
            '@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .\n'
            '@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n',
            '@prefix skos: <http://www.w3.org/2004/02/skos/core#> .\n',
            '@prefix dct: <http://purl.org/dc/terms/> .\n'])


# Add conceptscheme URI
prefixes = ''.join(['@prefix : <',concept_scheme_URI,'/> .\n',
                    concept_scheme_tuple,'\n'])

# Creating an empty output file
xml = open('data/output.ttl','w')
xml.close()

# Writing into the .xml file
xml = open('data/output.ttl','a')
xml.write(prefixes)

for item in items:
    xml.write(''.join([item.get_subject(),' skos:inScheme ',concept_scheme_URI,'.\n']))
    xml.write(str(item))

xml.close()