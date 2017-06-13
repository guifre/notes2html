import os
import re

import sys


def run():
    if len(sys.argv) < 3:
        print 'Usage: $ python %s src_dir dst_dir' % sys.argv[0]
        raise Exception

    for a_file in [a_file for a_file in os.listdir(sys.argv[1]) if a_file.endswith('.txt')]:
        with open(sys.argv[1] + '/' + a_file) as read:
            with open(sys.argv[2] + '/' + a_file.replace('.txt', '.html'), 'w') as write:
                write.write(parse(read.readlines()))


def parse(param):
    return BODY % (get_title(param), get_body(param))


BODY = '<!DOCTYPE html>\n' + \
       '<html>\n' + \
       '    <head>\n' + \
       '        <title>%s</title>\n' + \
       '        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">\n' + \
       '        <link rel="stylesheet" type="text/css" href="assets/main.css">\n' + \
       '        <link rel="icon" type="image/png" sizes="32x32" href="assets/favicon.png">\n' + \
       '    </head>\n' + \
       '    <body>\n' + \
       '%s' + \
       '    </body>\n' + \
       '</html>'

BOX = '        <fieldset class=\'box\'>\n' + \
      '            <legend>%s</legend>\n' + \
      '                <ul>\n' \
      '%s' + \
      '                </ul>\n' + \
      '        </fieldset>\n'
EMPTY_ENTRY = '                    <li><span>\n'
ENTRY_START = EMPTY_ENTRY + '                        %s\n'
ENTRY_END = '                    </span></li>\n'
ENTRY_BLOCK = '                        <ul>\n%s                        </ul>\n'
NESTED_ENTRY = '                            <li><span>%s</span></li>\n'
NESTED_TEXT_PREFIX = '        '
TEXT_PREFIX = '    '


def get_title(param):
    if len(param) == 0:
        return ''
    title = re.match('\\*(.*?)\\*', param[0])
    if title:
        return title.group(1)
    return ''


def clean_line(param):
    return param.replace('\n', '')


def tabs_to_spaces(line):
    return line.replace('\t\t\t', '         ').replace('\t\t', '     ').replace('\t', ' ')


def get_body(param):
    iter_text = iter(param)
    next(iter_text)

    sub_title = ''
    text = ''
    nested_text = ''
    body = ''
    state = 'title'
    for line in iter_text:
        line = tabs_to_spaces(line)
        if len(line) == 0:
            continue

        if line.startswith(NESTED_TEXT_PREFIX):
            if state == 'title':
                text = EMPTY_ENTRY
            state = 'nested'
            nested_text += NESTED_ENTRY % clean_line(line[len(NESTED_TEXT_PREFIX):])

        elif line.startswith(TEXT_PREFIX):
            if state == 'nested':
                text += flush_nested(nested_text)
                nested_text = ''
            if state == 'text':
                text += ENTRY_END

            text += ENTRY_START % clean_line(line[len(TEXT_PREFIX):])
            state = 'text'

        elif not line.startswith(' '):
            if state == 'nested':
                text += flush_nested(nested_text)
                nested_text = ''
            if state == 'text':
                text += ENTRY_END
            state = 'title'
            if sub_title != '':
                body += BOX % (sub_title, text)
                text = ''
            sub_title = clean_line(line)
    if sub_title == '' and body == '' and text == '':
        return ''
    if state == 'text':
        text += ENTRY_END
    if state == 'nested':
        text += flush_nested(nested_text)
    return body + BOX % (sub_title, text)


def flush_nested(nested_text):
    return ENTRY_BLOCK % nested_text + ENTRY_END


if __name__ == "__main__":
    run()
