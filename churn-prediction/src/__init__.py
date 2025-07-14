

import sys
import os
# Add the root folder of the project to the Python path
sys.path.append(os.path.abspath(".."))

from src.data_processing import download_dataset_kaggle
from src.useful_functions import generate_clean_requirements

packages = [
            "pandas", "numpy", "matplotlib", "seaborn", "scikit-learn",
            "xgboost", "lightgbm", "plotly", "missingno", "shap",
            "kagglehub", "lime", "streamlit", "gradio"
        ]
generate_clean_requirements()
