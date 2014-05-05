import mock
from nose.tools import eq_
from pyelasticsearch import exceptions
from test_utils import RequestFactory

import amo.tests
from search.middleware import ElasticsearchExceptionMiddleware as ESM


class TestElasticsearchExceptionMiddleware(amo.tests.TestCase):

    def setUp(self):
        self.request = RequestFactory()

    @mock.patch('search.middleware.render')
    def test_exceptions_we_catch(self, render_mock):
        # These are instantiated with an error string.
        for e in [exceptions.ElasticHttpNotFoundError,
                  exceptions.IndexAlreadyExistsError,
                  exceptions.ElasticHttpError]:
            ESM().process_exception(self.request, e('ES ERROR'))
            render_mock.assert_called_with(self.request, 'search/down.html',
                                           status=503)
            render_mock.reset_mock()

    @mock.patch('search.middleware.render')
    def test_exceptions_we_do_not_catch(self, render_mock):
        ESM().process_exception(self.request, Exception)
        eq_(render_mock.called, False)
