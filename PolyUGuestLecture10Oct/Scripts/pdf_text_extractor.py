#!/usr/bin/env python3
"""
PDF Text Extraction and Citation Analysis Script
This script processes split PDF pages to extract text, find citations, and create citation mappings.
"""

import os
import re
import csv
import subprocess
from pathlib import Path

def extract_text_from_pdf(pdf_path, output_path):
    """Extract text from a single PDF file using pdftotext"""
    try:
        # Use pdftotext to extract text
        result = subprocess.run(['pdftotext', '-layout', pdf_path, '-'], 
                               capture_output=True, text=True, encoding='utf-8')
        if result.returncode == 0:
            text = result.stdout
            
            # Save as markdown file
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(f"# Page {os.path.basename(pdf_path).replace('.pdf', '').replace('page_', '')}\n\n")
                f.write(text)
            
            return text
        else:
            print(f"Error extracting text from {pdf_path}: {result.stderr}")
            return None
    except Exception as e:
        print(f"Error processing {pdf_path}: {e}")
        return None

def find_citations_in_text(text):
    """Find all sentences containing in-text citations"""
    # Common citation patterns:
    # [1], [1,2], [1-3], (Smith, 2020), (Smith et al., 2020), etc.
    citation_patterns = [
        r'\[[0-9]+(?:[-,\s]*[0-9]+)*\]',  # [1], [1,2], [1-3], [1, 2, 3]
        r'\([A-Za-z]+(?:\s+et\s+al\.?)?,?\s+[0-9]{4}[a-z]?(?:;\s*[A-Za-z]+(?:\s+et\s+al\.?)?,?\s+[0-9]{4}[a-z]?)*\)',  # (Smith, 2020), (Smith et al., 2020)
        r'\([A-Za-z]+(?:\s+et\s+al\.?)?\s+[0-9]{4}[a-z]?(?:,\s*[0-9]{4}[a-z]?)*\)',  # (Smith 2020), (Smith et al. 2020)
    ]
    
    sentences_with_citations = []
    
    # Split text into sentences (simple approach)
    sentences = re.split(r'[.!?]+', text)
    
    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue
            
        for pattern in citation_patterns:
            if re.search(pattern, sentence):
                # Extract all citations from this sentence
                citations = []
                for p in citation_patterns:
                    citations.extend(re.findall(p, sentence))
                
                sentences_with_citations.append({
                    'sentence': sentence,
                    'citations': citations
                })
                break  # Don't duplicate the same sentence
    
    return sentences_with_citations

def process_pdf_pages(input_dir, output_dir):
    """Process all PDF pages in the input directory"""
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    
    all_citations = []
    all_text = ""
    
    # Process files in order
    pdf_files = sorted(input_path.glob('page_*.pdf'))
    
    for pdf_file in pdf_files:
        print(f"Processing {pdf_file.name}...")
        
        # Extract text to markdown
        md_file = output_path / f"{pdf_file.stem}.md"
        text = extract_text_from_pdf(str(pdf_file), str(md_file))
        
        if text:
            all_text += f"\n\n--- PAGE {pdf_file.stem.replace('page_', '')} ---\n\n"
            all_text += text
            
            # Find citations in this page
            citations = find_citations_in_text(text)
            for citation_data in citations:
                citation_data['page'] = pdf_file.stem.replace('page_', '')
                all_citations.append(citation_data)
    
    return all_citations, all_text

def extract_references_section(text):
    """Extract the references section from the text"""
    # Look for common reference section headers
    ref_patterns = [
        r'\n\s*References\s*\n',
        r'\n\s*REFERENCES\s*\n',
        r'\n\s*Bibliography\s*\n',
        r'\n\s*BIBLIOGRAPHY\s*\n'
    ]
    
    for pattern in ref_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            # Extract everything after the references header
            ref_section = text[match.end():]
            return ref_section
    
    return None

def map_citations_to_references(citations, references_text):
    """Map in-text citations to reference entries"""
    if not references_text:
        return []
    
    mappings = []
    
    # Split references into individual entries (simple approach)
    # Look for numbered references like [1], [2], etc.
    ref_entries = re.split(r'\n\s*\[[0-9]+\]', references_text)
    
    for i, citation_data in enumerate(citations):
        for citation in citation_data['citations']:
            # Extract number from citation like [1] or [1,2]
            numbers = re.findall(r'[0-9]+', citation)
            
            for num in numbers:
                try:
                    ref_index = int(num)
                    if 1 <= ref_index <= len(ref_entries):
                        ref_text = ref_entries[ref_index-1].strip() if ref_index > 0 else ref_entries[0].strip()
                        
                        mappings.append({
                            'page': citation_data['page'],
                            'sentence': citation_data['sentence'],
                            'citation': citation,
                            'reference_number': num,
                            'reference_text': ref_text[:200] + '...' if len(ref_text) > 200 else ref_text
                        })
                except (ValueError, IndexError):
                    continue
    
    return mappings

def save_citations_csv(citations, output_file):
    """Save citations to CSV file"""
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['page', 'sentence', 'citations']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for citation_data in citations:
            writer.writerow({
                'page': citation_data['page'],
                'sentence': citation_data['sentence'],
                'citations': '; '.join(citation_data['citations'])
            })

def save_citation_mappings_csv(mappings, output_file):
    """Save citation mappings to CSV file"""
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['page', 'sentence', 'citation', 'reference_number', 'reference_text']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for mapping in mappings:
            writer.writerow(mapping)

def main():
    """Main processing function"""
    base_dir = "/workspaces/vibeCoding101/PolyUGuestLecture10Oct/data"
    input_dir = f"{base_dir}/split_pages"
    output_dir = f"{base_dir}/extracted_text"
    
    print("Starting PDF text extraction and citation analysis...")
    
    # Process all PDF pages
    citations, full_text = process_pdf_pages(input_dir, output_dir)
    
    print(f"Found {len(citations)} sentences with citations")
    
    # Save citations to CSV
    citations_csv = f"{base_dir}/citations.csv"
    save_citations_csv(citations, citations_csv)
    print(f"Citations saved to {citations_csv}")
    
    # Extract references section
    references = extract_references_section(full_text)
    
    if references:
        print("References section found")
        # Create citation mappings
        mappings = map_citations_to_references(citations, references)
        
        # Save mappings to CSV
        mappings_csv = f"{base_dir}/citation_mappings.csv"
        save_citation_mappings_csv(mappings, mappings_csv)
        print(f"Citation mappings saved to {mappings_csv}")
        
        # Save references section
        ref_file = f"{output_dir}/references.md"
        with open(ref_file, 'w', encoding='utf-8') as f:
            f.write("# References Section\n\n")
            f.write(references)
        print(f"References section saved to {ref_file}")
    else:
        print("No references section found")
    
    # Save full text
    full_text_file = f"{output_dir}/full_document.md"
    with open(full_text_file, 'w', encoding='utf-8') as f:
        f.write("# Complete Document Text\n\n")
        f.write(full_text)
    print(f"Full document text saved to {full_text_file}")
    
    print("Processing complete!")

if __name__ == "__main__":
    main()