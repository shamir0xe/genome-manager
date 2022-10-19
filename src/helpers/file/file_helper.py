import os


class FileHelper:
    @staticmethod
    def dir_exists(path: str) -> bool:
        return os.path.exists(path)

    @staticmethod
    def make_directories(path: str) -> None:
        os.makedirs(path)
    
    @staticmethod
    def file_exists(path: str) -> bool:
        return os.path.isfile(path)
