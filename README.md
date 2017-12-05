# Valorum Data

This package provides a simplified interface to datasets that we use frequently.

To load a dataset, you should write

```python
import valorumdata as vd


df = vd.data_read("DataName")
```

If the dataset has already been loaded onto your computer, then it will load a local version, otherwise
the data will be retrieved from online and saved to your computer.

## Datasets

* [test](./datasets/test.md)

## Contributing datasets

To contribute a dataset, you need to do 2 things.

1. Write a `_data_retrieve_{name}` method which can download the data from online
2. Write a description of the data in a markdown file that goes in the "datasets" folder and provide a link from the README

