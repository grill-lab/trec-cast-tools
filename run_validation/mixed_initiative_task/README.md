## How to Run

Download necessary files
- `bash download.sh`

Create and activate a virtual environment
- `python3 -m venv env`
- `source env/bin/activate`

Install requirements
- `pip install --upgrade pip && pip install -r requirements.txt`

Compile protocol buffers
- `bash compile_protos.sh`

Run script
- `python3 main.py CAST [path to run file]`

Run tests
- `python3 -m pytest`
