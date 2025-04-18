import subprocess
import os


def generate_clean_requirements(packages=None, output_path=None):
    """
    Generates a clean requirements.txt with only selected packages.

    Parameters:
        packages (list): List of package names to include.
        output_path (str): Where to save the requirements.txt file.
                           If None, it saves it to the root of the project.
    """
    if packages is None:
        packages = [
            "pandas", "numpy", "matplotlib", "seaborn", "scikit-learn",
            "xgboost", "lightgbm", "plotly", "missingno", "shap",
            "kagglehub", "lime", "streamlit", "gradio"
        ]

    try:
        # Detect root folder of project
        current_file = os.path.abspath(__file__)
        project_root = os.path.dirname(os.path.dirname(current_file))

        # Set default path if none provided
        if output_path is None:
            output_path = os.path.join(project_root, "requirements.txt")

        # Run pip freeze
        result = subprocess.run(["pip", "freeze"], capture_output=True, text=True)
        installed = result.stdout.splitlines()

        # Filter only relevant packages
        filtered = [pkg for pkg in installed if any(p in pkg.lower() for p in packages)]

        # Write the output
        with open(output_path, "w") as f:
            f.write("\n".join(filtered))

        print(f"✅ Clean requirements.txt created at: {output_path}")

    except Exception as e:
        print(f"❌ Error creating requirements.txt: {e}")