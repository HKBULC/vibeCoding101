# Draft Revision Assistant UI

A comprehensive web-based interface for analyzing academic drafts and generating structured revision suggestions.

## 📋 Features

- **Input/Output Configuration**: Easy file path management
- **Custom Instructions**: Specify what aspects to focus on during revision
- **Draft Preview**: Load and preview draft content before processing
- **Automated Analysis**: Generate comprehensive revision suggestions
- **Three Main Focus Areas**:
  1. Grammar and Academic Tone Enhancement
  2. Structural Organization and Thesis Development
  3. Evidence, Specificity, and Critical Analysis

## 🚀 Quick Start

### Option 1: Using the Web UI

1. **Start the web server:**
   ```bash
   cd /workspaces/vibeCoding101/LANG0036
   python -m http.server 8080
   ```

2. **Open in browser:**
   ```
   http://localhost:8080/revision_ui.html
   ```

3. **Use the interface:**
   - Enter input file path (e.g., `/workspaces/vibeCoding101/LANG0036/draft.md`)
   - Enter output file path (e.g., `/workspaces/vibeCoding101/LANG0036/suggestion.md`)
   - Optionally modify processing instructions
   - Click "Load Draft" to preview
   - Click "Generate Suggestions" to analyze
   - Click "Save Output" to write to file

### Option 2: Using the Command Line

Run the Python backend directly:

```bash
python revision_backend.py <input_file> <output_file> [instructions]
```

**Example:**
```bash
python revision_backend.py draft.md suggestions.md "Focus on grammar and structure"
```

## 📁 Files

### Main Files
- **`revision_ui.html`** - Web-based user interface
- **`revision_backend.py`** - Python backend processor
- **`revise.md`** - Processing instructions template

### Generated Files
- **`suggestion.md`** - Comprehensive revision suggestions
- **`grammaticalErrors/`** - Grammar learning resources
  - `1_subject_verb_agreement.md`
  - `2_article_usage.md`
  - `3_sentence_fragments_and_run_ons.md`

## 🎨 UI Components

### 1. Input Configuration
- Input file path field
- Output file path field
- Example paths for reference

### 2. Processing Instructions
- **Basic Tab**: General revision instructions
- **Advanced Tab**: 
  - Specific focus areas
  - Toggle for including examples
  - Toggle for including checklists

### 3. Action Buttons
- **Load Draft**: Preview input file content
- **Generate Suggestions**: Analyze and create recommendations
- **Save Output**: Write suggestions to output file

### 4. Preview Areas
- **Draft Preview**: Shows loaded draft content
- **Generated Suggestions**: Displays revision recommendations

## 🔍 How It Works

### Analysis Process

1. **Grammar Analysis**
   - Subject-verb agreement errors
   - Article usage (a, an, the)
   - Informal language detection
   - Sentence fragments and run-ons
   - Verb tense consistency

2. **Structure Analysis**
   - Thesis statement clarity
   - Paragraph organization
   - Transitions between ideas
   - Introduction and conclusion effectiveness

3. **Content Analysis**
   - Specificity of examples
   - Use of evidence and data
   - Source citations
   - Depth of critical analysis

### Output Format

The generated suggestions file includes:
- Overview and timestamp
- Three detailed revision suggestions
- Before/after examples
- Actionable recommendations
- Detailed action plan with checkboxes
- Resource recommendations
- Estimated timeline

## 📝 Example Workflow

```bash
# 1. Prepare your draft
echo "Your draft content..." > draft.md

# 2. Process using command line
python revision_backend.py draft.md suggestion.md "Focus on academic tone"

# 3. Review suggestions
cat suggestion.md

# 4. Or use the web UI for interactive experience
python -m http.server 8080
# Then open http://localhost:8080/revision_ui.html
```

## 🎓 Educational Resources

The system includes comprehensive grammar guides:

### Subject-Verb Agreement
- Common errors and corrections
- Rules for singular/plural matching
- Practice examples

### Article Usage
- When to use a/an/the
- When to omit articles
- Common patterns in academic writing

### Sentence Structure
- Avoiding fragments
- Fixing run-on sentences
- Creating varied, correct sentences

## 🛠️ Customization

### Modify Instructions

Edit the default instructions in the UI or provide custom ones:

```javascript
// In revision_ui.html, modify the textarea default value
<textarea id="instructions">
Your custom instructions here...
</textarea>
```

### Extend Backend Analysis

Add custom analysis functions in `revision_backend.py`:

```python
def analyze_custom_aspect(self, text):
    """Your custom analysis"""
    issues = []
    # Add your analysis logic
    return issues
```

## 💡 Tips for Best Results

1. **Be Specific**: Provide detailed instructions about what to focus on
2. **Load Draft First**: Preview helps verify correct file path
3. **Review Carefully**: The suggestions are starting points, not final solutions
4. **Iterate**: Run multiple analyses with different focus areas
5. **Use Grammar Guides**: Reference the included markdown guides for learning

## 🔧 Technical Details

### Requirements
- Python 3.6+
- Modern web browser (Chrome, Firefox, Edge, Safari)
- File system access for reading/writing

### Browser Compatibility
- ✅ Chrome/Edge (Chromium)
- ✅ Firefox
- ✅ Safari
- ✅ Opera

### File Encoding
- UTF-8 encoding for all text files
- Markdown format for output

## 📊 Sample Output Structure

```markdown
# Revision Suggestions for Draft

## Overview
Brief analysis summary

## Suggestion 1: Grammar and Academic Tone Enhancement
- Issues identified
- Recommendations
- Examples

## Suggestion 2: Structural Organization
- Structure problems
- Proposed organization
- Thesis development

## Suggestion 3: Evidence and Analysis
- Content gaps
- Specific improvements needed
- Citation requirements

## Action Plan
Detailed checklist

## Resources
Links and references
```

## 🚦 Status Messages

The UI provides real-time feedback:
- **Success** (Green): Operation completed successfully
- **Error** (Red): Something went wrong
- **Info** (Blue): Process in progress or information

## 🔐 Security Note

This tool is designed for local use. If deploying to a server:
- Add authentication
- Sanitize file paths
- Validate input
- Implement rate limiting
- Use HTTPS

## 📄 License

Part of the vibeCoding101 educational project.

## 🤝 Contributing

Suggestions for improvement are welcome:
1. Add more analysis categories
2. Improve UI design
3. Add more languages support
4. Enhance grammar detection algorithms

## 📮 Support

For issues or questions:
- Check the grammatical error guides
- Review example files in the repository
- Examine the console for error messages

---

**Last Updated**: October 15, 2025
**Version**: 1.0.0
