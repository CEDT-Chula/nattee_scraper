# Nattee Scraper
CEDT Comprog Automated Creation Of Testcase for vscode [CPH Extension](https://github.com/agrawal-d/cph)
designed for getting CEDT NatteeGrader website testcase by reverse engineering ruby web auth of [Cafe Grader](https://github.com/cafe-grader-team/cafe-grader-web) created by T'Nattee

![showcase](https://github.com/CEDT-Chula/nattee_scraper/blob/master/showcase/showcase.gif?raw=true)

## Prerequisite
- Python 3.8 or higher
- vscode (who tf didn't have it?) or VsCodium (if you don't like microsoft)
- CPH Extension in vscode or VsCodium (if you don't like microsoft)
- Linux/MacOS preferred (Windows is not tested but if you trust ChadGPT... :D)
- This repo asssume you have basic knowledge about how to use terminal or cmd & know how to use CPH Extension

## Installation Method
### Method 1 Python Virtual Environment Installation (Recommended for Windows, as Method 2 is not tested)
```bash
git clone https://github.com/CEDT-Chula/nattee_scraper
cd nattee_scraper
python -m venv venv
# venv\Scripts\activate for windows
source venv/bin/activate # for linux/macos and unix like system
pip install -r requirements.txt
```
### Method 2 Self Compiled Binary Installation (Very Recommended for MacOS/Linux)
```bash
# This method allow you to run the program from cli "anywhere" using environment variable "path"
git clone https://github.com/CEDT-Chula/nattee_scraper
cd nattee_scraper
sudo chmod 755 ./build.sh # Give Execute Permission (for macos and linux only!)
./build.sh # for linux/macos and unix like system
# ./build.bat # for windows (btw this is not tested, this shell scripts was written by ChadGPT using build.sh as reference)
```

## Usage
1. Create some.cpp file in your vscode workspace
2. Open the file
3. Open CPH Extension
4. Press 'Create Problem' button
5. You can now use ntscraper to get testcase from NatteeGrader!
### Execution Command
```bash
# 1st time
executable [path/to/file.cpp] [grader_submission_url] --uid [your_login_uid] --password [your_login_password]
# 2nd time
executable [path/to/file.cpp] [grader_submission_url] # no need to type uid and password again
```
- password and uid will be cached temporarily in your system cache(temp) folder so you don't have to retype it again
- if you want to change your uid or password, just use the full command again with the new uid and password

### Python installation Example
```bash
# python installation
python ntscraper.py ./file.cpp https://2110104.nattee.net/submissions/direct_edit_problem/1307 --uid 66778899 --password 12345678
```
### Binary installation Example
```bash
# binary installation
ntscraper ./file.cpp https://2110104.nattee.net/submissions/direct_edit_problem/1307 --uid 66778899 --password 12345678
```
# Contribution Needed
- Testing And Fix (if it broke) build.bat on windows (please also update the docs na bro)
- Improvements On Codebase Algorithm & Maybe Some Refractor
- Add Functionality To Improve Users Experience Such As (Multi Quizs Testcase Generation)
