import os
import logging
from typing import List

# Constants
SOUND_FILES_COUNT = 4
REPLACEMENTS = {
    "FLATRIGHT": {"old": "flat_right", "new": "max_right", "display": "Max Right"},
    "FLATLEFT": {"old": "flat_left", "new": "max_left", "display": "Max Left"},
}


def setup_logging():
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )


def get_folder_paths(root_folder: str) -> tuple[str, str]:
    """Returns paths for descriptive.ini and strings.ini"""
    descriptive_path = os.path.join(
        root_folder,
        "plugins",
        "pacenote",
        "config",
        "pacenotes",
        "packages",
        "corners",
        "Descriptive.ini",
    )
    strings_path = os.path.join(
        root_folder,
        "plugins",
        "Pacenote",
        "language",
        "english",
        "pacenotes",
        "packages",
        "corners",
        "strings.ini",
    )
    logging.info(f"Found Descriptive.ini path: {descriptive_path}")
    logging.info(f"Found strings.ini path: {strings_path}")
    return descriptive_path, strings_path


def update_descriptive_file(path: str) -> None:
    """Updates the Descriptive.ini file"""
    try:
        with open(path, "r") as file:
            content = file.readlines()
            logging.info(f"Successfully opened {path}")

        changes_made = 0
        for i, line in enumerate(content):
            for section in REPLACEMENTS:
                if f"[PACENOTE::{section}]" in line:
                    logging.info(f"Found section {section} at line {i+1}")
                    for j in range(SOUND_FILES_COUNT):
                        snd_line_index = i + 3 + j
                        if REPLACEMENTS[section]["old"] in content[snd_line_index]:
                            old_line = content[snd_line_index]
                            content[snd_line_index] = content[snd_line_index].replace(
                                REPLACEMENTS[section]["old"],
                                REPLACEMENTS[section]["new"],
                            )
                            changes_made += 1
                            logging.info(
                                f"Line {snd_line_index+1}: '{old_line.strip()}' -> '{content[snd_line_index].strip()}'"
                            )

        with open(path, "w") as file:
            file.writelines(content)
        logging.info(f"Successfully updated {path} with {changes_made} changes")
    except FileNotFoundError:
        logging.error(f"Could not find file: {path}")
    except Exception as e:
        logging.error(f"Error processing {path}: {str(e)}")


def update_strings_file(path: str) -> None:
    """Updates the strings.ini file"""
    try:
        with open(path, "r") as file:
            content = file.readlines()
            logging.info(f"Successfully opened {path}")

        changes_made = 0
        found = {section: False for section in REPLACEMENTS}
        for i, line in enumerate(content):
            for section in REPLACEMENTS:
                if f"{section}=" in line:
                    new_line = f"{section}={REPLACEMENTS[section]['display']}\n"
                    if content[i] != new_line:
                        old_line = line
                        content[i] = new_line
                        changes_made += 1
                        logging.info(
                            f"Line {i+1}: '{old_line.strip()}' -> '{content[i].strip()}'"
                        )
                    found[section] = True

        for section, was_found in found.items():
            if not was_found:
                logging.warning(f"Could not find {section} in strings.ini")

        with open(path, "w") as file:
            file.writelines(content)
        logging.info(f"Successfully updated {path} with {changes_made} changes")
    except FileNotFoundError:
        logging.error(f"Could not find file: {path}")
    except Exception as e:
        logging.error(f"Error processing {path}: {str(e)}")


def main():
    setup_logging()

    drive = input("Please enter the drive letter (e.g. C): ").upper()
    folder = input("Please enter the folder path (e.g. Richard Burns Rally): ")

    if not drive or len(drive) != 1 or not drive.isalpha():
        logging.error("Invalid drive letter")
        return

    root_folder = f"{drive}:\\{folder.strip('\\/')}"
    if not os.path.exists(root_folder):
        logging.error(f"Path does not exist: {root_folder}")
        return

    try:
        os.chdir(f"{drive}:")
        descriptive_path, strings_path = get_folder_paths(root_folder)
        update_descriptive_file(descriptive_path)
        update_strings_file(strings_path)
        logging.info("Processing completed successfully")
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    main()
