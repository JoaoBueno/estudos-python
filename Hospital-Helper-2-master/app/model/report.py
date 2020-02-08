import os
import subprocess
import datetime
from collections import OrderedDict, defaultdict

from bs4 import BeautifulSoup

from PyQt5.Qt import QTextDocument, QTextDocumentWriter

from app import options
from app.model import db


class Report:
    def __init__(self, user, items):

        self.user = user

        if not self.user.organization:
            self.user.organization = db.SESSION.query(db.Organization).get(self.user.organization_id)

        self.template_groups = OrderedDict()

        for item in items:
            if item.name == options.CLIENT_TABLE_NAME:
                self.client = self._get_client(item)
            if not item.template:
                continue
            if not self.template_groups.get(item.group):
                self.template_groups[item.group] = []

            self.template_groups[item.group].append(item)

    def _get_client(self, item):
        # It's hardcoded for now
        # FIXME: change it in the future'
        return db.Client(surname=item['familiia'],
                         name=item['imia'],
                         patronymic=item['otchestvo'],
                         age=item['vozrast'],
                         hr=item['chss'],
                         height=item['rost'],
                         weight=item['ves'],
                         examined=datetime.date.today(),
                         user_id=self.user.id)

    def _get_global_style(self):
        return '<style>\n* {{\n{}\n}}\n</style>'.format(
            '\n'.join(['{}: {} !important;'.format(k, v)
                       for k, v in options.TEMPLATE_GLOBAL_STYLE.items()]))

    def _get_header(self):

        return self.user.organization.header or ''

    def _get_footer(self):

        if not self.user:
            return ''
        else:
            return ('<p style="text-align:right">{}<br>'
                    '{} {} {}</p>'.format(datetime.datetime.now().strftime('%d.%m.%Y'),
                                                 self.user.surname,
                                                 self.user.name,
                                                 self.user.patronymic))

    @staticmethod
    def open(path):
        name = os.name

        if name == 'posix':
            subprocess.call(['xdg-open', path])
        elif name == 'nt':
            os.startfile(path)
        else:
            raise AttributeError('Unknown system')

    def _get_report_path(self):
        _path_template = os.path.join(options.REPORTS_DIR, *(datetime.date.today().isoformat().split('-')))
        if not os.path.exists(_path_template):
            os.makedirs(_path_template)

        _path_template = os.path.join(_path_template, '{}{{}}.odt'.format(self.client))
        path = _path_template
        i = 1
        while os.path.exists(path.format('')):
            path = _path_template.format(' ({})'.format(i))
            i += 1
        return path.format('')

    def render(self):
        document = [self._get_global_style(), self._get_header()]

        keywords = defaultdict(lambda: defaultdict(str))
        for k, group in self.template_groups.items():
            for item in group:
                keywords.update(item.for_template())

        for k, group in self.template_groups.items():
            conclusion = []

            for item in group:
                document.append(item.template.body.format(**keywords))
                conclusion.append(item.template.conclusion)

            conclusion = ' '.join(conclusion)
            if BeautifulSoup(conclusion, 'html.parser').text:
                conclusion = BeautifulSoup(conclusion, 'html.parser')
                for p in conclusion.find_all('p'):
                    p.name = 'span'
                conclusion.insert(0, BeautifulSoup(options.CONCLUSION, 'html.parser'))
                document.append(str(conclusion))

        document.append(self._get_footer())

        return ''.join(document)

    def render_and_save(self):
        path = self._get_report_path()
        document = QTextDocument()
        document.setHtml(self.render())
        QTextDocumentWriter(path).write(document)

        self.client.save()
        report = db.Report(path=path, client_id=self.client.id)
        report.save()
        return report
