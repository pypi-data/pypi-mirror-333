import argparse
import json
import sys
from typing import List, Iterable, Union

import numpy as np
from wai.logging import LOGGING_WARNING
from wai.common.adams.imaging.locateobjects import LocatedObjects, LocatedObject
from wai.common.geometry import Polygon, Point
from seppl.placeholders import PlaceholderSupporter, placeholder_list
from seppl.io import locate_files
from idc.api import ObjectDetectionData, locate_image
from idc.api import Reader


class LabelMeObjectDetectionReader(Reader, PlaceholderSupporter):

    def __init__(self, source: Union[str, List[str]] = None, source_list: Union[str, List[str]] = None,
                 logger_name: str = None, logging_level: str = LOGGING_WARNING):
        """
        Initializes the reader.

        :param source: the filename(s)
        :param source_list: the file(s) with filename(s)
        :param logger_name: the name to use for the logger
        :type logger_name: str
        :param logging_level: the logging level to use
        :type logging_level: str
        """
        super().__init__(logger_name=logger_name, logging_level=logging_level)
        self.source = source
        self.source_list = source_list
        self._inputs = None
        self._current_input = None

    def name(self) -> str:
        """
        Returns the name of the handler, used as sub-command.

        :return: the name
        :rtype: str
        """
        return "from-labelme-od"

    def description(self) -> str:
        """
        Returns a description of the reader.

        :return: the description
        :rtype: str
        """
        return "Loads the bounding box and/or polygon definitions from the associated labelme .json file."

    def _create_argparser(self) -> argparse.ArgumentParser:
        """
        Creates an argument parser. Derived classes need to fill in the options.

        :return: the parser
        :rtype: argparse.ArgumentParser
        """
        parser = super()._create_argparser()
        parser.add_argument("-i", "--input", type=str, help="Path to the json file(s) to read; glob syntax is supported; " + placeholder_list(obj=self), required=False, nargs="*")
        parser.add_argument("-I", "--input_list", type=str, help="Path to the text file(s) listing the json files to use; " + placeholder_list(obj=self), required=False, nargs="*")
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

    def generates(self) -> List:
        """
        Returns the list of classes that get produced.

        :return: the list of classes
        :rtype: list
        """
        return [ObjectDetectionData]

    def initialize(self):
        """
        Initializes the processing, e.g., for opening files or databases.
        """
        super().initialize()
        self._inputs = locate_files(self.source, input_lists=self.source_list, fail_if_empty=True, default_glob="*.json")

    def read(self) -> Iterable:
        """
        Loads the data and returns the items one by one.

        :return: the data
        :rtype: Iterable
        """
        self.finalize()

        self._current_input = self._inputs.pop(0)
        self.session.current_input = self._current_input
        self.logger().info("Reading from: " + str(self.session.current_input))

        with open(self._current_input, "r") as fp:
            labelme = json.load(fp)
        annotations = LocatedObjects()
        if "shapes" in labelme:
            for shape in labelme["shapes"]:
                label = shape.get("label", None)
                lobj = None
                shape_type = shape.get("shape_type", None)
                if shape_type == "rectangle":
                    (xmin, ymin), (xmax, ymax) = shape["points"]
                    lobj = LocatedObject(xmin, ymin, xmax - xmin + 1, ymax - ymin + 1)
                elif shape_type == "circle":
                    self.logger().warning("circle type not supported, approximating")
                    # taken from: https://github.com/wkentaro/labelme/blob/main/examples/instance_segmentation/labelme2coco.py
                    (x1, y1), (x2, y2) = shape["points"]
                    r = np.linalg.norm([x2 - x1, y2 - y1])
                    # r(1-cos(a/2))<x, a=2*pi/N => N>pi/arccos(1-x/r)
                    # x: tolerance of the gap between the arc and the line segment
                    n_points_circle = max(int(np.pi / np.arccos(1 - 1 / r)), 12)
                    i = np.arange(n_points_circle)
                    x = x1 + r * np.sin(2 * np.pi / n_points_circle * i)
                    y = y1 + r * np.cos(2 * np.pi / n_points_circle * i)
                    lobj = LocatedObject(int(min(x)), int(min(y)), int(max(x) - min(x) + 1), int(max(y) - min(y) + 1))
                    points = [Point(x_, y_) for x_, y_ in zip(x, y)]
                    lobj.set_polygon(Polygon(*points))
                else:
                    xmin = sys.maxsize
                    xmax = 0
                    ymin = sys.maxsize
                    ymax = 0
                    points = []
                    for point in shape["points"]:
                        xmin = min(xmin, point[0])
                        xmax = max(xmax, point[0])
                        ymin = min(ymin, point[1])
                        ymax = max(ymax, point[1])
                        points.append(Point(point[0], point[1]))
                    lobj = LocatedObject(xmin, ymin, xmax - xmin + 1, ymax - ymin + 1)
                    lobj.set_polygon(Polygon(*points))

                # add object
                if lobj is not None:
                    if label is not None:
                        lobj.metadata["type"] = label
                    annotations.append(lobj)

        image = locate_image(self._current_input)
        if image is None:
            self.logger().warning("No associated image found: %s" % self._current_input)
            self._current_input = None
            yield None

        self._current_input = None
        yield ObjectDetectionData(source=image, annotation=annotations)

    def has_finished(self) -> bool:
        """
        Returns whether reading has finished.

        :return: True if finished
        :rtype: bool
        """
        return len(self._inputs) == 0

    def finalize(self):
        """
        Finishes the reading, e.g., for closing files or databases.
        """
        if self._current_input is not None:
            super().finalize()
            self._current_input = None
