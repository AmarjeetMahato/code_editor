import subprocess
import sys
import tempfile
import uuid
import os

def execute_code(code: str, input_data: str) -> dict:
    try:
        temp_code_file = os.path.join(tempfile.gettempdir(), f"{uuid.uuid4()}.py")

        # Write user code to a temp file
        with open(temp_code_file, "w") as f:
            f.write(code)

        # Run the code
        result = subprocess.run(
            [sys.executable, temp_code_file],
            input=input_data.encode(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=5
        )

        output = result.stdout.decode() + result.stderr.decode()

        return {
            "output": str(output),
        }

    except subprocess.TimeoutExpired:
        return {"output": "⛔ Code execution timed out! Possible infinite loop or long-running process.", "image": None}

    except Exception as e:
        return {"output": f"❌ Runtime error: {str(e)}", "image": None}
