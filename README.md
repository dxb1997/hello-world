# PyFlink ETL Project

A simple Extract, Transform, Load (ETL) pipeline built with Apache Flink's Python API (PyFlink). This project demonstrates how to process streaming data using Flink's table API for data transformation and analysis.

## Project Overview

This ETL pipeline:
1. **Extracts** data from CSV files (sales transactions)
2. **Transforms** the data by filtering, aggregating, and calculating metrics
3. **Loads** the processed results into output files

## Features

- Stream processing with PyFlink
- CSV data source and sink connectors
- Data validation and filtering
- Aggregation operations (sum, average)
- Configurable pipeline parameters
- Comprehensive logging
- Error handling

## Project Structure

```
├── etl_pipeline.py          # Main ETL pipeline script
├── config.py                # Configuration management
├── requirements.txt         # Python dependencies
├── .env                     # Environment variables
├── data/
│   ├── input/
│   │   └── sales.csv       # Sample input data
│   └── output/             # Processed output files
└── README.md               # This file
```

## Installation

1. **Clone the repository** (if not already done):
   ```bash
   git clone <repository-url>
   cd pyflink-etl-project
   ```

2. **Create a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running the ETL Pipeline

1. **Basic execution**:
   ```bash
   python etl_pipeline.py
   ```

2. **With custom configuration**:
   ```bash
   # Modify .env file or set environment variables
   export FLINK_PARALLELISM=2
   export MIN_QUANTITY=2
   python etl_pipeline.py
   ```

### Input Data Format

The pipeline expects CSV files with the following structure:
```csv
transaction_id,customer_id,product_name,quantity,price,transaction_date,store_location
TXN001,CUST001,Laptop,1,999.99,2024-01-15,New York
```

### Output Data Format

The processed data includes:
```csv
customer_id,total_amount,total_quantity,avg_price,store_location,processing_time
CUST001,1294.97,4,323.74,New York,2024-01-23 10:30:00
```

## Configuration

The pipeline can be configured through environment variables in the `.env` file:

- `FLINK_PARALLELISM`: Number of parallel tasks (default: 1)
- `CHECKPOINT_INTERVAL`: Checkpoint interval in milliseconds (default: 60000)
- `INPUT_PATH`: Path to input data directory (default: data/input)
- `OUTPUT_PATH`: Path to output data directory (default: data/output)
- `MIN_QUANTITY`: Minimum quantity filter (default: 1)
- `MIN_PRICE`: Minimum price filter (default: 0.01)
- `LOG_LEVEL`: Logging level (default: INFO)

## Data Transformations

The ETL pipeline performs the following transformations:

1. **Data Validation**: Filters out records with invalid quantities or prices
2. **Aggregation**: Groups data by customer and store location
3. **Calculations**: 
   - Total amount spent per customer per store
   - Total quantity purchased
   - Average price per transaction
4. **Enrichment**: Adds processing timestamp

## Development

### Adding New Transformations

To add new transformations, modify the `transform_data()` function in `etl_pipeline.py`:

```python
def transform_data(t_env):
    source_table = t_env.from_path('sales_data')
    
    # Add your transformations here
    transformed_table = source_table \
        .filter(your_filter_condition) \
        .select(your_columns) \
        .group_by(your_grouping_columns) \
        .select(your_aggregations)
    
    return transformed_table
```

### Extending Data Sources

To add new data sources, create additional source tables in `create_source_table()`:

```python
def create_additional_source_table(t_env):
    source_ddl = """
        CREATE TABLE your_table (
            column1 STRING,
            column2 INT
        ) WITH (
            'connector' = 'your-connector',
            'path' = 'your-path'
        )
    """
    t_env.execute_sql(source_ddl)
```

## Troubleshooting

### Common Issues

1. **Java Runtime Error**: Ensure Java 8 or 11 is installed
   ```bash
   java -version
   ```

2. **Memory Issues**: Adjust JVM memory settings
   ```bash
   export FLINK_CONF_DIR=/path/to/flink/conf
   ```

3. **Path Issues**: Ensure data directories exist
   ```bash
   mkdir -p data/input data/output
   ```

### Logs

Check the application logs for detailed error information. Logs include:
- Pipeline execution status
- Data processing metrics
- Error messages and stack traces

## Performance Tuning

For production environments, consider:

1. **Increase Parallelism**: Set `FLINK_PARALLELISM` to match your CPU cores
2. **Optimize Checkpointing**: Adjust `CHECKPOINT_INTERVAL` based on your requirements
3. **Memory Management**: Configure Flink's memory settings
4. **Batch Processing**: For large datasets, consider batch processing mode

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is open source and available under the [MIT License](LICENSE).

## Dependencies

- Apache Flink 1.18.0
- PyFlink 1.18.0
- Pandas 2.0.3
- NumPy 1.24.3
- python-dotenv 1.0.0

## Support

For questions or issues, please:
1. Check the troubleshooting section
2. Review Flink documentation: https://flink.apache.org/
3. Open an issue in the repository
