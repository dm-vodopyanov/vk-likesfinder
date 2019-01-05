class HtmlReportException(Exception):
    pass


class HtmlReport:
    def __init__(self):
        self.path = None
        self.file = None
        self.header = None
        self.start_time = None

    def set_path(self, path):
        self.path = path

    def initialize_file(self, path):
        self.file = open(path, 'w', encoding='utf-8', buffering=1)

    def write(self, string):
        if not self.file:
            raise HtmlReportException('HTML report is not initialized')
        self.file.write(string.encode('utf-8').decode('utf-8', errors='ignore'))

    def close_file(self):
        if self.file:
            self.write('</body></html>\n')
            self.file.close()
