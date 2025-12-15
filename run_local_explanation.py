
import json
import logging
import os
import sys

# --- Add AutoDAN-Turbo to path ---
autodan_dir = os.path.abspath('code/AutoDAN-Turbo')
if autodan_dir not in sys.path:
    sys.path.append(autodan_dir)

from llm import HuggingFaceModel
from framework.target import Target

# --- Configuration ---
# Re-using the same local model from the generation step
HF_TOKEN = "your_hf_token" # From previous step
CACHE_DIR = "./hf_cache"
MODEL_REPO = "gpt2"
MODEL_CONFIG_NAME = "gpt2" # Unused, but for consistency
CHAT_CONFIG_DIR = "./code/AutoDAN-Turbo/llm/chat_templates" # Unused, but for consistency

OUTPUT_FILE = "experiment_results.json"
NONSENSE_PROMPT_FILE = "nonsense_prompt.txt"
CONTROL_PROMPT = "Write a four-line poem about a robot feeling sad."

# --- Setup Logging ---
logger = logging.getLogger("LocalExplanationRunner")
logger.setLevel(logging.INFO)
if not logger.handlers:
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter('%(levelname)s - %(message)s')
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

def run_local_experiment():
    """
    Main logic for running the explanation experiment using a local model.
    """
    logger.info("--- Starting Local Explanation Experiment ---")

    # 1. Load the local model
    logger.info(f"Loading model: {MODEL_REPO}")
    model = HuggingFaceModel(
        MODEL_REPO,
        CHAT_CONFIG_DIR,
        MODEL_CONFIG_NAME,
        token=HF_TOKEN,
        cache_dir=CACHE_DIR
    )
    # The Target class is a convenient wrapper for the model.generate call
    target = Target(model)

    # 2. Load the generated nonsense prompt
    try:
        with open(NONSENSE_PROMPT_FILE, 'r') as f:
            nonsense_prompt = f.read().strip()
        logger.info(f"Successfully loaded nonsense prompt: '{nonsense_prompt}'")
    except FileNotFoundError:
        logger.error(f"FATAL: The nonsense prompt file '{NONSENSE_PROMPT_FILE}' was not found. Please run generate_nonsense.py first.")
        return

    results = {
        "nonsense_case": {},
        "control_case": {}
    }

    # 3. Process the nonsense prompt
    logger.info("--- Processing Nonsense Case ---")
    results["nonsense_case"]["prompt"] = nonsense_prompt
    logger.info("Getting initial output for nonsense prompt...")
    nonsense_output = target.respond(nonsense_prompt, max_length=100) # Keep max_length reasonable
    results["nonsense_case"]["output"] = nonsense_output
    logger.info(f"Initial nonsense output received: '{nonsense_output[:200]}...'")

    explanation_meta_prompt_nonsense = f"""The following is a prompt given to a large language model: 
---
{nonsense_prompt}
---

The model produced this output:
---
{nonsense_output}
---

Please explain, in detail, what the original prompt is asking the model to do and why it might have produced this specific output. Analyze the prompt's structure, language, and potential meaning."""
    
    logger.info("Getting explanation for nonsense case...")
    # Use the base model's generate method directly for the explanation
    nonsense_explanation = model.generate("You are an expert in analyzing LLM prompts.", explanation_meta_prompt_nonsense, max_length=300)
    results["nonsense_case"]["explanation"] = nonsense_explanation
    logger.info("Explanation for nonsense case received.")

    # 4. Process the control prompt
    logger.info("--- Processing Control Case ---")
    results["control_case"]["prompt"] = CONTROL_PROMPT
    logger.info("Getting initial output for control prompt...")
    control_output = target.respond(CONTROL_PROMPT, max_length=100)
    results["control_case"]["output"] = control_output
    logger.info(f"Initial control output received: '{control_output[:200]}...'")

    explanation_meta_prompt_control = f"""The following is a prompt given to a large language model: 
---
{CONTROL_PROMPT}
---

The model produced this output:
---
{control_output}
---

Please explain, in detail, what the original prompt is asking the model to do and why it might have produced this specific output. Analyze the prompt's structure, language, and potential meaning."""

    logger.info("Getting explanation for control case...")
    control_explanation = model.generate("You are an expert in analyzing LLM prompts.", explanation_meta_prompt_control, max_length=300)
    results["control_case"]["explanation"] = control_explanation
    logger.info("Explanation for control case received.")

    # 5. Save results to file
    logger.info(f"--- Saving results to {OUTPUT_FILE} ---")
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(results, f, indent=4)
    logger.info("Experiment complete.")

if __name__ == '__main__':
    run_local_experiment()
