from django.test import TestCase

# Create your tests here.
from markdown2 import Markdown
markdowner = Markdown()
text = '# CSS CSS is a language that can be used to add style to an [HTML](/wiki/HTML) page.'
print(markdowner.convert(text))