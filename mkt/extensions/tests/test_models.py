# -*- coding: utf-8 -*-
import mock
from nose.tools import eq_, ok_

from django.forms import ValidationError

from mkt.extensions.models import Extension
from mkt.files.tests.test_models import UploadCreationMixin, UploadTest
from mkt.site.storage_utils import private_storage
from mkt.site.tests import fixture, TestCase
from mkt.users.models import UserProfile


class TestExtensionUpload(UploadCreationMixin, UploadTest):
    fixtures = fixture('user_2519')

    # Expected manifest, to test zip file parsing.
    expected_manifest = {
        'description': u'A Dummÿ Extension',
        'default_locale': 'en_GB',
        'icons': {
            '128': '/icon.png'
        },
        'version': '0.1',
        'author': 'Mozilla',
        'name': u'My Lîttle Extension'
    }

    def setUp(self):
        super(TestExtensionUpload, self).setUp()
        self.user = UserProfile.objects.get(pk=2519)

    def create_extension(self, **kwargs):
        extension = Extension.objects.create(
            default_language='fr', version='0.9', manifest={}, **kwargs)
        return extension

    def test_auto_create_slug(self):
        extension = self.create_extension()
        eq_(extension.slug, 'extension')
        extension = self.create_extension()
        eq_(extension.slug, 'extension-1')
        extension = self.create_extension(name=u'Mŷ Ëxtension')
        eq_(extension.slug, u'mŷ-ëxtension')

    def test_upload_new(self):
        eq_(Extension.objects.count(), 0)
        upload = self.upload('extension')
        extension = Extension.from_upload(upload, user=self.user)
        eq_(extension.version, '0.1')
        eq_(list(extension.authors.all()), [self.user])
        eq_(extension.name, u'My Lîttle Extension')
        eq_(extension.default_language, 'en-GB')
        eq_(extension.slug, u'my-lîttle-extension')
        eq_(extension.filename, 'extension-%s.zip' % extension.version)
        ok_(extension.filename in extension.file_path)
        ok_(extension.file_path.startswith(extension.path_prefix))
        ok_(private_storage.exists(extension.file_path))
        eq_(extension.manifest, self.expected_manifest)
        eq_(Extension.objects.count(), 1)

    @mock.patch('mkt.extensions.utils.ExtensionParser.manifest_contents')
    def test_upload_no_version(self, manifest_mock):
        manifest_mock.__get__ = mock.Mock(return_value={'name': 'lol'})
        upload = self.upload('extension')
        with self.assertRaises(ValidationError):
            Extension.from_upload(upload)

    @mock.patch('mkt.extensions.utils.ExtensionParser.manifest_contents')
    def test_upload_no_name(self, manifest_mock):
        manifest_mock.__get__ = mock.Mock(return_value={'version': '0.1'})
        upload = self.upload('extension')
        with self.assertRaises(ValidationError):
            Extension.from_upload(upload)

    def test_upload_existing(self):
        extension = self.create_extension()
        upload = self.upload('extension')
        with self.assertRaises(NotImplementedError):
            Extension.from_upload(upload, instance=extension)


class TestExtensionDeletion(TestCase):
    def test_delete_with_file(self):
        """Test that when a Extension instance is deleted, the corresponding
        file on the filesystem is also deleted."""
        extension = Extension.objects.create(version='0.1')
        file_path = extension.file_path
        with private_storage.open(file_path, 'w') as f:
            f.write('sample data\n')
        assert private_storage.exists(file_path)
        try:
            extension.delete()
            assert not private_storage.exists(file_path)
        finally:
            if private_storage.exists(file_path):
                private_storage.delete(file_path)

    def test_delete_no_file(self):
        """Test that the Extension instance can be deleted without the file
        being present."""
        extension = Extension.objects.create(version='0.1')
        filename = extension.file_path
        assert not private_storage.exists(filename)
        extension.delete()

    def test_delete_signal(self):
        """Test that the Extension instance can be deleted with the filename
        field being empty."""
        extension = Extension.objects.create()
        extension.delete()


class TestExtensionESIndexation(TestCase):
    @mock.patch('mkt.search.indexers.BaseIndexer.index_ids')
    def test_update_search_index(self, update_mock):
        extension = Extension.objects.create()
        update_mock.assert_called_once_with([extension.pk])

    @mock.patch('mkt.search.indexers.BaseIndexer.unindex')
    def test_delete_search_index(self, delete_mock):
        for x in xrange(3):
            Extension.objects.create()
        count = Extension.objects.count()
        eq_(count, 3)
        Extension.objects.all().delete()
        eq_(delete_mock.call_count, count)
