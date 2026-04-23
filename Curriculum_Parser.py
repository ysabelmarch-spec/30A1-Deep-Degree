import fitz  # PyMuPDF
re import

def parse_rpi_curriculum(pdf_path):
    doc = fitz.open(pdf_path)
    full_text = ""
    for page in doc:
        full_text += page.get_text()

    # Regex to capture course code, name, and credits
    # Example match: CSCI 1100 - Computer Science I Credit Hours: 4
    course_pattern = r"([A-Z]{4}\s\d{4})\s?-\s?(.*?)\sCredit Hours:\s?(\d+)"
    
    # Trackers
    curriculum = {}
    current_term = "General Requirements"
    
    lines = full_text.split('\n')
    for line in lines:
        line = line.strip()
        
        # Update current term context
        if line in ["Fall", "Spring", "The Arch Summer Semester", "Summer"]:
            current_term = line
            if current_term not in curriculum:
                curriculum[current_term] = []
            continue

        # Match course data
        match = re.search(course_pattern, line)
        if match:
            course_data = {
                "code": match.group(1),
                "title": match.group(2),
                "credits": int(match.group(3))
            }
            curriculum.setdefault(current_term, []).append(course_data)

    return curriculum

# Example usage with your Cognitive Science B.S. file
# data = parse_rpi_curriculum("Cognitive_Science_BS.pdf")
