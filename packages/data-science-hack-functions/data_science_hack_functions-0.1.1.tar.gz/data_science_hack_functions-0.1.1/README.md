# summary_stats

A Python package for generating summary statistics of pandas DataFrames.

## Installation
Install directly from PyPI:
```bash
pip install summary-stats

## Usage
After installing, you can use the package like this:

```python
import pandas as pd
from summary_stats import summary_stats

# Create a sample dataset
df = pd.DataFrame({
    "A": [1, 2, 3, None],
    "B": ["x", "y", "z", "x"]
})

# Generate summary statistics
summary, desc = summary_stats(df)

# Print the summary
print(summary)
