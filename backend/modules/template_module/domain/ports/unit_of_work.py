from __future__ import annotations

import abc

from .repository import TemplateRepository
from ....common.ports.unit_of_work import AbstractUnitOfWork


class AbstractTemplatesUnitOfWork(AbstractUnitOfWork, abc.ABC):
    templates: TemplateRepository
