import subprocess
import os


def generate_requirements(output_path=None):
    """
    Generates a requirements.txt file listing all packages in the current environment.

    Parameters:
        output_path (str, optional): Custom path to save the requirements file.
                                     If None, saves it in the project root directory.
    """
    try:
        # If no output_path is given, default to project root: one level above /src
        current_file = os.path.abspath(__file__)
        project_root = os.path.dirname(os.path.dirname(current_file))
        if output_path is None:
            output_path = os.path.join(project_root, "requirements.txt")

        with open(output_path, "w") as f:
            subprocess.run(["pip", "freeze"], stdout=f, check=True)

        print(f"✅ requirements.txt successfully created at: {output_path}")

    except Exception as e:
        # This block was missing or not indented!
        print(f"❌ Error creating requirements.txt: {e}")
