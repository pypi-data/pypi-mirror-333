from typing import List, Dict


def list_classes() -> Dict[str, List[str]]:
    return {
        "seppl.io.Reader": [
            "idc.labelme.reader.imgcls",
            "idc.labelme.reader.objdet",
        ],
        "seppl.io.Writer": [
            "idc.labelme.writer.imgcls",
            "idc.labelme.writer.objdet",
        ],
    }
