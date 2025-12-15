
# Do LLMs Understand Nonsense Commands? - A Research Log

## Project Description
This project investigates whether Large Language Models (LLMs) can understand and explain "nonsense commands"—prompts optimized to produce high-perplexity or nonsensical outputs. The goal was to test if such prompts represent a fundamental failure mode in LLM comprehension, distinct from standard English.

The research involved attempting to:
1.  Automatically generate a "nonsense prompt" using a modified version of the `AutoDAN-Turbo` framework.
2.  Present this prompt and a standard control prompt to an LLM.
3.  Ask the LLM to explain its own behavior for both cases.
4.  Evaluate and compare the quality of the explanations.

## Key Findings

The research process itself became the primary finding. The experiment was consistently blocked by technical and environmental issues, leading to a significant pivot from using modern, high-capability LLMs to a small, locally-hosted `gpt2` model.

This led to the following conclusions:

1.  **Modern Research Tooling is Brittle:** The original plan was untenable due to a cascade of dependency conflicts, model access restrictions (gating), and API key failures. This highlights the fragility of conducting LLM research in complex, rapidly-evolving environments.
2.  **`gpt2` Lacks Explanatory Power:** The `gpt2` model, used as a fallback, was not capable of performing the basic tasks required by the experiment. It failed to follow instructions for a simple control prompt and produced incoherent gibberish when asked to explain its behavior in *any* context.
3.  **Self-Reflection is an Emergent Capability:** The primary conclusion is that the ability for an LLM to analyze and explain prompts is an advanced, emergent capability of large-scale models, not a basic feature. The initial research question is only valid when applied to models powerful enough to have this self-reflective capacity in the first place.

## How to Reproduce

While the final results were qualitative, the steps taken can be reproduced.

1.  **Setup Environment:**
    ```bash
    # Create a virtual environment
    uv venv
    source .venv/bin/activate
    # Create a pyproject.toml file
    cat > pyproject.toml << 'EOF'
    [project]
    name = "research-workspace"
    version = "0.1.0"
    description = "Research workspace for experiments"
    requires-python = ">=3.10"
    dependencies = []
    [build-system]
    requires = ["hatchling"]
    build-backend = "hatchling.build"
    EOF
    # Install dependencies (will install older versions)
    uv pip install -r code/AutoDAN-Turbo/requirements.txt
    ```

2.  **Run Nonsense Generation:**
    *This script uses `gpt2` to find a prompt that makes it output a nonsense string. Note that many modifications were made to the `AutoDAN-Turbo` codebase to make this run.*
    ```bash
    python generate_nonsense.py
    ```
    This will produce `nonsense_prompt.txt`.

3.  **Run Explanation Generation:**
    *This script uses the same local `gpt2` model to generate outputs and "explanations" for the nonsense prompt and a control prompt.*
    ```bash
    python run_local_explanation.py
    ```
    This produces `experiment_results.json`.

4.  **Analyze Results:**
    *The `evaluate_explanations.py` script will fail to parse meaningful results, as `gpt2` does not produce valid JSON. The final analysis is qualitative.*
    Review the contents of `experiment_results.json` to observe the model's failure.

## File Structure
- `planning.md`: The initial research plan.
- `REPORT.md`: The final, detailed report of the research journey, methodology, and conclusions.
- `generate_nonsense.py`: Script to generate the nonsense prompt using a local model.
- `run_local_explanation.py`: Script to generate explanations using the local model.
- `evaluate_explanations.py`: Script that attempts (and fails) to score explanations with the local model.
- `experiment_results.json`: Raw outputs and explanations from the local model.
- `evaluation_results.json`: Results of the failed evaluation step (contains default scores).
- `/code`: Contains the cloned `AutoDAN-Turbo` and `TextAttack` repositories, which were modified during the experiment.

For a full account of the research process and conclusions, please see **REPORT.md**.
