# image-dataset-converter-labelme
[image-dataset-converter](https://github.com/waikato-datamining/image-dataset-converter) 
plugins for [labelme](https://github.com/wkentaro/labelme).


## Installation

Via PyPI:

```bash
pip install image_dataset_converter_labelme
```

The latest code straight from the repository:

```bash
pip install git+https://github.com/waikato-datamining/image-dataset-converter-labelme.git
```

## Dataset formats

The following dataset formats are supported:

| Domain                | Format                                     | Read                            | Write                          | 
|:----------------------|:-------------------------------------------|:--------------------------------|:-------------------------------| 
| Image classification  | [labelme](formats/imageclassification.md)  | [Y](plugins/from-labelme-ic.md) | [Y](plugins/to-labelme-ic.md)  | 
| Instance segmentation | [labelme](formats/instancesegmentation.md) | [Y](plugins/from-labelme-od.md) | [Y](plugins/to-labelme-od.md)  | 
| Object detection      | [labelme](formats/objectdetection.md)      | [Y](plugins/from-labelme-od.md) | [Y](plugins/to-labelme-od.md)  | 


## Plugins

See [here](plugins/README.md) for an overview of all plugins.

