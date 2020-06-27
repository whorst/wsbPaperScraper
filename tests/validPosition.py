import unittest
import datetime
import objects.validPositionObject
from objects.validPositionObject import validPosition
from unittest.mock import patch
from unittest.mock import Mock


class TestValidPositionObject(unittest.TestCase):
    def test_formatDate_ShouldRemoveLeadingZero_When_OneExists(self):
        position = validPosition("MSFT", "100", "06/19")
        self.assertEqual("06/19", position.strikeDate)

    def test_formatDate_ShouldNotRemoveLeadingZero_When_OneDoesntExist(self):
        position = validPosition("MSFT", "100", "6/19")
        self.assertEqual("6/19", position.strikeDate)

    # Some pitfalls to this discussed here: https://stackoverflow.com/a/51213128/5233042
    @patch.object(objects.validPositionObject, 'datetime', Mock(wraps=datetime.datetime))
    def test_formatDate_ShouldAddYearToDate_When_YearNotIncluded(self):
        objects.validPositionObject.datetime.utcnow.return_value = datetime.datetime(2020, 2, 3)
        position = validPosition("MSFT", "100", "06/19")
        self.assertEqual("06/19", position.strikeDate)

    @patch.object(objects.validPositionObject, 'datetime', Mock(wraps=datetime.datetime))
    def test_formatDate_ShouldFormatYearAsNextYear_When_StrikeDateMonthEarlierThanCurrentMonth(self):
        objects.validPositionObject.datetime.utcnow.return_value = datetime.datetime(2020, 2, 3)
        position = validPosition("MSFT", "100", "01/01")
        self.assertEqual("01/01", position.strikeDate)

    @patch.object(objects.validPositionObject, 'datetime', Mock(wraps=datetime.datetime))
    def test_formatDate_ShouldFormatDate_When_StrikeDateIncludesPutOrCall(self):
        objects.validPositionObject.datetime.utcnow.return_value = datetime.datetime(2020, 2, 3)
        position = validPosition("MSFT", "100", "01/01p")
        self.assertEqual("01/01p", position.strikeDate)

if __name__ == '__main__':
    unittest.main()