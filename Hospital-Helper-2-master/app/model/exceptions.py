class AppNotReady(Exception):

    def __str__(self):
        return 'App is not ready yet'


class BadStructure(Exception):

    def __str__(self):
        return 'Bad Structure'


class NonUniqueObjectNames(BadStructure):

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return 'Non-unique name found in structure: {}'.format(self.name)


class CannotSaveTemplate(Exception):

    def __str__(self):
        return 'Cannot save template'


class TemplateAlreadyExists(Exception):

    def __str__(self):
        return 'Template Already Exists'


class NeedBodyOrConclusion(Exception):

    def __str__(self):
        return 'Need body or conclusion for template'


class NoSuchTranslation(Exception):

    def __str__(self):
        return 'No such translation'


class Warning(Exception):

    def __str__(self):
        return 'Something bad happened, but it is not critical'


class NoTemplateForItem(Warning):

    def __str__(self):
        return 'No template found for item'
