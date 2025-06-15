import subprocess
import re
from pathlib import Path

# Run the analysis script and capture its output
result = subprocess.run(
    ["python", "analysis/games/games_beated_analysis.py"],
    capture_output=True,
    text=True,
    check=True,
)
analysis_output = result.stdout.strip()

start_marker = "<!-- GAMES_BEATED_START -->"
end_marker = "<!-- GAMES_BEATED_END -->"

readme_path = Path("README.md")
readme_text = readme_path.read_text()

new_section = f"{start_marker}\n\n```\n{analysis_output}\n```\n{end_marker}"

# Replace existing section or insert after the heading
pattern = re.compile(f"{start_marker}.*?{end_marker}", re.S)
if pattern.search(readme_text):
    updated_text = pattern.sub(new_section, readme_text)
else:
    heading = "## Games Beated Analysis"
    if heading in readme_text:
        updated_text = readme_text.replace(heading, heading + "\n" + new_section)
    else:
        updated_text = readme_text + "\n" + heading + "\n" + new_section

readme_path.write_text(updated_text)
