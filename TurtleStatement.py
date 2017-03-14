import string_utilities as su

class TurtleStatement:
    def __init__(self, skos_predicates, values = None):  
        self.ttl_object = ''
        self.subject = ''
        self.predicates = ''
        for col in range(0,len(skos_predicates)):  
            if skos_predicates[col] == 'URI':
                self.subject = su.mapEnclose(values[col])
            else:
                self.predicates = ''.join([self.predicates,
                                    '\t\t',
                                    skos_predicates[col],
                                    ' ',
                                    su.mapEnclose(values[col]),
                                    ';\n'])
        self.predicates = self.predicates[:-2]+'.'
        self.ttl_object = ''.join([self.subject,' ', self.predicates])  
        print self.predicates #ttl_object

    def __str__(self):
        return self.ttl_object