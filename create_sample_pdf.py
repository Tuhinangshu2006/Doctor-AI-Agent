from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def create_pdf(filename):
    c = canvas.Canvas(filename, pagesize=letter)
    width, height = letter

    # Title
    c.setFont("Helvetica-Bold", 20)
    c.drawString(50, height - 50, "CITY HOSPITAL - MEDICAL REPORT")
    
    # Patient Info
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 100, "Patient Name: John Doe")
    c.drawString(50, height - 120, "Age: 45")
    c.drawString(50, height - 140, "Date: Nov 28, 2025")
    c.drawString(50, height - 160, "Patient ID: 12345")

    # Divider
    c.line(50, height - 170, 550, height - 170)

    # Symptoms
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, height - 200, "1. Presenting Symptoms")
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 220, "- Severe persistent cough for 2 weeks.")
    c.drawString(50, height - 235, "- High fever (102°F) at night.")
    c.drawString(50, height - 250, "- Shortness of breath during physical activity.")
    c.drawString(50, height - 265, "- General fatigue and body aches.")

    # Lab Results
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, height - 300, "2. Laboratory Results")
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 320, "- Hemoglobin: 13.5 g/dL (Normal)")
    c.drawString(50, height - 335, "- White Blood Cells (WBC): 14,000 /mcL (High - Indicates Infection)")
    c.drawString(50, height - 350, "- Platelets: 250,000 /mcL (Normal)")
    c.drawString(50, height - 365, "- C-Reactive Protein (CRP): 25 mg/L (High - Indicates Inflammation)")

    # Diagnosis
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, height - 400, "3. Diagnosis")
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 420, "Based on clinical examination and lab results, the patient is diagnosed with")
    c.drawString(50, height - 435, "Acute Bronchitis with possible secondary bacterial infection.")

    # Treatment
    c.setFont("Helvetica-Bold", 14)
    c.drawString(50, height - 470, "4. Prescribed Treatment")
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 490, "- Amoxicillin 500mg (Antibiotic) - 3 times daily for 7 days.")
    c.drawString(50, height - 505, "- Paracetamol 500mg (For fever) - As needed.")
    c.drawString(50, height - 520, "- Plenty of fluids and rest.")

    # Footer
    c.setFont("Helvetica-Oblique", 10)
    c.drawString(50, 50, "Dr. Alice Baker, M.D. - Senior Pulmonologist")

    c.save()
    print(f"✅ Generated: {filename}")

if __name__ == "__main__":
    create_pdf("sample_report.pdf")
    