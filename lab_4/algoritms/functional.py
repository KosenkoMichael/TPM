"""
This module implements the functionality of reading/writing to a file
"""
import json
import logging


logger = logging.getLogger("functional")


class Functional:
    """
    This class contains the definition of functions for reading and writing files
    """
    def __init__( self ):
        logger.info("functional class initialize")

    def read_file( file_path: str ) -> str:
        """get file data
        Args:
            file_path: path to file
        Returns:
            file data
        """
        try:
            with open( file_path, "r", encoding = "utf-8" ) as file:
                logger.info(f"reading from {file_path}")
                data = file.read()
            
            return data
        except Exception as error:
            logger.error(f"error {error} while reading from {file_path}")

    def read_file_bytes( file_path: str ) -> str:
        """get file data
        Args:
            file_path: path to file
        Returns:
            file data
        """
        try:
            with open( file_path, "rb" ) as file:
                logger.info(f"reading(bytes) from {file_path}")
                data = file.read()
            
            return data
        except Exception as error:
            logger.error(f"error {error} while reading(bytes) from {file_path}")

    def write_file(
        file_path : str,
        data      : str,
    ) -> None:
        """write data to file
        Args:
            file_path : path to file
            data      : data we need to write
        """
        try:
            with open( file_path, "w", encoding = "utf-8" ) as file:
                logger.info(f"writing to {file_path}")
                file.write(data)
            
        except Exception as error:
            logger.error(f"error {error} while writing to {file_path}")

    def write_file_bytes(
        file_path : str,
        data      : str,
    ) -> None:
        """write data to file
        Args:
            file_path : path to file
            data      : data we need to write
        """
        try:
            with open( file_path, "wb" ) as file:
                logger.info(f"writing(bytes) to {file_path}")
                file.write(data)
            
        except Exception as error:
            logger.error(f"error {error} while writing(bytes) to {file_path}")

    def read_json(path: str) -> dict:
        """get data from json file
        Args:
            path: path to json file
        Returns:
            file data
        """
        try:
            with open( path, "r", encoding = "UTF-8" ) as file:
                logger.info(f"reading from {path}")
                return json.load(file)
        except Exception as error:
            logger.error(f"error {error} while reading from {path}")
 