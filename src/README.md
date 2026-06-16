# Hurricane Net

`hurricane_net` is a Python package designed to facilitate the analysis and exploration of hurricane and tropical storm data from the International Best Track Archive for Climate Stewardship (IBTrACS). The package leverages the power of Pandas to filter and manipulate data, making it easier to perform analyses on specific storm regions or types, such as Atlantic hurricanes.

## Features

- **Data Loading**: Easily load IBTrACS data directly from a provided URL.
- **Filtering**: Filter data by storm basin or type (e.g., hurricanes) using intuitive methods.
- **Logging**: Comprehensive logging for debugging and tracking the data loading and filtering processes.
- **Prompt Templates**: Use predefined prompt templates for generating daily reports or other structured outputs.

## Installation

To install `hurricane_net`, you can use pip to install it from a local source or directly from a repository if available. If you are building a wheel, follow the instructions in the setup documentation.

```bash
pip install hurricane_net
```

## Usage

Below are examples demonstrating how to use `hurricane_net` to load, filter, and generate reports on storm data.

### Importing the Package

```python
import hurricane_net as hn
```

### Loading and Filtering Data

1. **Load Latest Data**

   Load the IBTrACS data from a specified URL. The default URL points to the IBTrACS database. Run this again to update data to the latest.

   ```python
   data_loader = hn.data()
   ```

   Note that this requires internet so that the latest data is available.

2. **Create Data Frame**

   Filter the data based on different criteria. For example, to get all storms, Atlantic storms, or hurricanes:

   ```python
   # Load all available storms
   data_loader.filter('all')
   all_storms = data_loader.storms

   # Load storms from the North Atlantic basin
   data_loader.filter('NA')
   atlantic_storms = data_loader.storms

   # Load hurricanes (NA basin with USA_STATUS 'HU' or 'HR')
   data_loader.filter('hurricanes')
   hurricanes = data_loader.storms
   ```

3. **Logging**

   The package logs all major actions, such as data loading and filtering, to help trace operations.

### Generating Reports

The `Prompt` class provides functionality to generate reports using predefined templates.


## References

- [IBTrACS Data Access](https://www.ncei.noaa.gov/data/international-best-track-archive-for-climate-stewardship-ibtracs/v04r01/access/csv/)
- [IBTrACS Documentation](https://www.ncei.noaa.gov/products/international-best-track-archive)
- [IBTrACS v04r01 Column Documentation](https://www.ncei.noaa.gov/sites/default/files/2025-09/IBTrACS_v04r01_column_documentation.pdf)

## Troubleshooting

- [Python Package](https://github.com/hammad93/hurricane-net/issues/19)

## License

This package is open source. Please see the LICENSE file for more information.

## Contributing

Contributions are welcome! Please feel free to open issues or submit pull requests.

## Acknowledgments

This package uses data from the International Best Track Archive for Climate Stewardship (IBTrACS) maintained by NOAA's National Centers for Environmental Information (NCEI).