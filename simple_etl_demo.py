#!/usr/bin/env python3
"""
Simple ETL Demo using Pandas (PyFlink Alternative)
This demonstrates the ETL concept when PyFlink is not available
"""

import pandas as pd
import os
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def extract_data():
    """Extract data from CSV file"""
    input_file = 'data/input/sales.csv'
    
    if not os.path.exists(input_file):
        logger.error(f"Input file not found: {input_file}")
        return None
    
    logger.info(f"Extracting data from {input_file}")
    df = pd.read_csv(input_file)
    logger.info(f"Extracted {len(df)} records")
    
    return df

def transform_data(df):
    """Transform the data - clean, filter, and aggregate"""
    logger.info("Starting data transformations...")
    
    # Data validation - filter out invalid records
    df_clean = df[
        (df['quantity'] > 0) & 
        (df['price'] > 0) & 
        (df['customer_id'].notna()) &
        (df['store_location'].notna())
    ].copy()
    
    logger.info(f"After validation: {len(df_clean)} valid records")
    
    # Calculate total amount per transaction
    df_clean['total_amount'] = df_clean['quantity'] * df_clean['price']
    
    # Group by customer and store location, then aggregate
    df_aggregated = df_clean.groupby(['customer_id', 'store_location']).agg({
        'total_amount': 'sum',
        'quantity': 'sum',
        'price': 'mean',
        'transaction_id': 'count'
    }).round(2)
    
    # Rename columns for clarity
    df_aggregated.columns = ['total_amount', 'total_quantity', 'avg_price', 'transaction_count']
    
    # Reset index to make customer_id and store_location regular columns
    df_aggregated = df_aggregated.reset_index()
    
    # Add processing timestamp
    df_aggregated['processing_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    logger.info(f"Transformation complete: {len(df_aggregated)} aggregated records")
    
    return df_aggregated

def load_data(df):
    """Load the transformed data to output file"""
    output_dir = 'data/output'
    os.makedirs(output_dir, exist_ok=True)
    
    output_file = os.path.join(output_dir, 'processed_sales.csv')
    
    logger.info(f"Loading data to {output_file}")
    df.to_csv(output_file, index=False)
    
    logger.info(f"Successfully saved {len(df)} records to {output_file}")
    return output_file

def validate_output(output_file):
    """Validate the output file"""
    if not os.path.exists(output_file):
        logger.error(f"Output file not found: {output_file}")
        return False
    
    # Read and validate output
    try:
        df_output = pd.read_csv(output_file)
        
        if df_output.empty:
            logger.error("Output file is empty")
            return False
        
        logger.info(f"Output validation successful. Found {len(df_output)} processed records.")
        logger.info("Sample output:")
        print(df_output.head().to_string(index=False))
        
        return True
        
    except Exception as e:
        logger.error(f"Error validating output: {str(e)}")
        return False

def run_etl_pipeline():
    """Run the complete ETL pipeline"""
    logger.info("Starting Simple ETL Pipeline...")
    
    try:
        # Extract
        df_raw = extract_data()
        if df_raw is None:
            return False
        
        # Transform
        df_transformed = transform_data(df_raw)
        
        # Load
        output_file = load_data(df_transformed)
        
        # Validate
        if validate_output(output_file):
            logger.info("ETL Pipeline completed successfully!")
            return True
        else:
            logger.error("ETL Pipeline failed during validation")
            return False
        
    except Exception as e:
        logger.error(f"ETL Pipeline failed: {str(e)}")
        return False

if __name__ == "__main__":
    success = run_etl_pipeline()
    exit(0 if success else 1)