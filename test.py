import re
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
            '        <link rel="stylesheet" type="text/css" href="/assets/main.css">\n' +
            '        <link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon.png">\n' +
            '        <script src="/assets/syntaxhighlighter.js"></script>\n' +
            '    </head>\n' +
            '    <body>\n' +
            '        <fieldset class=\'box\'>\n' +
            '            <legend> ToC</legend>\n' +
            '                <ul>\n' +
            '                </ul>\n' +
            '        </fieldset>\n' +
            '    <script>new Highlighter().run(document);</script>\n' +
            '    <script> (function(i,s,o,g,r,a,m){i[\'GoogleAnalyticsObject\']=r;i[r]=i[r]||function(){ (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o), m = s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m) })(window,document,\'script\',\'https://www.google-analytics.com/analytics.js\',\'ga\'); ga(\'create\', \'UA-106217827-1\', \'auto\'); ga(\'send\', \'pageview\'); </script>\n' +
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
            '        <link rel="stylesheet" type="text/css" href="/assets/main.css">\n' +
            '        <link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon.png">\n' +
            '        <script src="/assets/syntaxhighlighter.js"></script>\n' +
            '    </head>\n' +
            '    <body>\n' +
            '        <fieldset class=\'box\'>\n' +
            '            <legend>title ToC</legend>\n' +
            '                <ul>\n' +
            '                </ul>\n' +
            '        </fieldset>\n' +
            '    <script>new Highlighter().run(document);</script>\n' +
            '    <script> (function(i,s,o,g,r,a,m){i[\'GoogleAnalyticsObject\']=r;i[r]=i[r]||function(){ (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o), m = s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m) })(window,document,\'script\',\'https://www.google-analytics.com/analytics.js\',\'ga\'); ga(\'create\', \'UA-106217827-1\', \'auto\'); ga(\'send\', \'pageview\'); </script>\n' +
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
            '        <link rel="stylesheet" type="text/css" href="/assets/main.css">\n' +
            '        <link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon.png">\n' +
            '        <script src="/assets/syntaxhighlighter.js"></script>\n' +
            '    </head>\n' +
            '    <body>\n' +
            '        <fieldset class=\'box\'>\n' +
            '            <legend> ToC</legend>\n' +
            '                <ul>\n' +
            '                </ul>\n' +
            '        </fieldset>\n' +
            '    <script>new Highlighter().run(document);</script>\n' +
            '    <script> (function(i,s,o,g,r,a,m){i[\'GoogleAnalyticsObject\']=r;i[r]=i[r]||function(){ (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o), m = s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m) })(window,document,\'script\',\'https://www.google-analytics.com/analytics.js\',\'ga\'); ga(\'create\', \'UA-106217827-1\', \'auto\'); ga(\'send\', \'pageview\'); </script>\n' +
            '    </body>\n' +
            '</html>'
        )

    def test_whenTextHasTitleAndSubtitle_thenExpectedMarkupBuilt(self):
        self.assert_exception_thrown(
            '*title*\n' +
            'Subtitle',
            "Failed to parse, found title[Subtitle] with no text"
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
            '        <link rel="stylesheet" type="text/css" href="/assets/main.css">\n' +
            '        <link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon.png">\n' +
            '        <script src="/assets/syntaxhighlighter.js"></script>\n' +
            '    </head>\n' +
            '    <body>\n' +
            '        <fieldset class=\'box\'>\n' +
            '            <legend>title ToC</legend>\n' +
            '                <ul>\n' +
            '                    <li><span><a href=\'#subtitle\'>subtitle</a></span></li>\n' +
            '                </ul>\n' +
            '        </fieldset>\n' +
            '        <fieldset class=\'box\'>\n' +
            '            <a name=\'subtitle\'></a>\n' +
            '            <legend>subtitle</legend>\n' +
            '                <ul>\n' +
            '                    <li><span>text</span></li>\n' +
            '                </ul>\n' +
            '        </fieldset>\n' +
            '    <script>new Highlighter().run(document);</script>\n' +
            '    <script> (function(i,s,o,g,r,a,m){i[\'GoogleAnalyticsObject\']=r;i[r]=i[r]||function(){ (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o), m = s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m) })(window,document,\'script\',\'https://www.google-analytics.com/analytics.js\',\'ga\'); ga(\'create\', \'UA-106217827-1\', \'auto\'); ga(\'send\', \'pageview\'); </script>\n' +
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
            '        <link rel="stylesheet" type="text/css" href="/assets/main.css">\n' +
            '        <link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon.png">\n' +
            '        <script src="/assets/syntaxhighlighter.js"></script>\n' +
            '    </head>\n' +
            '    <body>\n' +
            '        <fieldset class=\'box\'>\n' +
            '            <legend>title ToC</legend>\n' +
            '                <ul>\n' +
            '                    <li><span><a href=\'#subtitle\'>subtitle</a></span></li>\n' +
            '                </ul>\n' +
            '        </fieldset>\n' +
            '        <fieldset class=\'box\'>\n' +
            '            <a name=\'subtitle\'></a>\n' +
            '            <legend>subtitle</legend>\n' +
            '                <ul>\n' +
            '                    <li><span>text</span></li>\n' +
            '                </ul>\n' +
            '        </fieldset>\n' +
            '    <script>new Highlighter().run(document);</script>\n' +
            '    <script> (function(i,s,o,g,r,a,m){i[\'GoogleAnalyticsObject\']=r;i[r]=i[r]||function(){ (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o), m = s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m) })(window,document,\'script\',\'https://www.google-analytics.com/analytics.js\',\'ga\'); ga(\'create\', \'UA-106217827-1\', \'auto\'); ga(\'send\', \'pageview\'); </script>\n' +
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
            '        <link rel="stylesheet" type="text/css" href="/assets/main.css">\n' +
            '        <link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon.png">\n' +
            '        <script src="/assets/syntaxhighlighter.js"></script>\n' +
            '    </head>\n' +
            '    <body>\n' +
            '        <fieldset class=\'box\'>\n' +
            '            <legend>title ToC</legend>\n' +
            '                <ul>\n' +
            '                    <li><span><a href=\'#subtitle\'>subtitle</a></span></li>\n' +
            '                </ul>\n' +
            '        </fieldset>\n' +
            '        <fieldset class=\'box\'>\n' +
            '            <a name=\'subtitle\'></a>\n' +
            '            <legend>subtitle</legend>\n' +
            '                <ul>\n' +
            '                    <li><span>first text line</span></li>\n' +
            '                    <li><span>second text line</span></li>\n' +
            '                </ul>\n' +
            '        </fieldset>\n' +
            '    <script>new Highlighter().run(document);</script>\n' +
            '    <script> (function(i,s,o,g,r,a,m){i[\'GoogleAnalyticsObject\']=r;i[r]=i[r]||function(){ (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o), m = s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m) })(window,document,\'script\',\'https://www.google-analytics.com/analytics.js\',\'ga\'); ga(\'create\', \'UA-106217827-1\', \'auto\'); ga(\'send\', \'pageview\'); </script>\n' +
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
            '        <link rel="stylesheet" type="text/css" href="/assets/main.css">\n' +
            '        <link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon.png">\n' +
            '        <script src="/assets/syntaxhighlighter.js"></script>\n' +
            '    </head>\n' +
            '    <body>\n' +
            '        <fieldset class=\'box\'>\n' +
            '            <legend>title ToC</legend>\n' +
            '                <ul>\n' +
            '                    <li><span><a href=\'#subtitle\'>subtitle</a></span></li>\n' +
            '                </ul>\n' +
            '        </fieldset>\n' +
            '        <fieldset class=\'box\'>\n' +
            '            <a name=\'subtitle\'></a>\n' +
            '            <legend>subtitle</legend>\n' +
            '                <ul>\n' +
            '                    <li><span>text</span></li>\n' +
            '                        <ul>\n' +
            '                            <li><span>nested</span></li>\n' +
            '                        </ul>\n' +
            '                </ul>\n' +
            '        </fieldset>\n' +
            '    <script>new Highlighter().run(document);</script>\n' +
            '    <script> (function(i,s,o,g,r,a,m){i[\'GoogleAnalyticsObject\']=r;i[r]=i[r]||function(){ (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o), m = s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m) })(window,document,\'script\',\'https://www.google-analytics.com/analytics.js\',\'ga\'); ga(\'create\', \'UA-106217827-1\', \'auto\'); ga(\'send\', \'pageview\'); </script>\n' +
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
            '        <link rel="stylesheet" type="text/css" href="/assets/main.css">\n' +
            '        <link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon.png">\n' +
            '        <script src="/assets/syntaxhighlighter.js"></script>\n' +
            '    </head>\n' +
            '    <body>\n' +
            '        <fieldset class=\'box\'>\n' +
            '            <legend>title ToC</legend>\n' +
            '                <ul>\n' +
            '                    <li><span><a href=\'#first subtitle\'>first subtitle</a></span></li>\n' +
            '                    <li><span><a href=\'#second subtitle\'>second subtitle</a></span></li>\n' +
            '                </ul>\n' +
            '        </fieldset>\n' +
            '        <fieldset class=\'box\'>\n' +
            '            <a name=\'first subtitle\'></a>\n' +
            '            <legend>first subtitle</legend>\n' +
            '                <ul>\n' +
            '                    <li><span>first text line</span></li>\n' +
            '                    <li><span>second text line</span></li>\n' +
            '                </ul>\n' +
            '        </fieldset>\n' +
            '        <fieldset class=\'box\'>\n' +
            '            <a name=\'second subtitle\'></a>\n' +
            '            <legend>second subtitle</legend>\n' +
            '                <ul>\n' +
            '                    <li><span>first text line of the second block</span></li>\n' +
            '                    <li><span>second text line of the second block</span></li>\n' +
            '                </ul>\n' +
            '        </fieldset>\n' +
            '    <script>new Highlighter().run(document);</script>\n' +
            '    <script> (function(i,s,o,g,r,a,m){i[\'GoogleAnalyticsObject\']=r;i[r]=i[r]||function(){ (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o), m = s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m) })(window,document,\'script\',\'https://www.google-analytics.com/analytics.js\',\'ga\'); ga(\'create\', \'UA-106217827-1\', \'auto\'); ga(\'send\', \'pageview\'); </script>\n' +
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
            '        <link rel="stylesheet" type="text/css" href="/assets/main.css">\n' +
            '        <link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon.png">\n' +
            '        <script src="/assets/syntaxhighlighter.js"></script>\n' +
            '    </head>\n' +
            '    <body>\n' +
            '        <fieldset class=\'box\'>\n' +
            '            <legend>alpha ToC</legend>\n' +
            '                <ul>\n' +
            '                    <li><span><a href=\'#bravo\'>bravo</a></span></li>\n' +
            '                    <li><span><a href=\'#foxtrot\'>foxtrot</a></span></li>\n' +
            '                    <li><span><a href=\'#kilo\'>kilo</a></span></li>\n' +
            '                </ul>\n' +
            '        </fieldset>\n' +
            '        <fieldset class=\'box\'>\n' +
            '            <a name=\'bravo\'></a>\n' +
            '            <legend>bravo</legend>\n' +
            '                <ul>\n' +
            '                    <li><span>charlie</span></li>\n' +
            '                        <ul>\n' +
            '                            <li><span>delta</span></li>\n' +
            '                        </ul>\n'
            '                    <li><span>echo</span></li>\n' +
            '                </ul>\n' +
            '        </fieldset>\n' +
            '        <fieldset class=\'box\'>\n' +
            '            <a name=\'foxtrot\'></a>\n' +
            '            <legend>foxtrot</legend>\n' +
            '                <ul>\n' +
            '                        <ul>\n' +
            '                            <li><span>golf</span></li>\n' +
            '                        </ul>\n' +
            '                    <li><span>hotel</span></li>\n' +
            '                    <li><span>india</span></li>\n' +
            '                        <ul>\n' +
            '                            <li><span>juliett</span></li>\n' +
            '                        </ul>\n' +
            '                </ul>\n' +
            '        </fieldset>\n' +
            '        <fieldset class=\'box\'>\n' +
            '            <a name=\'kilo\'></a>\n' +
            '            <legend>kilo</legend>\n' +
            '                <ul>\n' +
            '                        <ul>\n' +
            '                            <li><span>lima</span></li>\n' +
            '                        </ul>\n'
            '                    <li><span>mike</span></li>\n' +
            '                </ul>\n' +
            '        </fieldset>\n' +
            '    <script>new Highlighter().run(document);</script>\n' +
            '    <script> (function(i,s,o,g,r,a,m){i[\'GoogleAnalyticsObject\']=r;i[r]=i[r]||function(){ (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o), m = s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m) })(window,document,\'script\',\'https://www.google-analytics.com/analytics.js\',\'ga\'); ga(\'create\', \'UA-106217827-1\', \'auto\'); ga(\'send\', \'pageview\'); </script>\n' +
            '    </body>\n' +
            '</html>'
        )

    def test_whenNotEnoughArguments_thenExceptionRaised(self):
        sys.argv = ['bin']
        self.assertRaises(Exception, run)

    def test_whenFilesNotFound_thenExceptionRaised(self):
        sys.argv = ['bin', 'in']
        self.assertRaises(Exception, run)

    @mock.patch('notes2html.os.listdir')
    def test_whenEmptyFiles_thenFilesOpen(self, mock_listdir):
        sys.argv = ['bin', 'in', 'out', 'out']
        mock_listdir.return_value = ['a.txt']
        with patch('notes2html.open', create=True) as mock_open:
            mock_open.return_value = MagicMock(spec=file)
            run()

    def test_whenNarrativeAttribute_thenExpectedMarkupBuilt(self):
        self.assert_markup_generated(
            '*alpha*narrative',

            '<!DOCTYPE html>\n' +
            '<html>\n' +
            '    <head>\n' +
            '        <title>alpha</title>\n' +
            '        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">\n' +
            '        <link rel="stylesheet" type="text/css" href="/assets/main.css">\n' +
            '        <link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon.png">\n' +
            '        <script src="/assets/syntaxhighlighter.js"></script>\n' +
            '    </head>\n' +
            '    <body>\n' +
            '        <fieldset class=\'box\'>\n' +
            '            <legend>alpha ToC</legend>\n' +
            '                <ul>\n' +
            '                </ul>\n' +
            '        </fieldset>\n' +
            '    <script>new Highlighter().run(document);</script>\n' +
            '    <script> (function(i,s,o,g,r,a,m){i[\'GoogleAnalyticsObject\']=r;i[r]=i[r]||function(){ (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o), m = s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m) })(window,document,\'script\',\'https://www.google-analytics.com/analytics.js\',\'ga\'); ga(\'create\', \'UA-106217827-1\', \'auto\'); ga(\'send\', \'pageview\'); </script>\n' +
            '    </body>\n' +
            '</html>'
        )

    def test_whenNarrativeAttributeAndSubtitle_thenExceptionThrown(self):
        self.assert_exception_thrown(
            '*alpha*narrative\n'
            'bravo',
            'Failed to parse, found title[bravo] with no text'
        )

    def test_whenNarrativeAttributeAndSubtitleAndParagraph_thenExpectedMarkupBuilt(self):
        self.assert_markup_generated(
            '*alpha*narrative\n'
            'bravo\n'
            '    charlie',

            '<!DOCTYPE html>\n' +
            '<html>\n' +
            '    <head>\n' +
            '        <title>alpha</title>\n' +
            '        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">\n' +
            '        <link rel="stylesheet" type="text/css" href="/assets/main.css">\n' +
            '        <link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon.png">\n' +
            '        <script src="/assets/syntaxhighlighter.js"></script>\n' +
            '    </head>\n' +
            '    <body>\n' +
            '        <fieldset class=\'box\'>\n' +
            '            <legend>alpha ToC</legend>\n' +
            '                <ul>\n' +
            '                    <li><span><a href=\'#bravo\'>bravo</a></span></li>\n' +
            '                </ul>\n' +
            '        </fieldset>\n' +
            '        <fieldset class=\'box\'>\n' +
            '            <a name=\'bravo\'></a>\n' +
            '            <legend>bravo</legend>\n' +
            '                <p>charlie</p>\n' +
            '        </fieldset>\n' +
            '    <script>new Highlighter().run(document);</script>\n' +
            '    <script> (function(i,s,o,g,r,a,m){i[\'GoogleAnalyticsObject\']=r;i[r]=i[r]||function(){ (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o), m = s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m) })(window,document,\'script\',\'https://www.google-analytics.com/analytics.js\',\'ga\'); ga(\'create\', \'UA-106217827-1\', \'auto\'); ga(\'send\', \'pageview\'); </script>\n' +
            '    </body>\n' +
            '</html>'
        )

    def test_whenNarrativeAttributeAndSubtitleAndMultipleParagraphs_thenExpectedMarkupBuilt(self):
        self.assert_markup_generated(
            '*alpha*narrative\n'
            'bravo\n'
            '    charlie\n' +
            '    delta\n',

            '<!DOCTYPE html>\n' +
            '<html>\n' +
            '    <head>\n' +
            '        <title>alpha</title>\n' +
            '        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">\n' +
            '        <link rel="stylesheet" type="text/css" href="/assets/main.css">\n' +
            '        <link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon.png">\n' +
            '        <script src="/assets/syntaxhighlighter.js"></script>\n' +
            '    </head>\n' +
            '    <body>\n' +
            '        <fieldset class=\'box\'>\n' +
            '            <legend>alpha ToC</legend>\n' +
            '                <ul>\n' +
            '                    <li><span><a href=\'#bravo\'>bravo</a></span></li>\n' +
            '                </ul>\n' +
            '        </fieldset>\n' +
            '        <fieldset class=\'box\'>\n' +
            '            <a name=\'bravo\'></a>\n' +
            '            <legend>bravo</legend>\n' +
            '                <p>charlie</p>\n' +
            '                <p>delta</p>\n' +
            '        </fieldset>\n' +
            '    <script>new Highlighter().run(document);</script>\n' +
            '    <script> (function(i,s,o,g,r,a,m){i[\'GoogleAnalyticsObject\']=r;i[r]=i[r]||function(){ (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o), m = s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m) })(window,document,\'script\',\'https://www.google-analytics.com/analytics.js\',\'ga\'); ga(\'create\', \'UA-106217827-1\', \'auto\'); ga(\'send\', \'pageview\'); </script>\n' +
            '    </body>\n' +
            '</html>'
        )

    def test_whenNarrativeAttributeAndSubtitleAndMultipleComplexParagraphs_thenExpectedMarkupBuilt(self):
        self.assert_markup_generated(
            '*alpha*narrative\n' +
            'bravo\n' +
            '    charlie\n' +
            '    delta\n' +
            '\n\n'
            'echo\n' +
            '    foxtrot\n' +
            '    golf\n',

            '<!DOCTYPE html>\n' +
            '<html>\n' +
            '    <head>\n' +
            '        <title>alpha</title>\n' +
            '        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">\n' +
            '        <link rel="stylesheet" type="text/css" href="/assets/main.css">\n' +
            '        <link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon.png">\n' +
            '        <script src="/assets/syntaxhighlighter.js"></script>\n' +
            '    </head>\n' +
            '    <body>\n' +
            '        <fieldset class=\'box\'>\n' +
            '            <legend>alpha ToC</legend>\n' +
            '                <ul>\n' +
            '                    <li><span><a href=\'#bravo\'>bravo</a></span></li>\n' +
            '                    <li><span><a href=\'#echo\'>echo</a></span></li>\n' +
            '                </ul>\n' +
            '        </fieldset>\n' +
            '        <fieldset class=\'box\'>\n' +
            '            <a name=\'bravo\'></a>\n' +
            '            <legend>bravo</legend>\n' +
            '                <p>charlie</p>\n' +
            '                <p>delta</p>\n' +
            '        </fieldset>\n' +
            '        <fieldset class=\'box\'>\n' +
            '            <a name=\'echo\'></a>\n' +
            '            <legend>echo</legend>\n' +
            '                <p>foxtrot</p>\n' +
            '                <p>golf</p>\n' +
            '        </fieldset>\n' +
            '    <script>new Highlighter().run(document);</script>\n' +
            '    <script> (function(i,s,o,g,r,a,m){i[\'GoogleAnalyticsObject\']=r;i[r]=i[r]||function(){ (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o), m = s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m) })(window,document,\'script\',\'https://www.google-analytics.com/analytics.js\',\'ga\'); ga(\'create\', \'UA-106217827-1\', \'auto\'); ga(\'send\', \'pageview\'); </script>\n' +
            '    </body>\n' +
            '</html>'
        )

    def test_whenNarrativeAttributeAndCodeAttribute_thenExpectedMarkupBuilt(self):
        self.assert_markup_generated(
            '*alpha*narrative\n' +
            'bravo\n' +
            '    charlie\n' +
            '    **delta** echo\n',

            '<!DOCTYPE html>\n' +
            '<html>\n' +
            '    <head>\n' +
            '        <title>alpha</title>\n' +
            '        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">\n' +
            '        <link rel="stylesheet" type="text/css" href="/assets/main.css">\n' +
            '        <link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon.png">\n' +
            '        <script src="/assets/syntaxhighlighter.js"></script>\n' +
            '    </head>\n' +
            '    <body>\n' +
            '        <fieldset class=\'box\'>\n' +
            '            <legend>alpha ToC</legend>\n' +
            '                <ul>\n' +
            '                    <li><span><a href=\'#bravo\'>bravo</a></span></li>\n' +
            '                </ul>\n' +
            '        </fieldset>\n' +
            '        <fieldset class=\'box\'>\n' +
            '            <a name=\'bravo\'></a>\n' +
            '            <legend>bravo</legend>\n' +
            '                <p>charlie</p>\n' +
            '                <p><strong>delta</strong> echo</p>\n' +
            '        </fieldset>\n' +
            '    <script>new Highlighter().run(document);</script>\n' +
            '    <script> (function(i,s,o,g,r,a,m){i[\'GoogleAnalyticsObject\']=r;i[r]=i[r]||function(){ (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o), m = s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m) })(window,document,\'script\',\'https://www.google-analytics.com/analytics.js\',\'ga\'); ga(\'create\', \'UA-106217827-1\', \'auto\'); ga(\'send\', \'pageview\'); </script>\n' +
            '    </body>\n' +
            '</html>'
        )

    def test_whenNarrativeAttributeAndTwoLineCodeAttribute_thenExpectedMarkupBuilt(self):
        self.assert_markup_generated(
            '*alpha*narrative\n' +
            'bravo\n' +
            '    charlie\n' +
            '    *delta\n'
            '\n'
            '    echo*\n',

            '<!DOCTYPE html>\n' +
            '<html>\n' +
            '    <head>\n' +
            '        <title>alpha</title>\n' +
            '        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">\n' +
            '        <link rel="stylesheet" type="text/css" href="/assets/main.css">\n' +
            '        <link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon.png">\n' +
            '        <script src="/assets/syntaxhighlighter.js"></script>\n' +
            '    </head>\n' +
            '    <body>\n' +
            '        <fieldset class=\'box\'>\n' +
            '            <legend>alpha ToC</legend>\n' +
            '                <ul>\n' +
            '                    <li><span><a href=\'#bravo\'>bravo</a></span></li>\n' +
            '                </ul>\n' +
            '        </fieldset>\n' +
            '        <fieldset class=\'box\'>\n' +
            '            <a name=\'bravo\'></a>\n' +
            '            <legend>bravo</legend>\n' +
            '                <p>charlie</p>\n' +
            '                <pre><code>delta\n'
            '\n' +
            '    echo</code></pre>\n' +
            '        </fieldset>\n' +
            '    <script>new Highlighter().run(document);</script>\n' +
            '    <script> (function(i,s,o,g,r,a,m){i[\'GoogleAnalyticsObject\']=r;i[r]=i[r]||function(){ (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o), m = s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m) })(window,document,\'script\',\'https://www.google-analytics.com/analytics.js\',\'ga\'); ga(\'create\', \'UA-106217827-1\', \'auto\'); ga(\'send\', \'pageview\'); </script>\n' +
            '    </body>\n' +
            '</html>'
        )

    def test_whenNarrativeAttributeAndMultipleLineCodeAttributeAndCodeHasMassiveIndentation_thenExpectedMarkupBuilt(self):
        self.assert_markup_generated(
            '*alpha*narrative\n' +
            'bravo\n' +
            '    charlie\n' +
            '    *delta\n' +
            '                      echo\n' +
            '    foxtrot*\n',

            '<!DOCTYPE html>\n' +
            '<html>\n' +
            '    <head>\n' +
            '        <title>alpha</title>\n' +
            '        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">\n' +
            '        <link rel="stylesheet" type="text/css" href="/assets/main.css">\n' +
            '        <link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon.png">\n' +
            '        <script src="/assets/syntaxhighlighter.js"></script>\n' +
            '    </head>\n' +
            '    <body>\n' +
            '        <fieldset class=\'box\'>\n' +
            '            <legend>alpha ToC</legend>\n' +
            '                <ul>\n' +
            '                    <li><span><a href=\'#bravo\'>bravo</a></span></li>\n' +
            '                </ul>\n' +
            '        </fieldset>\n' +
            '        <fieldset class=\'box\'>\n' +
            '            <a name=\'bravo\'></a>\n' +
            '            <legend>bravo</legend>\n' +
            '                <p>charlie</p>\n' +
            '                <pre><code>delta\n'
            '                      echo\n'
            '    foxtrot</code></pre>\n' +
            '        </fieldset>\n' +
            '    <script>new Highlighter().run(document);</script>\n' +
            '    <script> (function(i,s,o,g,r,a,m){i[\'GoogleAnalyticsObject\']=r;i[r]=i[r]||function(){ (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o), m = s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m) })(window,document,\'script\',\'https://www.google-analytics.com/analytics.js\',\'ga\'); ga(\'create\', \'UA-106217827-1\', \'auto\'); ga(\'send\', \'pageview\'); </script>\n' +
            '    </body>\n' +
            '</html>'
        )

    def test_whenNarrativeHasStrongTag_thenExpectedMarkupBuilt(self):
        self.assert_markup_generated(
            '*alpha*narrative\n' +
            'bravo\n' +
            '    charlie **delta** echo\n',

            '<!DOCTYPE html>\n' +
            '<html>\n' +
            '    <head>\n' +
            '        <title>alpha</title>\n' +
            '        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">\n' +
            '        <link rel="stylesheet" type="text/css" href="/assets/main.css">\n' +
            '        <link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon.png">\n' +
            '        <script src="/assets/syntaxhighlighter.js"></script>\n' +
            '    </head>\n' +
            '    <body>\n' +
            '        <fieldset class=\'box\'>\n' +
            '            <legend>alpha ToC</legend>\n' +
            '                <ul>\n' +
            '                    <li><span><a href=\'#bravo\'>bravo</a></span></li>\n' +
            '                </ul>\n' +
            '        </fieldset>\n' +
            '        <fieldset class=\'box\'>\n' +
            '            <a name=\'bravo\'></a>\n' +
            '            <legend>bravo</legend>\n' +
            '                <p>charlie <strong>delta</strong> echo</p>\n' +
            '        </fieldset>\n' +
            '    <script>new Highlighter().run(document);</script>\n' +
            '    <script> (function(i,s,o,g,r,a,m){i[\'GoogleAnalyticsObject\']=r;i[r]=i[r]||function(){ (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o), m = s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m) })(window,document,\'script\',\'https://www.google-analytics.com/analytics.js\',\'ga\'); ga(\'create\', \'UA-106217827-1\', \'auto\'); ga(\'send\', \'pageview\'); </script>\n' +
            '    </body>\n' +
            '</html>'
        )

    def test_whenTextAttributeAndCodeAttribute_thenExpectedMarkupBuilt(self):
        self.assert_markup_generated(
            '*alpha*\n' +
            'bravo\n' +
            '    charlie\n' +
            '    **delta**\n',

            '<!DOCTYPE html>\n' +
            '<html>\n' +
            '    <head>\n' +
            '        <title>alpha</title>\n' +
            '        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">\n' +
            '        <link rel="stylesheet" type="text/css" href="/assets/main.css">\n' +
            '        <link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon.png">\n' +
            '        <script src="/assets/syntaxhighlighter.js"></script>\n' +
            '    </head>\n' +
            '    <body>\n' +
            '        <fieldset class=\'box\'>\n' +
            '            <legend>alpha ToC</legend>\n' +
            '                <ul>\n' +
            '                    <li><span><a href=\'#bravo\'>bravo</a></span></li>\n' +
            '                </ul>\n' +
            '        </fieldset>\n' +
            '        <fieldset class=\'box\'>\n' +
            '            <a name=\'bravo\'></a>\n' +
            '            <legend>bravo</legend>\n' +
            '                <ul>\n' +
            '                    <li><span>charlie</span></li>\n' +
            '                    <li><span><strong>delta</strong></span></li>\n' +
            '                </ul>\n' +
            '        </fieldset>\n' +
            '    <script>new Highlighter().run(document);</script>\n' +
            '    <script> (function(i,s,o,g,r,a,m){i[\'GoogleAnalyticsObject\']=r;i[r]=i[r]||function(){ (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o), m = s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m) })(window,document,\'script\',\'https://www.google-analytics.com/analytics.js\',\'ga\'); ga(\'create\', \'UA-106217827-1\', \'auto\'); ga(\'send\', \'pageview\'); </script>\n' +
            '    </body>\n' +
            '</html>'
        )

    def test_whenTextAttributeAndTwoLineCodeAttribute_thenExpectedMarkupBuilt(self):
        self.assert_markup_generated(
            '*alpha*\n' +
            'bravo\n' +
            '    charlie\n' +
            '    *delta\n'
            '\n'
            'echo*\n',

            '<!DOCTYPE html>\n' +
            '<html>\n' +
            '    <head>\n' +
            '        <title>alpha</title>\n' +
            '        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">\n' +
            '        <link rel="stylesheet" type="text/css" href="/assets/main.css">\n' +
            '        <link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon.png">\n' +
            '        <script src="/assets/syntaxhighlighter.js"></script>\n' +
            '    </head>\n' +
            '    <body>\n' +
            '        <fieldset class=\'box\'>\n' +
            '            <legend>alpha ToC</legend>\n' +
            '                <ul>\n' +
            '                    <li><span><a href=\'#bravo\'>bravo</a></span></li>\n' +
            '                </ul>\n' +
            '        </fieldset>\n' +
            '        <fieldset class=\'box\'>\n' +
            '            <a name=\'bravo\'></a>\n' +
            '            <legend>bravo</legend>\n' +
            '                <ul>\n' +
            '                    <li><span>charlie</span></li>\n' +
            '                <pre><code>delta\n'
            '\n' +
            'echo</code></pre>\n' +
            '                </ul>\n' +
            '        </fieldset>\n' +
            '    <script>new Highlighter().run(document);</script>\n' +
            '    <script> (function(i,s,o,g,r,a,m){i[\'GoogleAnalyticsObject\']=r;i[r]=i[r]||function(){ (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o), m = s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m) })(window,document,\'script\',\'https://www.google-analytics.com/analytics.js\',\'ga\'); ga(\'create\', \'UA-106217827-1\', \'auto\'); ga(\'send\', \'pageview\'); </script>\n' +
            '    </body>\n' +
            '</html>'
        )

    def test_whenTextAttributeAndMultipleLineCodeAttribute_thenExpectedMarkupBuilt(self):
        self.assert_markup_generated(
            '*alpha*\n' +
            'bravo\n' +
            '    charlie\n' +
            '    *delta\n' +
            'echo\n' +
            '        foxtrot*\n',

            '<!DOCTYPE html>\n' +
            '<html>\n' +
            '    <head>\n' +
            '        <title>alpha</title>\n' +
            '        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">\n' +
            '        <link rel="stylesheet" type="text/css" href="/assets/main.css">\n' +
            '        <link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon.png">\n' +
            '        <script src="/assets/syntaxhighlighter.js"></script>\n' +
            '    </head>\n' +
            '    <body>\n' +
            '        <fieldset class=\'box\'>\n' +
            '            <legend>alpha ToC</legend>\n' +
            '                <ul>\n' +
            '                    <li><span><a href=\'#bravo\'>bravo</a></span></li>\n' +
            '                </ul>\n' +
            '        </fieldset>\n' +
            '        <fieldset class=\'box\'>\n' +
            '            <a name=\'bravo\'></a>\n' +
            '            <legend>bravo</legend>\n' +
            '                <ul>\n' +
            '                    <li><span>charlie</span></li>\n' +
            '                <pre><code>delta\n'
            'echo\n'
            '        foxtrot</code></pre>\n' +
            '                </ul>\n' +
            '        </fieldset>\n' +
            '    <script>new Highlighter().run(document);</script>\n' +
            '    <script> (function(i,s,o,g,r,a,m){i[\'GoogleAnalyticsObject\']=r;i[r]=i[r]||function(){ (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o), m = s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m) })(window,document,\'script\',\'https://www.google-analytics.com/analytics.js\',\'ga\'); ga(\'create\', \'UA-106217827-1\', \'auto\'); ga(\'send\', \'pageview\'); </script>\n' +
            '    </body>\n' +
            '</html>'
        )

    def test_whenTextHasStrongTag_thenExpectedMarkupBuilt(self):
        self.assert_markup_generated(
            '*alpha*\n' +
            'bravo\n' +
            '    charlie **<$delta>** echo\n',

            '<!DOCTYPE html>\n'
            '<html>\n' +
            '    <head>\n' +
            '        <title>alpha</title>\n' +
            '        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">\n' +
            '        <link rel="stylesheet" type="text/css" href="/assets/main.css">\n' +
            '        <link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon.png">\n' +
            '        <script src="/assets/syntaxhighlighter.js"></script>\n' +
            '    </head>\n' +
            '    <body>\n' +
            '        <fieldset class=\'box\'>\n' +
            '            <legend>alpha ToC</legend>\n' +
            '                <ul>\n' +
            '                    <li><span><a href=\'#bravo\'>bravo</a></span></li>\n' +
            '                </ul>\n' +
            '        </fieldset>\n' +
            '        <fieldset class=\'box\'>\n' +
            '            <a name=\'bravo\'></a>\n' +
            '            <legend>bravo</legend>\n' +
            '                <ul>\n' +
            '                    <li><span>charlie <strong>&lt;$delta&gt;</strong> echo</span></li>\n' +
            '                </ul>\n' +
            '        </fieldset>\n' +
            '    <script>new Highlighter().run(document);</script>\n' +
            '    <script> (function(i,s,o,g,r,a,m){i[\'GoogleAnalyticsObject\']=r;i[r]=i[r]||function(){ (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o), m = s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m) })(window,document,\'script\',\'https://www.google-analytics.com/analytics.js\',\'ga\'); ga(\'create\', \'UA-106217827-1\', \'auto\'); ga(\'send\', \'pageview\'); </script>\n' +
            '    </body>\n' +
            '</html>'
        )

    def test_whenListHasNestedCode_thenExpectedMarkupBuilt(self):
        self.assert_markup_generated(
            '*alpha*\n' +
            'bravo\n' +
            '    charlie\n'+
            '        *delta echo*\n',

            '<!DOCTYPE html>\n'
            '<html>\n' +
            '    <head>\n' +
            '        <title>alpha</title>\n' +
            '        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">\n' +
            '        <link rel="stylesheet" type="text/css" href="/assets/main.css">\n' +
            '        <link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon.png">\n' +
            '        <script src="/assets/syntaxhighlighter.js"></script>\n' +
            '    </head>\n' +
            '    <body>\n' +
            '        <fieldset class=\'box\'>\n' +
            '            <legend>alpha ToC</legend>\n' +
            '                <ul>\n' +
            '                    <li><span><a href=\'#bravo\'>bravo</a></span></li>\n' +
            '                </ul>\n' +
            '        </fieldset>\n' +
            '        <fieldset class=\'box\'>\n' +
            '            <a name=\'bravo\'></a>\n' +
            '            <legend>bravo</legend>\n' +
            '                <ul>\n' +
            '                    <li><span>charlie</span></li>\n' +
            '                <pre><code>delta echo</code></pre>\n' +
            '                </ul>\n' +
            '        </fieldset>\n' +
            '    <script>new Highlighter().run(document);</script>\n' +
            '    <script> (function(i,s,o,g,r,a,m){i[\'GoogleAnalyticsObject\']=r;i[r]=i[r]||function(){ (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o), m = s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m) })(window,document,\'script\',\'https://www.google-analytics.com/analytics.js\',\'ga\'); ga(\'create\', \'UA-106217827-1\', \'auto\'); ga(\'send\', \'pageview\'); </script>\n' +
            '    </body>\n' +
            '</html>'
        )

    def test_whenListHasTwoLevelsNestedCode_thenExpectedMarkupBuilt(self):
        self.assert_markup_generated(
            '*alpha*\n' +
            'bravo\n' +
            '    charlie\n'+
            '        delta\n' +
            '    **echo** foxtrot\n',

            '<!DOCTYPE html>\n'
            '<html>\n' +
            '    <head>\n' +
            '        <title>alpha</title>\n' +
            '        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">\n' +
            '        <link rel="stylesheet" type="text/css" href="/assets/main.css">\n' +
            '        <link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon.png">\n' +
            '        <script src="/assets/syntaxhighlighter.js"></script>\n' +
            '    </head>\n' +
            '    <body>\n' +
            '        <fieldset class=\'box\'>\n' +
            '            <legend>alpha ToC</legend>\n' +
            '                <ul>\n' +
            '                    <li><span><a href=\'#bravo\'>bravo</a></span></li>\n' +
            '                </ul>\n' +
            '        </fieldset>\n' +
            '        <fieldset class=\'box\'>\n' +
            '            <a name=\'bravo\'></a>\n' +
            '            <legend>bravo</legend>\n' +
            '                <ul>\n' +
            '                    <li><span>charlie</span></li>\n' +
            '                        <ul>\n' +
            '                            <li><span>delta</span></li>\n' +
            '                        </ul>\n' +
            '                    <li><span><strong>echo</strong> foxtrot</span></li>\n' +
            '                </ul>\n' +
            '        </fieldset>\n' +
            '    <script>new Highlighter().run(document);</script>\n' +
            '    <script> (function(i,s,o,g,r,a,m){i[\'GoogleAnalyticsObject\']=r;i[r]=i[r]||function(){ (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o), m = s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m) })(window,document,\'script\',\'https://www.google-analytics.com/analytics.js\',\'ga\'); ga(\'create\', \'UA-106217827-1\', \'auto\'); ga(\'send\', \'pageview\'); </script>\n' +
            '    </body>\n' +
            '</html>'
        )

    def test_whenListHasNestedCodeWithLiteralStarCharacter_thenExpectedMarkupBuilt(self):
        self.assert_markup_generated(
            '*alpha*\n' +
            'bravo\n' +
            '    charlie\n'+
            '        *delta echo* foxtrot*\n',

            '<!DOCTYPE html>\n'
            '<html>\n' +
            '    <head>\n' +
            '        <title>alpha</title>\n' +
            '        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">\n' +
            '        <link rel="stylesheet" type="text/css" href="/assets/main.css">\n' +
            '        <link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon.png">\n' +
            '        <script src="/assets/syntaxhighlighter.js"></script>\n' +
            '    </head>\n' +
            '    <body>\n' +
            '        <fieldset class=\'box\'>\n' +
            '            <legend>alpha ToC</legend>\n' +
            '                <ul>\n' +
            '                    <li><span><a href=\'#bravo\'>bravo</a></span></li>\n' +
            '                </ul>\n' +
            '        </fieldset>\n' +
            '        <fieldset class=\'box\'>\n' +
            '            <a name=\'bravo\'></a>\n' +
            '            <legend>bravo</legend>\n' +
            '                <ul>\n' +
            '                    <li><span>charlie</span></li>\n' +
            '                <pre><code>delta echo* foxtrot</code></pre>\n' +
            '                </ul>\n' +
            '        </fieldset>\n' +
            '    <script>new Highlighter().run(document);</script>\n' +
            '    <script> (function(i,s,o,g,r,a,m){i[\'GoogleAnalyticsObject\']=r;i[r]=i[r]||function(){ (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o), m = s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m) })(window,document,\'script\',\'https://www.google-analytics.com/analytics.js\',\'ga\'); ga(\'create\', \'UA-106217827-1\', \'auto\'); ga(\'send\', \'pageview\'); </script>\n' +
            '    </body>\n' +
            '</html>'
        )

    def test_whenListHasOneSpaceInFirstLevel_thenErrorThrown(self):
        self.assert_exception_thrown(
            '*alpha*\n' +
            ' bravo\n',
            'Unsupported number of spaces [1] in line [ bravo]'
        )

    def test_whenListHasTooNestedElement_thenErrorThrown(self):
        self.assert_exception_thrown(
            '*alpha*\n' +
            'bravo\n' +
            '                                                     charlie\n',
            'Unsupported number of spaces [53] in line [                                                     charlie]'
        )

    def test_whenListHasTwoEmptyTitles_thenErrorThrown(self):
        self.assert_exception_thrown(
            '*alpha*\n' +
            'bravo\n' +
            'charlie\n',
            'Failed to parse, found title[charlie] with no text'
        )

    def test_whenTextHasStrongTagAndLists_thenExpectedMarkupBuilt(self):
        self.assert_markup_generated(
            '*alpha*\n' +
            'bravo\n' +
            '    *charlie delta*\n',

            '<!DOCTYPE html>\n'
            '<html>\n' +
            '    <head>\n' +
            '        <title>alpha</title>\n' +
            '        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">\n' +
            '        <link rel="stylesheet" type="text/css" href="/assets/main.css">\n' +
            '        <link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon.png">\n' +
            '        <script src="/assets/syntaxhighlighter.js"></script>\n' +
            '    </head>\n' +
            '    <body>\n' +
            '        <fieldset class=\'box\'>\n' +
            '            <legend>alpha ToC</legend>\n' +
            '                <ul>\n' +
            '                    <li><span><a href=\'#bravo\'>bravo</a></span></li>\n' +
            '                </ul>\n' +
            '        </fieldset>\n' +
            '        <fieldset class=\'box\'>\n' +
            '            <a name=\'bravo\'></a>\n' +
            '            <legend>bravo</legend>\n' +
            '                <ul>\n' +
            '                <pre><code>charlie delta</code></pre>\n' +
            '                </ul>\n' +
            '        </fieldset>\n' +
            '    <script>new Highlighter().run(document);</script>\n' +
            '    <script> (function(i,s,o,g,r,a,m){i[\'GoogleAnalyticsObject\']=r;i[r]=i[r]||function(){ (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o), m = s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m) })(window,document,\'script\',\'https://www.google-analytics.com/analytics.js\',\'ga\'); ga(\'create\', \'UA-106217827-1\', \'auto\'); ga(\'send\', \'pageview\'); </script>\n' +
            '    </body>\n' +
            '</html>'
        )

    def test_whenTextHasMultipleCodeblocksTagAndLists_thenExpectedMarkupBuilt(self):
        self.assert_markup_generated(
            '*alpha*\n' +
            'bravo\n' +
            '    **charlie**\n' +
            '    delta\n' +
            '    *echo foxtrot*\n',

            '<!DOCTYPE html>\n'
            '<html>\n' +
            '    <head>\n' +
            '        <title>alpha</title>\n' +
            '        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">\n' +
            '        <link rel="stylesheet" type="text/css" href="/assets/main.css">\n' +
            '        <link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon.png">\n' +
            '        <script src="/assets/syntaxhighlighter.js"></script>\n' +
            '    </head>\n' +
            '    <body>\n' +
            '        <fieldset class=\'box\'>\n' +
            '            <legend>alpha ToC</legend>\n' +
            '                <ul>\n' +
            '                    <li><span><a href=\'#bravo\'>bravo</a></span></li>\n' +
            '                </ul>\n' +
            '        </fieldset>\n' +
            '        <fieldset class=\'box\'>\n' +
            '            <a name=\'bravo\'></a>\n' +
            '            <legend>bravo</legend>\n' +
            '                <ul>\n' +
            '                    <li><span><strong>charlie</strong></span></li>\n' +
            '                    <li><span>delta</span></li>\n' +
            '                <pre><code>echo foxtrot</code></pre>\n' +
            '                </ul>\n' +
            '        </fieldset>\n' +
            '    <script>new Highlighter().run(document);</script>\n' +
            '    <script> (function(i,s,o,g,r,a,m){i[\'GoogleAnalyticsObject\']=r;i[r]=i[r]||function(){ (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o), m = s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m) })(window,document,\'script\',\'https://www.google-analytics.com/analytics.js\',\'ga\'); ga(\'create\', \'UA-106217827-1\', \'auto\'); ga(\'send\', \'pageview\'); </script>\n' +
            '    </body>\n' +
            '</html>'
        )

    def test_whenTextEscapedCodeBlocks_thenExpectedMarkupBuilt(self):
        self.assert_markup_generated(
            '*alpha*\n' +
            'bravo\n' +
            '    \\*\\*charlie\\*\\*\n' +
            '    delta\n' +
            '    **echo**\n',

            '<!DOCTYPE html>\n'
            '<html>\n' +
            '    <head>\n' +
            '        <title>alpha</title>\n' +
            '        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">\n' +
            '        <link rel="stylesheet" type="text/css" href="/assets/main.css">\n' +
            '        <link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon.png">\n' +
            '        <script src="/assets/syntaxhighlighter.js"></script>\n' +
            '    </head>\n' +
            '    <body>\n' +
            '        <fieldset class=\'box\'>\n' +
            '            <legend>alpha ToC</legend>\n' +
            '                <ul>\n' +
            '                    <li><span><a href=\'#bravo\'>bravo</a></span></li>\n' +
            '                </ul>\n' +
            '        </fieldset>\n' +
            '        <fieldset class=\'box\'>\n' +
            '            <a name=\'bravo\'></a>\n' +
            '            <legend>bravo</legend>\n' +
            '                <ul>\n' +
            '                    <li><span>**charlie**</span></li>\n' +
            '                    <li><span>delta</span></li>\n' +
            '                    <li><span><strong>echo</strong></span></li>\n' +
            '                </ul>\n' +
            '        </fieldset>\n' +
            '    <script>new Highlighter().run(document);</script>\n' +
            '    <script> (function(i,s,o,g,r,a,m){i[\'GoogleAnalyticsObject\']=r;i[r]=i[r]||function(){ (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o), m = s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m) })(window,document,\'script\',\'https://www.google-analytics.com/analytics.js\',\'ga\'); ga(\'create\', \'UA-106217827-1\', \'auto\'); ga(\'send\', \'pageview\'); </script>\n' +
            '    </body>\n' +
            '</html>'
        )

    def test_whenTextEscapedCodeBlocksAndHasThreeNestedLevels_thenExpectedMarkupBuilt(self):
        self.assert_markup_generated(
            '*alpha*\n' +
            'bravo\n' +
            '    \\*\\*charlie\\*\\*\n' +
            '    delta\n' +
            '        echo\n',

            '<!DOCTYPE html>\n'
            '<html>\n' +
            '    <head>\n' +
            '        <title>alpha</title>\n' +
            '        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">\n' +
            '        <link rel="stylesheet" type="text/css" href="/assets/main.css">\n' +
            '        <link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon.png">\n' +
            '        <script src="/assets/syntaxhighlighter.js"></script>\n' +
            '    </head>\n' +
            '    <body>\n' +
            '        <fieldset class=\'box\'>\n' +
            '            <legend>alpha ToC</legend>\n' +
            '                <ul>\n' +
            '                    <li><span><a href=\'#bravo\'>bravo</a></span></li>\n' +
            '                </ul>\n' +
            '        </fieldset>\n' +
            '        <fieldset class=\'box\'>\n' +
            '            <a name=\'bravo\'></a>\n' +
            '            <legend>bravo</legend>\n' +
            '                <ul>\n' +
            '                    <li><span>**charlie**</span></li>\n' +
            '                    <li><span>delta</span></li>\n' +
            '                        <ul>\n'
            '                            <li><span>echo</span></li>\n' +
            '                        </ul>\n' +
            '                </ul>\n' +
            '        </fieldset>\n' +
            '    <script>new Highlighter().run(document);</script>\n' +
            '    <script> (function(i,s,o,g,r,a,m){i[\'GoogleAnalyticsObject\']=r;i[r]=i[r]||function(){ (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o), m = s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m) })(window,document,\'script\',\'https://www.google-analytics.com/analytics.js\',\'ga\'); ga(\'create\', \'UA-106217827-1\', \'auto\'); ga(\'send\', \'pageview\'); </script>\n' +
            '    </body>\n' +
            '</html>'
        )

    def test_whenTextEscapedStrongBlocks_thenExpectedMarkupBuilt(self):
        self.assert_markup_generated(
            '*alpha*\n' +
            'bravo\n' +
            '    \\*\\*charlie\\*\\* delta\n' +
            '    **echo**\n',

            '<!DOCTYPE html>\n'
            '<html>\n' +
            '    <head>\n' +
            '        <title>alpha</title>\n' +
            '        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">\n' +
            '        <link rel="stylesheet" type="text/css" href="/assets/main.css">\n' +
            '        <link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon.png">\n' +
            '        <script src="/assets/syntaxhighlighter.js"></script>\n' +
            '    </head>\n' +
            '    <body>\n' +
            '        <fieldset class=\'box\'>\n' +
            '            <legend>alpha ToC</legend>\n' +
            '                <ul>\n' +
            '                    <li><span><a href=\'#bravo\'>bravo</a></span></li>\n' +
            '                </ul>\n' +
            '        </fieldset>\n' +
            '        <fieldset class=\'box\'>\n' +
            '            <a name=\'bravo\'></a>\n' +
            '            <legend>bravo</legend>\n' +
            '                <ul>\n' +
            '                    <li><span>**charlie** delta</span></li>\n' +
            '                    <li><span><strong>echo</strong></span></li>\n' +
            '                </ul>\n' +
            '        </fieldset>\n' +
            '    <script>new Highlighter().run(document);</script>\n' +
            '    <script> (function(i,s,o,g,r,a,m){i[\'GoogleAnalyticsObject\']=r;i[r]=i[r]||function(){ (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o), m = s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m) })(window,document,\'script\',\'https://www.google-analytics.com/analytics.js\',\'ga\'); ga(\'create\', \'UA-106217827-1\', \'auto\'); ga(\'send\', \'pageview\'); </script>\n' +
            '    </body>\n' +
            '</html>'
        )

    def test_whenNarrativeAttributeAndSubtitleAndMultipleComplexParagraphsAndEscapedCodeBlocks_thenExpectedMarkupBuilt(self):
        self.assert_markup_generated(
            '*alpha*narrative\n' +
            'bravo\n' +
            '    charlie\n' +
            '    \\*delta\\*\n' +
            '\n\n'
            'echo\n' +
            '    foxtrot\n' +
            '    golf\n',

            '<!DOCTYPE html>\n' +
            '<html>\n' +
            '    <head>\n' +
            '        <title>alpha</title>\n' +
            '        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">\n' +
            '        <link rel="stylesheet" type="text/css" href="/assets/main.css">\n' +
            '        <link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon.png">\n' +
            '        <script src="/assets/syntaxhighlighter.js"></script>\n' +
            '    </head>\n' +
            '    <body>\n' +
            '        <fieldset class=\'box\'>\n' +
            '            <legend>alpha ToC</legend>\n' +
            '                <ul>\n' +
            '                    <li><span><a href=\'#bravo\'>bravo</a></span></li>\n' +
            '                    <li><span><a href=\'#echo\'>echo</a></span></li>\n' +
            '                </ul>\n' +
            '        </fieldset>\n' +
            '        <fieldset class=\'box\'>\n' +
            '            <a name=\'bravo\'></a>\n' +
            '            <legend>bravo</legend>\n' +
            '                <p>charlie</p>\n' +
            '                <p>*delta*</p>\n' +
            '        </fieldset>\n' +
            '        <fieldset class=\'box\'>\n' +
            '            <a name=\'echo\'></a>\n' +
            '            <legend>echo</legend>\n' +
            '                <p>foxtrot</p>\n' +
            '                <p>golf</p>\n' +
            '        </fieldset>\n' +
            '    <script>new Highlighter().run(document);</script>\n' +
            '    <script> (function(i,s,o,g,r,a,m){i[\'GoogleAnalyticsObject\']=r;i[r]=i[r]||function(){ (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o), m = s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m) })(window,document,\'script\',\'https://www.google-analytics.com/analytics.js\',\'ga\'); ga(\'create\', \'UA-106217827-1\', \'auto\'); ga(\'send\', \'pageview\'); </script>\n' +
            '    </body>\n' +
            '</html>'
        )

    def test_whenNarrativeAttributeAndSubtitleAndMultipleComplexParagraphsAndEscapedStrongBlocks_thenExpectedMarkupBuilt(self):
        self.assert_markup_generated(
            '*alpha*narrative\n' +
            'bravo\n' +
            '    charlie \\*\\*delta\\*\\*\n' +
            '\n\n'
            'echo\n' +
            '    foxtrot\n' +
            '    golf\n',

            '<!DOCTYPE html>\n' +
            '<html>\n' +
            '    <head>\n' +
            '        <title>alpha</title>\n' +
            '        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">\n' +
            '        <link rel="stylesheet" type="text/css" href="/assets/main.css">\n' +
            '        <link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon.png">\n' +
            '        <script src="/assets/syntaxhighlighter.js"></script>\n' +
            '    </head>\n' +
            '    <body>\n' +
            '        <fieldset class=\'box\'>\n' +
            '            <legend>alpha ToC</legend>\n' +
            '                <ul>\n' +
            '                    <li><span><a href=\'#bravo\'>bravo</a></span></li>\n' +
            '                    <li><span><a href=\'#echo\'>echo</a></span></li>\n' +
            '                </ul>\n' +
            '        </fieldset>\n' +
            '        <fieldset class=\'box\'>\n' +
            '            <a name=\'bravo\'></a>\n' +
            '            <legend>bravo</legend>\n' +
            '                <p>charlie **delta**</p>\n' +
            '        </fieldset>\n' +
            '        <fieldset class=\'box\'>\n' +
            '            <a name=\'echo\'></a>\n' +
            '            <legend>echo</legend>\n' +
            '                <p>foxtrot</p>\n' +
            '                <p>golf</p>\n' +
            '        </fieldset>\n' +
            '    <script>new Highlighter().run(document);</script>\n' +
            '    <script> (function(i,s,o,g,r,a,m){i[\'GoogleAnalyticsObject\']=r;i[r]=i[r]||function(){ (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o), m = s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m) })(window,document,\'script\',\'https://www.google-analytics.com/analytics.js\',\'ga\'); ga(\'create\', \'UA-106217827-1\', \'auto\'); ga(\'send\', \'pageview\'); </script>\n' +
            '    </body>\n' +
            '</html>'
        )

    def test_whenNarrativeAndHasCodeBlockWithMultipleHtmlCharacters_thenExpectedMarkupBuilt(self):
        self.assert_markup_generated(
            '*alpha*narrative\n' +
            'bravo\n' +
            '    *<>charlie\n' +
            'delta<>\n' +
            'echo<>*\n',

            '<!DOCTYPE html>\n' +
            '<html>\n' +
            '    <head>\n' +
            '        <title>alpha</title>\n' +
            '        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">\n' +
            '        <link rel="stylesheet" type="text/css" href="/assets/main.css">\n' +
            '        <link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon.png">\n' +
            '        <script src="/assets/syntaxhighlighter.js"></script>\n' +
            '    </head>\n' +
            '    <body>\n' +
            '        <fieldset class=\'box\'>\n' +
            '            <legend>alpha ToC</legend>\n' +
            '                <ul>\n' +
            '                    <li><span><a href=\'#bravo\'>bravo</a></span></li>\n' +
            '                </ul>\n' +
            '        </fieldset>\n' +
            '        <fieldset class=\'box\'>\n' +
            '            <a name=\'bravo\'></a>\n' +
            '            <legend>bravo</legend>\n' +
            '                <pre><code>&lt;&gt;charlie\n' +
            'delta&lt;&gt;\n' +
            'echo&lt;&gt;</code></pre>\n' +
            '        </fieldset>\n' +
            '    <script>new Highlighter().run(document);</script>\n' +
            '    <script> (function(i,s,o,g,r,a,m){i[\'GoogleAnalyticsObject\']=r;i[r]=i[r]||function(){ (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o), m = s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m) })(window,document,\'script\',\'https://www.google-analytics.com/analytics.js\',\'ga\'); ga(\'create\', \'UA-106217827-1\', \'auto\'); ga(\'send\', \'pageview\'); </script>\n' +
            '    </body>\n' +
            '</html>'
        )

    def test_whenNarrativeAndHasStrongBlockWithUrl_thenExpectedMarkupBuilt(self):
        self.assert_markup_generated(
            '*alpha*narrative\n' +
            'bravo\n' +
            '    foo **/charlie/delta** echo\n',

            '<!DOCTYPE html>\n' +
            '<html>\n' +
            '    <head>\n' +
            '        <title>alpha</title>\n' +
            '        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">\n' +
            '        <link rel="stylesheet" type="text/css" href="/assets/main.css">\n' +
            '        <link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon.png">\n' +
            '        <script src="/assets/syntaxhighlighter.js"></script>\n' +
            '    </head>\n' +
            '    <body>\n' +
            '        <fieldset class=\'box\'>\n' +
            '            <legend>alpha ToC</legend>\n' +
            '                <ul>\n' +
            '                    <li><span><a href=\'#bravo\'>bravo</a></span></li>\n' +
            '                </ul>\n' +
            '        </fieldset>\n' +
            '        <fieldset class=\'box\'>\n' +
            '            <a name=\'bravo\'></a>\n' +
            '            <legend>bravo</legend>\n' +
            '                <p>foo <strong>/charlie/delta</strong> echo</p>\n' +
            '        </fieldset>\n' +
            '    <script>new Highlighter().run(document);</script>\n' +
            '    <script> (function(i,s,o,g,r,a,m){i[\'GoogleAnalyticsObject\']=r;i[r]=i[r]||function(){ (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o), m = s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m) })(window,document,\'script\',\'https://www.google-analytics.com/analytics.js\',\'ga\'); ga(\'create\', \'UA-106217827-1\', \'auto\'); ga(\'send\', \'pageview\'); </script>\n' +
            '    </body>\n' +
            '</html>'
        )

    def test_whenNarrativeAndHasMultipleStrongBlocks_thenExpectedMarkupBuilt(self):
        self.assert_markup_generated(
            '*alpha*narrative\n' +
            'bravo\n' +
            '    foo **$charlie** **$delta** echo\n',

            '<!DOCTYPE html>\n' +
            '<html>\n' +
            '    <head>\n' +
            '        <title>alpha</title>\n' +
            '        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">\n' +
            '        <link rel="stylesheet" type="text/css" href="/assets/main.css">\n' +
            '        <link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon.png">\n' +
            '        <script src="/assets/syntaxhighlighter.js"></script>\n' +
            '    </head>\n' +
            '    <body>\n' +
            '        <fieldset class=\'box\'>\n' +
            '            <legend>alpha ToC</legend>\n' +
            '                <ul>\n' +
            '                    <li><span><a href=\'#bravo\'>bravo</a></span></li>\n' +
            '                </ul>\n' +
            '        </fieldset>\n' +
            '        <fieldset class=\'box\'>\n' +
            '            <a name=\'bravo\'></a>\n' +
            '            <legend>bravo</legend>\n' +
            '                <p>foo <strong>$charlie</strong> <strong>$delta</strong> echo</p>\n' +
            '        </fieldset>\n' +
            '    <script>new Highlighter().run(document);</script>\n' +
            '    <script> (function(i,s,o,g,r,a,m){i[\'GoogleAnalyticsObject\']=r;i[r]=i[r]||function(){ (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o), m = s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m) })(window,document,\'script\',\'https://www.google-analytics.com/analytics.js\',\'ga\'); ga(\'create\', \'UA-106217827-1\', \'auto\'); ga(\'send\', \'pageview\'); </script>\n' +
            '    </body>\n' +
            '</html>'
        )

    def test_whenNarrativeAndHasCodeBlocksWithEmptyBlankLines_thenExpectedMarkupBuilt(self):
        self.assert_markup_generated(
            '*alpha*narrative\n' +
            'bravo\n' +
            '    *charlie\n'
            '\n'
            'delta*\n',

            '<!DOCTYPE html>\n' +
            '<html>\n' +
            '    <head>\n' +
            '        <title>alpha</title>\n' +
            '        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">\n' +
            '        <link rel="stylesheet" type="text/css" href="/assets/main.css">\n' +
            '        <link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon.png">\n' +
            '        <script src="/assets/syntaxhighlighter.js"></script>\n' +
            '    </head>\n' +
            '    <body>\n' +
            '        <fieldset class=\'box\'>\n' +
            '            <legend>alpha ToC</legend>\n' +
            '                <ul>\n' +
            '                    <li><span><a href=\'#bravo\'>bravo</a></span></li>\n' +
            '                </ul>\n' +
            '        </fieldset>\n' +
            '        <fieldset class=\'box\'>\n' +
            '            <a name=\'bravo\'></a>\n' +
            '            <legend>bravo</legend>\n' +
            '                <pre><code>charlie\n' +
            '\n' +
            'delta</code></pre>\n' +
            '        </fieldset>\n' +
            '    <script>new Highlighter().run(document);</script>\n' +
            '    <script> (function(i,s,o,g,r,a,m){i[\'GoogleAnalyticsObject\']=r;i[r]=i[r]||function(){ (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o), m = s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m) })(window,document,\'script\',\'https://www.google-analytics.com/analytics.js\',\'ga\'); ga(\'create\', \'UA-106217827-1\', \'auto\'); ga(\'send\', \'pageview\'); </script>\n' +
            '    </body>\n' +
            '</html>'
        )

    def test_whenNarrativeAndHasInlineCodeBlocksWithEmptyBlankLines_thenExpectedMarkupBuilt(self):
        self.assert_markup_generated(
            '*alpha*narrative\n' +
            'bravo\n' +
            '    charlie **delta echo** foxtrot\n',

            '<!DOCTYPE html>\n' +
            '<html>\n' +
            '    <head>\n' +
            '        <title>alpha</title>\n' +
            '        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">\n' +
            '        <link rel="stylesheet" type="text/css" href="/assets/main.css">\n' +
            '        <link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon.png">\n' +
            '        <script src="/assets/syntaxhighlighter.js"></script>\n' +
            '    </head>\n' +
            '    <body>\n' +
            '        <fieldset class=\'box\'>\n' +
            '            <legend>alpha ToC</legend>\n' +
            '                <ul>\n' +
            '                    <li><span><a href=\'#bravo\'>bravo</a></span></li>\n' +
            '                </ul>\n' +
            '        </fieldset>\n' +
            '        <fieldset class=\'box\'>\n' +
            '            <a name=\'bravo\'></a>\n' +
            '            <legend>bravo</legend>\n' +
            '                <p>charlie <strong>delta echo</strong> foxtrot</p>\n' +
            '        </fieldset>\n' +
            '    <script>new Highlighter().run(document);</script>\n' +
            '    <script> (function(i,s,o,g,r,a,m){i[\'GoogleAnalyticsObject\']=r;i[r]=i[r]||function(){ (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o), m = s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m) })(window,document,\'script\',\'https://www.google-analytics.com/analytics.js\',\'ga\'); ga(\'create\', \'UA-106217827-1\', \'auto\'); ga(\'send\', \'pageview\'); </script>\n' +
            '    </body>\n' +
            '</html>'
        )

    def test_whenNarrativeWithImage_thenExpectedMarkupBuilt(self):
        self.assert_markup_generated(
            '*alpha*narrative\n' +
            'bravo\n' +
            '    #charlie.png#\n',

            '<!DOCTYPE html>\n' +
            '<html>\n' +
            '    <head>\n' +
            '        <title>alpha</title>\n' +
            '        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">\n' +
            '        <link rel="stylesheet" type="text/css" href="/assets/main.css">\n' +
            '        <link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon.png">\n' +
            '        <script src="/assets/syntaxhighlighter.js"></script>\n' +
            '    </head>\n' +
            '    <body>\n' +
            '        <fieldset class=\'box\'>\n' +
            '            <legend>alpha ToC</legend>\n' +
            '                <ul>\n' +
            '                    <li><span><a href=\'#bravo\'>bravo</a></span></li>\n' +
            '                </ul>\n' +
            '        </fieldset>\n' +
            '        <fieldset class=\'box\'>\n' +
            '            <a name=\'bravo\'></a>\n' +
            '            <legend>bravo</legend>\n' +
            '                <a href=\'/assets/charlie.png\'><img class=\'imgbody\' src=\'/assets/charlie.png\'></a>\n' +
            '        </fieldset>\n' +
            '    <script>new Highlighter().run(document);</script>\n' +
            '    <script> (function(i,s,o,g,r,a,m){i[\'GoogleAnalyticsObject\']=r;i[r]=i[r]||function(){ (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o), m = s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m) })(window,document,\'script\',\'https://www.google-analytics.com/analytics.js\',\'ga\'); ga(\'create\', \'UA-106217827-1\', \'auto\'); ga(\'send\', \'pageview\'); </script>\n' +
            '    </body>\n' +
            '</html>'
        )

    def test_whenNarrativeWithComplexBoldString_thenExpectedMarkupBuilt(self):
        self.assert_markup_generated(
            '*alpha*narrative\n' +
            'bravo\n' +
            '    charlie **http://127.0.0.1/wolfcms/?/admin/login**\n',

            '<!DOCTYPE html>\n' +
            '<html>\n' +
            '    <head>\n' +
            '        <title>alpha</title>\n' +
            '        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">\n' +
            '        <link rel="stylesheet" type="text/css" href="/assets/main.css">\n' +
            '        <link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon.png">\n' +
            '        <script src="/assets/syntaxhighlighter.js"></script>\n' +
            '    </head>\n' +
            '    <body>\n' +
            '        <fieldset class=\'box\'>\n' +
            '            <legend>alpha ToC</legend>\n' +
            '                <ul>\n' +
            '                    <li><span><a href=\'#bravo\'>bravo</a></span></li>\n' +
            '                </ul>\n' +
            '        </fieldset>\n' +
            '        <fieldset class=\'box\'>\n' +
            '            <a name=\'bravo\'></a>\n' +
            '            <legend>bravo</legend>\n' +
            '                <p>charlie <strong>http://127.0.0.1/wolfcms/?/admin/login</strong></p>\n' +
            '        </fieldset>\n' +
            '    <script>new Highlighter().run(document);</script>\n' +
            '    <script> (function(i,s,o,g,r,a,m){i[\'GoogleAnalyticsObject\']=r;i[r]=i[r]||function(){ (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o), m = s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m) })(window,document,\'script\',\'https://www.google-analytics.com/analytics.js\',\'ga\'); ga(\'create\', \'UA-106217827-1\', \'auto\'); ga(\'send\', \'pageview\'); </script>\n' +
            '    </body>\n' +
            '</html>'
        )

    def assert_markup_generated(self, input, expected):
        actual = parse(string.split(input, '\n'))
        a = actual.split("\n")
        e = expected.split("\n")
        for i in range(0, len(a)):
            self.assertEqual(e[i], a[i], '[' + actual + ']' + '\n[' + expected + ']\nactual[' + a[i] +']\nexpected[' + e[i] +']')
        self.assertEqual(expected, actual)

    def assert_exception_thrown(self, input, message):
        with self.assertRaisesRegexp(Exception, re.escape(message)):
            parse(string.split(input, '\n'))
