import markdown

from django.template import Context
from django.template.backends.base import BaseEngine
from django.template.engine import Engine
from django.template.loaders.filesystem import Loader as FileSystemLoader
from django.template.utils import get_app_template_dirs
from django.utils.safestring import mark_safe



class MessagesTemplates(BaseEngine):

    app_dirname = "messages"

    def __init__(self, params):
        params = params.copy()
        options = params.pop('OPTIONS').copy()
        options.setdefault('autoescape', True)
        super().__init__(params)

        self.engine = Engine(self.dirs, self.app_dirs, **options)

    def from_string(self, template_code):
        return MarkdownTemplate(self.engine.from_string(template_code))

    def get_template(self, message):
        file_name = f'{message.code}.md'

        return MarkdownTemplate(self.engine.get_template(file_name), message=message)


class MarkdownTemplate:

    def __init__(self, template, message=None):
        self.template = template
        self.message = message

    def render(self, context=None, request=None):
        if context is None:
            context = {}

        context.setdefault('msg', self.message)

        context = Context(context, autoescape=True)
        rendered_markdown = self.template.render(context)

        return mark_safe(markdown.markdown(rendered_markdown))


class FileDirectoryMessageLoader(FileSystemLoader):
    app_dirname = 'messages'

    def get_dirs(self):
        return get_app_template_dirs(self.app_dirname)