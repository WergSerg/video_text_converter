from app.settings import TEMPORARY_FILE_NAME

class converter:
    def __init__(self, binary_string, file_name = None):
        self.binary_string = binary_string
        self.file_name = file_name
        self.type = self._get_file_format()
        self.TEMPORARY_FILE_NAME = TEMPORARY_FILE_NAME+self.type
        self._convert()

    def _get_file_format(self) -> str:
        if self.file_name is not None:
            # return self.file_name.split('.')[-1]
            return self.file_name
        else:
            # return (self.binary_string.decode(errors='ignore').split('"')[3].split('.')[1])
            return (self.binary_string.decode(errors='ignore').split('"')[3])


    def _convert(self):
        with open(self.TEMPORARY_FILE_NAME, 'wb') as ss:
            ss.write(self.binary_string)

    def get_format(self):
        return self.type

    def get_temporary_file_name(self):
        return self.TEMPORARY_FILE_NAME
