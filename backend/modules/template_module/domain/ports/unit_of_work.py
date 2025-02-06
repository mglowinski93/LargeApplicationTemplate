import abc

from .repository import TemplateRepository


class AbstractTemplatesUnitOfWork(AbstractUnitOfWork, abc.ABC):
    templates: TemplateRepository
