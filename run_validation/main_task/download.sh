#!/bin/sh

echo "Creating directories"
mkdir -p files
mkdir -p compiled_protobufs

echo "Downloading passage ids and hashes"
wget -c https://cast-y4-collection.s3.amazonaws.com/all_hashes.csv -P files
wget -c https://raw.githubusercontent.com/daltonj/treccastweb/master/2022/2022_evaluation_topics_turn_ids.json -P files

echo "Checksumming downloaded files..."
echo "70560402b9148ea7f7c5bc68a606eff75654408a568b9c62de0d6f5b9d187597 files/all_hashes.csv" | sha256sum --check
if [ $? -ne 0 ]
then
    echo "Checksum failed to match!"
    exit 1
fi
echo "feed7fc80b7a2c896fc6d32a4805e333fc639c4308d615ba26f3dece8780eaa5 files/2022_evaluation_topics_turn_ids.json" | sha256sum --check
if [ $? -ne 0 ]
then
    echo "Checksum failed to match!"
    exit 1
fi
exit

echo "Building database"
python3 passage_id_db.py -b 20000 -i 20 files/all_hashes.csv
