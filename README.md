# restaurant



Navigate to the Project Directory

cd /path/to/your/project

Install Git on your system:

Ubuntu/Debian:
sudo apt-get update
sudo apt-get install git

macOS: Install Git via Homebrew:
brew install git

Verify Git installation:
git --version

Add Git to JSON Configuration in VS Code

To integrate Git with VS Code:

    Open VS Code.
    Install the GitLens or Git Graph extension for Git visualization.
    Open VS Code Settings (Ctrl + , or Cmd + , on macOS).
    Search for Git Path and update the Git path if not auto-detected.
        Example:
            Windows: "C:\\Program Files\\Git\\bin\\git.exe"
            macOS/Linux: "/usr/bin/git" or "/usr/local/bin/git"

Alternatively, edit the settings.json file directly:

    Open Command Palette (Ctrl+Shift+P or Cmd+Shift+P) and select Preferences: Open Settings (JSON).
    Add or update the Git path:

    {
  "git.path": "/path/to/git"
}

Pull the Latest Changes from main Ensure you’re on the main branch and pull the latest changes:

git checkout main
git pull origin main

install Python3 and pip
Ensure Python 3.8 or higher is installed. Verify:
python3 --version
Install pip:
sudo apt-get install python3-pip  # For Ubuntu/Debian
brew install python               # For macOS

nstall venv (if not already installed)

    Install venv to create a virtual environment:
sudo apt-get install python3-venv  # For Ubuntu/Debian

python3 -m venv venv
source venv/bin/activate

nstall Project Dependencies

    Use pip to install the dependencies listed in the requirements.txt file:
pip install -r requirements.txt

Set Up the SQLite Database

    Run the data.py script to set up and populate the database:

python3 app/data.py

flask run
pipx run flask run

