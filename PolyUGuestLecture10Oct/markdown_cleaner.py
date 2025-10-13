import re
import os

def clean_markdown_file(input_path, output_path):
    """Clean up the messy markdown file"""
    
    with open(input_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Split into lines for processing
    lines = content.split('\n')
    cleaned_lines = []
    outline = []
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Skip empty lines for now (we'll add them back strategically)
        if not line:
            i += 1
            continue
            
        # Handle title (first few lines)
        if i < 10 and ('Natural language processing' in line or 'current trends' in line):
            if 'Natural language processing' in line:
                cleaned_lines.append('# Natural Language Processing: State of the Art, Current Trends and Challenges')
                outline.append('# Natural Language Processing: State of the Art, Current Trends and Challenges')
            # Skip the continuation lines of title
            i += 1
            continue
            
        # Handle author information
        if any(name in line for name in ['Diksha Khurana', 'Aditya Koli', 'Kiran Khatter', 'Sukhdev Singh']):
            if 'Diksha Khurana' in line:
                cleaned_lines.append('\n**Authors:** Diksha Khurana, Aditya Koli, Kiran Khatter, Sukhdev Singh\n')
            i += 1
            continue
            
        # Handle section headings - look for numbered sections
        if re.match(r'^\d+\s+[A-Z]', line):  # Like "1 Introduction"
            section_title = line
            cleaned_lines.append(f'\n## {section_title}\n')
            outline.append(f'## {section_title}')
            i += 1
            continue
            
        # Handle subsection headings 
        if re.match(r'^\d+\.\d+', line):  # Like "2.1 Something"
            subsection_title = line
            cleaned_lines.append(f'\n### {subsection_title}\n')
            outline.append(f'### {subsection_title}')
            i += 1
            continue
            
        # Handle special sections
        if line.lower() in ['abstract', 'introduction', 'conclusion', 'references']:
            cleaned_lines.append(f'\n## {line.title()}\n')
            outline.append(f'## {line.title()}')
            i += 1
            continue
            
        # Remove ### markers that were incorrectly added
        if line.startswith('###'):
            line = line.replace('###', '').strip()
            
        # Handle paragraph text - join broken lines
        if line and not line.startswith('#'):
            paragraph = line
            
            # Look ahead to join broken sentences
            j = i + 1
            while j < len(lines):
                next_line = lines[j].strip()
                if not next_line:
                    break
                if next_line.startswith('#') or re.match(r'^\d+\s+[A-Z]', next_line):
                    break
                if next_line.startswith('###'):
                    next_line = next_line.replace('###', '').strip()
                if next_line and not next_line[0].isupper() or len(paragraph.split()[-1]) < 3:
                    paragraph += ' ' + next_line
                    j += 1
                else:
                    break
            
            cleaned_lines.append(paragraph)
            i = j
            continue
            
        i += 1
    
    # Join the cleaned content
    cleaned_content = '\n'.join(cleaned_lines)
    
    # Save cleaned file
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(cleaned_content)
    
    return outline

def generate_outline(outline_items, output_path):
    """Generate a separate outline file"""
    outline_content = "# Paper Outline\n\n"
    outline_content += '\n'.join(outline_items)
    
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(outline_content)

if __name__ == "__main__":
    input_file = "/workspaces/vibeCoding101/PolyUGuestLecture10Oct/output/mdPaper.md"
    cleaned_file = "/workspaces/vibeCoding101/PolyUGuestLecture10Oct/output/mdPaper_cleaned.md"
    outline_file = "/workspaces/vibeCoding101/PolyUGuestLecture10Oct/output/paper_outline.md"
    
    print("Cleaning markdown file...")
    outline = clean_markdown_file(input_file, cleaned_file)
    
    print("Generating outline...")
    generate_outline(outline, outline_file)
    
    print(f"✅ Cleaned file saved to: {cleaned_file}")
    print(f"✅ Outline saved to: {outline_file}")