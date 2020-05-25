import urllib
from unittest import TestCase
from moto import mock_s3

from tests.helper_utils.s3_extra import S3Operator


class TestS3(TestCase):
    def setUp(self):
        self.s3_mock = mock_s3()
        self.s3_mock.start()
        self.s3 = S3Operator(
            access_key='AKIAIOSFODNN7EXAMPLE',
            secret='wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY'
        )
        self.bucket = 'fakebucket'
        self.s3.delete_bucket(self.bucket)
        self.s3.create_bucket_if_not_exists(self.bucket)

    def tearDown(self):
        self.s3.delete_bucket(self.bucket)
        self.s3_mock.stop()

    def test_upload(self):
        result = self.s3.upload_file('./README.md', self.bucket, 'README.md')
        self.assertTrue(result)
        objects = self.s3.list_objects(self.bucket)
        self.assertEqual(1, len(objects))
        self.assertIn('README.md', objects)

    def test_download(self):
        result = self.s3.upload_file_blob('[1, 2]', self.bucket, 'nums.json')
        self.assertTrue(result)
        blob = self.s3.download_file_blob(self.bucket, 'nums.json')
        self.assertEqual(b'[1, 2]', blob)

    def test_list_objects(self):
        # Upload more than 1000 objects
        for i in range(1000):
            self.s3.upload_file_blob(str(i), self.bucket, 'data/test/nums1/{}.txt'.format(i))
            self.s3.upload_file_blob(str(i), self.bucket, 'data/test/nums2/{}.txt'.format(i))
        all_objects = self.s3.list_objects(self.bucket)
        self.assertEqual(2000, len(all_objects))
        all_objects = self.s3.list_objects(self.bucket, path_prefix='data/test/nums1/')
        self.assertEqual(1000, len(all_objects))

    def test_signed_url(self):
        self.s3.upload_file('./README.md', self.bucket, 'README.md')
        url = self.s3.get_signed_url(self.bucket, 'README.md')
        urlobj = urllib.parse.urlparse(url)
        self.assertEqual('/README.md', urlobj.path)
        params = urllib.parse.parse_qs(urlobj.query)
        self.assertSetEqual({u'AWSAccessKeyId', u'Expires', u'Signature'}, set(params.keys()))
        self.assertEqual(['AKIAIOSFODNN7EXAMPLE'], params['AWSAccessKeyId'])
