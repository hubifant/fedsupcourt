# -*- coding: utf-8 -*-

import re


class TextCleanerPipeline(object):

    def process_item(self, item, spider):

        if 'paragraph' in item:
            self._clean_text(item, 'paragraph')

        if 'title_of_judgement' in item:
            self._clean_text(item, 'title_of_judgement')

        if 'core_issue' in item:
            self._clean_text(item, 'core_issue')

        if 'statement_of_affairs' in item:
            self._clean_text(item, 'statement_of_affairs')

        return item

    def _clean_text(self, item, field):
        item[field] = self._remove_space_at_beginning(item[field])
        item[field] = self._remove_space_at_end(item[field])
        item[field] = self._remove_unnecessary_newlines(item[field])
        return item

    def _remove_space_at_beginning(self, s):
        return re.sub(r'^\s+', '', s)

    def _remove_space_at_end(self, s):
        return re.sub(r'\s+$', '', s)

    def _remove_unnecessary_newlines(self, s):
        # remove newlines in middle of sentences
        s = self._remove_newlines_in_sentences(s)

        # get all text passages in parantheses and clean them
        pattern_bracketed = r'(?<=\()[^\)]+'
        bracketed_clean = [self._remove_newlines_in_brackets(bracketed) for bracketed in re.findall(pattern_bracketed, s)]

        # replace 'dirty' text passages with their cleaned version
        pick_next_passage = lambda match: bracketed_clean.pop(0)
        return re.sub(pattern_bracketed, pick_next_passage, s)

    def _remove_newlines_in_brackets(self, s):
        # case 1: remove newline
        new_s = re.sub(r'(^|(?<=\s))\n|\n(?=[\W\s])', '', s)

        # case 2: replace newline through space
        return new_s.replace('\n', ' ')

    def _remove_newlines_in_sentences(self, s):
        # case 1: newline not after completed sentence and not followed by another newline or special character or tab
        return re.sub(r'(?<!\.|\n) ?\n(?!\n|\W|\t)', ' ', s)
