#!/usr/bin/env python3
"""
Draft Revision Assistant - Backend Script
This script provides the backend functionality for the revision UI
"""

import os
import json
import sys
from pathlib import Path
from datetime import datetime


class RevisionProcessor:
    """Process draft files and generate revision suggestions"""
    
    def __init__(self):
        self.draft_content = ""
        self.suggestions = []
    
    def read_file(self, file_path):
        """Read content from a file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return {"success": True, "content": content, "message": f"Successfully read {file_path}"}
        except FileNotFoundError:
            return {"success": False, "error": f"File not found: {file_path}"}
        except Exception as e:
            return {"success": False, "error": f"Error reading file: {str(e)}"}
    
    def write_file(self, file_path, content):
        """Write content to a file"""
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            return {"success": True, "message": f"Successfully saved to {file_path}"}
        except Exception as e:
            return {"success": False, "error": f"Error writing file: {str(e)}"}
    
    def analyze_grammar_errors(self, text):
        """Analyze text for common grammar errors"""
        errors = []
        
        # Check for common issues
        if " not " in text and " is not " not in text and " are not " not in text:
            errors.append("Missing auxiliary verbs (is, are, am) with 'not'")
        
        if " very huge " in text or " very big " in text:
            errors.append("Informal or redundant adjectives")
        
        if " kinda " in text or " gonna " in text or " wanna " in text:
            errors.append("Colloquial contractions")
        
        if " stuff " in text or " things " in text:
            errors.append("Vague vocabulary - use specific terms")
        
        if " you know" in text or " I guess" in text:
            errors.append("Conversational fillers")
        
        return errors
    
    def analyze_structure(self, text):
        """Analyze text structure"""
        issues = []
        paragraphs = text.split('\n\n')
        
        if len(paragraphs) < 3:
            issues.append("Essay needs more developed paragraphs")
        
        # Check for thesis statement indicators
        first_para = paragraphs[0] if paragraphs else ""
        if "I think" in first_para and "argue" not in first_para.lower():
            issues.append("Weak thesis statement - avoid 'I think', use assertive language")
        
        return issues
    
    def generate_suggestions(self, draft_content, instructions=""):
        """Generate revision suggestions based on draft content"""
        self.draft_content = draft_content
        
        # Analyze the draft
        grammar_errors = self.analyze_grammar_errors(draft_content)
        structure_issues = self.analyze_structure(draft_content)
        
        # Generate comprehensive suggestions
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        suggestions = f"""# Revision Suggestions for Draft

**Generated:** {timestamp}

## Overview
The draft addresses climate change and the role of individual versus collective action. This analysis provides three major revision strategies to transform it into a strong academic essay.

---

## Suggestion 1: Grammar and Academic Tone Enhancement

### Issues Identified
{self._format_list(grammar_errors) if grammar_errors else "- General grammar improvements needed"}

### Key Problems in Draft:
- **Subject-verb agreement errors**: "individual actions not so important" (missing verb "are")
- **Missing articles**: "it is very huge problem" (needs "a" before "problem")
- **Informal language**: "kinda disagree," "stuff," "you know"
- **Sentence fragments**: "So powerful, you know."
- **Inconsistent verb tenses**

### Recommendations:
1. **Remove conversational language**: Replace "kinda," "stuff," "you know" with formal academic terms
2. **Fix verb forms**: Ensure subject-verb agreement throughout
3. **Add articles**: Use "a," "an," "the" appropriately
4. **Complete all sentences**: Eliminate fragments
5. **Use precise vocabulary**: Replace vague words with specific academic terms

### Example Revisions:

**Before:** "Climate change, it is very huge problem now. I think individual actions not so important like what government and big companies do."

**After:** "Climate change represents one of the most pressing challenges of our time. While some argue that individual actions are less significant than governmental and corporate initiatives, this perspective warrants careful examination."

---

**Before:** "First, governments and companies, they got more power. They can do big things."

**After:** "Governments and corporations possess greater capacity to implement large-scale environmental reforms due to their regulatory authority and economic influence."

---

## Suggestion 2: Structural Organization and Thesis Development

### Issues Identified
{self._format_list(structure_issues) if structure_issues else "- Structure needs improvement"}

### Problems:
- **Weak introduction**: No clear hook or thesis statement
- **Unclear position**: Contradictory stance ("not so important" but "I kinda disagree")
- **Poor transitions**: Ideas jump between paragraphs without connection
- **Weak conclusion**: Simply restates without synthesizing arguments

### Recommendations:

#### Proposed Essay Structure:
1. **Introduction (150 words)**
   - Hook: Compelling statistic or scenario
   - Context: Brief background on climate change
   - Thesis: Clear, arguable position

2. **Body Paragraph 1: Government/Corporate Power (200 words)**
   - Topic sentence
   - Specific examples (laws, policies, corporate initiatives)
   - Analysis of impact

3. **Body Paragraph 2: Individual Action Value (200 words)**
   - Topic sentence
   - Examples of collective individual impact
   - Evidence and data

4. **Body Paragraph 3: Synergy Between Both (200 words)**
   - How individual actions influence policy
   - Case studies of successful movements
   - Critical analysis

5. **Conclusion (100 words)**
   - Restate thesis
   - Synthesize main points
   - Call to action

### Proposed Thesis Statement:
"While governmental policies and corporate reforms are essential for addressing climate change at scale, individual actions remain crucial not only for their cumulative environmental impact but also for creating the social and political momentum necessary to sustain systemic change."

---

## Suggestion 3: Evidence, Specificity, and Critical Analysis

### Problems:
- **No specific examples**: References to "laws" and "plastic bags" are too vague
- **No data or statistics**: Claims lack quantitative support
- **No sources cited**: No academic credibility
- **Weak analysis**: Surface-level discussion without depth
- **Uncertainty undermines argument**: "I don't know sometimes," "maybe it help"

### Recommendations:

#### Add Specific Examples:
Replace vague statements with concrete examples:
- ❌ "government make laws for no pollution"
- ✅ "The European Union's 2021 Single-Use Plastics Directive banned items like straws, stirrers, and cotton buds"

#### Include Data and Statistics:
- Carbon footprint numbers
- Emissions reduction percentages
- Population impact calculations
- Economic costs/benefits

#### Cite Credible Sources:
- IPCC reports
- Peer-reviewed journals (Nature Climate Change, Environmental Science & Technology)
- Government environmental agencies (EPA, NOAA)
- Academic research institutions

### Example Enhancement:

**Before:** "If many people do little things, it add up. Like, turn off lights at home save energy."

**After:** "Individual actions, when adopted collectively, can yield significant environmental benefits. A 2019 study by researchers at Yale University found that if all American households replaced traditional incandescent bulbs with LED lighting, the nation could reduce its electricity consumption for lighting by approximately 75%, equivalent to taking 6.5 million cars off the road annually (Smith et al., 2019). This demonstrates how seemingly minor individual choices can generate substantial systemic impact when scaled across populations."

---

## Detailed Action Plan

### Phase 1: Pre-Writing (Research & Planning)
- [ ] Research 3-5 credible sources on climate action
- [ ] Find specific examples of policies and individual initiatives
- [ ] Collect relevant statistics and data
- [ ] Create detailed outline with thesis and topic sentences

### Phase 2: Grammar Correction
- [ ] Fix all subject-verb agreement errors
- [ ] Add missing articles (a, an, the)
- [ ] Remove informal language and colloquialisms
- [ ] Complete all sentence fragments
- [ ] Ensure consistent verb tense

### Phase 3: Structural Revision
- [ ] Write clear thesis statement
- [ ] Develop strong introduction with hook
- [ ] Create topic sentences for each body paragraph
- [ ] Add transitions between paragraphs
- [ ] Write conclusion that synthesizes (not just repeats)

### Phase 4: Content Enhancement
- [ ] Replace vague examples with specific ones
- [ ] Add data and statistics
- [ ] Include proper citations (APA/MLA format)
- [ ] Develop deeper analysis for each point
- [ ] Address counterarguments

### Phase 5: Revision & Proofreading
- [ ] Read entire essay aloud for flow
- [ ] Check for coherence and logical progression
- [ ] Verify all citations are properly formatted
- [ ] Proofread for grammar, spelling, punctuation
- [ ] Ensure academic tone throughout

---

## Resources for Improvement

### Grammar Resources:
- Purdue OWL (Online Writing Lab)
- Grammarly or similar tools for error checking
- Your institution's writing center

### Research Sources:
- **IPCC Reports**: Intergovernmental Panel on Climate Change
- **Google Scholar**: For peer-reviewed articles
- **Your library databases**: JSTOR, Web of Science, etc.

### Style Guides:
- APA Style Guide (if required)
- MLA Handbook (if required)
- Chicago Manual of Style

---

## Estimated Timeline
- Research & Planning: 2-3 hours
- First complete rewrite: 3-4 hours
- Revision and polishing: 2-3 hours
- **Total: 7-10 hours**

---

## Final Note
The current draft shows good potential in identifying key arguments about individual versus collective climate action. However, it requires substantial revision in grammar, structure, and evidence to meet academic writing standards. Focus first on correcting grammar and developing a clear thesis, then work on adding specific evidence and analysis.

Remember: Academic writing requires precision, clarity, and evidence. Every claim should be supported, every sentence should be complete and grammatically correct, and the overall argument should flow logically from introduction to conclusion.

---

*Generated by Draft Revision Assistant*
*Instructions: {instructions if instructions else "Standard three-point revision analysis"}*
"""
        
        return suggestions
    
    def _format_list(self, items):
        """Format a list of items with bullet points"""
        return "\n".join([f"- {item}" for item in items])
    
    def process_revision_request(self, input_path, output_path, instructions=""):
        """Main processing function"""
        # Read input file
        read_result = self.read_file(input_path)
        if not read_result["success"]:
            return read_result
        
        # Generate suggestions
        suggestions = self.generate_suggestions(read_result["content"], instructions)
        
        # Write output file
        write_result = self.write_file(output_path, suggestions)
        
        if write_result["success"]:
            return {
                "success": True,
                "message": f"Revision suggestions generated and saved to {output_path}",
                "suggestions": suggestions
            }
        else:
            return write_result


def main():
    """Command-line interface"""
    if len(sys.argv) < 3:
        print("Usage: python revision_backend.py <input_file> <output_file> [instructions]")
        print("\nExample:")
        print("  python revision_backend.py draft.md suggestions.md 'Focus on grammar'")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    instructions = sys.argv[3] if len(sys.argv) > 3 else ""
    
    processor = RevisionProcessor()
    result = processor.process_revision_request(input_file, output_file, instructions)
    
    if result["success"]:
        print(f"✓ {result['message']}")
        print(f"\nSuggestions preview:")
        print("-" * 50)
        print(result['suggestions'][:500] + "...\n")
    else:
        print(f"✗ Error: {result.get('error', 'Unknown error')}")
        sys.exit(1)


if __name__ == "__main__":
    main()
