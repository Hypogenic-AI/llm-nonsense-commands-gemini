
from datasets import load_dataset
import os

try:
    # Create the directory if it doesn't exist
    os.makedirs("datasets/JailbreakBench_JBB-Behaviors", exist_ok=True)

    # Load the dataset
    dataset = load_dataset("JailbreakBench/JBB-Behaviors", "behaviors")

    # Save the dataset to disk
    dataset.save_to_disk("datasets/JailbreakBench_JBB-Behaviors")

    print("Dataset saved successfully.")

except Exception as e:
    print(f"An error occurred: {e}")
