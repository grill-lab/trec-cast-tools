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

Run Passage Validator service in background
- `python3 passage_validator_servicer.py files/all_hashes.sqlite3`

Run main validation script (in another terminal but within same virtual env)
- `python3 main.py CAST [path to run file] [--skip_passage_validation]`

NOTE: `--skip_passage_validation` is an optional argument that skips passage validation if added. If used, passage_validator does not need to be run in the background.

To generate a trec run file, ideally after main script runs successfully
- `python3 generate_run.py [path to run file]`

### Tests

To run the normal set of tests:

- `pytest`

To run the full set (including some slower tests):

- `pytest --runslow`
