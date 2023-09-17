from ...domain.ports import TaskDispatcher


class CeleryTaskDispatcher(TaskDispatcher):
    def send_email(self, content: str):
        pass
