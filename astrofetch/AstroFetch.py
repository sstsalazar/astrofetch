#!/usr/bin/python3

import json
import os

from .XPathFetch import XPathFetch


class AstroFetch:
    def __init__(self, source, sections):
        self.__source = None
        self.__sections = None
        self.fetcher = None
        self.set_source(source)
        self.set_sections(sections)

    def set_source(self, source):
        """
        Check if the sections were passed as a valid dict.

        :param dict source: The data structure that contains the sections info.
        """
        if not isinstance(source, dict):
            raise TypeError("The source must be passed as a dict.")
        else:
            missing = []
            if "name" not in source:
                missing.append("name")
            if "url" not in source:
                missing.append("url")
            if "method" not in source:
                missing.append("method")
            if len(missing) != 0:
                raise ValueError("Missing the obligatory source tags: ".format("".join([m+"," for m in missing])[0:-1]))
        self.__source = source

    def set_sections(self, sections):
        """
        Check if the sections were passed as a valid list.

        :param list sections: The data structure that contains the sections info.
        """
        if not isinstance(sections, list):
            raise TypeError("The sections must be passed as a list.")
        else:
            for s in sections:
                missing = []
                if "path" not in s:
                    missing.append("path")
                if "fetch" not in s:
                    missing.append("fetch")
                if "tags" not in s:
                    missing.append("tags")
                if len(missing) != 0:
                    raise ValueError("Missing the obligatory section tags: ".format(
                        "".join([m + "," for m in missing])[0:-1]))
        self.__sections = sections

    def scrap(self):
        """
        Scrap the information out of the resource.
        """
        if self.__source["method"] == "XPath":
            self.fetcher = XPathFetch(self.__source["url"])
        elif self.__source["method"] == "CSSPath":
            # TODO:  implement CSS Path extraction method
            pass
        else:
            raise ValueError("The fetching method is invalid.")
        for s in self.__sections:
            self.fetcher.scrap(s)

    def access_path(self, path):
        """
        Verifies if the current proccess is in the path desired and if not changes the current working directory to it
        """
        if os.getcwd() != path:
            try:
                os.chdir(path)
            except FileNotFoundError:
                print("Directory {} is not accessible!".format(path))

    def fetch(self, path):
        """
        Fetch the data requested from the resource available.
        """
        pwd = os.getcwd()
        self.access_path(path)
        for s in self.__sections:
            for f in s["fetch"]:
                self.fetcher.fetch(f)
        self.access_path(pwd)

    @staticmethod
    def print_json(data, log):
        """
        Writes a dictionary into a JSON file.

        :param dict data: Data dictionary to be printed.
        :param str log: Filename of the output file.
        """
        with open(log, 'w') as f:
            json.dump(data, f, sort_keys=True, indent=4, ensure_ascii=False)

    def print_results(self, path):
        self.print_json(self.fetcher.results, path + "/data.json")

    def print_logs(self, path):
        self.print_json(self.fetcher.results, path + "/log.json")
