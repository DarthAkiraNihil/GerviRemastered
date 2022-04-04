from configparser import ConfigParser
import codecs

class GIDEConfig:
    def __init__(self, file):
        self.config = ConfigParser()
        self.config.read_file(codecs.open(file, "r", "utf8"))
        self.path = file
    
    def setOption(self, section, parameter, value):
        self.config.set(section, parameter, value)

    def setOptions(self, sections, parameters, values):
        for i in range(len(sections)):
            #if values[i] != 'PREVIOUS':
            self.config.set(sections[i], parameters[i], values[i])#.decode('utf-8'))

    def update(self):
        with open(self.path, 'w', encoding='utf8') as fout:
            self.config.write(fout)

    def extract(self):
        out = {}
        for section in self.config.sections():
            opt = {}
            for value in self.config.options(section):
                opt[value] = self.config.get(section, value)
                opt[value] = opt[value]#.decode('utf-8')
            out[section] = opt
        return out


