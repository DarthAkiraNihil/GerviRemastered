class Parser:
    def parse(self, string):
        """
        Returns a dictionary which has a structure like this:
            - com
            - arg1
            - arg2
            ...
            -argN
        """
        parsedString = {}
        strArr = string.split()
        parsedString['com'] = strArr[0]
        for i in range(1, len(strArr)):
            parsedString[f'arg{i}'] = strArr[i]
        return parsedString
