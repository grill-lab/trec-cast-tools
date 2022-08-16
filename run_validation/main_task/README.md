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

Run Passage Validator Flask app in background
- `python3 passage_validator.py`

Run main script (in another terminal but within virtual env)
- `python3 main.py CAST [path to run file] [--skip_passage_validation]`

NOTE: `--skip_passage_validation` is an optional argument that skips passage validation if added. If used, passage_validator does not need to be run in the background.