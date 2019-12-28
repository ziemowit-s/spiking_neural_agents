import abc


class BrianEventHandler:
    def __init__(self, **kwargs):
        self.__dict__ = kwargs

    @abc.abstractmethod
    def exec(self, *args, **kwargs):
        raise NotImplementedError()