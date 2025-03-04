from __future__ import annotations

import abc

from modules.common.ports.unit_of_work import AbstractUnitOfWork

from .repository import AbstractTemplatesDomainRepository


class AbstractTemplatesUnitOfWork(AbstractUnitOfWork, abc.ABC):
    templates: AbstractTemplatesDomainRepository
