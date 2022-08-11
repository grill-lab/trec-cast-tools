from typing import Dict, List


def deduplicate_run(run_file: str) -> List:

    # {'106_1': [], '106_2' : [], ... }
    document_ids = {}

    with open(run_file) as f:

        run_rows: List = []

        for line in f:

            line_dict: Dict = {}

            line_content = line.split()

            line_content[2] = line_content[2].rsplit("-",1)[0]

            # check if turn_id is in the dictionary
            if document_ids.get(line_content[0]):

                # check if turn has document id in its list
                if line_content[2] not in document_ids[line_content[0]]:

                    document_ids[line_content[0]].append(line_content[2])

                    line_dict = {
                        "turn_id": line_content[0],
                        "dummy_value": line_content[1],
                        "doc_id": line_content[2],
                        "rank": line_content[3],
                        "score": line_content[4],
                        "run_name": line_content[5]
                    }

                    run_rows.append(line_dict)
            else:

                document_ids[line_content[0]] = []
                document_ids[line_content[0]].append(line_content[2])

                line_dict = {
                    "turn_id": line_content[0],
                    "dummy_value": line_content[1],
                    "doc_id": line_content[2],
                    "rank": line_content[3],
                    "score": line_content[4],
                    "run_name": line_content[5]
                }

                run_rows.append(line_dict)

        return run_rows


def adjust_run_ranking(run_rows: List) -> List:

    for i in range(1, len(run_rows)):

        if run_rows[i]["turn_id"] == run_rows[i-1]["turn_id"]:
            run_rows[i]["rank"] = str(int(run_rows[i-1]["rank"]) + 1)

        else:
            run_rows[i]['rank'] = str(1)

    return run_rows
