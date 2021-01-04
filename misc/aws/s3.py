import os
from functools import wraps
from io import BytesIO
from typing import BinaryIO, Tuple

import boto3

AWS_ACCESS_KEY_ID = ''
AWS_SECRET_ACCESS_KEY = ''
AWS_S3_BUCKET_NAME = ''
AWS_S3_URL = ''


class S3Error(Exception):
    pass


def _handle_exception(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            raise S3Error()

    return wrapper


@_handle_exception
def upload(file_: BinaryIO, path: str) -> str:
    """
    Upload a file to s3
    :param file_: file-like object (supports read() method).
    :param path: specify the path of the file in the S3 bucket
    :return: uploaded url
    """
    # IMPORTANT: move the cursor to the begin of the file
    file_.seek(0, 0)

    s3 = _get_s3_client()
    s3.upload_fileobj(file_, AWS_S3_BUCKET_NAME, path)

    return os.path.join(AWS_S3_URL, path)


@_handle_exception
def download(file_url: str) -> Tuple[BinaryIO, str]:
    """
    Download a file from s3
    :param file_url: a s3 file url
    :return: a tuple contains a file-like object, file_name
    """
    file_key = _get_file_key_from_a_link(file_url)
    s3 = _get_s3_client()
    s3_response_object = s3.get_object(Bucket=AWS_S3_BUCKET_NAME, Key=file_key)
    file_ = s3_response_object['Body']
    return BytesIO(file_.read()), file_key.split('/')[-1]


@_handle_exception
def delete(file_url: str) -> None:
    """
    Delete a file from s3. If the bucket support version, delete the latest version.
    :param file_url: a s3 file url
    :return:
    """
    file_key = _get_file_key_from_a_link(file_url)

    s3 = _get_s3_client()

    file_object = s3.get_object(Bucket=AWS_S3_BUCKET_NAME, Key=file_key)
    if file_object.get('VersionId'):
        s3.delete_object(
            Bucket=AWS_S3_BUCKET_NAME,
            Key=file_key,
            VersionId=file_object.get('VersionId'),
        )
    else:
        s3.delete_object(Bucket=AWS_S3_BUCKET_NAME, Key=file_key)


def _get_s3_client():
    return boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    )


def _get_file_key_from_a_link(s3_url: str) -> str:
    return s3_url.replace(f'{AWS_S3_URL}/', '')
