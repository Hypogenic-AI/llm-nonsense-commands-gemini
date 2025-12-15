
import google.generativeai as genai
import os
import json
import logging

# --- Configuration ---
GEMINI_API_KEY = "your_gemini_api_key"
MODEL_NAME = "gemini-1.5-flash-latest"
OUTPUT_FILE = "experiment_results.json"
NONSENSE_PROMPT_FILE = "nonsense_prompt.txt"
CONTROL_PROMPT = "Write a four-line poem about a robot feeling sad."

# --- Setup Logging ---
logger = logging.getLogger("ExplanationRunner")
logger.setLevel(logging.INFO)
if not logger.handlers:
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter('%(levelname)s - %(message)s')
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

def get_gemini_response(prompt):
    """
    Sends a prompt to the Gemini API and returns the response.
    """
    try:
        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        logger.error(f"Error calling Gemini API: {e}")
        # In case of API error, return an error message instead of crashing.
        return f"[API Error: {e}]"

def run_experiment():
    """
    Main logic for running the explanation experiment.
    """
    if not GEMINI_API_KEY:
        logger.error("FATAL: GEMINI_API_KEY environment variable not set.")
        return

    genai.configure(api_key=GEMINI_API_KEY)

    logger.info("--- Starting Explanation Experiment ---")

    # 1. Load the generated nonsense prompt
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

    # 2. Process the nonsense prompt
    logger.info("--- Processing Nonsense Case ---")
    results["nonsense_case"]["prompt"] = nonsense_prompt
    logger.info("Getting initial output for nonsense prompt...")
    nonsense_output = get_gemini_response(nonsense_prompt)
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
    nonsense_explanation = get_gemini_response(explanation_meta_prompt_nonsense)
    results["nonsense_case"]["explanation"] = nonsense_explanation
    logger.info("Explanation for nonsense case received.")

    # 3. Process the control prompt
    logger.info("--- Processing Control Case ---")
    results["control_case"]["prompt"] = CONTROL_PROMPT
    logger.info("Getting initial output for control prompt...")
    control_output = get_gemini_response(CONTROL_PROMPT)
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
    control_explanation = get_gemini_response(explanation_meta_prompt_control)
    results["control_case"]["explanation"] = control_explanation
    logger.info("Explanation for control case received.")

    # 4. Save results to file
    logger.info(f"--- Saving results to {OUTPUT_FILE} ---")
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(results, f, indent=4)
    logger.info("Experiment complete.")

if __name__ == '__main__':
    run_experiment()
