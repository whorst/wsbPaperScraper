import unittest

import praw

import redditScraper
from unittest.mock import MagicMock
from unittest.mock import patch

import database.databaseTransactions
from objects import validPositionObject

class Comment:
    link_id = None
    body = None
    def __init__(self, link_id, body):
        self.body = body
        self.link_id = link_id


def createValidPositionObjects(ticker, price, date):
    return validPositionObject.validPosition(ticker, price, date)

def createCommentObject(body, link_id):
    return Comment(link_id, body)

class TestSearchCommentsForPositions(unittest.TestCase):

    @patch('redditScraper.getValidTickersFromPotentialTickers', MagicMock(return_value=["MSFT"]))
    @patch('redditScraper.isStrikePriceRidiculouslyHighOrLow', MagicMock(return_value=False))
    def test_searchCommentsForPositions_ShouldCreateOpenPosition_When_CommentIsValid(self):
        commentObject = createCommentObject("Im gonna get my money MSFT 370p 4/14", "0000123567")
        submission_id = "123567"
        with patch('paperTrading.paperTradingUtilities.openPosition'
                   ) as openPosition:
            redditScraper.searchCommentsForPositions(submission_id, commentObject)
            openPosition.assert_called()

    @patch('redditScraper.getValidTickersFromPotentialTickers', MagicMock(return_value=["MSFT"]))
    def test_searchCommentsForPositions_ShouldNotCreateOpenPosition_When_CommentIdAndSubmissionIdAreDifferent(self):
        commentObject = createCommentObject("Im gonna get my money MSFT 370p 4/14", "0000666666")
        submission_id = "123567"
        with patch('paperTrading.paperTradingUtilities.openPosition'
                   ) as openPosition:
            redditScraper.searchCommentsForPositions(submission_id, commentObject)
            openPosition.assert_not_called()

    @patch('redditScraper.getValidTickersFromPotentialTickers', MagicMock(return_value=["MSFT"]))
    def test_searchCommentsForPositions_ShouldNotCreateOpenPosition_When_CommentContainsUrl(self):
        commentObject = createCommentObject("Im gonna get my money https://www.google.com MSFT 370p 4/14", "0000666666")
        submission_id = "123567"
        with patch('paperTrading.paperTradingUtilities.openPosition'
                   ) as openPosition:
            redditScraper.searchCommentsForPositions(submission_id, commentObject)
            openPosition.assert_not_called()

    @patch('redditScraper.getValidTickersFromPotentialTickers', MagicMock(return_value=["MSFT"]))
    def test_searchCommentsForPositions_ShouldNotCreateOpenPosition_When_UnableToDetermineCallOrPut(self):
        commentObject = createCommentObject("Im gonna get my money MSFT 370 4/14", "0000666666")
        submission_id = "123567"
        with patch('paperTrading.paperTradingUtilities.openPosition'
                   ) as openPosition:
            redditScraper.searchCommentsForPositions(submission_id, commentObject)
            openPosition.assert_not_called()

class TestReturnValidPositionsInComment(unittest.TestCase):
    @patch('redditScraper.getValidTickersFromPotentialTickers', MagicMock(return_value=["MSFT"]))
    def test_returnValidPositionsInComment_ShouldReturnListOfValidPositionObjects_When_ValidPositionsAreFound(self):
        mockPosition = createValidPositionObjects("MSFT", "$179C", "06/19")
        comment = "Money $MSFT printer $179C go 06/19 Brrrr"
        actualPosition = redditScraper.returnValidPositionsInComment(comment)
        self.assertEqual(mockPosition.ticker, actualPosition[0].ticker)
        self.assertEqual(mockPosition.price, actualPosition[0].price)
        self.assertEqual(mockPosition.strikeDate, actualPosition[0].strikeDate)
        self.assertEqual(mockPosition.isCall, actualPosition[0].isCall)

    @patch('redditScraper.getValidTickersFromPotentialTickers', MagicMock(return_value=["MSFT"]))
    def test_returnValidPositionsInComment_ShouldReturnEmptyList_When_MismatchOfPrice(self):
        comment = "300C Money $23.30 $MSFT printer $179C go 06/19 Brrrr"
        actualPosition = redditScraper.returnValidPositionsInComment(comment)
        self.assertEqual([], actualPosition)

    @patch('redditScraper.getValidTickersFromPotentialTickers', MagicMock(return_value=["MSFT", "AAPL", "HBAN"]))
    def test_returnValidPositionsInComment_ShouldReturnEmptyList_When_MismatchOfTicker(self):
        comment = "AAPL Money $MSFT printer $179C go HBAN 06/19 Brrrr"
        actualPosition = redditScraper.returnValidPositionsInComment(comment)
        self.assertEqual([], actualPosition)

    @patch('redditScraper.getValidTickersFromPotentialTickers', MagicMock(return_value=["MSFT"]))
    def test_returnValidPositionsInComment_ShouldReturnEmptyList_When_MismatchOfDate(self):
        comment = "7/13 Money 2/11C printer $179C MSFT go 06/19 Brrrr"
        actualPosition = redditScraper.returnValidPositionsInComment(comment)
        self.assertEqual([], actualPosition)

    @patch('redditScraper.getValidTickersFromPotentialTickers', MagicMock(return_value=["MSFT", "AAPL", "HBAN"]))
    ##This test is broken. Fix Later
    def test_returnValidPositionsInComment_ShouldReturnMultiplePositions_When_MultipleValidPositions(self):
        comment = "AAPL MSFT  HBAN Money printer 45C $179C 11 go 06/19 2/7c 4/18P Brrrr"
        actualPosition = redditScraper.returnValidPositionsInComment(comment)
        self.assertEqual(3, len(actualPosition))

class TestGetValidTickersFromPotentialTickerList(unittest.TestCase):
    #I can't mock functions in files other than the file that I'm testing
    @patch('redditScraper.isTickerInDatabase', MagicMock(return_value=True))
    def test_getValidTickersFromPotentialTickers_ShouldReturnValidTickers_When_ValidTickersInComment(self):
            potentialTickerList = ["MSFT", "$MSFT", "GUH", "$SMH", "FUK", "OTM"]
            self.assertEqual(["MSFT", "MSFT", "SMH"], redditScraper.getValidTickersFromPotentialTickers(potentialTickerList))

    @patch('redditScraper.isTickerInDatabase', MagicMock(return_value=False))
    def test_getValidTickersFromPotentialTickers_ShouldReturnNoTickers_When_NoValidTickersInComment(self):
            potentialTickerList = ["MSFT", "$MSFT", "$SMH"]
            self.assertEqual([], redditScraper.getValidTickersFromPotentialTickers(potentialTickerList))

class TestTicker(unittest.TestCase):
    def test_TickerInComment_shouldReturnTicker_When_ValidTickerInComment(self):
        comment = "n wkjrwbnr wehbfgwh MSFT"
        self.assertEqual(["MSFT"], redditScraper.getTickerInComment(comment))

    def test_TickerInComment_shouldReturnTicker_When_TickerHasDollarSign(self):
        comment = "n wkjrwbnr wehbfgwh $MSFT"
        self.assertEqual(["$MSFT"], redditScraper.getTickerInComment(comment))

    def test_TickerInComment_shouldReturnEmptyList_When_ExclusionWordsInString(self):
        comment = "ALL ER PDT FREE RH ATH NBA NFL NHL UP FUCK US USSR THE ITM AND RIP OTM USD EOD CAD PE YOLO I SAAS " \
                  "GIGS GDP GTFO BTFD EXP MINS PP DD LMAO LOL AMA TLDR RN TME GUH FUK WUT WAT WSB TEH WTF FOMO ROPE IDK " \
                  "AI TP IV DOWN IMO PLS"
        self.assertEqual([], redditScraper.getTickerInComment(comment))

    def test_TickerInComment_shouldReturnTicker_When_TickerIsLowercase(self):
        comment = "n wkjrwbnr wehbfgwh msft"
        self.assertEqual([], redditScraper.getTickerInComment(comment))

class TestPrice(unittest.TestCase):
    def test_PriceInComment_shouldReturnEmptyList_When_PriceAtFrontOfComment(self):
        comment = "300 9/16 ewrgretger"
        self.assertEqual(["300"], redditScraper.getPriceInComment(comment))

    def test_PriceInComment_shouldReturnPriceList_When_PriceContainsDollarSign(self):
        comment = "9/16 $300 ewrgretger"
        self.assertEqual(["$300"], redditScraper.getPriceInComment(comment))

    def test_PriceInComment_shouldReturnPriceList_When_PriceContainsDecimal(self):
        comment = "9/16 $300.00 ewrgretger"
        self.assertEqual(["$300.00"], redditScraper.getPriceInComment(comment))

    def test_PriceInComment_shouldReturnPriceList_When_PriceContainsPutAndCall(self):
        comment = "9/16 $300p 300.50c ewrgretger"
        self.assertEqual(["$300p", "300.50c"], redditScraper.getPriceInComment(comment))

    def test_PriceInComment_shouldReturnPriceList_When_PriceContainsPutAndCallCapital(self):
        comment = "9/16 $300P 300.50C ewrgretger"
        self.assertEqual(["$300P", "300.50C"], redditScraper.getPriceInComment(comment))

    def test_PriceInComment_shouldReturnEmptyList_When_PriceUnderTenDollars(self):
        comment = "9/16 $9.99 $8 ewrgretger"
        self.assertEqual(["$9.99"], redditScraper.getPriceInComment(comment))

class TestStrikeDate(unittest.TestCase):
    def test_StrikeDateInComment_shouldReturnTrue_When_ValidDateAtFrontOnfComment(self):
        comment = "9/16 wngrwng"
        self.assertTrue(redditScraper.getStrikeDatesInComment(comment))

    def test_StrikeDateInComment_shouldReturnTrue_When_ValidDateInComment(self):
        comment = "lsnrw 9/16 wngrwng"
        self.assertTrue(redditScraper.getStrikeDatesInComment(comment))

    def test_StrikeDateInComment_shouldReturnTrue_When_ValidDateAndCallInComment(self):
        comment = "lsnrw 9/16c wngrwng"
        self.assertTrue(redditScraper.getStrikeDatesInComment(comment))

    def test_StrikeDateInComment_shouldReturnTrue_When_ValidDateAndPutInComment(self):
        comment = "lsnrw 9/16p wngrwng"
        self.assertTrue(redditScraper.getStrikeDatesInComment(comment))

    def test_StrikeDateInComment_shouldReturnFalse_When_InvalidDateInComment(self):
        comment = "lsnrw9/16p5/6wngrwng"
        self.assertFalse(redditScraper.getStrikeDatesInComment(comment))

    def test_StrikeDateInComment_shouldReturnFalse_When_DateWithYearInComment(self):
        comment = "lsnrw 2/2020 wngrwng"
        self.assertFalse(redditScraper.getStrikeDatesInComment(comment))

    def test_StrikeDateInComment_shouldReturnFalse_When_DayMonthYearInComment(self):
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