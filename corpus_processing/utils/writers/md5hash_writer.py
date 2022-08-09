import hashlib

def write_md5_hashes(output_file, document_batch):

    with open(output_file, "w") as md5_hash_file:
        for document in document_batch:
            passages = document['contents']
            for passage in passages:
                md5_hash = hashlib.md5(passage['body'].encode())
                md5_hash_file.write(f"{document['id']}-{passage['id']},{md5_hash.hexdigest()}\n")