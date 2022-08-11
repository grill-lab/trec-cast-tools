echo "Creating directories"
mkdir -p files
mkdir -p compiled_protobufs

echo "Downloading turn ids and MI question bank"
wget -c https://raw.githubusercontent.com/daltonj/treccastweb/master/2022/2022_mixed_initiative_question_pool.json -P files
wget -c https://raw.githubusercontent.com/daltonj/treccastweb/master/2022/2022_evaluation_topics_turn_ids.json -P files