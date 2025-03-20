import argparse
import os.path
import re
from typing import Iterable, List, Union

from gitingest import ingest

from wai.logging import LOGGING_WARNING
from ldc.core import domain_suffix
from ldc.api.pretrain import PretrainData, PretrainReader
from seppl.placeholders import PlaceholderSupporter, placeholder_list, expand_placeholders


class GitIngestPretrainReader(PretrainReader, PlaceholderSupporter):
    """
    Turns git repositories (local dirs or remote URLs) into text to use for pretraining.
    """

    def __init__(self, source: Union[str, List[str]] = None, source_list: Union[str, List[str]] = None,
                 include_pattern: Union[str, List[str]] = None, exclude_pattern: Union[str, List[str]] = None,
                 logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the reader.

        :param source: the dir(s) or url(s)
        :param source_list: the file(s) with dir(s) or url(s)
        :param include_pattern: the fnmatch patterns to use for including files, include all if None
        :param exclude_pattern: the fnmatch patterns to use for excluding files, exclude none if None
        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(logger_name=logger_name, logging_level=logging_level)
        self.source = source
        self.source_list = source_list
        self.include_pattern = include_pattern
        self.exclude_pattern = exclude_pattern
        self._inputs = None
        self._current_input = None
        self._current_doc = None

    def name(self) -> str:
        """
        Returns the name of the reader, used as command-line name.

        :return: the name
        :rtype: str
        """
        return "from-gitingest-" + domain_suffix(self)

    def description(self) -> str:
        """
        Returns a description of the reader.

        :return: the description
        :rtype: str
        """
        return "Turns git repositories (local dirs or remote URLs) into text to use for pretraining. Summary and directory tree get stored in the meta-data."

    def _create_argparser(self) -> argparse.ArgumentParser:
        """
        Creates an argument parser. Derived classes need to fill in the options.

        :return: the parser
        :rtype: argparse.ArgumentParser
        """
        parser = super()._create_argparser()
        parser.add_argument("-i", "--input", type=str, help="Path or URL to the git repository to read; " + placeholder_list(obj=self), required=False, nargs="*")
        parser.add_argument("-I", "--input_list", type=str, help="Path to the text file(s) listing the git repository dirs and/or remote URLs to use; " + placeholder_list(obj=self), required=False, nargs="*")
        parser.add_argument("-p", "--include_pattern", type=str, help="The filename pattern for including files (default: all included), see: https://docs.python.org/3/library/fnmatch.html", required=False, nargs="*")
        parser.add_argument("-e", "--exclude_pattern", type=str, help="The filename pattern for excluding files (default: none excluded), see: https://docs.python.org/3/library/fnmatch.html", required=False, nargs="*")
        return parser

    def _apply_args(self, ns: argparse.Namespace):
        """
        Initializes the object with the arguments of the parsed namespace.

        :param ns: the parsed arguments
        :type ns: argparse.Namespace
        """
        super()._apply_args(ns)
        self.source = ns.input
        self.source_list = ns.input_list
        self.include_pattern = ns.include_pattern
        self.exclude_pattern = ns.exclude_pattern

    def _accept_input(self, resource: str) -> bool:
        """
        Checks whether to keep this resource path/url as input.

        :param resource: the resource to check
        :type resource: str
        :return: whether to keep (True) or not (False)
        :rtype: bool
        """
        resource = resource.strip()
        if len(resource) == 0:
            return False
        if resource.startswith("http://") or resource.startswith("https://"):
            return True
        if os.path.exists(resource) and os.path.isdir(resource):
            return True
        return False

    def initialize(self):
        """
        Initializes the reading, e.g., for opening files or databases.
        """
        super().initialize()
        self._inputs = []
        if self.source is not None:
            for d in self.source:
                d = expand_placeholders(d.strip())
                if self._accept_input(d):
                    self._inputs.append(d)
        if self.source_list is not None:
            for d in self.source_list:
                with open(d, "r") as fp:
                    lines = fp.readlines()
                for line in lines:
                    line = expand_placeholders(line.strip())
                    if self._accept_input(line):
                        self._inputs.append(line)

    def read(self) -> Iterable[PretrainData]:
        """
        Loads the data and returns the items one by one.

        :return: the data
        :rtype: Iterable[PretrainData]
        """
        self._current_input = self._inputs.pop(0)
        self.session.current_input = self._current_input
        self.logger().info("Reading from: " + str(self.session.current_input))

        try:
            summary, tree, content = ingest(self.session.current_input,
                                            include_patterns=self.include_pattern,
                                            exclude_patterns=self.exclude_pattern)
            meta = dict()
            meta["file"] = re.sub("[^0-9a-zA-Z]+", "_", self.session.current_input)
            meta["repository"] = self.session.current_input
            meta["summary"] = summary
            meta["tree"] = tree
            yield PretrainData(
                content=content,
                meta=meta,
            )
        except:
            self.logger().exception("Failed to read from: %s" % self.session.current_input)
            yield None

    def has_finished(self) -> bool:
        """
        Returns whether reading has finished.

        :return: True if finished
        :rtype: bool
        """
        return len(self._inputs) == 0
