import pyperclip
import subprocess

class DataGatherer:
    @staticmethod
    def get_clipboard_content():
        try:
            return pyperclip.paste()
        except:
            return "Error: Unable to access clipboard"

    @staticmethod
    def get_file_content(file_path):
        try:
            with open(file_path, 'r') as file:
                return file.read()
        except Exception as e:
            return f"Error reading file: {str(e)}"

    @staticmethod
    def execute_command(command):
        try:
            result = subprocess.run(command, capture_output=True, text=True, shell=True)
            return result.stdout if result.returncode == 0 else f"Error: {result.stderr}"
        except Exception as e:
            return f"Error executing command: {str(e)}"