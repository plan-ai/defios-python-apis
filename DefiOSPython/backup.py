import os, datetime, tarfile, os.path
from pymongo import MongoClient
from bson.json_util import dumps
import boto3
from datetime import datetime
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

session = boto3.Session(
    aws_access_key_id=config["AWS"]["S3_ACCESS_KEY"],
    aws_secret_access_key=config["AWS"]["S3_SECRET_ACCESS_KEY"],
)
s3 = session.client("s3")

now = datetime.now()


def create_folder_backup(dbname):
    dt = datetime.now()
    directory = "backups/bk"
    if not os.path.exists(directory):
        os.makedirs(directory)
    return directory


def run_backup(mongoUri, dbname):
    client = MongoClient(mongoUri)
    db = client[dbname]
    collections = db.list_collection_names()
    files_to_compress = []
    directory = create_folder_backup(dbname)
    for collection in collections:
        db_collection = db[collection]
        cursor = db_collection.find({})
        filename = "%s/%s.json" % (directory, collection)
        files_to_compress.append(filename)
        with open(filename, "w") as file:
            file.write("[")
            for document in cursor:
                file.write(dumps(document))
                file.write(",")
            file.write("]")
    tar_file = "%s.tar.gz" % (directory)
    make_tarfile(tar_file, files_to_compress)


def make_tarfile(output_filename, source_dir):
    tar = tarfile.open(output_filename, "w:gz")
    for filename in source_dir:
        tar.add(filename)
    tar.close()


if __name__ == "__main__":
    mongoUri = "localhost:27017"
    dbname = config["MONGODB"]["HOST"]
    try:
        run_backup(mongoUri, dbname)
        print("[*] Successfully performed backup")
    except Exception as e:
        print("[-] An unexpected error has occurred")
        print("[-] " + str(e))
        print("[-] EXIT")
    now = datetime.now()
    with open(
        "/home/ubuntu/defios-python-apis/DefiOSPython/backups/bk.tar.gz", "rb"
    ) as tar:
        s3.upload_fileobj(tar, "defios-db-backup", f"DefiOS-backup-{now}")
