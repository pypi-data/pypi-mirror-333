# MLFastFlow

A Python package for fast dataflow and workflow processing.

## Installation

```bash
pip install mlfastflow
```

## Features

- Easy-to-use data sourcing with the Sourcing class
- Flexible vector search capabilities
- Optimized for data processing workflows

## Quick Start

```python
from mlfastflow import Sourcing

# Create a sourcing instance
sourcing = Sourcing(
    query_df=your_query_dataframe,
    db_df=your_database_dataframe,
    columns_for_sourcing=["column1", "column2"],
    label="your_label"
)

# Process your data
sourced_db_df_without_label, sourced_db_df_with_label = (
    sourcing.sourcing()
)
```

## License

MIT

## Author

Xileven
