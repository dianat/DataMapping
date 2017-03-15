# DataMapping
Utility scripts for converting data to XML or TTL format

Run the scripts with Python 2.7 

**Input:** An Excel file to convert to XML with tagnames based on the header row of the xml file

**Output:** A .xml file; Edit the input and output file paths before running the script.

```
python excel2XMLDataMapper.py
```

**Input:** An excel file to convert to ttl format with a section describing the concept scheme and 
           a separate section describing the concepts in the vocabulary.


| ConceptScheme URI   |      http://www.example.org/vocabulary/size                             |                 |
|---------------------|:-----------------------------------------------------------------------:|----------------:|
| dct:title           |  japanese size                                                          |                 |
| URI                 |  skos:prefLabel                                                         | skos:definition |
| :large              |  "large format"@en                                                      | Japanese print  |

**Output:** A .ttl file; Edit the input and output file paths before running the script.

```
python excel2TTLDataMapper.py
```
