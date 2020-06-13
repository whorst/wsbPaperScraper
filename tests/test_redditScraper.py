import unittest

import praw

import redditScraper
from unittest.mock import MagicMock

class TestStrikeDate(unittest.TestCase):
    def test_StrikeDateInComment_shouldReturnTrue_When_CallValidPriceInComment(self):
        comment = "lsnrw 9/16 wngrwng"
        self.assertTrue(redditScraper.getStrikeDatesInComment(comment))

    def test_StrikeDateInComment_shouldReturnTrue_When_CallValidPriceAndCallInComment(self):
        comment = "lsnrw 9/16c wngrwng"
        self.assertTrue(redditScraper.getStrikeDatesInComment(comment))

    def test_StrikeDateInComment_shouldReturnTrue_When_CallValidPriceAndPutInComment(self):
        comment = "lsnrw 9/16p wngrwng"
        self.assertTrue(redditScraper.getStrikeDatesInComment(comment))

    def test_StrikeDateInComment_shouldReturnFalse_When_CallInvalidDateInComment(self):
        comment = "lsnrw9/16p5/6wngrwng"
        self.assertFalse(redditScraper.getStrikeDatesInComment(comment))

    def test_StrikeDateInComment_shouldReturnFalse_When_CallDateWithYearInComment(self):
        comment = "lsnrw 2/2020 wngrwng"
        self.assertFalse(redditScraper.getStrikeDatesInComment(comment))

    def test_StrikeDateInComment_shouldReturnFalse_When_CallDateWithYearInComment(self):
        comment = "lsnrw 2/2020 wngrwng"
        self.assertFalse(redditScraper.getStrikeDatesInComment(comment))

    def test_StrikeDateInComment_shouldReturnFalse_When_CalledWith_DayMonthYearInComment(self):
        comment = "lsnrw 2/2/2020 wngrwng"
        self.assertFalse(redditScraper.getStrikeDatesInComment(comment))

class TestCallReferences(unittest.TestCase):
    def test_isCallReferenceInComment_shouldReturnTrue_When_CallLowercaseInComment(self):
        comment = "newf enfjw ef w  ef ewnwef call eafjejn"
        self.assertTrue(redditScraper.isCallReferenceInComment(comment))

    def test_isCallReferenceInComment_shouldReturnTrue_When_CallUppercaseInComment(self):
        comment = "newf enfjw ef w  ef ewnwef CALL eafjejn"
        self.assertTrue(redditScraper.isCallReferenceInComment(comment))

    def test_isCallReferenceInComment_shouldReturnTrue_When_CallsLowercaseInComment(self):
        comment = "newf enfjw ef w  ef ewnwef call eafjejn"
        self.assertTrue(redditScraper.isCallReferenceInComment(comment))

    def test_isCallReferenceInComment_shouldReturnTrue_When_CallsUppercaseInComment(self):
        comment = "newf enfjw ef w  ef ewnwef CALL eafjejn"
        self.assertTrue(redditScraper.isCallReferenceInComment(comment))

    def test_isCallReferenceInComment_shouldReturnFalse_When_CallsCoveredByWord(self):
        comment = "newf enfjw ef w  ef ewnwefcalleafjejn"
        self.assertFalse(redditScraper.isCallReferenceInComment(comment))

    def test_isCallReferenceInComment_shouldReturnFalse_When_CallsCoveredByWord(self):
        comment = "newf enfjw ef w  ef ewnwef CALLeafjejn"
        self.assertFalse(redditScraper.isCallReferenceInComment(comment))

class TestPutReferences(unittest.TestCase):
    def test_isPutReferenceInComment_shouldReturnTrue_When_PutLowercaseInComment(self):
        comment = "newf enfjw ef w  ef ewnwef put eafjejn"
        self.assertTrue(redditScraper.isPutReferenceInComment(comment))

    def test_isPutReferenceInComment_shouldReturnTrue_When_PutUppercaseInComment(self):
        comment = "newf enfjw ef w  ef ewnwef PUT eafjejn"
        self.assertTrue(redditScraper.isPutReferenceInComment(comment))

    def test_isPutReferenceInComment_shouldReturnTrue_When_PutsLowercaseInComment(self):
        comment = "newf enfjw ef w  ef ewnwef put eafjejn"
        self.assertTrue(redditScraper.isPutReferenceInComment(comment))

    def test_isPutReferenceInComment_shouldReturnTrue_When_PutsUppercaseInComment(self):
        comment = "newf enfjw ef w  ef ewnwef PUT eafjejn"
        self.assertTrue(redditScraper.isPutReferenceInComment(comment))

    def test_isPutReferenceInComment_shouldReturnFalse_When_PutsCoveredByWord(self):
        comment = "newf enfjw ef w  ef ewnwefputeafjejn"
        self.assertFalse(redditScraper.isPutReferenceInComment(comment))

    def test_isPutReferenceInComment_shouldReturnFalse_When_PutsCoveredByWord(self):
        comment = "newf enfjw ef w  ef ewnwef PUTeafjejn"
        self.assertFalse(redditScraper.isPutReferenceInComment(comment))



    # def test_isupper(self):
    #     self.assertTrue('FOO'.isupper())
    #     self.assertFalse('Foo'.isupper())
    #
    # def test_split(self):
    #     s = 'hello world'
    #     self.assertEqual(s.split(), ['hello', 'world'])
    #     # check that s.split fails when the separator is not a string
    #     with self.assertRaises(TypeError):
    #         s.split(2)

if __name__ == '__main__':
    unittest.main()