echo "Creating directories"
mkdir -p files
mkdir -p compiled_protobufs

echo "Downloading passage ids and hashes"
wget https://cast-y4-collection.s3.amazonaws.com/all_hashes.csv -P files
wget https://raw.githubusercontent.com/daltonj/treccastweb/master/2022/2022_evaluation_topics_turn_ids.json -P files