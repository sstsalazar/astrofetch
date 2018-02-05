#!/usr/bin/python3
import argparse
import json

from .AstroFetch import AstroFetch

if __name__ == "__main__":
    """
    Execute the script with the JSON config file passed.
    """
    parser = argparse.ArgumentParser(description="Scraps data out of a URL.")
    parser.prog = "astrofetcher"
    parser.add_argument("-c", action="store", dest="configFile",
                        help="Config file", required=True)
    parser.add_argument("-d", action="store", type=str, dest="dest", default=".",
                        help="Destination of the extracted data.")
    parser.add_argument("-l", action="store", type=str,dest="logDest", default=".",
                        help=" Directory to store the logs.")
    parameters = parser.parse_args()
    with open(parameters.configFile) as configFile:
        config = json.load(configFile)
        fetcher = AstroFetch(config["source"], config["sections"])
        fetcher.scrap()
        fetcher.fetch(parameters.dest)
        fetcher.print_results(parameters.dest)
        fetcher.print_logs(parameters.logDest)
