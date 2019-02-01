MAX_CONSOLE_LINE_LENGTH = 79


class CliReport:
    def __init__(self):
        self.is_initialized = False

    def print(self, string='', length=MAX_CONSOLE_LINE_LENGTH, end='\n'):
        if self.is_initialized:
            number_of_spaces = 0
            if length > len(string):
                number_of_spaces = length - len(string)
            print((string + ' ' * number_of_spaces).encode('cp866', errors='ignore').decode('cp866').encode(
                'cp1251', errors='ignore').decode('cp1251'), end=end)
