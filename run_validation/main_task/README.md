## How to Run

### Prerequisites and setup

Download necessary files
- `bash download.sh`

Create and activate a virtual environment
- `python3 -m venv env`
- `source env/bin/activate`

Install requirements

- `pip install --upgrade pip && pip install -r requirements.txt`

Compile protocol buffers

- `bash compile_protos.sh`

### Running the validation script

Run the Passage Validator service in the background: `python3 passage_validator_servicer.py files/all_hashes.sqlite3`

Run the main validation script (in another terminal but within the same virtual env). The script has several parameters you can view by running `python3 main.py -h`.

Some examples:

```shell
# Run with default parameters
python3 main.py CAST <run file path>
# Run without having the validator service available
python3 main.py CAST <run file path> --skip_passage_validation
# Abort the run if more than 50 validation warnings are generated
python3 main.py CAST <run file path> -m 50
# Abort the run if any gRPC errors occur contacting the validation service
python3 main.py CAST <run file path> -s
# Set a 10s timeout for gRPC calls to the validation service
python3 main.py CAST <run file path> -t 10
```

The script logs to stdout and to a file in the current working directory named `<run_file>.errlog` (e.g. a run file named `sample_run.json` will have logs saved to `sample_run.json.errlog`).

### Generating a TREC run file

To generate a trec run file, ideally after main script runs successfully: `python3 generate_run.py <run file path>`

### Tests

To run the normal set of tests: `pytest`

To run the full set (including some slower tests): `pytest --runslow`
