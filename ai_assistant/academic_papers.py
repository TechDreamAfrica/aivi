"""
Academic Paper Support for Visually Impaired Students
PDF-to-audio, citation management, research paper analysis
"""

import os
import re
from typing import List, Dict, Optional, Tuple
from datetime import datetime
import ai_assistant.tts as tts

class AcademicPaperManager:
    """Manages academic papers and research materials"""
    
    def __init__(self):
        self.papers_dir = "academic_papers"
        self.citations_file = "citations.txt"
        self.notes_dir = "research_notes"
        os.makedirs(self.papers_dir, exist_ok=True)
        os.makedirs(self.notes_dir, exist_ok=True)
    
    def pdf_to_audio_description(self, pdf_path: str) -> Dict:
        """Convert PDF to structured audio description"""
        # This would use PDF libraries like PyPDF2 or pdfplumber
        # For now, provide framework
        
        try:
            # Simulated PDF extraction
            content = {
                'title': "Research Paper Title",
                'authors': ["Author 1", "Author 2"],
                'abstract': "This is the abstract of the paper...",
                'sections': [
                    {'heading': 'Introduction', 'content': '...'},
                    {'heading': 'Methods', 'content': '...'},
                    {'heading': 'Results', 'content': '...'},
                    {'heading': 'Discussion', 'content': '...'},
                    {'heading': 'Conclusion', 'content': '...'},
                ],
                'references': [],
                'figures': [],
                'tables': [],
            }
            
            return content
        
        except Exception as e:
            return {'error': str(e)}
    
    def read_paper_aloud(self, pdf_path: str, section: Optional[str] = None):
        """Read academic paper aloud with proper structure"""
        content = self.pdf_to_audio_description(pdf_path)
        
        if 'error' in content:
            tts.speak_text(f"Error reading paper: {content['error']}")
            return
        
        # Read title and authors
        tts.speak_text(f"Paper title: {content['title']}")
        tts.speak_text(f"Authors: {', '.join(content['authors'])}")
        
        # Read abstract
        if not section or section.lower() == 'abstract':
            tts.speak_text("Abstract:")
            tts.speak_text(content['abstract'])
        
        # Read specific section or all
        if section:
            for sec in content['sections']:
                if sec['heading'].lower() == section.lower():
                    tts.speak_text(f"Section: {sec['heading']}")
                    tts.speak_text(sec['content'])
                    break
        else:
            for sec in content['sections']:
                tts.speak_text(f"Section: {sec['heading']}")
                tts.speak_text(sec['content'])
    
    def summarize_paper(self, pdf_path: str) -> str:
        """Generate accessible summary of research paper"""
        content = self.pdf_to_audio_description(pdf_path)
        
        if 'error' in content:
            return f"Error: {content['error']}"
        
        summary = f"Title: {content['title']}\n\n"
        summary += f"Authors: {', '.join(content['authors'])}\n\n"
        summary += f"Abstract Summary:\n{content['abstract'][:300]}...\n\n"
        summary += f"Number of sections: {len(content['sections'])}\n"
        summary += f"Number of references: {len(content['references'])}\n"
        
        return summary
    
    def extract_citations(self, pdf_path: str, style: str = 'APA') -> List[str]:
        """Extract and format citations from paper"""
        content = self.pdf_to_audio_description(pdf_path)
        citations = []
        
        for ref in content.get('references', []):
            if style == 'APA':
                citation = self._format_apa(ref)
            elif style == 'MLA':
                citation = self._format_mla(ref)
            elif style == 'Chicago':
                citation = self._format_chicago(ref)
            else:
                citation = str(ref)
            
            citations.append(citation)
        
        return citations
    
    def _format_apa(self, reference: Dict) -> str:
        """Format reference in APA style"""
        # APA: Author, A. A. (Year). Title of work. Publisher.
        authors = reference.get('authors', ['Unknown'])
        year = reference.get('year', 'n.d.')
        title = reference.get('title', 'Untitled')
        publisher = reference.get('publisher', '')
        
        author_str = ', '.join(authors)
        citation = f"{author_str} ({year}). {title}."
        if publisher:
            citation += f" {publisher}."
        
        return citation
    
    def _format_mla(self, reference: Dict) -> str:
        """Format reference in MLA style"""
        # MLA: Author Last, First. "Title." Publisher, Year.
        authors = reference.get('authors', ['Unknown'])
        year = reference.get('year', 'n.d.')
        title = reference.get('title', 'Untitled')
        publisher = reference.get('publisher', '')
        
        citation = f"{authors[0]}. \"{title}.\" "
        if publisher:
            citation += f"{publisher}, "
        citation += f"{year}."
        
        return citation
    
    def _format_chicago(self, reference: Dict) -> str:
        """Format reference in Chicago style"""
        # Chicago: Author Last, First. Title. Publisher, Year.
        authors = reference.get('authors', ['Unknown'])
        year = reference.get('year', 'n.d.')
        title = reference.get('title', 'Untitled')
        publisher = reference.get('publisher', '')
        
        citation = f"{authors[0]}. {title}. "
        if publisher:
            citation += f"{publisher}, "
        citation += f"{year}."
        
        return citation
    
    def create_bibliography(self, citations: List[Dict], style: str = 'APA') -> str:
        """Generate formatted bibliography"""
        bibliography = f"Bibliography ({style} Style)\n"
        bibliography += "=" * 50 + "\n\n"
        
        for i, cite in enumerate(citations, 1):
            if style == 'APA':
                formatted = self._format_apa(cite)
            elif style == 'MLA':
                formatted = self._format_mla(cite)
            elif style == 'Chicago':
                formatted = self._format_chicago(cite)
            else:
                formatted = str(cite)
            
            bibliography += f"{i}. {formatted}\n\n"
        
        return bibliography
    
    def annotate_paper(self, pdf_path: str, page: int, annotation: str):
        """Add audio annotation to specific page"""
        timestamp = datetime.now().isoformat()
        annotation_entry = {
            'pdf': pdf_path,
            'page': page,
            'annotation': annotation,
            'timestamp': timestamp
        }
        
        # Save annotation
        annotation_file = os.path.join(
            self.notes_dir,
            f"{os.path.basename(pdf_path)}_annotations.txt"
        )
        
        with open(annotation_file, 'a', encoding='utf-8') as f:
            f.write(f"\n[Page {page}] {timestamp}\n")
            f.write(f"{annotation}\n")
            f.write("-" * 50 + "\n")
        
        return f"Annotation added to page {page}"
    
    def search_papers(self, query: str, database: str = 'general') -> List[Dict]:
        """Search academic databases (simulated)"""
        # This would integrate with actual APIs: PubMed, IEEE, ACM, Google Scholar
        
        results = [
            {
                'title': f"Sample paper about {query}",
                'authors': ['Researcher, A.', 'Scholar, B.'],
                'year': 2023,
                'journal': 'Journal of Science',
                'abstract': f"This paper discusses {query} in detail...",
                'doi': '10.1234/example.2023',
                'citations': 42,
            }
        ]
        
        return results
    
    def speak_search_results(self, results: List[Dict]):
        """Read search results aloud"""
        tts.speak_text(f"Found {len(results)} papers. Reading results:")
        
        for i, paper in enumerate(results, 1):
            tts.speak_text(f"Result {i}")
            tts.speak_text(f"Title: {paper['title']}")
            tts.speak_text(f"Authors: {', '.join(paper['authors'])}")
            tts.speak_text(f"Year: {paper['year']}")
            tts.speak_text(f"Journal: {paper['journal']}")
            tts.speak_text(f"Cited {paper['citations']} times")
            tts.speak_text("Abstract:")
            tts.speak_text(paper['abstract'][:200] + "...")
            tts.speak_text("---")
    
    def describe_figure(self, figure_data: Dict) -> str:
        """Generate accessible description of figure"""
        description = f"Figure {figure_data.get('number', 'unknown')}: "
        description += figure_data.get('caption', 'No caption available')
        description += "\n\n"
        
        fig_type = figure_data.get('type', 'unknown')
        
        if fig_type == 'graph':
            description += "This is a graph. "
            description += f"X-axis: {figure_data.get('x_label', 'unlabeled')}. "
            description += f"Y-axis: {figure_data.get('y_label', 'unlabeled')}. "
            description += f"The graph shows {figure_data.get('trend', 'data points')}."
        
        elif fig_type == 'diagram':
            description += "This is a diagram showing "
            description += figure_data.get('description', 'a schematic representation')
        
        elif fig_type == 'photo':
            description += "This is a photograph depicting "
            description += figure_data.get('description', 'a visual scene')
        
        return description
    
    def describe_table(self, table_data: Dict) -> str:
        """Generate accessible description of data table"""
        description = f"Table {table_data.get('number', 'unknown')}: "
        description += table_data.get('caption', 'No caption')
        description += "\n\n"
        
        rows = table_data.get('rows', 0)
        cols = table_data.get('cols', 0)
        description += f"This table has {rows} rows and {cols} columns. "
        
        headers = table_data.get('headers', [])
        if headers:
            description += f"Column headers are: {', '.join(headers)}. "
        
        # Describe key findings
        if 'summary' in table_data:
            description += f"\nKey findings: {table_data['summary']}"
        
        return description
    
    def export_notes(self, export_format: str = 'txt') -> str:
        """Export research notes in accessible format"""
        notes_file = os.path.join(self.notes_dir, f"research_notes.{export_format}")
        
        # Collect all notes
        all_notes = []
        for filename in os.listdir(self.notes_dir):
            if filename.endswith('_annotations.txt'):
                with open(os.path.join(self.notes_dir, filename), 'r', encoding='utf-8') as f:
                    all_notes.append(f.read())
        
        # Write combined notes
        with open(notes_file, 'w', encoding='utf-8') as f:
            f.write("Research Notes Export\n")
            f.write("=" * 50 + "\n\n")
            f.write('\n\n'.join(all_notes))
        
        return f"Notes exported to {notes_file}"

# Global instance
_paper_manager = None

def get_paper_manager():
    """Get or create academic paper manager"""
    global _paper_manager
    if _paper_manager is None:
        _paper_manager = AcademicPaperManager()
    return _paper_manager

def read_paper_aloud(pdf_path: str, section: Optional[str] = None):
    """Read academic paper aloud"""
    get_paper_manager().read_paper_aloud(pdf_path, section)

def summarize_paper(pdf_path: str) -> str:
    """Summarize research paper"""
    return get_paper_manager().summarize_paper(pdf_path)

def create_bibliography(citations: List[Dict], style: str = 'APA') -> str:
    """Create formatted bibliography"""
    return get_paper_manager().create_bibliography(citations, style)

def search_papers(query: str, database: str = 'general') -> List[Dict]:
    """Search academic databases"""
    return get_paper_manager().search_papers(query, database)
