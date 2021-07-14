import sys
import spacy

from pyspark.sql import SparkSession
from pyspark.sql import *
from pyspark.sql.functions import udf, struct

from trecweb_utils import convert_to_trecweb, add_passage_ids
from passage_chunker import SpacyPassageChunker

import findspark
findspark.init()

SPACY_MODEL = None


def get_spacy_model():
    global SPACY_MODEL
    if not SPACY_MODEL:
        _model = spacy.load("en_core_web_sm", exclude=["parser"])
        _model.enable_pipe("senter")
        SPACY_MODEL = _model
    return SPACY_MODEL


def create_spark_session():
    """Create spark session.
Returns:
        spark (SparkSession) - spark session connected to AWS EMR
            cluster
    """
    spark = SparkSession \
        .builder \
        .appName("spacy-on-spark") \
        .getOrCreate()
    # Enable the arrow based udf calls or data transfer between python and jvm.
    return spark


def process_doc(doc):
    idx = 'KILT_' + doc['wikipedia_id']
    title = doc['wikipedia_title']
    body = ' '.join(doc['text'])
    url = doc['history']['url']

    passage_chunker = SpacyPassageChunker(get_spacy_model(), body)
    passages = passage_chunker.create_passages()
    passage_splits = add_passage_ids(passages)
    trecweb_format = convert_to_trecweb(idx, title, passage_splits, url)
    return trecweb_format


def process_kilt_data(spark, input_path, output_path):
    """Process the kilt and write to S3.
Arguments:
        spark (SparkSession) - spark session connected to AWS EMR
        input_path (str) - path for source data
        output_path (str) - path for writing processed data
    """
    df = spark.read.option("mode", "PERMISSIVE").json(input_path)
    df.show(n=2)

    # Tokenize and process with spacy.
    # Do we need to do this anymore? I think the UDF annotation might do it now.
    tokenization_udf = spark.udf.register("PassageSplitSpacy", process_doc)

    new_records = df.withColumn("trecweb", tokenization_udf(struct([df[x] for x in df.columns])))
    filtered_records = new_records.select("trecweb")
    # Save the data to S3 bucket as a text file.
    #filtered_records.show()
    filtered_records.write.format("text").option("header", "false").mode('overwrite').save(output_path)


def main(input_path, output_path):
    print("Starting spark session...")
    spark = create_spark_session()
    print("Starting processing.")
    print("Input directory: " + input_path)
    print("Output directory: " + output_path)
    process_kilt_data(spark, input_path, output_path)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("USAGE: python kilt_trecweb_spark.py path_to_kilt_file path_to_output")
        exit(0)

    input_path = sys.argv[1]
    output_path = sys.argv[2]
    main(input_path, output_path)
