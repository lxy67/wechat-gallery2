#!/usr/bin/env python3
"""
Script to import data from CSV file to PostgreSQL database.
"""
import os
import logging
import pandas as pd
import psycopg2
from psycopg2.extras import execute_batch
from dotenv import load_dotenv
from typing import Dict, List, Optional, Tuple

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('import.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

class DatabaseImporter:
    def __init__(self):
        self.conn = None
        self.cur = None
        self.cache = {
            'countries': {},
            'regions': {},
            'diseases': {},
            'drug_resistances': {}
        }
        
    def connect(self):
        """Establish database connection."""
        try:
            self.conn = psycopg2.connect(
                dbname=os.getenv('DB_NAME', 'hpdata'),
                user=os.getenv('DB_USER', 'postgres'),
                password=os.getenv('DB_PASSWORD', '123456'),
                host=os.getenv('DB_HOST', '127.0.0.1'),
                port=os.getenv('DB_PORT', '5432')
            )
            self.cur = self.conn.cursor()
            logger.info("Successfully connected to the database")
        except Exception as e:
            logger.error(f"Error connecting to database: {e}")
            raise
    
    def close(self):
        """Close database connection."""
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()
            logger.info("Database connection closed")
    
    def get_or_create_country(self, country_name: str) -> int:
        """Get country ID or create if it doesn't exist."""
        if not country_name:
            return None
            
        if country_name in self.cache['countries']:
            return self.cache['countries'][country_name]
            
        try:
            self.cur.execute(
                """
                INSERT INTO countries (name) 
                VALUES (%s) 
                ON CONFLICT (name) DO UPDATE SET name = EXCLUDED.name 
                RETURNING id
                """,
                (country_name,)
            )
            country_id = self.cur.fetchone()[0]
            self.cache['countries'][country_name] = country_id
            return country_id
        except Exception as e:
            logger.error(f"Error getting/creating country {country_name}: {e}")
            self.conn.rollback()
            raise
    
    def get_or_create_region(self, region_name: str, country_id: int) -> int:
        """Get region ID or create if it doesn't exist."""
        if not region_name or not country_id:
            return None
            
        cache_key = f"{country_id}_{region_name}"
        if cache_key in self.cache['regions']:
            return self.cache['regions'][cache_key]
            
        try:
            self.cur.execute(
                """
                INSERT INTO regions (name, country_id) 
                VALUES (%s, %s) 
                ON CONFLICT (name, country_id) DO UPDATE SET name = EXCLUDED.name 
                RETURNING id
                """,
                (region_name, country_id)
            )
            region_id = self.cur.fetchone()[0]
            self.cache['regions'][cache_key] = region_id
            return region_id
        except Exception as e:
            logger.error(f"Error getting/creating region {region_name}: {e}")
            self.conn.rollback()
            raise
    
    def get_or_create_disease(self, disease_name: str) -> int:
        """Get disease ID or create if it doesn't exist."""
        if not disease_name:
            return None
            
        if disease_name in self.cache['diseases']:
            return self.cache['diseases'][disease_name]
            
        try:
            self.cur.execute(
                """
                INSERT INTO diseases (name) 
                VALUES (%s) 
                ON CONFLICT (name) DO UPDATE SET name = EXCLUDED.name 
                RETURNING id
                """,
                (disease_name,)
            )
            disease_id = self.cur.fetchone()[0]
            self.cache['diseases'][disease_name] = disease_id
            return disease_id
        except Exception as e:
            logger.error(f"Error getting/creating disease {disease_name}: {e}")
            self.conn.rollback()
            raise
    
    def get_or_create_drug_resistance(self, resistance_name: str) -> int:
        """Get drug resistance ID or create if it doesn't exist."""
        if not resistance_name:
            return None
            
        if resistance_name in self.cache['drug_resistances']:
            return self.cache['drug_resistances'][resistance_name]
            
        try:
            self.cur.execute(
                """
                INSERT INTO drug_resistances (name) 
                VALUES (%s) 
                ON CONFLICT (name) DO UPDATE SET name = EXCLUDED.name 
                RETURNING id
                """,
                (resistance_name,)
            )
            resistance_id = self.cur.fetchone()[0]
            self.cache['drug_resistances'][resistance_name] = resistance_id
            return resistance_id
        except Exception as e:
            logger.error(f"Error getting/creating drug resistance {resistance_name}: {e}")
            self.conn.rollback()
            raise
    
    def import_csv(self, file_path: str, batch_size: int = 100):
        """Import data from CSV file to database."""
        try:
            # Read CSV file
            logger.info(f"Reading CSV file: {file_path}")
            df = pd.read_csv(file_path, encoding='utf-8')
            
            # Convert column names to lowercase for case-insensitive matching
            df.columns = df.columns.str.strip().str.lower()
            
            # Validate required columns
            required_columns = ['strain', 'gene_seq', 'raw_country', 'region', 'host_disease', 'drug_resistance']
            missing_columns = [col for col in required_columns if col not in df.columns]
            if missing_columns:
                raise ValueError(f"Missing required columns in CSV: {', '.join(missing_columns)}")
            
            # Process data in batches
            total_rows = len(df)
            logger.info(f"Starting import of {total_rows} rows...")
            
            for i in range(0, total_rows, batch_size):
                batch = df.iloc[i:i+batch_size]
                strain_data = []
                
                for _, row in batch.iterrows():
                    try:
                        # Get or create related entities
                        country_id = self.get_or_create_country(str(row['raw_country']).strip())
                        region_id = self.get_or_create_region(
                            str(row['region']).strip(), 
                            country_id
                        ) if pd.notna(row['region']) else None
                        disease_id = self.get_or_create_disease(str(row['host_disease']).strip()) \
                            if pd.notna(row['host_disease']) else None
                        resistance_id = self.get_or_create_drug_resistance(
                            str(row['drug_resistance']).strip()
                        ) if pd.notna(row['drug_resistance']) else None
                        
                        # Prepare strain data
                        strain_data.append((
                            str(row['strain']).strip(),
                            str(row['gene_seq']).strip(),
                            country_id,
                            region_id,
                            disease_id,
                            resistance_id
                        ))
                        
                    except Exception as e:
                        logger.error(f"Error processing row {_}: {e}")
                        continue
                
                # Insert strains in batch
                if strain_data:
                    self.cur.executemany(
                        """
                        INSERT INTO strains 
                        (strain_id, gene_seq, country_id, region_id, disease_id, drug_resistance_id)
                        VALUES (%s, %s, %s, %s, %s, %s)
                        ON CONFLICT (strain_id) DO UPDATE SET
                            gene_seq = EXCLUDED.gene_seq,
                            country_id = EXCLUDED.country_id,
                            region_id = EXCLUDED.region_id,
                            disease_id = EXCLUDED.disease_id,
                            drug_resistance_id = EXCLUDED.drug_resistance_id
                        """,
                        strain_data
                    )
                    self.conn.commit()
                    logger.info(f"Imported batch {i//batch_size + 1}/{(total_rows + batch_size - 1)//batch_size}")
            
            logger.info("Import completed successfully!")
            
        except Exception as e:
            logger.error(f"Error during import: {e}")
            if self.conn:
                self.conn.rollback()
            raise

def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Import CSV data to PostgreSQL database')
    parser.add_argument('csv_file', help='Path to the CSV file to import')
    parser.add_argument('--batch-size', type=int, default=100, help='Batch size for database operations')
    args = parser.parse_args()
    
    importer = DatabaseImporter()
    try:
        importer.connect()
        importer.import_csv(args.csv_file, args.batch_size)
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        return 1
    finally:
        importer.close()
    
    return 0

if __name__ == "__main__":
    exit(main())
