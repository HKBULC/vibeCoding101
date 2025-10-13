import PyPDF2
import os

# File paths
input_pdf = "/workspaces/vibeCoding101/PolyUGuestLecture10Oct/data/s11042-022-13428-4.pdf"
output_md = "/workspaces/vibeCoding101/PolyUGuestLecture10Oct/output/mdPaper.md"

def extract_text_from_pdf(pdf_path):
    """Extract text from PDF file"""
    text = ""
    
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        print(f"Number of pages: {len(pdf_reader.pages)}")
        
        for page_num, page in enumerate(pdf_reader.pages):
            print(f"Extracting page {page_num + 1}...")
            text += page.extract_text()
            text += "\n\n"  # Add spacing between pages
    
    return text

def format_as_markdown(text):
    """Format extracted text as markdown"""
    # Clean up the text and add basic markdown formatting
    lines = text.split('\n')
    formatted_lines = []
    
    for line in lines:
        line = line.strip()
        if not line:
            formatted_lines.append('')
            continue
        
        # Try to identify headings (lines that look like titles)
        if len(line) < 100 and line.isupper() and len(line.split()) > 1:
            formatted_lines.append(f"## {line.title()}")
        elif len(line) < 80 and not line.endswith('.') and len(line.split()) < 15:
            formatted_lines.append(f"### {line}")
        else:
            formatted_lines.append(line)
    
    return '\n'.join(formatted_lines)

def save_to_markdown(text, output_path):
    """Save text to markdown file"""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(text)
    
    print(f"Markdown file saved to: {output_path}")

# Main process
if __name__ == "__main__":
    print("Starting PDF to Markdown conversion...")
    
    # Extract text from PDF
    extracted_text = extract_text_from_pdf(input_pdf)
    print(f"Extracted {len(extracted_text)} characters")
    
    # Format as markdown
    markdown_text = format_as_markdown(extracted_text)
    
    # Save to file
    save_to_markdown(markdown_text, output_md)
    
    print("Conversion completed!")