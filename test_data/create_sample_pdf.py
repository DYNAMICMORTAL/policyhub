from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import os

def create_sample_policy_pdf():
    """Create a sample insurance policy PDF for testing"""
    
    # Ensure test_data directory exists
    os.makedirs('test_data', exist_ok=True)
    
    # Create PDF
    pdf_path = 'test_data/sample_insurance_policy.pdf'
    doc = SimpleDocTemplate(pdf_path, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []
    
    # Title
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=30,
        alignment=1  # Center alignment
    )
    
    story.append(Paragraph("SAMPLE INSURANCE POLICY", title_style))
    story.append(Spacer(1, 20))
    
    # Policy clauses
    clauses = [
        {
            'title': '1. COVERAGE EXCLUSIONS',
            'text': 'The insurer shall not be liable for any loss or damage caused by war, invasion, act of foreign enemy, hostilities or warlike operations, whether war be declared or not, or caused directly or indirectly by nuclear reaction, nuclear radiation, or radioactive contamination, whether controlled or uncontrolled, or any other perils specifically excluded in the policy schedule attached hereto and forming part of this contract.'
        },
        {
            'title': '2. CLAIMS NOTIFICATION REQUIREMENTS',
            'text': 'Claims must be reported to the company within thirty (30) days of the occurrence of the loss, except where such notification is not reasonably possible due to circumstances beyond the control of the insured, notwithstanding any other provisions herein contained. The insured shall provide all necessary documentation as may be required by the company from time to time.'
        },
        {
            'title': '3. INSURED\'S DUTIES AFTER LOSS',
            'text': 'The insured shall take all reasonable steps to minimize the loss and preserve the property for inspection by the company\'s representatives. The insured shall not, without the written consent of the company, make any admission, offer, promise, or payment in respect of any claim. Failure to comply with this condition may result in denial of the claim, subject to the discretion of the company.'
        },
        {
            'title': '4. AUTOMATIC TERMINATION CONDITIONS',
            'text': 'This policy shall automatically terminate upon the sale, transfer, or disposal of the insured property unless prior written consent is obtained from the insurer. The premium shall be adjusted on a pro-rata basis upon such termination, provided that no claim has been made during the period of coverage.'
        },
        {
            'title': '5. MAXIMUM LIABILITY AND COVERAGE LIMITS',
            'text': 'The maximum liability of the company under this policy shall not exceed the sum insured as stated in the schedule, regardless of the actual value of the property at the time of loss, and subject to all terms, conditions, and exclusions contained herein. Any increase in the value of the property shall not automatically increase the coverage unless specifically endorsed.'
        },
        {
            'title': '6. DEDUCTIBLE PROVISIONS',
            'text': 'The insured shall bear the first amount of each and every loss as specified in the policy schedule as deductible. The company\'s liability shall commence only after the deductible amount has been satisfied by the insured. Multiple losses arising from the same cause shall be treated as one loss for deductible purposes.'
        },
        {
            'title': '7. SUBROGATION AND RECOVERY RIGHTS',
            'text': 'Upon payment of any claim hereunder, the company shall be subrogated to all rights of recovery which the insured may have against any party, and the insured shall execute all papers required and do everything necessary to secure such rights. The insured shall not prejudice such rights of the company.'
        },
        {
            'title': '8. PREMIUM PAYMENT OBLIGATIONS',
            'text': 'The premium is due and payable at the commencement of the policy period. Non-payment of premium within the grace period of thirty (30) days shall render this policy null and void ab initio. Any partial payment shall not constitute acceptance of the premium unless specifically acknowledged by the company in writing.'
        },
        {
            'title': '9. DISPUTE RESOLUTION MECHANISM',
            'text': 'All disputes arising out of this policy shall be settled through arbitration in accordance with the provisions of the Arbitration and Conciliation Act, 1996, as amended from time to time. The seat of arbitration shall be Mumbai, and the proceedings shall be conducted in English.'
        },
        {
            'title': '10. MATERIAL MISREPRESENTATION CONSEQUENCES',
            'text': 'Any material misrepresentation, concealment, or fraud in relation to this insurance shall render the policy void ab initio, and the company shall not be liable for any claims whatsoever, without prejudice to any other rights or remedies available to the company under law or equity.'
        }
    ]
    
    # Add each clause
    for clause in clauses:
        # Add clause title
        story.append(Paragraph(clause['title'], styles['Heading2']))
        story.append(Spacer(1, 10))
        
        # Add clause text
        story.append(Paragraph(clause['text'], styles['Normal']))
        story.append(Spacer(1, 20))
    
    # Add footer
    story.append(Spacer(1, 30))
    story.append(Paragraph("This is a sample policy document created for testing the PolicyIntelliHub AI system.", styles['Italic']))
    
    # Build PDF
    doc.build(story)
    print(f"Sample PDF created: {pdf_path}")
    return pdf_path

if __name__ == '__main__':
    create_sample_policy_pdf()
