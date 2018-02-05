#!/usr/bin/python3

from abc import ABC, abstractmethod


class Fetcher(ABC):
    @abstractmethod
    def scrap(self, section):
        pass

    @abstractmethod
    def fetch(self, source):
        pass
