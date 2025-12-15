from datasets import load_dataset

try:
    # Load the dataset
    dataset = load_dataset("JailbreakBench/JBB-Behaviors", "behaviors")

    # Print the available splits
    print("\nAvailable Splits:")
    print(list(dataset.keys()))

    # Print the dataset features
    print("\nDataset Features:")
    print(dataset["harmful"].features)

    # Print a few examples from the 'harmful' split
    print("\nDataset Examples (Harmful):")
    for i in range(3):
        print(dataset["harmful"][i])

    # Print a few examples from the 'benign' split
    print("\nDataset Examples (Benign):")
    for i in range(3):
        print(dataset["benign"][i])

except Exception as e:
    print(f"An error occurred: {e}")