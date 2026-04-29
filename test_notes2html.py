import re
import tempfile
import textwrap
import unittest
from pathlib import Path

import notes2html
from notes2html import parse, run


def note(text):
    return textwrap.dedent(text).lstrip('\n').rstrip('\n')


class ParserTest(unittest.TestCase):
    def test_whenEmptyString_thenExpectedMarkupBuilt(self):
        self.assert_markup_contains(
            '',
            [
                '<title></title>',
                '<legend> ToC</legend>',
            ],
        )

    def test_whenTextHasTitle_thenExpectedMarkupBuilt(self):
        self.assert_markup_contains(
            '*title*',
            [
                '<title>title</title>',
                '<legend>title ToC</legend>',
            ],
        )

    def test_whenTextHasEmptyTitle_thenExpectedMarkupBuilt(self):
        self.assert_markup_contains(
            '**',
            [
                '<title></title>',
                '<legend> ToC</legend>',
            ],
        )

    def test_whenTextHasTitleAndSubtitleAndText_thenExpectedMarkupBuilt(self):
        self.assert_markup_contains(
            note(r"""
                *title*
                subtitle
                    text
            """),
            [
                '<title>title</title>',
                '<legend>title ToC</legend>',
                "<li><span><a href='#subtitle'>subtitle</a></span></li>",
                "<a name='subtitle'></a>",
                '<legend>subtitle</legend>',
                '<li><span>text</span></li>',
            ],
        )

    def test_whenTextHasTitleAndSubtitleWithSpecialCharsAndText_thenExpectedMarkupBuilt(self):
        self.assert_markup_contains(
            note(r"""
                *title*
                subtitle'\foo
                    text
            """),
            [
                '<title>title</title>',
                '<legend>title ToC</legend>',
                "<li><span><a href='#subtitle&#x27;\\\\foo'>subtitle'\\foo</a></span></li>",
                "<a name='subtitle&#x27;\\\\foo'></a>",
                "<legend>subtitle'\\foo</legend>",
                '<li><span>text</span></li>',
            ],
        )

    def test_whenTextHasTitleAndSubtitleAndTextAndBlankLine_thenExpectedMarkupBuilt(self):
        self.assert_markup_contains(
            note(r"""
                *title*

                subtitle
                    text
            """),
            [
                '<title>title</title>',
                '<legend>title ToC</legend>',
                "<li><span><a href='#subtitle'>subtitle</a></span></li>",
                "<a name='subtitle'></a>",
                '<legend>subtitle</legend>',
                '<li><span>text</span></li>',
            ],
        )

    def test_whenTextHasTitleAndSubtitleAndTextAndMultipleLines_thenExpectedMarkupBuilt(self):
        self.assert_markup_contains(
            note(r"""
                *title*

                subtitle
                    first text line
                    second text line
            """),
            [
                '<title>title</title>',
                '<legend>title ToC</legend>',
                "<li><span><a href='#subtitle'>subtitle</a></span></li>",
                "<a name='subtitle'></a>",
                '<legend>subtitle</legend>',
                '<li><span>first text line</span></li>',
                '<li><span>second text line</span></li>',
            ],
        )

    def test_whenTextHasTitleAndSubtitleAndTextAndFinalIsNested_thenExpectedMarkupBuilt(self):
        self.assert_markup_contains(
            note(r"""
                *title*
                subtitle
                    text
                        nested
            """),
            [
                '<title>title</title>',
                '<legend>title ToC</legend>',
                "<li><span><a href='#subtitle'>subtitle</a></span></li>",
                "<a name='subtitle'></a>",
                '<legend>subtitle</legend>',
                '<li><span>text</span></li>',
                '<li><span>nested</span></li>',
            ],
        )

    def test_whenMultipleTextBlocks_thenExpectedMarkupBuilt(self):
        self.assert_markup_contains(
            note(r"""
                *title*

                first subtitle
                    first text line
                    second text line


                second subtitle
                    first text line of the second block
                    second text line of the second block
            """),
            [
                '<title>title</title>',
                '<legend>title ToC</legend>',
                "<li><span><a href='#first subtitle'>first subtitle</a></span></li>",
                "<li><span><a href='#second subtitle'>second subtitle</a></span></li>",
                "<a name='first subtitle'></a>",
                '<legend>first subtitle</legend>',
                '<li><span>first text line</span></li>',
                '<li><span>second text line</span></li>',
                "<a name='second subtitle'></a>",
                '<legend>second subtitle</legend>',
                '<li><span>first text line of the second block</span></li>',
                '<li><span>second text line of the second block</span></li>',
            ],
        )

    def test_whenMultipleNestedTextBlocks_thenExpectedMarkupBuilt(self):
        self.assert_markup_contains(
            note(r"""
                *alpha*

                bravo
                    charlie
                        delta
                    echo


                foxtrot
                        golf
                    hotel
                    india
                        juliett
                kilo
                        lima
                    mike
            """),
            [
                '<title>alpha</title>',
                '<legend>alpha ToC</legend>',
                "<li><span><a href='#bravo'>bravo</a></span></li>",
                "<li><span><a href='#foxtrot'>foxtrot</a></span></li>",
                "<li><span><a href='#kilo'>kilo</a></span></li>",
                "<a name='bravo'></a>",
                '<legend>bravo</legend>',
                '<li><span>charlie</span></li>',
                '<li><span>delta</span></li>',
                '<li><span>echo</span></li>',
                "<a name='foxtrot'></a>",
                '<legend>foxtrot</legend>',
                '<li><span>golf</span></li>',
                '<li><span>hotel</span></li>',
                '<li><span>india</span></li>',
                '<li><span>juliett</span></li>',
                "<a name='kilo'></a>",
                '<legend>kilo</legend>',
                '<li><span>lima</span></li>',
                '<li><span>mike</span></li>',
            ],
        )

    def test_whenNarrativeAttribute_thenExpectedMarkupBuilt(self):
        self.assert_markup_contains(
            '*alpha*narrative',
            [
                '<title>alpha</title>',
                '<legend>alpha ToC</legend>',
            ],
        )

    def test_whenNarrativeAttributeAndSubtitleAndParagraph_thenExpectedMarkupBuilt(self):
        self.assert_markup_contains(
            note(r"""
                *alpha*narrative
                bravo
                    charlie
            """),
            [
                '<title>alpha</title>',
                '<legend>alpha ToC</legend>',
                "<li><span><a href='#bravo'>bravo</a></span></li>",
                "<a name='bravo'></a>",
                '<legend>bravo</legend>',
                '<p>charlie</p>',
            ],
        )

    def test_whenNarrativeAttributeAndSubtitleAndMultipleParagraphs_thenExpectedMarkupBuilt(self):
        self.assert_markup_contains(
            note(r"""
                *alpha*narrative
                bravo
                    charlie
                    delta
            """),
            [
                '<title>alpha</title>',
                '<legend>alpha ToC</legend>',
                "<li><span><a href='#bravo'>bravo</a></span></li>",
                "<a name='bravo'></a>",
                '<legend>bravo</legend>',
                '<p>charlie</p>',
                '<p>delta</p>',
            ],
        )

    def test_whenNarrativeAttributeAndSubtitleAndMultipleComplexParagraphs_thenExpectedMarkupBuilt(self):
        self.assert_markup_contains(
            note(r"""
                *alpha*narrative
                bravo
                    charlie
                    delta


                echo
                    foxtrot
                    golf
            """),
            [
                '<title>alpha</title>',
                '<legend>alpha ToC</legend>',
                "<li><span><a href='#bravo'>bravo</a></span></li>",
                "<li><span><a href='#echo'>echo</a></span></li>",
                "<a name='bravo'></a>",
                '<legend>bravo</legend>',
                '<p>charlie</p>',
                '<p>delta</p>',
                "<a name='echo'></a>",
                '<legend>echo</legend>',
                '<p>foxtrot</p>',
                '<p>golf</p>',
            ],
        )

    def test_whenNarrativeAttributeAndCodeAttribute_thenExpectedMarkupBuilt(self):
        self.assert_markup_contains(
            note(r"""
                *alpha*narrative
                bravo
                    charlie
                    **delta** echo
            """),
            [
                '<title>alpha</title>',
                '<legend>alpha ToC</legend>',
                "<li><span><a href='#bravo'>bravo</a></span></li>",
                "<a name='bravo'></a>",
                '<legend>bravo</legend>',
                '<p>charlie</p>',
                '<p><strong>delta</strong> echo</p>',
            ],
        )

    def test_whenNarrativeAttributeAndTwoLineCodeAttribute_thenExpectedMarkupBuilt(self):
        self.assert_markup_contains(
            note(r"""
                *alpha*narrative
                bravo
                    charlie
                    *delta

                    echo*
            """),
            [
                '<title>alpha</title>',
                '<legend>alpha ToC</legend>',
                "<li><span><a href='#bravo'>bravo</a></span></li>",
                "<a name='bravo'></a>",
                '<legend>bravo</legend>',
                '<p>charlie</p>',
                '<pre><code>delta',
                'echo</code></pre>',
            ],
        )

    def test_whenNarrativeAttributeAndMultipleLineCodeAttributeAndCodeHasMassiveIndentation_thenExpectedMarkupBuilt(self):
        self.assert_markup_contains(
            note(r"""
                *alpha*narrative
                bravo
                    charlie
                    *delta
                                      echo
                    foxtrot*
            """),
            [
                '<title>alpha</title>',
                '<legend>alpha ToC</legend>',
                "<li><span><a href='#bravo'>bravo</a></span></li>",
                "<a name='bravo'></a>",
                '<legend>bravo</legend>',
                '<p>charlie</p>',
                '<pre><code>delta',
                'echo',
                'foxtrot</code></pre>',
            ],
        )

    def test_whenNarrativeHasStrongTag_thenExpectedMarkupBuilt(self):
        self.assert_markup_contains(
            note(r"""
                *alpha*narrative
                bravo
                    charlie **delta** echo
            """),
            [
                '<title>alpha</title>',
                '<legend>alpha ToC</legend>',
                "<li><span><a href='#bravo'>bravo</a></span></li>",
                "<a name='bravo'></a>",
                '<legend>bravo</legend>',
                '<p>charlie <strong>delta</strong> echo</p>',
            ],
        )

    def test_whenTextAttributeAndCodeAttribute_thenExpectedMarkupBuilt(self):
        self.assert_markup_contains(
            note(r"""
                *alpha*
                bravo
                    charlie
                    **delta**
            """),
            [
                '<title>alpha</title>',
                '<legend>alpha ToC</legend>',
                "<li><span><a href='#bravo'>bravo</a></span></li>",
                "<a name='bravo'></a>",
                '<legend>bravo</legend>',
                '<li><span>charlie</span></li>',
                '<li><span><strong>delta</strong></span></li>',
            ],
        )

    def test_whenTextAttributeAndTwoLineCodeAttribute_thenExpectedMarkupBuilt(self):
        self.assert_markup_contains(
            note(r"""
                *alpha*
                bravo
                    charlie
                    *delta

                echo*
            """),
            [
                '<title>alpha</title>',
                '<legend>alpha ToC</legend>',
                "<li><span><a href='#bravo'>bravo</a></span></li>",
                "<a name='bravo'></a>",
                '<legend>bravo</legend>',
                '<li><span>charlie</span></li>',
                '<pre><code>delta',
                'echo</code></pre>',
            ],
        )

    def test_whenTextAttributeAndMultipleLineCodeAttribute_thenExpectedMarkupBuilt(self):
        self.assert_markup_contains(
            note(r"""
                *alpha*
                bravo
                    charlie
                    *delta
                echo
                        foxtrot*
            """),
            [
                '<title>alpha</title>',
                '<legend>alpha ToC</legend>',
                "<li><span><a href='#bravo'>bravo</a></span></li>",
                "<a name='bravo'></a>",
                '<legend>bravo</legend>',
                '<li><span>charlie</span></li>',
                '<pre><code>delta',
                'echo',
                'foxtrot</code></pre>',
            ],
        )

    def test_whenTextHasStrongTag_thenExpectedMarkupBuilt(self):
        self.assert_markup_contains(
            note(r"""
                *alpha*
                bravo
                    charlie **<$delta>** echo
            """),
            [
                '<title>alpha</title>',
                '<legend>alpha ToC</legend>',
                "<li><span><a href='#bravo'>bravo</a></span></li>",
                "<a name='bravo'></a>",
                '<legend>bravo</legend>',
                '<li><span>charlie <strong>&lt;$delta&gt;</strong> echo</span></li>',
            ],
        )

    def test_whenListHasNestedCode_thenExpectedMarkupBuilt(self):
        self.assert_markup_contains(
            note(r"""
                *alpha*
                bravo
                    charlie
                        *delta echo*
            """),
            [
                '<title>alpha</title>',
                '<legend>alpha ToC</legend>',
                "<li><span><a href='#bravo'>bravo</a></span></li>",
                "<a name='bravo'></a>",
                '<legend>bravo</legend>',
                '<li><span>charlie</span></li>',
                '<pre><code>delta echo</code></pre>',
            ],
        )

    def test_whenListHasTwoLevelsNestedCode_thenExpectedMarkupBuilt(self):
        self.assert_markup_contains(
            note(r"""
                *alpha*
                bravo
                    charlie
                        delta
                    **echo** foxtrot
            """),
            [
                '<title>alpha</title>',
                '<legend>alpha ToC</legend>',
                "<li><span><a href='#bravo'>bravo</a></span></li>",
                "<a name='bravo'></a>",
                '<legend>bravo</legend>',
                '<li><span>charlie</span></li>',
                '<li><span>delta</span></li>',
                '<li><span><strong>echo</strong> foxtrot</span></li>',
            ],
        )

    def test_whenListHasNestedCodeWithLiteralStarCharacter_thenExpectedMarkupBuilt(self):
        self.assert_markup_contains(
            note(r"""
                *alpha*
                bravo
                    charlie
                        *delta echo* foxtrot*
            """),
            [
                '<title>alpha</title>',
                '<legend>alpha ToC</legend>',
                "<li><span><a href='#bravo'>bravo</a></span></li>",
                "<a name='bravo'></a>",
                '<legend>bravo</legend>',
                '<li><span>charlie</span></li>',
                '<pre><code>delta echo* foxtrot</code></pre>',
            ],
        )

    def test_whenTextHasStrongTagAndLists_thenExpectedMarkupBuilt(self):
        self.assert_markup_contains(
            note(r"""
                *alpha*
                bravo
                    *charlie delta*
            """),
            [
                '<title>alpha</title>',
                '<legend>alpha ToC</legend>',
                "<li><span><a href='#bravo'>bravo</a></span></li>",
                "<a name='bravo'></a>",
                '<legend>bravo</legend>',
                '<pre><code>charlie delta</code></pre>',
            ],
        )

    def test_whenTextHasMultipleCodeblocksTagAndLists_thenExpectedMarkupBuilt(self):
        self.assert_markup_contains(
            note(r"""
                *alpha*
                bravo
                    **charlie**
                    delta
                    *echo foxtrot*
            """),
            [
                '<title>alpha</title>',
                '<legend>alpha ToC</legend>',
                "<li><span><a href='#bravo'>bravo</a></span></li>",
                "<a name='bravo'></a>",
                '<legend>bravo</legend>',
                '<li><span><strong>charlie</strong></span></li>',
                '<li><span>delta</span></li>',
                '<pre><code>echo foxtrot</code></pre>',
            ],
        )

    def test_whenTextEscapedCodeBlocks_thenExpectedMarkupBuilt(self):
        self.assert_markup_contains(
            note(r"""
                *alpha*
                bravo
                    \*\*charlie\*\*
                    delta
                    **echo**
            """),
            [
                '<title>alpha</title>',
                '<legend>alpha ToC</legend>',
                "<li><span><a href='#bravo'>bravo</a></span></li>",
                "<a name='bravo'></a>",
                '<legend>bravo</legend>',
                '<li><span>**charlie**</span></li>',
                '<li><span>delta</span></li>',
                '<li><span><strong>echo</strong></span></li>',
            ],
        )

    def test_whenTextEscapedCodeBlocksAndHasThreeNestedLevels_thenExpectedMarkupBuilt(self):
        self.assert_markup_contains(
            note(r"""
                *alpha*
                bravo
                    \*\*charlie\*\*
                    delta
                        echo
            """),
            [
                '<title>alpha</title>',
                '<legend>alpha ToC</legend>',
                "<li><span><a href='#bravo'>bravo</a></span></li>",
                "<a name='bravo'></a>",
                '<legend>bravo</legend>',
                '<li><span>**charlie**</span></li>',
                '<li><span>delta</span></li>',
                '<li><span>echo</span></li>',
            ],
        )

    def test_whenTextEscapedStrongBlocks_thenExpectedMarkupBuilt(self):
        self.assert_markup_contains(
            note(r"""
                *alpha*
                bravo
                    \*\*charlie\*\* delta
                    **echo**
            """),
            [
                '<title>alpha</title>',
                '<legend>alpha ToC</legend>',
                "<li><span><a href='#bravo'>bravo</a></span></li>",
                "<a name='bravo'></a>",
                '<legend>bravo</legend>',
                '<li><span>**charlie** delta</span></li>',
                '<li><span><strong>echo</strong></span></li>',
            ],
        )

    def test_whenNarrativeAttributeAndSubtitleAndMultipleComplexParagraphsAndEscapedCodeBlocks_thenExpectedMarkupBuilt(self):
        self.assert_markup_contains(
            note(r"""
                *alpha*narrative
                bravo
                    charlie
                    \*delta\*


                echo
                    foxtrot
                    golf
            """),
            [
                '<title>alpha</title>',
                '<legend>alpha ToC</legend>',
                "<li><span><a href='#bravo'>bravo</a></span></li>",
                "<li><span><a href='#echo'>echo</a></span></li>",
                "<a name='bravo'></a>",
                '<legend>bravo</legend>',
                '<p>charlie</p>',
                '<p>*delta*</p>',
                "<a name='echo'></a>",
                '<legend>echo</legend>',
                '<p>foxtrot</p>',
                '<p>golf</p>',
            ],
        )

    def test_whenNarrativeAttributeAndSubtitleAndMultipleComplexParagraphsAndEscapedStrongBlocks_thenExpectedMarkupBuilt(self):
        self.assert_markup_contains(
            note(r"""
                *alpha*narrative
                bravo
                    charlie \*\*delta\*\*


                echo
                    foxtrot
                    golf
            """),
            [
                '<title>alpha</title>',
                '<legend>alpha ToC</legend>',
                "<li><span><a href='#bravo'>bravo</a></span></li>",
                "<li><span><a href='#echo'>echo</a></span></li>",
                "<a name='bravo'></a>",
                '<legend>bravo</legend>',
                '<p>charlie **delta**</p>',
                "<a name='echo'></a>",
                '<legend>echo</legend>',
                '<p>foxtrot</p>',
                '<p>golf</p>',
            ],
        )

    def test_whenNarrativeAndHasCodeBlockWithMultipleHtmlCharacters_thenExpectedMarkupBuilt(self):
        self.assert_markup_contains(
            note(r"""
                *alpha*narrative
                bravo
                    *<>charlie
                delta<>
                echo<>*
            """),
            [
                '<title>alpha</title>',
                '<legend>alpha ToC</legend>',
                "<li><span><a href='#bravo'>bravo</a></span></li>",
                "<a name='bravo'></a>",
                '<legend>bravo</legend>',
                '<pre><code>&lt;&gt;charlie',
                'delta&lt;&gt;',
                'echo&lt;&gt;</code></pre>',
            ],
        )

    def test_whenNarrativeAndHasStrongBlockWithUrl_thenExpectedMarkupBuilt(self):
        self.assert_markup_contains(
            note(r"""
                *alpha*narrative
                bravo
                    foo **/charlie/delta** echo
            """),
            [
                '<title>alpha</title>',
                '<legend>alpha ToC</legend>',
                "<li><span><a href='#bravo'>bravo</a></span></li>",
                "<a name='bravo'></a>",
                '<legend>bravo</legend>',
                '<p>foo <strong>/charlie/delta</strong> echo</p>',
            ],
        )

    def test_whenNarrativeAndHasMultipleStrongBlocks_thenExpectedMarkupBuilt(self):
        self.assert_markup_contains(
            note(r"""
                *alpha*narrative
                bravo
                    foo **$charlie** **$delta** echo
            """),
            [
                '<title>alpha</title>',
                '<legend>alpha ToC</legend>',
                "<li><span><a href='#bravo'>bravo</a></span></li>",
                "<a name='bravo'></a>",
                '<legend>bravo</legend>',
                '<p>foo <strong>$charlie</strong> <strong>$delta</strong> echo</p>',
            ],
        )

    def test_whenNarrativeAndHasCodeBlocksWithEmptyBlankLines_thenExpectedMarkupBuilt(self):
        self.assert_markup_contains(
            note(r"""
                *alpha*narrative
                bravo
                    *charlie

                delta*
            """),
            [
                '<title>alpha</title>',
                '<legend>alpha ToC</legend>',
                "<li><span><a href='#bravo'>bravo</a></span></li>",
                "<a name='bravo'></a>",
                '<legend>bravo</legend>',
                '<pre><code>charlie',
                'delta</code></pre>',
            ],
        )

    def test_whenNarrativeAndHasInlineCodeBlocksWithEmptyBlankLines_thenExpectedMarkupBuilt(self):
        self.assert_markup_contains(
            note(r"""
                *alpha*narrative
                bravo
                    charlie **delta echo** foxtrot
            """),
            [
                '<title>alpha</title>',
                '<legend>alpha ToC</legend>',
                "<li><span><a href='#bravo'>bravo</a></span></li>",
                "<a name='bravo'></a>",
                '<legend>bravo</legend>',
                '<p>charlie <strong>delta echo</strong> foxtrot</p>',
            ],
        )

    def test_whenNarrativeWithImage_thenExpectedMarkupBuilt(self):
        self.assert_markup_contains(
            note(r"""
                *alpha*narrative
                bravo
                    #charlie.png#
            """),
            [
                '<title>alpha</title>',
                '<legend>alpha ToC</legend>',
                "<li><span><a href='#bravo'>bravo</a></span></li>",
                "<a name='bravo'></a>",
                '<legend>bravo</legend>',
                "<a href='/assets/charlie.png'><img class='imgbody' src='/assets/charlie.png'></a>",
            ],
        )

    def test_whenNarrativeWithComplexBoldString_thenExpectedMarkupBuilt(self):
        self.assert_markup_contains(
            note(r"""
                *alpha*narrative
                bravo
                    charlie **http://127.0.0.1/wolfcms/?/admin/login**
            """),
            [
                '<title>alpha</title>',
                '<legend>alpha ToC</legend>',
                "<li><span><a href='#bravo'>bravo</a></span></li>",
                "<a name='bravo'></a>",
                '<legend>bravo</legend>',
                '<p>charlie <strong>http://127.0.0.1/wolfcms/?/admin/login</strong></p>',
            ],
        )

    def test_whenTextHasTitleAndSubtitle_thenExpectedMarkupBuilt(self):
        self.assert_exception_thrown(
            note(r"""
                *title*
                Subtitle
            """),
            'Failed to parse, found title[Subtitle] with no text',
        )

    def test_whenNarrativeAttributeAndSubtitle_thenExceptionThrown(self):
        self.assert_exception_thrown(
            note(r"""
                *alpha*narrative
                bravo
            """),
            'Failed to parse, found title[bravo] with no text',
        )

    def test_whenListHasOneSpaceInFirstLevel_thenErrorThrown(self):
        self.assert_exception_thrown(
            note(r"""
                *alpha*
                 bravo
            """),
            'Unsupported number of spaces [1] in line [ bravo]',
        )

    def test_whenListHasTooNestedElement_thenErrorThrown(self):
        self.assert_exception_thrown(
            note(r"""
                *alpha*
                bravo
                                                                     charlie
            """),
            'Unsupported number of spaces [53] in line [                                                     charlie]',
        )

    def test_whenListHasTwoEmptyTitles_thenErrorThrown(self):
        self.assert_exception_thrown(
            note(r"""
                *alpha*
                bravo
                charlie
            """),
            'Failed to parse, found title[charlie] with no text',
        )

    def test_whenTxtFileInNestedDirectory_thenHtmlFileWritten(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            src_dir = Path(tmp_dir) / 'src'
            dst_dir = Path(tmp_dir) / 'dst'
            note_dir = src_dir / 'nested'
            note_dir.mkdir(parents=True)
            (note_dir / 'note.txt').write_text(
                note("""
                    *T\u00edtulo*
                    Section
                        caf\u00e9 **ol\u00e9**
                    """),
                encoding='utf-8',
            )
            (note_dir / 'ignore.md').write_text('not a note', encoding='utf-8')

            run(src_dir, dst_dir)

            generated_note = dst_dir / 'nested' / 'note.html'
            self.assertTrue(generated_note.exists())
            self.assertFalse((dst_dir / 'nested' / 'ignore.html').exists())
            generated_html = generated_note.read_text(encoding='utf-8')
            self.assertIn('<title>T\u00edtulo</title>', generated_html)
            self.assertIn('caf\u00e9 <strong>ol\u00e9</strong>', generated_html)

    def test_whenMainGetsSourceAndDestination_thenHtmlFileWritten(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            src_dir = Path(tmp_dir) / 'src'
            dst_dir = Path(tmp_dir) / 'dst'
            src_dir.mkdir()
            (src_dir / 'note.txt').write_text(
                note(r"""
                    *Title*
                    Section
                        text
                    """),
                encoding='utf-8',
            )

            notes2html.main([str(src_dir), str(dst_dir)])

            self.assertTrue((dst_dir / 'note.html').exists())

    def assert_markup_contains(self, input_text, snippets):
        actual = parse(input_text.split('\n'))
        self.assertTrue(actual.startswith('<!DOCTYPE html>'))
        self.assertIn('<script>new Highlighter().run(document);</script>', actual)
        position = -1
        for snippet in snippets:
            next_position = actual.find(snippet, position + 1)
            self.assertNotEqual(-1, next_position, actual)
            position = next_position

    def assert_exception_thrown(self, input_text, message):
        with self.assertRaisesRegex(Exception, re.escape(message)):
            parse(input_text.split('\n'))
