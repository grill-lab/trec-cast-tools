echo "Creating directories"
mkdir -p files
mkdir -p compiled_protobufs

echo "Downloading passage ids and hashes"
wget -c https://cast-y4-collection.s3.amazonaws.com/all_hashes.csv -P files
wget -c https://raw.githubusercontent.com/daltonj/treccastweb/master/2022/2022_evaluation_topics_turn_ids.json -P files

echo "Building database"
python3 hash_db.py -b 20000 -i 100000 files/all_hashes.csv
