# check if windows
if [ -n "$WINDIR" ]; then
    echo "Windows detected"
    echo "Please run build.bat"
    exit 1
fi

# check if venv exists
if [ ! -d "./venv" ]; then
    echo "venv not found"
    echo "Setting up venv"
    python3 -m venv venv
    source ./venv/bin/activate
    echo "dependencies installing"
    pip install -r requirements.txt
    echo "venv setup complete!!"
fi
echo "venv found, activating"
source ./venv/bin/activate
echo "dependencies installing"
pip install -r requirements.txt

# check if build folder exists
pyinstaller --onefile ./ntscraper.py
# remove build folder, cache, and spec file
rm -rf ./build
rm -rf ./ntscraper.spec