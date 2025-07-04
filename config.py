#!/usr/bin/env python3
"""
Configuration settings for PyFlink ETL Pipeline
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class ETLConfig:
    """Configuration class for ETL pipeline"""
    
    # Flink Configuration
    PARALLELISM = int(os.getenv('FLINK_PARALLELISM', '1'))
    CHECKPOINT_INTERVAL = int(os.getenv('CHECKPOINT_INTERVAL', '60000'))  # milliseconds
    
    # Data Paths
    INPUT_PATH = os.getenv('INPUT_PATH', 'data/input')
    OUTPUT_PATH = os.getenv('OUTPUT_PATH', 'data/output')
    
    # Source Configuration
    SOURCE_FILE = os.path.join(INPUT_PATH, 'sales.csv')
    
    # Sink Configuration
    SINK_FILE = os.path.join(OUTPUT_PATH, 'processed_sales.csv')
    
    # Processing Configuration
    MIN_QUANTITY = int(os.getenv('MIN_QUANTITY', '1'))
    MIN_PRICE = float(os.getenv('MIN_PRICE', '0.01'))
    
    # Logging Configuration
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    @classmethod
    def validate_paths(cls):
        """Validate that required directories exist"""
        os.makedirs(cls.INPUT_PATH, exist_ok=True)
        os.makedirs(cls.OUTPUT_PATH, exist_ok=True)
    
    @classmethod
    def get_flink_config(cls):
        """Get Flink-specific configuration as dictionary"""
        return {
            'parallelism': cls.PARALLELISM,
            'checkpoint_interval': cls.CHECKPOINT_INTERVAL,
        }
    
    @classmethod
    def get_source_config(cls):
        """Get source configuration as dictionary"""
        return {
            'path': cls.SOURCE_FILE,
            'format': 'csv',
            'min_quantity': cls.MIN_QUANTITY,
            'min_price': cls.MIN_PRICE,
        }
    
    @classmethod
    def get_sink_config(cls):
        """Get sink configuration as dictionary"""
        return {
            'path': cls.SINK_FILE,
            'format': 'csv',
        }