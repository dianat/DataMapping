import re

def count(sequence, item):
    return sum([1 for elem in sequence if elem == item])

def enclose(string):
    if string.find('http://') > -1:
        return '<'+string.strip()+'>'
    else:
        return langString(string)

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

def mapEnclose(string):
    if count(re.split('[:// ,]',string),'http') > 1:
        return ', '.join(map(enclose,string.split(',')))
    else:
        return enclose(string)

def processString(string):
    string = escapeAmpersandCharacter(string)
    string = toUnicode(string)
    return string

def langString(string):
    if string.find('@') > 0:
        string = string.replace('@','"@')
    else:
        string = string + '"'
    return '"' + string.encode('utf-8')

def generateXMLTagName(string):
    string = toUnicode(string)
    string = escapeBracketCharacter(string)
    string = escapeApostropheCharacter(string)
    string = escapeForwardSlashCharacter(string)
    return (string.lower()).replace(' ','_')

def toUnicode(string):
    return string.encode('utf-8').strip()
