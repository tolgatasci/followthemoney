import unittest

from followthemoney.types import registry

urls = registry.url


class UrlsTest(unittest.TestCase):
    def test_is_url(self):
        self.assertTrue(urls.validate("http://foo.org"))
        self.assertFalse(urls.validate(None))
        self.assertFalse(urls.validate("hello"))
        self.assertTrue(urls.validate("foo.org"))
        self.assertTrue(urls.validate("//foo.org"))

    def test_unicode_url(self):
        utext = "http://ko.wikipedia.org/wiki/위키백과:대문"
        self.assertTrue(urls.validate(utext))
        self.assertTrue(urls.validate(utext.encode("utf-8")))

    def test_parse_url(self):
        self.assertEqual(urls.clean("http://foo.com/"), "http://foo.com/")
        self.assertEqual(urls.clean("http://foo.com/#lala"), "http://foo.com/#lala")

        self.assertEqual(
            urls.clean("http://foo.com?b=1&a=2"), "http://foo.com/?b=1&a=2"
        )
        self.assertEqual(urls.clean("http://FOO.com"), "http://FOO.com/")
        self.assertEqual(urls.clean("http://FOO.com/A"), "http://FOO.com/A")

    def test_specificity(self):
        self.assertGreater(urls.specificity("http://foo.com/#banana"), 0.1)
