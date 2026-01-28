import re
import os
import sys
from datetime import datetime
from app import app, db
from sqlalchemy import text, MetaData

# Map SQL table names to Model classes or table objects
# We can mostly rely on SQLAlchemy metadata, but need to map "public.tablename" to "tablename"
# And handle "public.\"user\"" -> "user"

from sqlalchemy import text, MetaData, DateTime, Date, Boolean, Integer

def parse_date(val):
    if not val:
        return None
    try:
        # Try generic ISO format
        val = val.replace(' ', 'T')
        return datetime.fromisoformat(val)
    except:
        # Fallback or return original
        return val

def parse_value(val, col_type=None):
    if val == '\\N':
        return None
    
    # Handle based on column type if provided
    if col_type is not None:
        if isinstance(col_type, (DateTime, Date)):
            return parse_date(val)
        if isinstance(col_type, Boolean):
            if val == 't': return True
            if val == 'f': return False
            return val # Maybe already bool or 1/0
            
    # Legacy fallback
    if val == 't':
        return True
    if val == 'f':
        return False
    return val

def import_backup(sql_file_path):
    print(f"Importing from {sql_file_path}...")
    
    with app.app_context():
        # Disable FK checks for SQLite to allow out-of-order insertion
        db.session.execute(text("PRAGMA foreign_keys=OFF;"))
        db.session.commit()
        
        # Get all tables from metadata
        metadata = MetaData()
        metadata.reflect(bind=db.engine)
        
        current_table = None
        columns = []
        buffer = []
        
        with open(sql_file_path, 'r', encoding='utf8') as f:
            for line in f:
                line = line.strip()
                
                # Check for COPY start
                # COPY public."user" (id, ... ) FROM stdin;
                copy_match = re.match(r'COPY public\.("?\w+"?)\s*\((.*?)\) FROM stdin;', line)
                
                if copy_match:
                    full_table_name = copy_match.group(1).replace('"', '')
                    columns_str = copy_match.group(2)
                    columns = [c.strip().replace('"', '') for c in columns_str.split(',')]
                    
                    # Map to local table name
                    # logic: remove public., remove quotes
                    current_table = full_table_name
                    
                    print(f"Processing table: {current_table}")
                    
                    # Clear existing data? logic: yes, clear for clean import
                    # Be careful with dependencies if clearing independently, but we disable FKs
                    try:
                        table_obj = metadata.tables.get(current_table)
                        if table_obj is not None:
                            print(f"  - Cleaning existing data in {current_table}...")
                            db.session.execute(table_obj.delete())
                        else:
                            print(f"  - WARNING: Table {current_table} not found in models.")
                            current_table = None # Skip this block
                    except Exception as e:
                        print(f"  - Error clearing table: {e}")
                    
                    continue
                
                # Check for End of COPY
                if line == '\.':
                    if current_table and buffer and metadata.tables.get(current_table) is not None:
                        print(f"  - Inserting {len(buffer)} rows into {current_table}...")
                        table_obj = metadata.tables.get(current_table)
                        
                        # Bulk insert
                        try:
                            # Process buffer into list of dicts
                            data_to_insert = []
                            for row_vals in buffer:
                                if len(row_vals) != len(columns):
                                    print(f"    ERROR: Row length {len(row_vals)} does not match columns {len(columns)}")
                                    continue
                                row_dict = dict(zip(columns, row_vals))
                                data_to_insert.append(row_dict)
                            
                            if data_to_insert:
                                db.session.execute(table_obj.insert(), data_to_insert)
                                db.session.commit()
                                print("    Success.")
                                if current_table == 'user':
                                    print("User table imported successfully. Exiting.")
                                    sys.exit(0)
                        except Exception as e:
                            print(f"    ERROR inserting data into {current_table}")
                            err_msg = str(e)
                            print(f"    Error Message (truncated): {err_msg[:500]}")
                            if current_table == 'user':
                                with open('user_error.txt', 'w', encoding='utf-8') as f_err:
                                    f_err.write(err_msg)
                            if current_table == 'client':
                                with open('client_error.txt', 'w', encoding='utf-8') as f_err:
                                    f_err.write(err_msg)
                            db.session.rollback()
                            
                            if current_table == 'user':
                                print("DEBUG: User table processed. Exiting for debug.")
                                return
                    
                    current_table = None
                    columns = []
                    buffer = []
                    continue
                
                # If we are inside a COPY block
                if current_table:
                    # Parse data line (tabs)
                    # Note: Original line might have spaces/tabs. We stripped it, but split('\t') needs exact content.
                    # Re-read line without strip for data splitting? 
                    # Actually, pg_dump shouldn't have leading/trailing whitespace meaningful unless in value.
                    # But the earlier strip() removed newline. Let's rely on split('\t')
                    
                    # Wait, the iteration variable 'line' is already stripped. 
                    # Some string values might end with space? copy format usually safe.
                    # Let's use the raw file read but inside the loop
                    pass 

        # Re-enable FKs
        db.session.execute(text("PRAGMA foreign_keys=ON;"))
        db.session.commit()
        print("Import finished.")

# Refined reading loop to handle data correctly
def run_import():
    sql_file = r"C:\Users\User\projetos antigravity\FGinovaigestao\backup_producao_inovaigestao (3).sql"
    if not os.path.exists(sql_file):
        print("File not found")
        return

    print(f"Importing {sql_file}...")
    
    with app.app_context():
        # Recreate schema to match models.py
        print("Recreating database schema...")
        db.drop_all()
        db.create_all()
        
        db.session.execute(text("PRAGMA foreign_keys=OFF;"))
        
        metadata = MetaData()
        metadata.reflect(bind=db.engine)
        print(f"DEBUG: All reflected tables: {list(metadata.tables.keys())}")
        
        current_table = None
        columns = []
        data_batch = []
        
        with open(sql_file, 'r', encoding='utf8') as f:
            for line in f:
                # Don't strip yet, we need to check for COPY vs Data
                clean_line = line.strip()
                
                if "COPY public." in clean_line:
                    # Robust regex: table name is anything until space or (
                    # Group 1: Table Name
                    # Group 2: Columns
                    match = re.match(r'COPY public\.([^\s(]+)\s*\((.*?)\) FROM stdin;', clean_line)
                    if match:
                        raw_table_name = match.group(1).replace('"', '')
                        cols_str = match.group(2)
                        columns = [c.strip().replace('"', '') for c in cols_str.split(',')]
                        current_table = raw_table_name
                        
                        # Prepare column types map
                        col_types = {}
                        if current_table and current_table in metadata.tables:
                            table = metadata.tables[current_table]
                            for c in table.columns:
                                col_types[c.name] = c.type

                        print(f"Found table: {current_table}")
                        
                        # Truncate table
                        if current_table in metadata.tables:
                            db.session.execute(metadata.tables[current_table].delete())
                            print(f"  Cleared {current_table}")
                        else:
                            print(f"  Skipping {current_table} (not in metadata)")
                            current_table = None # Skip
                    continue
                
                if "clean_line" in locals() and clean_line == r'\.': # Safe check
                    if current_table and data_batch:
                        table = metadata.tables.get(current_table)
                        if table is not None:
                            print(f"  Inserting {len(data_batch)} rows...")
                            try:
                                db.session.execute(table.insert(), data_batch)
                                db.session.commit()
                                print("    Success.")
                            except Exception as e:
                                print(f"    ERROR inserting data into {current_table}: {repr(e)}")
                                # import traceback
                                # traceback.print_exc()
                                db.session.rollback()
                    current_table = None
                    data_batch = []
                    continue
                
                if current_table and clean_line and not clean_line.startswith("--"):
                    # Parse row
                    row_data = line.rstrip('\n').split('\t')
                    
                    # Need column list to verify length and map types
                    if len(row_data) != len(columns):
                         print(f"Error: Column count mismatch in {current_table}. Expected {len(columns)}, got {len(row_data)}")
                         continue

                    row_dict = {}
                    for i, col_name in enumerate(columns):
                        val = row_data[i]
                        # Get type
                        ctype = col_types.get(col_name)
                        parsed_val = parse_value(val, ctype)
                        row_dict[col_name] = parsed_val
                    
                    data_batch.append(row_dict)
        
        db.session.execute(text("PRAGMA foreign_keys=ON;"))
        print("\nDone!")

if __name__ == "__main__":
    run_import()
