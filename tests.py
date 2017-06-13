import string
import sys
import unittest

from mock import mock, MagicMock, patch

from notes2html import parse, run


class ParserTest(unittest.TestCase):
    def test_whenEmptyString_thenExpectedMarkupBuilt(self):
        self.assert_markup_generated(
            '',

            '<!DOCTYPE html>\n' +
            '<html>\n' +
            '    <head>\n' +
            '        <title></title>\n' +
            '        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">\n' +
            '        <link rel="stylesheet" type="text/css" href="assets/main.css">\n' +
            '        <link rel="icon" type="image/png" sizes="32x32" href="assets/favicon.png">\n' +
            '    </head>\n' +
            '    <body>\n' +
            '    </body>\n' +
            '</html>'
        )

    def test_whenTextHasTitle_thenExpectedMarkupBuilt(self):
        self.assert_markup_generated(
            '*title*',

            '<!DOCTYPE html>\n' +
            '<html>\n' +
            '    <head>\n' +
            '        <title>title</title>\n' +
            '        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">\n' +
            '        <link rel="stylesheet" type="text/css" href="assets/main.css">\n' +
            '        <link rel="icon" type="image/png" sizes="32x32" href="assets/favicon.png">\n' +
            '    </head>\n' +
            '    <body>\n' +
            '    </body>\n' +
            '</html>'
        )

    def test_whenTextHasEmptyTitle_thenExpectedMarkupBuilt(self):
        self.assert_markup_generated(
            '**',

            '<!DOCTYPE html>\n' +
            '<html>\n' +
            '    <head>\n' +
            '        <title></title>\n' +
            '        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">\n' +
            '        <link rel="stylesheet" type="text/css" href="assets/main.css">\n' +
            '        <link rel="icon" type="image/png" sizes="32x32" href="assets/favicon.png">\n' +
            '    </head>\n' +
            '    <body>\n' +
            '    </body>\n' +
            '</html>'
        )

    def test_whenTextHasTitleAndSubtitle_thenExpectedMarkupBuilt(self):
        self.assert_markup_generated(
            '*title*\n' +
            'Subtitle',

            '<!DOCTYPE html>\n' +
            '<html>\n' +
            '    <head>\n' +
            '        <title>title</title>\n' +
            '        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">\n' +
            '        <link rel="stylesheet" type="text/css" href="assets/main.css">\n' +
            '        <link rel="icon" type="image/png" sizes="32x32" href="assets/favicon.png">\n' +
            '    </head>\n' +
            '    <body>\n' +
            '        <fieldset class=\'box\'>\n' +
            '            <legend>Subtitle</legend>\n' +
            '                <ul>\n' +
            '                </ul>\n' +
            '        </fieldset>\n' +
            '    </body>\n' +
            '</html>'
        )

    def test_whenTextHasTitleAndSubtitleAndText_thenExpectedMarkupBuilt(self):
        self.assert_markup_generated(
            '*title*\n' +
            'subtitle\n' +
            '    text',

            '<!DOCTYPE html>\n' +
            '<html>\n' +
            '    <head>\n' +
            '        <title>title</title>\n' +
            '        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">\n' +
            '        <link rel="stylesheet" type="text/css" href="assets/main.css">\n' +
            '        <link rel="icon" type="image/png" sizes="32x32" href="assets/favicon.png">\n' +
            '    </head>\n' +
            '    <body>\n' +
            '        <fieldset class=\'box\'>\n' +
            '            <legend>subtitle</legend>\n' +
            '                <ul>\n' +
            '                    <li><span>\n'
            '                        text\n'
            '                    </span></li>\n' +
            '                </ul>\n' +
            '        </fieldset>\n' +
            '    </body>\n' +
            '</html>'
        )

    def test_whenTextHasTitleAndSubtitleAndTextAndBlankLine_thenExpectedMarkupBuilt(self):
        self.assert_markup_generated(
            '*title*\n' +
            '\n' +
            'subtitle\n' +
            '    text',

            '<!DOCTYPE html>\n' +
            '<html>\n' +
            '    <head>\n' +
            '        <title>title</title>\n' +
            '        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">\n' +
            '        <link rel="stylesheet" type="text/css" href="assets/main.css">\n' +
            '        <link rel="icon" type="image/png" sizes="32x32" href="assets/favicon.png">\n' +
            '    </head>\n' +
            '    <body>\n' +
            '        <fieldset class=\'box\'>\n' +
            '            <legend>subtitle</legend>\n' +
            '                <ul>\n' +
            '                    <li><span>\n'
            '                        text\n'
            '                    </span></li>\n' +
            '                </ul>\n' +
            '        </fieldset>\n' +
            '    </body>\n' +
            '</html>'
        )

    def test_whenTextHasTitleAndSubtitleAndTextAndMultipleLines_thenExpectedMarkupBuilt(self):
        self.assert_markup_generated(
            '*title*\n' +
            '\n' +
            'subtitle\n' +
            '    first text line\n' +
            '    second text line',

            '<!DOCTYPE html>\n' +
            '<html>\n' +
            '    <head>\n' +
            '        <title>title</title>\n' +
            '        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">\n' +
            '        <link rel="stylesheet" type="text/css" href="assets/main.css">\n' +
            '        <link rel="icon" type="image/png" sizes="32x32" href="assets/favicon.png">\n' +
            '    </head>\n' +
            '    <body>\n' +
            '        <fieldset class=\'box\'>\n' +
            '            <legend>subtitle</legend>\n' +
            '                <ul>\n' +
            '                    <li><span>\n'
            '                        first text line\n'
            '                    </span></li>\n' +
            '                    <li><span>\n'
            '                        second text line\n'
            '                    </span></li>\n' +
            '                </ul>\n' +
            '        </fieldset>\n' +
            '    </body>\n' +
            '</html>'
        )

    def test_whenTextHasTitleAndSubtitleAndTextAndFinalIsNested_thenExpectedMarkupBuilt(self):
        self.assert_markup_generated(
            '*title*\n' +
            'subtitle\n' +
            '    text\n' +
            '        nested',

            '<!DOCTYPE html>\n' +
            '<html>\n' +
            '    <head>\n' +
            '        <title>title</title>\n' +
            '        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">\n' +
            '        <link rel="stylesheet" type="text/css" href="assets/main.css">\n' +
            '        <link rel="icon" type="image/png" sizes="32x32" href="assets/favicon.png">\n' +
            '    </head>\n' +
            '    <body>\n' +
            '        <fieldset class=\'box\'>\n' +
            '            <legend>subtitle</legend>\n' +
            '                <ul>\n' +
            '                    <li><span>\n'
            '                        text\n' +
            '                        <ul>\n' +
            '                            <li><span>nested</span></li>\n' +
            '                        </ul>\n' +
            '                    </span></li>\n' +
            '                </ul>\n' +
            '        </fieldset>\n' +
            '    </body>\n' +
            '</html>'
        )

    def test_whenMultipleTextBlocks_thenExpectedMarkupBuilt(self):
        self.assert_markup_generated(
            '*title*\n' +
            '\n' +
            'first subtitle\n' +
            '    first text line\n' +
            '    second text line\n'
            '\n\n' +
            'second subtitle\n' +
            '    first text line of the second block\n' +
            '    second text line of the second block',

            '<!DOCTYPE html>\n' +
            '<html>\n' +
            '    <head>\n' +
            '        <title>title</title>\n' +
            '        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">\n' +
            '        <link rel="stylesheet" type="text/css" href="assets/main.css">\n' +
            '        <link rel="icon" type="image/png" sizes="32x32" href="assets/favicon.png">\n' +
            '    </head>\n' +
            '    <body>\n' +
            '        <fieldset class=\'box\'>\n' +
            '            <legend>first subtitle</legend>\n' +
            '                <ul>\n' +
            '                    <li><span>\n'
            '                        first text line\n'
            '                    </span></li>\n' +
            '                    <li><span>\n'
            '                        second text line\n'
            '                    </span></li>\n' +
            '                </ul>\n' +
            '        </fieldset>\n' +
            '        <fieldset class=\'box\'>\n' +
            '            <legend>second subtitle</legend>\n' +
            '                <ul>\n' +
            '                    <li><span>\n'
            '                        first text line of the second block\n'
            '                    </span></li>\n' +
            '                    <li><span>\n'
            '                        second text line of the second block\n'
            '                    </span></li>\n' +
            '                </ul>\n' +
            '        </fieldset>\n' +
            '    </body>\n' +
            '</html>'
        )

    def test_whenMultipleNestedTextBlocks_thenExpectedMarkupBuilt(self):
        self.assert_markup_generated(
            '*alpha*\n' +
            '\n' +
            'bravo\n' +
            '    charlie\n' +
            '        delta\n' +
            '    echo\n'
            '\n\n' +
            'foxtrot\n' +
            '        golf\n' +
            '    hotel\n' +
            '    india\n' +
            '        juliett\n' +
            'kilo\n' +
            '        lima\n' +
            '    mike\n',

            '<!DOCTYPE html>\n' +
            '<html>\n' +
            '    <head>\n' +
            '        <title>alpha</title>\n' +
            '        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">\n' +
            '        <link rel="stylesheet" type="text/css" href="assets/main.css">\n' +
            '        <link rel="icon" type="image/png" sizes="32x32" href="assets/favicon.png">\n' +
            '    </head>\n' +
            '    <body>\n' +
            '        <fieldset class=\'box\'>\n' +
            '            <legend>bravo</legend>\n' +
            '                <ul>\n' +
            '                    <li><span>\n'
            '                        charlie\n' +
            '                        <ul>\n' +
            '                            <li><span>delta</span></li>\n' +
            '                        </ul>\n'
            '                    </span></li>\n' +
            '                    <li><span>\n'
            '                        echo\n'
            '                    </span></li>\n' +
            '                </ul>\n' +
            '        </fieldset>\n' +
            '        <fieldset class=\'box\'>\n' +
            '            <legend>foxtrot</legend>\n' +
            '                <ul>\n' +
            '                    <li><span>\n'
            '                        <ul>\n' +
            '                            <li><span>golf</span></li>\n' +
            '                        </ul>\n' +
            '                    </span></li>\n'
            '                    <li><span>\n'
            '                        hotel\n'
            '                    </span></li>\n' +
            '                    <li><span>\n'
            '                        india\n' +
            '                        <ul>\n' +
            '                            <li><span>juliett</span></li>\n' +
            '                        </ul>\n' +
            '                    </span></li>\n' +
            '                </ul>\n' +
            '        </fieldset>\n' +
            '        <fieldset class=\'box\'>\n' +
            '            <legend>kilo</legend>\n' +
            '                <ul>\n' +
            '                    <li><span>\n'
            '                        <ul>\n' +
            '                            <li><span>lima</span></li>\n' +
            '                        </ul>\n'
            '                    </span></li>\n' +
            '                    <li><span>\n'
            '                        mike\n'
            '                    </span></li>\n' +
            '                </ul>\n' +
            '        </fieldset>\n' +
            '    </body>\n' +
            '</html>'
        )

    def test_whenNotEnoughArguments_thenExceptionRaised(self):
        sys.argv = ['bin']
        self.assertRaises(Exception, run)

    def test_whenFilesNotFound_thenExceptionRaised(self):
        sys.argv = ['bin', 'in', 'out', 'out']
        self.assertRaises(Exception, run)

    def assert_markup_generated(self, input, expected):
        assert parse(string.split(input, '\n')) == expected

    @mock.patch('notes2html.os.listdir')
    def test_whenEmptyFiles_thenFilesOpen(self, mock_listdir):
        sys.argv = ['bin', 'in', 'out', 'out']
        mock_listdir.return_value = ['a.txt']
        with patch('notes2html.open', create=True) as mock_open:
            mock_open.return_value = MagicMock(spec=file)
            self.assertRaises(StopIteration, run)