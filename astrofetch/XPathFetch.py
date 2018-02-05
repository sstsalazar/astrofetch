#!/usr/bin/python3

import subprocess
import sys
import time
from urllib import request
from urllib.error import HTTPError

from lxml import html, etree

from .Fetcher import Fetcher


class XPathFetch(Fetcher):
    def __init__(self, url):
        """
        Constructor for the XPathFetch Class

        :param str url: The URL for the webpage to be scrapped.
        """
        super()
        self.url = url
        self.results = []
        self.log = []

    def scrap(self, section):
        """
        Crawls the webpage and extracts the content associated with the elements desired.

        :param dict section: Dictionary with the tags of the information desired and it's XPath notation path.
        """
        site = html.parse(request.urlopen(self.url))
        root = site.xpath(section["path"])
        # Processes each element of the parse tree
        for e in root:
            # Convert relative links into absolute ones.
            e.make_links_absolute()
            result = {}
            # Verifies the path of the sub element relative to the base search path.
            for k in section["tags"].keys():
                for r in e.xpath(section["tags"][k]):
                    # Different elements will give instances of different classes whose
                    # content extraction method varies.
                    if isinstance(r, etree._ElementUnicodeResult):
                        result[k] = r.strip()
                    else:
                        result[k] = r.text_content().strip()
            self.results.append(result)

    def fetch(self, source):
        """
        Fetches the content of the provided URL and saves it locally.

        :param str source: URL of the source of the content to be downloaded.
        """
        for result in self.results:
            if source in result:
                filename = result[source].rsplit("/")[-1]
                # FIXME: Define a standard Date format to be used for the majority of the project
                info = dict(Date=time.asctime(time.localtime(time.time())))
                info["File"] = filename
                try:
                    with request.urlopen(result[source]) as response, open(filename, 'wb') as output:
                        print("Downloading: {}.".format(filename))
                        data = response.read()  # a `bytes` object
                        output.write(data)
                        # As of now, Oct/03/2017, md5sum was the chosen as the default hash function
                        info["Checksum"] = subprocess.check_output(["md5sum", filename]).decode("utf-8").split()[0]
                        info["Status"] = "OK"
                except HTTPError:
                    print("[ERROR] Could not download file {}.".format(filename), file=sys.stderr)
                    info["Status"] = "ERROR"
                self.log.append(info)
