from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
import whisper
from reportlab.pdfgen import canvas
from docx import Document
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['TRANSCRIPT_FOLDER'] = 'transcripts'
app.config['ALLOWED_EXTENSIONS'] = {'flac', 'm4a', 'mp3', 'mp4', 'mpeg', 'mpga', 'oga', 'ogg', 'wav', 'webm'}

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['TRANSCRIPT_FOLDER'], exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        # If user does not select file, browser also submit an empty part without filename
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = file.filename
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            # Get model size, language, and output format from form
            model_size = request.form.get('model_size', 'tiny')
            language = request.form.get('language', 'en')
            output_format = request.form.get('output_format', 'txt')

            # Transcribe and save transcript
            base_filename = transcribe_and_save(filepath, filename, model_size, language, output_format)
            return redirect(url_for('transcript', filename=base_filename))
    return render_template('index.html')

def transcribe_and_save(filepath, filename, model_size, language, output_format):
    model = whisper.load_model(model_size)
    
    # Handling "auto" option for automatic language detection
    if language == "auto":
        result = model.transcribe(filepath)  # Automatic language detection
    else:
        result = model.transcribe(filepath, language=language)
    
    transcript = result["text"]

    base_filename = os.path.splitext(filename)[0]
    transcript_path = os.path.join(app.config['TRANSCRIPT_FOLDER'], base_filename + f".{output_format}")

    # Always save a .txt version
    txt_path = os.path.join(app.config['TRANSCRIPT_FOLDER'], base_filename + ".txt")
    with open(txt_path, "w", encoding="utf-8") as file:
        file.write(transcript)
        
    # Save in chosen format (if not txt)
    if output_format != 'txt':
        if output_format == 'pdf':
            c = canvas.Canvas(transcript_path, pagesize=letter)
            text_object = c.beginText(72, 10.5 * inch)  # Adjusted for padding at the top
            text_object.setFont("Times-Roman", 12)
            
            # Basic text wrapping and line splitting
            max_line_length = 100  # Adjust as needed
            lines = []
            for paragraph in transcript.split('\n'):
                line = ''
                for word in paragraph.split():
                    if len(line + ' ' + word) > max_line_length:
                        lines.append(line)
                        line = word
                    else:
                        line = line + ' ' + word if line else word
                lines.append(line)

            for line in lines:
                text_object.textLine(line)
            
            c.drawText(text_object)
            c.save()
        elif output_format == 'docx':
            doc = Document()
            doc.add_paragraph(transcript)
            doc.save(transcript_path)
        elif output_format == 'html':
            with open(transcript_path, "w", encoding="utf-8") as file:
                file.write(f"<html><body><p>{transcript}</p></body></html>")
        elif output_format == 'json':
            import json
            with open(transcript_path, "w", encoding="utf-8") as file:
                json.dump({"transcript": transcript}, file, ensure_ascii=False, indent=4)

    return base_filename + f".{output_format}"

@app.route('/transcript/<filename>')
def transcript(filename):
    format_mapping = {
        'txt': 'Text file (.txt)',
        'pdf': 'PDF file (.pdf)',
        'docx': 'Word file (.docx)',
        'html': 'HTML file (.html)',
        'json': 'JSON file (.json)'
    }
    base_filename = os.path.splitext(filename)[0]
    transcript_path = os.path.join(app.config['TRANSCRIPT_FOLDER'], base_filename + ".txt")
    chosen_format_extension = os.path.splitext(filename)[1][1:]  # Extract format extension without dot
    chosen_format_name = format_mapping.get(chosen_format_extension, chosen_format_extension)
    with open(transcript_path, "r", encoding="utf-8") as file:
        transcript = file.read()
    return render_template('transcript.html', transcript=transcript, filename=filename, chosen_format_name=chosen_format_name)



@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(app.config['TRANSCRIPT_FOLDER'], filename, as_attachment=True)



if __name__ == "__main__":
    app.run(debug=True)
    
