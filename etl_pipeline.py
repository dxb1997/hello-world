#!/usr/bin/env python3
"""
Simple PyFlink ETL Pipeline
This script demonstrates a basic ETL workflow using PyFlink:
1. Extract: Read data from CSV files
2. Transform: Clean and process the data
3. Load: Write results to output files
"""

import os
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import StreamTableEnvironment, EnvironmentSettings
from pyflink.table.expressions import col, lit
from pyflink.table.window import Tumble
from pyflink.common import Types
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def create_environment():
    """Create and configure the Flink execution environment"""
    # Create streaming environment
    env = StreamExecutionEnvironment.get_execution_environment()
    env.set_parallelism(1)  # Set parallelism for local execution
    
    # Create table environment
    settings = EnvironmentSettings.new_instance().in_streaming_mode().build()
    t_env = StreamTableEnvironment.create(env, environment_settings=settings)
    
    return env, t_env

def create_source_table(t_env):
    """Create source table from CSV file"""
    # Define the source table DDL
    source_ddl = """
        CREATE TABLE sales_data (
            transaction_id STRING,
            customer_id STRING,
            product_name STRING,
            quantity INT,
            price DECIMAL(10,2),
            transaction_date STRING,
            store_location STRING
        ) WITH (
            'connector' = 'filesystem',
            'path' = 'data/input/sales.csv',
            'format' = 'csv',
            'csv.ignore-parse-errors' = 'true',
            'csv.allow-comments' = 'true'
        )
    """
    t_env.execute_sql(source_ddl)
    logger.info("Source table 'sales_data' created successfully")

def create_sink_table(t_env):
    """Create sink table for processed data"""
    # Ensure output directory exists
    os.makedirs('data/output', exist_ok=True)
    
    sink_ddl = """
        CREATE TABLE processed_sales (
            customer_id STRING,
            total_amount DECIMAL(10,2),
            total_quantity INT,
            avg_price DECIMAL(10,2),
            store_location STRING,
            processing_time TIMESTAMP(3)
        ) WITH (
            'connector' = 'filesystem',
            'path' = 'data/output/processed_sales.csv',
            'format' = 'csv'
        )
    """
    t_env.execute_sql(sink_ddl)
    logger.info("Sink table 'processed_sales' created successfully")

def transform_data(t_env):
    """Apply transformations to the source data"""
    # Get source table
    source_table = t_env.from_path('sales_data')
    
    # Apply transformations
    transformed_table = source_table \
        .filter(col('quantity') > 0) \
        .filter(col('price') > 0) \
        .select(
            col('customer_id'),
            col('quantity'),
            col('price'),
            (col('quantity') * col('price')).alias('total_amount'),
            col('store_location')
        ) \
        .group_by(col('customer_id'), col('store_location')) \
        .select(
            col('customer_id'),
            col('total_amount').sum.alias('total_amount'),
            col('quantity').sum.alias('total_quantity'),
            col('total_amount').avg.alias('avg_price'),
            col('store_location'),
            lit('CURRENT_TIMESTAMP').alias('processing_time')
        )
    
    logger.info("Data transformations applied successfully")
    return transformed_table

def run_etl_pipeline():
    """Main ETL pipeline execution"""
    try:
        logger.info("Starting PyFlink ETL pipeline...")
        
        # Create environment
        env, t_env = create_environment()
        
        # Create tables
        create_source_table(t_env)
        create_sink_table(t_env)
        
        # Transform data
        result_table = transform_data(t_env)
        
        # Insert results into sink
        result_table.execute_insert('processed_sales')
        
        logger.info("ETL pipeline completed successfully!")
        
    except Exception as e:
        logger.error(f"ETL pipeline failed: {str(e)}")
        raise

if __name__ == "__main__":
    run_etl_pipeline()