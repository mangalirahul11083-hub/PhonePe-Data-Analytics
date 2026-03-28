import sqlite3
import pandas as pd
import json
import os

# Connect to DB
conn = sqlite3.connect('phonepe_pulse.db')
print("✅ Database connected successfully!\n")

def extract_and_load_top(category, table_name):
    print(f"🔍 Locating and Extracting: {table_name}...")
    target_path = ""
    
    # Auto-detect the path for Top data
    for root, dirs, files in os.walk("data"):
        if f"top/{category}/country/india/state" in root.replace("\\", "/"):
            target_path = root
            break

    if not target_path:
        print(f"❌ Could not find path for {category}.\n")
        return

    data_list = []
    
    for state in os.listdir(target_path):
        state_path = os.path.join(target_path, state)
        if os.path.isdir(state_path):
            for year in os.listdir(state_path):
                year_path = os.path.join(state_path, year)
                if os.path.isdir(year_path):
                    for file in os.listdir(year_path):
                        if file.endswith('.json'):
                            with open(os.path.join(year_path, file), 'r') as f:
                                try:
                                    data = json.load(f)
                                    if not data.get('data'):
                                        continue
                                        
                                    # Extract both districts and pincodes to find top performers
                                    for entity_type in ['districts', 'pincodes']:
                                        if data['data'].get(entity_type):
                                            for i in data['data'][entity_type]:
                                                # Handle varying JSON key names
                                                entity_name = i.get('entityName') or i.get('name')
                                                
                                                if category in ['transaction', 'insurance']:
                                                    count = i['metric']['count']
                                                    amount = i['metric']['amount']
                                                    
                                                    data_list.append({
                                                        'State': state,
                                                        'Year': int(year),
                                                        'Quarter': int(file.replace('.json', '')),
                                                        'Entity_Type': entity_type.capitalize(),
                                                        'Entity_Name': str(entity_name), # Pincodes kept as string
                                                        'Count': count,
                                                        'Amount': amount
                                                    })
                                                    
                                                elif category == 'user':
                                                    reg_users = i['registeredUsers']
                                                    
                                                    data_list.append({
                                                        'State': state,
                                                        'Year': int(year),
                                                        'Quarter': int(file.replace('.json', '')),
                                                        'Entity_Type': entity_type.capitalize(),
                                                        'Entity_Name': str(entity_name),
                                                        'Registered_Users': reg_users
                                                    })
                                except Exception as e:
                                    pass # Skip corrupted files

    # Convert to DataFrame and push to SQL
    df = pd.DataFrame(data_list)
    if not df.empty:
        df['State'] = df['State'].str.replace('-', ' ').str.title()
        # Clean up district names if they appear
        df['Entity_Name'] = df.apply(lambda x: x['Entity_Name'].replace(' district', '').title() if x['Entity_Type'] == 'Districts' else x['Entity_Name'], axis=1)
        
        df.to_sql(table_name, conn, if_exists='replace', index=False)
        print(f"🎉 Success! '{table_name}' created with {df.shape[0]} rows.\n")
    else:
        print(f"⚠️ No data extracted for {table_name}.\n")

# Run the extractions for the entire Top category
extract_and_load_top('transaction', 'Top_transaction')
extract_and_load_top('user', 'Top_user')
extract_and_load_top('insurance', 'Top_insurance')

conn.close()
print("✅ Phase 3: All Top Tables Complete! Database is fully built.")