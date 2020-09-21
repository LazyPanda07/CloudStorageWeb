class FileData:
    file_name = None
    file_path = None
    file_extension = None
    upload_date = None
    date_of_change = None
    file_size = None

    def __init__(self, file_name: str, file_path: str, file_extension: str, upload_date: str, date_of_change: str, file_size: int):
        self.file_name = file_name
        self.file_path = file_path
        self.file_extension = file_extension
        self.upload_date = upload_date
        self.date_of_change = date_of_change
        self.file_size = file_size
