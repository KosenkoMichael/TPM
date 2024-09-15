import json


class Functional:
    def __init__(self):
        pass

    def read_file(file_path: str) -> str:
        """get file data
        Args:
            file_path: path to file
        Returns:
            file data
        """
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                data = file.read()
            return data
        except Exception as error:
            print(error)

    def read_file_bytes(file_path: str) -> str:
        """get file data
        Args:
            file_path: path to file
        Returns:
            file data
        """
        try:
            with open(file_path, "rb") as file:
                data = file.read()
            return data
        except Exception as error:
            print(error)

    def write_file(
        file_path: str,
        data: str,
    ) -> None:
        """write data to file
        Args:
            file_path: path to file
            data: data we need to write
        """
        try:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(data)
        except Exception as error:
            print(error)

    def write_file_bytes(
        file_path: str,
        data: str,
    ) -> None:
        """write data to file
        Args:
            file_path: path to file
            data: data we need to write
        """
        try:
            with open(file_path, "wb") as file:
                file.write(data)
        except Exception as error:
            print(error)

    def read_json(path: str) -> dict:
        """get data from json file
        Args:
            path: path to json file
        Returns:
            file data
        """
        with open(path, "r", encoding="UTF-8") as file:
            return json.load(file)
 