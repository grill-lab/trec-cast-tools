from flask import Flask, render_template, request
import csv
import sys

# collect passge ids and hashes
with open(f"./files/all_hashes.csv") as passage_hashes_file:
    passage_lookup_dict = {}
    passage_hashes_reader = csv.reader(passage_hashes_file)
    for row in passage_hashes_reader:
        passage_lookup_dict[row[0]] = row[1]

# check that passage ids and hashes were loaded correctly
try:
    assert len(passage_lookup_dict.keys()) == 106400940
except AssertionError:
    print("Passage Ids and hashes not loaded correctly")
    sys.exit(255)

app = Flask(__name__)

@app.route('/<passage_id>', methods=['GET'])
def validate_passage(passage_id):
    return {
        'passage_id': passage_id,
        'is_valid' : passage_id in passage_lookup_dict
    }

if __name__ == '__main__':
    app.run(debug=True, port=5000, use_reloader=False)