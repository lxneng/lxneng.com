import re
import markdown


class Tools(object):
    """A collection of tools that can be used in templates."""

    def __init__(self, request):
        self.request = request
        
    def markdown_content(self, content):
        return markdown.markdown(content, ['codehilite'])
