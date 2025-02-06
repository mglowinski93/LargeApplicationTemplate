import abc
from .repository import TemplateRepository
from modules.common.ports.unit_of_work import AbstractUnitOfWork


class AbstractTemplatesUnitOfWork(AbstractUnitOfWork, abc.ABC):
    templates: TemplateRepository
