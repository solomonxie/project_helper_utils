import urllib
from unittest import TestCase

import S3Operator


class TestS3(TestCase):
    def setUp(self):
        # Set the configs according to the "envfile-local.txt"
        self.s3 = S3Operator(
            access_key='AKIAIOSFODNN7EXAMPLE',
            secret='wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY',
            endpoint='http://s3-minio:9000'
        )
        self.bucket_name = 'fakebucket'
        self.s3.delete_bucket(self.bucket_name)
        self.s3.create_bucket_if_not_exists(self.bucket_name)

    def tearDown(self):
        self.s3.delete_bucket(self.bucket_name)

    def test_upload(self):
        result = self.s3.upload_file('./README.md', self.bucket_name, 'README.md')
        self.assertTrue(result)
        objects = self.s3.list_objects(self.bucket_name)
        self.assertEqual(1, len(objects))
        self.assertIn('README.md', objects)

    def test_download(self):
        result = self.s3.upload_file_blob('[1, 2]', self.bucket_name, 'nums.json')
        self.assertTrue(result)
        blob = self.s3.download_file_blob(self.bucket_name, 'nums.json')
        self.assertEqual('[1, 2]', blob)

    def test_signed_url(self):
        self.s3.upload_file('./README.md', self.bucket_name, 'README.md')
        url = self.s3.get_signed_url(self.bucket_name, 'README.md')
        urlobj = urllib.parse.urlparse(url)
        self.assertEqual(f'/{self.bucket_name}/README.md', urlobj.path)
        params = urllib.parse.parse_qs(urlobj.query)
        self.assertListEqual(['AWSAccessKeyId', 'Signature', 'Expires'], list(params.keys()))
        self.assertEqual(['AKIAIOSFODNN7EXAMPLE'], params['AWSAccessKeyId'])
