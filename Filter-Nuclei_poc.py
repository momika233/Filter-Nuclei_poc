#!/usr/bin/env python3
import os
import hashlib
import yaml
import shutil
from pathlib import Path

def extract_content(file_path):
    """Extract content, get the requests or http part"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split content
    parts = content.split('requests:') if 'requests:' in content else content.split('http:')
    if len(parts) > 1:
        content = parts[1]
    else:
        content = parts[0]
    
    # Remove comments
    lines = content.split('\n')
    cleaned_lines = []
    for line in lines:
        if not line.strip().startswith('#'):
            cleaned_lines.append(line)
    
    return ''.join(cleaned_lines)

def calculate_md5(content):
    """Calculate MD5 hash of content"""
    # Remove all whitespace characters
    cleaned_content = ''.join(content.split())
    return hashlib.md5(cleaned_content.encode('utf-8')).hexdigest()

def process_directory(source_dir, target_dir):
    """Process all yaml files in directory"""
    # Ensure target directory exists
    os.makedirs(target_dir, exist_ok=True)
    
    # Store processed hash values
    processed_hashes = set()
    
    # Traverse all yaml files
    for root, _, files in os.walk(source_dir):
        for file in files:
            if file.endswith('.yaml'):
                file_path = os.path.join(root, file)
                try:
                    # Extract content
                    content = extract_content(file_path)
                    # Calculate hash
                    content_hash = calculate_md5(content)
                    
                    # If hash not seen before, copy file
                    if content_hash not in processed_hashes:
                        processed_hashes.add(content_hash)
                        target_file = os.path.join(target_dir, f"{content_hash}.yaml")
                        shutil.copy2(file_path, target_file)
                        print(f"Processing file: {file_path} -> {target_file}")
                except Exception as e:
                    print(f"Error processing file {file_path}: {str(e)}")

def get_severity(file_path):
    """Get POC security severity level"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = yaml.safe_load(f)
            return content.get('info', {}).get('severity', '').lower()
    except Exception as e:
        print(f"Error reading severity from file {file_path}: {str(e)}")
        return None

def process_severity(source_dir, target_dir):
    """Process severity levels, move non-info level POCs to step2 directory"""
    os.makedirs(target_dir, exist_ok=True)
    
    for file in os.listdir(source_dir):
        if file.endswith('.yaml'):
            source_file = os.path.join(source_dir, file)
            severity = get_severity(source_file)
            
            if severity and severity != 'info':
                target_file = os.path.join(target_dir, file)
                shutil.move(source_file, target_file)
                print(f"Moving non-info level file: {source_file} -> {target_file}")

def check_keywords(file_path):
    """Check if file contains specific keywords"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Check for HTTP-related keywords
        http_keywords = ['HTTP', 'GET', 'POST', 'PUT', 'BaseURL']
        has_http = any(keyword in content for keyword in http_keywords)
        
        # Check for keywords to skip
        skip_keywords = ['/readme.txt', '/style.css']
        should_skip = any(keyword in content for keyword in skip_keywords)
        
        return has_http and not should_skip
    except Exception as e:
        print(f"Error checking keywords in file {file_path}: {str(e)}")
        return False

def process_keywords(source_dir, target_dir):
    """Process keywords, move matching POCs to step3 directory"""
    os.makedirs(target_dir, exist_ok=True)
    
    for file in os.listdir(source_dir):
        if file.endswith('.yaml'):
            source_file = os.path.join(source_dir, file)
            if check_keywords(source_file):
                target_file = os.path.join(target_dir, file)
                shutil.move(source_file, target_file)
                print(f"Moving file matching keyword criteria: {source_file} -> {target_file}")

def main():
    os.system("git clone https://github.com/adysec/nuclei_poc && cd nuclei_poc")
    # Set directory paths
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    step1_dir = os.path.join(base_dir, 'step1')
    step2_dir = os.path.join(base_dir, 'step2')
    step3_dir = os.path.join(base_dir, 'step3')
    
    # Step 1: Process original files
    print("\n=== Step 1: Processing Original Files ===")
    process_directory(base_dir, step1_dir)
    
    # Step 2: Process severity levels
    print("\n=== Step 2: Processing Severity Levels ===")
    process_severity(step1_dir, step2_dir)
    
    # Step 3: Process keywords
    print("\n=== Step 3: Processing Keywords ===")
    process_keywords(step2_dir, step3_dir)
    os.system("mv ./step3 /root/nuclei-templates/")
    os.system("rm -rf ./nuclei_poc step1 ./step2")
    
    print("\nProcessing complete!")

if __name__ == "__main__":
    main() 
