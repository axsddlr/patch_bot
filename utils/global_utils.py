import pathlib
import shutil


def news_exists(s):
    path = pathlib.Path(s)
    if path.exists():
        return
        # print("File exist")
    else:
        source = "./assets/empty_news.json"
        try:
            shutil.copy(source, s)
            print("File copied successfully.")

        # If source and destination are same
        except shutil.SameFileError:
            print("Source and destination represents the same file.")

        # If there is any permission issue
        except PermissionError:
            print("Permission denied.")

        # For other errors
        except:
            print("Error occurred while copying file.")


def matches_exists(s):
    path = pathlib.Path(s)
    if path.exists():
        return
        # print("File exist")
    else:
        source = "./assets/empty_matches.json"
        try:
            shutil.copy(source, s)
            print("File copied successfully.")

        # If source and destination are same
        except shutil.SameFileError:
            print("Source and destination represents the same file.")

        # If there is any permission issue
        except PermissionError:
            print("Permission denied.")

        # For other errors
        except:
            print("Error occurred while copying file.")
