# QA Automation LLM Analyzer

A Python tool for analyzing **QA automation code** using a large language model (LLM) via [Ollama](https://ollama.com/).  
It helps identify potential bugs, fragile test scripts, and provides suggestions for improvements and better project organization. Supports multiple file types and outputs a detailed analysis report.

---

## Features

- Analyzes JavaScript, TypeScript, Python, JSON, and other file types.
- Detects fragile or problematic test automation code.
- Suggests refactoring and improvements.
- Generates a comprehensive report in plain text.
- Handles large files by splitting them into chunks for LLM processing.

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/your-username/qa-automation-llm-analyzer.git
cd qa-automation-llm-analyzer
```

2. Ensure Python 3.9+ is installed.

3. Install Ollama and ensure it’s available in your system PATH.

## Usage
1. Default (hard-coded config)
Run the script directly:
```bash
python analyze_project.py
```

- Analyzes the folder specified in the PROJECT_FOLDER variable.
- Generates a report named project_analysis.txt.


2. Flexible CLI (if using the generalized version)
```bash
python analyze_project.py "C:\path\to\your\project" --extensions .js .ts .py --model mistral --report analysis.txt
```

- project_folder: Path to the QA automation project.
- --extensions: List of file types to include (default: .js .ts .json .py).
- --model: LLM model to use (default: mistral).
- --report: Name of the output report file (default: project_analysis.txt).
- --chunk-size: Maximum characters per chunk (default: 5000).


## Usage
This will generate analysis.txt with LLM feedback on test scripts and project structure.


## Contributing
Contributions are welcome! Feel free to open issues or submit pull requests for:
- Supporting more file types.
- Adding additional LLM models.
- Improving report formatting or analysis prompts.
