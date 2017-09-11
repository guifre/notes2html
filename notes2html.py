import cgi
import os
import re

import sys


def run():
    if len(sys.argv) < 3:
        raise Exception('Usage: $ python %s src_dir dst_dir' % sys.argv[0])

    for a_file in [os.path.join(dp, f) for dp, dn, filenames in os.walk(sys.argv[1]) for f in filenames if os.path.splitext(f)[1] == '.txt']:
        with open(a_file) as read:
            out_file = sys.argv[2] + '/' + a_file.replace(sys.argv[1], '').replace('.txt', '.html')
            if not os.path.exists(out_file[:out_file.rindex('/')]):
                os.makedirs(out_file[:out_file.rindex('/')])
            with open(out_file, 'w') as write:
                try:
                    write.write(parse(read.readlines()))
                except Exception as e:
                    print 'Error when parsing [%s] [%s]' % (a_file, str(e))


def parse(param):
    title = get_title(param)
    if title['is_narrative']:
        body = get_list_body(param, BOX_NARRATIVE, TEXT_BOX_NARRAtIVE, True)
    else:
        body = get_list_body(param, BOX, SECOND_LEVEL_ENTRY, False)

    return BODY % (title['value'], body)


BODY = '<!DOCTYPE html>\n' + \
       '<html>\n' + \
       '    <head>\n' + \
       '        <title>%s</title>\n' + \
       '        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">\n' + \
       '        <link rel="stylesheet" type="text/css" href="/assets/main.css">\n' \
       '        <link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon.png">\n' + \
       '        <script src="/assets/syntaxhighlighter.js"></script>\n' \
       '    </head>\n' + \
       '    <body>\n' + \
       '%s' + \
       '    <script>new Highlighter().run(document);</script>\n' \
       '    </body>\n' + \
       '</html>'

BOX = '        <fieldset class=\'box\'>\n' + \
      '            <legend>%s</legend>\n' + \
      '                <ul>\n' \
      '%s' + \
      '                </ul>\n' + \
      '        </fieldset>\n'

BOX_NARRATIVE = \
    '        <fieldset class=\'box\'>\n' + \
    '            <legend>%s</legend>\n' + \
    '%s' + \
    '        </fieldset>\n'

INDENTATION = '    '
SECOND_LEVEL_ENTRY = '<li><span>%s</span></li>\n'
THIRD_LEVEL_ENTRY = '<ul>\n                            <li><span>%s</span></li>\n                        </ul>\n'
ENTRY_BLOCK = '                        <ul>\n%s                        </ul>\n'
TEXT_BOX_NARRAtIVE = '<p>%s</p>\n'
ENTRY_CODE_START = '                <pre><code>'
ENTRY_CODE_END = '</code></pre>\n'


def get_title(param):
    if len(param) == 0:
        return {'value': '', 'is_narrative': False}
    title = re.match('\\*(.*?)\\*(narrative)?', param[0])
    if title:
        return {'value': title.group(1), 'is_narrative': title.group(2) == 'narrative'}
    return {'value': '', 'is_narrative': False}


def escape(line):
    line = cgi.escape(line)
    while re.search(r'([^\\]*)\*([a-zA-Z0-9<>;&-./$]+)([^\\|$])\*', line):
        line = re.sub(r'([^\\]*)\*([a-zA-Z0-9<>;&-./$]+)([^\\|$])\*', '\\1<strong>\\2\\3</strong>', line.replace('\n', ''))
    while re.search('^\*([a-zA-Z0-9<>;&-./$]+)([^\\|$])\*', line):
        line = re.sub(r'^\*([a-zA-Z0-9<>;&-./$]+)([^\\|$])\*', '<strong>\\2\\3</strong>', line)
    return re.sub('\\\\\*', '*', line)


def tabs_to_spaces(line):
    return line.replace('\t\t\t', '         ').replace('\t\t', '     ').replace('\t', ' ')


def build_indentation(next_level, is_narrative):
    if next_level == 'second_level':
        if is_narrative:
            return INDENTATION * 4
        else:
            return INDENTATION * 5
    elif next_level == 'third_level':
        return INDENTATION * 6


def get_white_spacing(next_level):
    if next_level == 'first_level':
        return 0
    elif next_level == 'second_level':
        return 4
    elif next_level == 'third_level':
        return 8
    else:
        raise Exception("Could not find level " + next_level)


def line_finishes_code_block(current_level, line):
    return current_level == 'code' and line.endswith('*')


def line_starts_code_block(current_level, line):
    return line.startswith('*') and current_level != 'code' and not re.match('^\*[a-zA-Z0-9<>;&]+\*', line)


def get_list_body(param, body_box, paragraph_box, is_narrative):
    iter_text = iter(param)
    next(iter_text)

    current_level = 'start'
    html = ''
    title = None
    text = ''
    for line in iter_text:
        try:
            line = tabs_to_spaces(line)
            if line == '' and current_level != 'code':
                continue

            if current_level != 'code':
                next_level = find_level(line)
                line = line[get_white_spacing(next_level):]

            if line_finishes_code_block(current_level, line):
                text += escape(line[:-1]) + ENTRY_CODE_END
                current_level = 'nocode'
                next_level = 'nocode'
            elif current_level == 'code':
                text += escape(line) + '\n'
            elif line_starts_code_block(current_level, line):
                if line.endswith('*'):
                    text += ENTRY_CODE_START + escape(line[1:-1]) + ENTRY_CODE_END
                    current_level = next_level
                else:
                    text += ENTRY_CODE_START + escape(line[1:]) + '\n'
                    next_level = 'code'
            elif next_level == 'first_level':
                if current_level != 'start':
                    html += body_box % (title, text)
                    text = ''
                title = escape(line)
            elif next_level == 'second_level':
                text += build_indentation(next_level, is_narrative) + paragraph_box % escape(line)
            elif next_level == 'third_level':
                text += build_indentation(next_level, is_narrative) + THIRD_LEVEL_ENTRY % escape(line)
            else:
                raise Exception('Unsupported state current level[%s] nextLevel[%s]' % (current_level, next_level))
            if current_level != 'code':
                current_level = next_level

        except Exception as e:
            raise Exception('%s in line [%s]' % (str(e), line))

    if title is not None:
        if text is '':
            raise Exception('Failed to parse, found title[%s] with no text' % title)
        return html + body_box % (title, text)
    else:
        return html


def find_level(line):
    spaces = 0
    for c in line:
        if c == ' ':
            spaces += 1
        else:
            break
    if spaces == 0:
        return 'first_level'
    elif spaces == 4:
        return 'second_level'
    elif spaces == 8:
        return 'third_level'
    else:
        raise Exception("Unsupported number of spaces [%d]" % spaces)


if __name__ == "__main__":
    run()
