import os
import subprocess
import argparse
from pathlib import Path

# === DEFAULT CONFIG ===
DEFAULT_EXTENSIONS = [".js", ".ts", ".json", ".py"]
DEFAULT_MODEL = "mistral"
DEFAULT_REPORT = "project_analysis.txt"
DEFAULT_CHUNK_SIZE = 5000


# === HELPER FUNCTIONS ===
def read_project_files(folder, extensions):
    project_files = []
    for root, _, files in os.walk(folder):
        for file in files:
            if any(file.endswith(ext) for ext in extensions):
                full_path = os.path.join(root, file)
                try:
                    with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                        project_files.append({
                            "path": full_path.replace(folder + os.sep, ""),
                            "content": f.read()
                        })
                except Exception as e:
                    print(f"⚠️ Error reading {full_path}: {e}")
    return project_files


def chunk_text(text, max_chars):
    for i in range(0, len(text), max_chars):
        yield text[i:i + max_chars]


def analyze_chunk_with_llm(chunk, file_path, model):
    prompt = f"""
You are an expert QA automation engineer. Critique this file. Be concise.

File path: {file_path}
File content:
{chunk}

Tasks:
- Point out potential bugs or fragile code.
- Suggest improvements and refactoring ideas.
- Give folder/organization suggestions if relevant.

Output your response as plain text.
"""
    try:
        result = subprocess.run(
            ["ollama", "run", model],
            input=prompt,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="ignore"
        )
    except FileNotFoundError:
        return "Ollama is not installed or not found in PATH.\n"

    if not result.stdout.strip():
        return f"No response from model for {file_path}\n"
    return result.stdout.strip() + "\n"


def analyze_file(file, model, chunk_size):
    output = f"==== Analyzing {file['path']} ====\n"
    for i, chunk in enumerate(chunk_text(file['content'], chunk_size)):
        output += analyze_chunk_with_llm(chunk, file['path'], model)
    output += "\n"
    return output


# === MAIN SCRIPT ===
def main():
    parser = argparse.ArgumentParser(description="Analyze a project with an LLM via Ollama.")
    parser.add_argument("project_folder", type=str, help="Path to the project folder")
    parser.add_argument("--extensions", nargs="+", default=DEFAULT_EXTENSIONS, help="File extensions to include (default: .js .ts .json .py)")
    parser.add_argument("--model", type=str, default=DEFAULT_MODEL, help="LLM model to use (default: mistral)")
    parser.add_argument("--report", type=str, default=DEFAULT_REPORT, help="Output report file (default: project_analysis.txt)")
    parser.add_argument("--chunk-size", type=int, default=DEFAULT_CHUNK_SIZE, help="Max characters per chunk (default: 5000)")
    args = parser.parse_args()

    folder = Path(args.project_folder).resolve()
    if not folder.exists():
        print(f"Project folder not found: {folder}")
        return

    print(f"Reading project files from {folder}...")
    project_files = read_project_files(str(folder), args.extensions)

    if not project_files:
        print("No files found with given extensions.")
        return

    full_output = ""

    for file in project_files:
        print(f"Analyzing {file['path']}...")
        full_output += analyze_file(file, args.model, args.chunk_size)

    with open(args.report, "w", encoding="utf-8") as f:
        f.write(full_output)

    print(f"Analysis complete! Report saved to {args.report}")


if __name__ == "__main__":
    main()
