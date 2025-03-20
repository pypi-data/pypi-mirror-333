import argparse
import json
import os
from collections import OrderedDict
from typing import List

from seppl.placeholders import placeholder_list, InputBasedPlaceholderSupporter
from wai.logging import LOGGING_WARNING
from idc.api import ImageClassificationData, SplittableStreamWriter, make_list, AnnotationsOnlyWriter, add_annotations_only_param


class LabelMeImageClassificationWriter(SplittableStreamWriter, AnnotationsOnlyWriter, InputBasedPlaceholderSupporter):

    def __init__(self, output_dir: str = None, labels: List[str] = None, annotations_only: bool = None,
                 split_names: List[str] = None, split_ratios: List[int] = None,
                 logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the reader.

        :param output_dir: the output directory to save the image/report in
        :type output_dir: str
        :param labels: all the possible labels to store in the flags section of the json file
        :type labels: str
        :param split_names: the names of the splits, no splitting if None
        :type split_names: list
        :param split_ratios: the integer ratios of the splits (must sum up to 100)
        :type split_ratios: list
        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(split_names=split_names, split_ratios=split_ratios, logger_name=logger_name, logging_level=logging_level)
        self.output_dir = output_dir
        self.labels = labels
        self.annotations_only = annotations_only

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "to-labelme-ic"

    def description(self) -> str:
        """
        Returns a description of the writer.

        :return: the description
        :rtype: str
        """
        return "Saves the classification label in a labelme .json file alongside the image."

    def _create_argparser(self) -> argparse.ArgumentParser:
        """
        Creates an argument parser. Derived classes need to fill in the options.

        :return: the parser
        :rtype: argparse.ArgumentParser
        """
        parser = super()._create_argparser()
        parser.add_argument("-o", "--output", type=str, help="The directory to store the images/.json files in. Any defined splits get added beneath there. " + placeholder_list(obj=self), required=True)
        parser.add_argument("--labels", metavar="LABEL", type=str, default=None, help="All the available labels to store in the 'flags' section of the json file.", nargs="*")
        add_annotations_only_param(parser)
        return parser

    def _apply_args(self, ns: argparse.Namespace):
        """
        Initializes the object with the arguments of the parsed namespace.

        :param ns: the parsed arguments
        :type ns: argparse.Namespace
        """
        super()._apply_args(ns)
        self.output_dir = ns.output
        self.labels = ns.labels
        self.annotations_only = ns.annotations_only

    def accepts(self) -> List:
        """
        Returns the list of classes that are accepted.

        :return: the list of classes
        :rtype: list
        """
        return [ImageClassificationData]

    def initialize(self):
        """
        Initializes the processing, e.g., for opening files or databases.
        """
        super().initialize()
        if self.labels is None:
            self.labels = []
        if self.annotations_only is None:
            self.annotations_only = False

    def write_stream(self, data):
        """
        Saves the data one by one.

        :param data: the data to write (single record or iterable of records)
        """
        for item in make_list(data):
            sub_dir = self.session.expand_placeholders(self.output_dir)
            if self.splitter is not None:
                split = self.splitter.next()
                sub_dir = os.path.join(sub_dir, split)
            if not os.path.exists(sub_dir):
                self.logger().info("Creating dir: %s" % sub_dir)
                os.makedirs(sub_dir)

            annotations = OrderedDict()
            annotations["version"] = "4.0.0"
            annotations["flags"] = OrderedDict()
            annotations["shapes"] = []
            annotations["imagePath"] = item.image_name
            annotations["imageData"] = None
            annotations["imageHeight"] = item.image_height
            annotations["imageWidth"] = item.image_width
            annotations["flags"]["__ignored__"] = False
            for l in self.labels:
                annotations["flags"][l] = False
            if item.has_annotation():
                annotations["flags"][item.annotation] = True

            path = os.path.join(sub_dir, item.image_name)
            if not self.annotations_only:
                self.logger().info("Writing image to: %s" % path)
                item.save_image(path)

            path = os.path.splitext(path)[0] + ".json"
            self.logger().info("Writing annotation to: %s" % path)
            with open(path, "w") as fp:
                json.dump(annotations, fp, indent=2)
