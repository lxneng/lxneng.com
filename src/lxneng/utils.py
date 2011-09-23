import re
from pygments import lexers
from pygments import highlight
from pygments.formatters import HtmlFormatter
from pygments.util import ClassNotFound


class Tools(object):
    """A collection of tools that can be used in templates."""

    def __init__(self, request):
        self.request = request
        
    def get_lexer(self, code_string, lexer_name='py'):
        try:
            lexer = lexers.get_lexer_by_name(lexer_name)
        except ClassNotFound:
            try:
                lexer = lexers.guess_lexer(code_string)
            except ClassNotFound:
                lexer = lexers.TextLexer()

        return (code_string, lexer)
            
    def pygmentize(self, content):
        pygments_formatter = HtmlFormatter()
        regex = re.compile(r'(<pre.*?>(.*?)</pre>)', re.DOTALL)
        last_end = found = 0
        to_return = ''
        for match_obj in regex.finditer(content):
            code_string = match_obj.group(2)
            code_string, lexer = self.get_lexer(code_string)
            pygmented_string = highlight(code_string, lexer, pygments_formatter)
            pygmented_string = pygmented_string.replace('&amp;', '&')
            to_return = to_return + content[last_end:match_obj.start(1)] + pygmented_string
            last_end = match_obj.end(1)
            found += 1
        to_return = to_return + content[last_end:]

        return to_return
