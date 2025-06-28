from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
import os
from datetime import datetime
import uuid

class ReportGenerator:
    def __init__(self):
        self.reports_dir = 'reports'
        os.makedirs(self.reports_dir, exist_ok=True)
        self.styles = getSampleStyleSheet()
    
    def generate_bulk_report(self, document_results, filename):
        """Generate comprehensive PDF report for bulk analysis"""
        try:
            # Generate unique report ID
            report_id = str(uuid.uuid4())[:8]
            report_filename = f"{report_id}_analysis_report.pdf"
            report_path = os.path.join(self.reports_dir, report_filename)
            
            # Create PDF document
            doc = SimpleDocTemplate(report_path, pagesize=A4)
            story = []
            
            # Title
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=self.styles['Heading1'],
                fontSize=18,
                spaceAfter=30,
                alignment=1  # Center alignment
            )
            
            story.append(Paragraph("PolicyIntelliHub Analysis Report", title_style))
            story.append(Spacer(1, 20))
            
            # Document info
            info_data = [
                ['Document Name:', filename],
                ['Analysis Date:', datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
                ['Total Clauses Analyzed:', str(len(document_results))],
                ['Report ID:', report_id]
            ]
            
            info_table = Table(info_data, colWidths=[2*inch, 3*inch])
            info_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.lightgrey),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(info_table)
            story.append(Spacer(1, 30))
            
            # Summary Statistics
            story.append(Paragraph("Summary Statistics", self.styles['Heading2']))
            story.append(Spacer(1, 10))
            
            # Calculate summary stats
            total_clauses = len(document_results)
            compliant_clauses = sum(1 for r in document_results 
                                  if r.get('compliance_check', {}).get('irdai_compliant', False))
            high_risk_clauses = sum(1 for r in document_results 
                                  if r.get('risk_score', {}).get('risk_level') == 'High')
            
            avg_readability = sum(r.get('plain_english', {}).get('readability_improvement', 0) 
                                for r in document_results) / max(total_clauses, 1)
            
            summary_data = [
                ['Total Clauses', str(total_clauses)],
                ['IRDAI Compliant', f"{compliant_clauses} ({compliant_clauses/total_clauses*100:.1f}%)"],
                ['High Risk Clauses', f"{high_risk_clauses} ({high_risk_clauses/total_clauses*100:.1f}%)"],
                ['Avg. Readability Improvement', f"{avg_readability:.1f} points"]
            ]
            
            summary_table = Table(summary_data, colWidths=[3*inch, 2*inch])
            summary_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.beige),
                ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(summary_table)
            story.append(Spacer(1, 30))
            
            # Detailed Analysis for each clause
            story.append(Paragraph("Detailed Clause Analysis", self.styles['Heading2']))
            story.append(Spacer(1, 15))
            
            for i, result in enumerate(document_results[:10]):  # Limit to first 10 for demo
                clause_title = f"Clause {result.get('clause_number', i+1)}"
                story.append(Paragraph(clause_title, self.styles['Heading3']))
                
                # Original clause (truncated)
                original = result.get('original_clause', '')[:200] + "..." if len(result.get('original_clause', '')) > 200 else result.get('original_clause', '')
                story.append(Paragraph(f"<b>Original:</b> {original}", self.styles['Normal']))
                story.append(Spacer(1, 10))
                
                # Plain English version
                plain_english = result.get('plain_english', {}).get('plain_english_text', 'Not available')[:200]
                if len(plain_english) > 200:
                    plain_english += "..."
                story.append(Paragraph(f"<b>Plain English:</b> {plain_english}", self.styles['Normal']))
                story.append(Spacer(1, 10))
                
                # Compliance and Risk info
                compliance_score = result.get('compliance_check', {}).get('compliance_score', 'N/A')
                risk_level = result.get('risk_score', {}).get('risk_level', 'N/A')
                
                metrics_data = [
                    ['Compliance Score', str(compliance_score)],
                    ['Risk Level', str(risk_level)],
                    ['IRDAI Compliant', 'Yes' if result.get('compliance_check', {}).get('irdai_compliant') else 'No']
                ]
                
                metrics_table = Table(metrics_data, colWidths=[2*inch, 1.5*inch])
                metrics_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, -1), colors.lightblue),
                    ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 0), (-1, -1), 9),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))
                
                story.append(metrics_table)
                story.append(Spacer(1, 20))
            
            # Build PDF
            doc.build(story)
            
            return report_id
            
        except Exception as e:
            print(f"Report generation error: {e}")
            return None
