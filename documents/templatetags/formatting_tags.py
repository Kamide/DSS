from django import template
from django.template.defaultfilters import stringfilter
from collections import deque

register = template.Library()

TAG_IDX = 0
WORD_IDX = 1
OPENING_TAG_BRACKET = '['
CLOSING_TAG_BRACKET = ']'
OPENING_TAGS = ['[b]', '[i]', '[u]', '[s]', '[code]', '[img]']
CLOSING_TAGS = ['[/b]', '[/i]', '[/u]', '[/s]', '[/code]', '[/img]']
HTML_TAGS = {
    '[b]': '<strong>',
    '[/b]': '</strong>',
    '[i]': '<em>',
    '[/i]': '</em>',
    '[u]': '<ins>',
    '[/u]': '</ins>',
    '[s]': '<del>',
    '[/s]': '</del>',
    '[code]': '<code>',
    '[/code]': '</code>',
    '[img]': '<img src="',
    '[/img]': '" />',
}


@register.filter(is_safe=True)
@stringfilter
def concatenater(arg, value):
    return str(arg) + str(value)


@register.filter(is_safe=True)
@stringfilter
def parse_formatting_tags(value):
    line_break_char = '<br>'
    sentences = value.split(line_break_char)
    parsed_sentences = []
    for sentence in sentences:
        words = sentence.split(' ')
        o_stack = []
        c_queue = deque()

        for word_idx, word in enumerate(words):
            l_b_idx = r_b_idx = 0
            for char_idx, char in enumerate(word):
                if char == OPENING_TAG_BRACKET:
                    l_b_idx = char_idx
                if char == CLOSING_TAG_BRACKET:
                    r_b_idx = char_idx
                if l_b_idx >= r_b_idx:
                    continue
                tag = word[l_b_idx:r_b_idx+1]
                if tag in OPENING_TAGS:
                    o_stack.append((tag, word_idx))
                elif tag in CLOSING_TAGS:
                    c_queue.append((tag, word_idx))
                l_b_idx = r_b_idx

            while o_stack and c_queue:
                if len(o_stack) > len(c_queue):
                    o_stack.pop()
                    continue
                if len(c_queue) > len(o_stack):
                    c_queue.popleft()
                    continue

                o_tag = o_stack[-1][TAG_IDX]
                c_tag = c_queue[0][TAG_IDX]
                o_word_idx = o_stack[-1][WORD_IDX]
                c_word_idx = c_queue[0][WORD_IDX]
                if o_tag[-2:0:-1] == c_tag[-2:1:-1]:
                    html_o_tag = HTML_TAGS[o_tag]
                    if html_o_tag[-1] == '"':
                        words[o_word_idx] = words[o_word_idx].replace(o_tag, html_o_tag)
                        words[c_word_idx] = words[c_word_idx].replace(c_tag, HTML_TAGS[c_tag])
                    else:
                        words[o_word_idx] = words[o_word_idx].replace(o_tag, html_o_tag)
                        words[c_word_idx] = words[c_word_idx].replace(c_tag, HTML_TAGS[c_tag])
                o_stack.pop()
                c_queue.popleft()

        parsed_sentences.append(' '.join(words))

    return line_break_char.join(parsed_sentences)
