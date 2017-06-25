import cgi
import os
import re

import sys


def run():
    if len(sys.argv) < 3:
        print 'Usage: $ python %s src_dir dst_dir' % sys.argv[0]
        raise Exception

    for a_file in [os.path.join(dp, f) for dp, dn, filenames in os.walk(sys.argv[1]) for f in filenames if os.path.splitext(f)[1] == '.txt']:
        with open(a_file) as read:
            out_file = sys.argv[2] + '/' + a_file.replace(sys.argv[1], '').replace('.txt', '.html')
            if not os.path.exists(out_file[:out_file.rindex('/')]):
                os.makedirs(out_file[:out_file.rindex('/')])
            with open(out_file, 'w') as write:
                write.write(parse(read.readlines()))


def parse(param):
    title = get_title(param)
    if title['is_narrative']:
        body = get_narrative_body(param)
    else:
        body = get_list_body(param)

    return BODY % (title['value'], body)


BODY = '<!DOCTYPE html>\n' + \
       '<html>\n' + \
       '    <head>\n' + \
       '        <title>%s</title>\n' + \
       '        <meta http-equiv="Content-Type" content="text/html; charset=utf-8">\n' + \
       '        <link rel="stylesheet" type="text/css" href="/assets/main.css">\n' \
       '        <link rel="stylesheet" href="/assets/vs.css">\n' + \
       '        <link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon.png">\n' + \
       '        <script src="/assets/highlight.pack.js"></script>\n' \
       '    </head>\n' + \
       '    <body>\n' + \
       '%s' + \
       '    <script>hljs.initHighlightingOnLoad();</script>\n' \
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

BOX_NARRATIVE = \
    '        <fieldset class=\'box\'>\n' + \
    '            <legend>%s</legend>\n' + \
    '%s' + \
    '        </fieldset>\n'
ENTRY_NARRATIVE = '                <p>%s</p>\n'
ENTRY_CODE_START = '                <pre><code>'
ENTRY_CODE_END = '%s</code></pre>\n'
ENTRY_CODE_MIDDLE = '%s\n'
ENTRY_CODE = ENTRY_CODE_START + '%s</code></pre>\n'


def get_title(param):
    if len(param) == 0:
        return {'value': '', 'is_narrative': False}
    title = re.match('\\*(.*?)\\*(narrative)?', param[0])
    if title:
        return {'value': title.group(1), 'is_narrative': title.group(2) == 'narrative'}
    return {'value': '', 'is_narrative': False}


def clean_line(param):
    return cgi.escape(param.replace('\n', ''))


def tabs_to_spaces(line):
    return line.replace('\t\t\t', '         ').replace('\t\t', '     ').replace('\t', ' ').replace('\n', '')

def add_strong_tag(line):
    strong_entities = re.findall('\\*(.*?)\\*', line)
    for strong_entity in strong_entities:
        line = line.replace('*%s*' % strong_entity, '<strong>%s</strong>' % strong_entity)
    return line

def get_narrative_body(param):
    iter_text = iter(param)
    next(iter_text)

    sub_title = ''
    text = ''
    body = ''
    state = 'title'
    for line in iter_text:
        c_line = tabs_to_spaces(line)
        if state == 'code' and line == '\n':
            text += '\n'
        elif len(c_line) == 0 or c_line == '\n':
            continue
        elif c_line.startswith(TEXT_PREFIX):
            code = re.match(TEXT_PREFIX + '\*(.*?)\*', c_line)
            if code:
                text += ENTRY_CODE % clean_line(code.group(1))
                state = 'text'
            elif c_line.startswith(TEXT_PREFIX + "*"):
                text += ENTRY_CODE_START + clean_line(c_line[len(TEXT_PREFIX + "*"):]) + '\n'
                state = 'code'
            else:
                if state == 'code' and c_line.endswith('*'):
                    text += ENTRY_CODE_END % clean_line(c_line[4:-1])
                    state = 'text'
                elif state == 'code' and not c_line.endswith('*'):
                    text += ENTRY_CODE_MIDDLE % clean_line(c_line[4:])
                else:
                    text += ENTRY_NARRATIVE % add_strong_tag(clean_line(c_line[len(TEXT_PREFIX):]))
                    state = 'text'

        elif not c_line.startswith(' '):
            state = 'title'
            if sub_title != '':
                body += BOX_NARRATIVE % (sub_title, text)
                text = ''
            sub_title = clean_line(c_line)
    if sub_title == '' and body == '' and text == '':
        return ''
    return body + BOX_NARRATIVE % (sub_title, text)


def get_list_body(param):
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

        if line.startswith(NESTED_TEXT_PREFIX) and state != 'code':
            if state == 'title':
                text = EMPTY_ENTRY
            state = 'nested'
            nested_text += NESTED_ENTRY % clean_line(line[len(NESTED_TEXT_PREFIX):])

        elif line.startswith(TEXT_PREFIX):
            if state == 'nested':
                text += flush_nested(nested_text)
                nested_text = ''
            code = re.match(TEXT_PREFIX + '\*(.*?)\*', line)
            if code:
                text += ENTRY_END
                text += ENTRY_CODE % clean_line(code.group(1))
                state = 'finished_code'
            elif line.startswith(TEXT_PREFIX + "*"):
                text += ENTRY_CODE_START + clean_line(line[len(TEXT_PREFIX + "*"):]) + '\n'
                state = 'code'
            elif state == 'code' and line.endswith('*'):
                text += ENTRY_CODE_END % clean_line(line[4:-1])
                state = 'text'
            elif state == 'code' and not line.endswith('*'):
                text += ENTRY_CODE_MIDDLE % clean_line(line[4:])
                state = 'code'
            else:
                if state == 'text':
                    text += ENTRY_END
                text += ENTRY_START % add_strong_tag(clean_line(line[len(TEXT_PREFIX):]))
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
