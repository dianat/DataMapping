import string_utilities as su

class TurtleStatement(object):
    def __init__(self, skos_predicates, values = None):  
        self.ttl_object = ''
        self.subject = ''
        self.predicates = ''
        for col in range(0,len(skos_predicates)):  
            if skos_predicates[col] == 'URI':
                if values[col].find('http://') > 0:
                    self.subject = su.enclose(values[col])
                else:
                    self.subject = values[col]
            else:
                if values[col]!= '':
                    self.predicates = ''.join([self.predicates,
                                        '\t\t',
                                        skos_predicates[col],
                                        ' ',
                                        su.mapEnclose(values[col]),
                                        ';\n'])
        self.predicates = self.predicates[:-2]+'.\n'
        self.ttl_object = ''.join([self.subject,' ', self.predicates])  

    def get_subject(self):
        return self.subject

    def __str__(self):
        return self.ttl_object.encode('UTF-8')