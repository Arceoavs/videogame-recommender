from py_stringmatching import utils
from py_stringmatching.tokenizer.delimiter_tokenizer import DelimiterTokenizer

from .clean_string import clean_string
from .grams2 import grams2
from .grams3 import grams3
from .grams4 import grams4
from .grams5 import grams5
from .grams6 import grams6

predefined_grams = {
  2: grams2,
  3: grams3,
  4: grams4,
  5: grams5,
  6: grams6,
}

class GameTokenizer(DelimiterTokenizer):
  def __init__(self, return_set=False):
    super(GameTokenizer, self).__init__([' ', '\t', '\n'], return_set)

  def tokenize(self, input_string):
    utils.tok_check_for_none(input_string)
    utils.tok_check_for_string_input(input_string)

    initial_token_list = clean_string(input_string).split()
    token_list = []

    while len(initial_token_list) != 0:
      l = min(6, len(initial_token_list))
      found = False
      for i in reversed(range(2,l+1)):
        joined = ' '.join(initial_token_list[0:i])
        if joined in predefined_grams[i]:
          token_list.append(joined)
          del initial_token_list[0:i]
          found = True
          break
      if not found:
        token_list.append(initial_token_list[0])
        del initial_token_list[0]

    if self.return_set:
        return utils.convert_bag_to_set(token_list)

    return token_list

  def set_delim_set(self, delim_set):
    raise AttributeError('Delimiters cannot be set for WhitespaceTokenizer')

