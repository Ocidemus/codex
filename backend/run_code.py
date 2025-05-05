import subprocess
import os
from flask import jsonify

TEMP_DIR = "temp"
os.makedirs(TEMP_DIR, exist_ok=True)

def execute_code(language, code):
    file_path = ""
    command = ""
    output_file = ""

    try:
        if language == "Python":
            file_path = os.path.join(TEMP_DIR, "script.py")
            with open(file_path, "w") as f:
                f.write(code)
            command = ["python", file_path]

        elif language == "Javascript":
            file_path = os.path.join(TEMP_DIR, "script.js")
            with open(file_path, "w") as f:
                f.write(code)
            command = ["node", file_path]

        elif language == "C":
            file_path = os.path.join(TEMP_DIR, "program.c")
            output_file = os.path.join(TEMP_DIR, "program.exe")
            with open(file_path, "w") as f:
                f.write(code)
            compile_command = ["gcc", file_path, "-o", output_file]
            subprocess.run(compile_command, capture_output=True, text=True)
            command = [output_file]

        elif language == "cpp":
            file_path = os.path.join(TEMP_DIR, "program.cpp")
            output_file = os.path.join(TEMP_DIR, "program.exe")
            with open(file_path, "w") as f:
                f.write(code)
            compile_command = ["g++", file_path, "-o", output_file]
            subprocess.run(compile_command, capture_output=True, text=True)
            command = [output_file]

        else:
            return jsonify({"output": "Unsupported language"})

        result = subprocess.run(command, capture_output=True, text=True, timeout=5)
        output = result.stdout if result.stdout else result.stderr

        # Cleanup
        os.remove(file_path)
        if output_file and os.path.exists(output_file):
            os.remove(output_file)

        return jsonify({"output": output})

    except Exception as e:
        return jsonify({"output": f"Execution error: {str(e)}"})
