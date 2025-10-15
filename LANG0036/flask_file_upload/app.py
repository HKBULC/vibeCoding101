from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from datetime import datetime
import os
import hashlib
try:
    import openai
    import PyPDF2
    from PIL import Image
    import io
    import base64
    AI_ENABLED = True
except ImportError:
    AI_ENABLED = False
    print("AI features disabled. Install: pip install openai PyPDF2 Pillow")
import openai
import PyPDF2
import docx
from PIL import Image
import io
import base64

app = Flask(__name__)

# Configuration
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
DATABASE_PATH = os.path.join(BASE_DIR, 'files.db')

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DATABASE_PATH}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key-here-change-in-production'

# Initialize database
db = SQLAlchemy(app)

# Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Database Model
class UploadedFile(db.Model):
    __tablename__ = 'uploaded_files'
    
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    file_size = db.Column(db.Integer, nullable=False)  # in bytes
    file_type = db.Column(db.String(100))
    file_hash = db.Column(db.String(64))  # SHA256 hash
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    description = db.Column(db.Text)
    
    def __repr__(self):
        return f'<File {self.original_filename}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'filename': self.filename,
            'original_filename': self.original_filename,
            'file_size': self.file_size,
            'file_size_readable': self.get_readable_size(),
            'file_type': self.file_type,
            'upload_date': self.upload_date.strftime('%Y-%m-%d %H:%M:%S'),
            'description': self.description
        }
    
    def get_readable_size(self):
        """Convert bytes to human readable format"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if self.file_size < 1024.0:
                return f"{self.file_size:.2f} {unit}"
            self.file_size /= 1024.0
        return f"{self.file_size:.2f} TB"

# Create tables
with app.app_context():
    db.create_all()

def calculate_file_hash(file_path):
    """Calculate SHA256 hash of file"""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def allowed_file(filename):
    """Check if file extension is allowed"""
    # You can customize this list
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx', 
                          'xls', 'xlsx', 'zip', 'rar', 'mp4', 'mp3', 'md', 'csv'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Render main upload page"""
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload"""
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    description = request.form.get('description', '')
    
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        # Secure the filename
        original_filename = file.filename
        filename = secure_filename(original_filename)
        
        # Create unique filename if duplicate exists
        base_name, extension = os.path.splitext(filename)
        counter = 1
        while os.path.exists(os.path.join(app.config['UPLOAD_FOLDER'], filename)):
            filename = f"{base_name}_{counter}{extension}"
            counter += 1
        
        # Save file
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Get file info
        file_size = os.path.getsize(file_path)
        file_type = extension[1:] if extension else 'unknown'
        file_hash = calculate_file_hash(file_path)
        
        # Save to database
        new_file = UploadedFile(
            filename=filename,
            original_filename=original_filename,
            file_path=file_path,
            file_size=file_size,
            file_type=file_type,
            file_hash=file_hash,
            description=description
        )
        
        db.session.add(new_file)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'File uploaded successfully',
            'file': new_file.to_dict()
        }), 200
    
    return jsonify({'error': 'File type not allowed'}), 400

@app.route('/files', methods=['GET'])
def get_files():
    """Get list of all uploaded files"""
    files = UploadedFile.query.order_by(UploadedFile.upload_date.desc()).all()
    return jsonify({
        'files': [file.to_dict() for file in files],
        'total': len(files)
    })

@app.route('/files/<int:file_id>', methods=['GET'])
def get_file(file_id):
    """Get specific file info"""
    file = UploadedFile.query.get_or_404(file_id)
    return jsonify(file.to_dict())

@app.route('/files/<int:file_id>', methods=['DELETE'])
def delete_file(file_id):
    """Delete a file"""
    file = UploadedFile.query.get_or_404(file_id)
    
    # Delete physical file
    try:
        if os.path.exists(file.file_path):
            os.remove(file.file_path)
    except Exception as e:
        return jsonify({'error': f'Error deleting file: {str(e)}'}), 500
    
    # Delete database record
    db.session.delete(file)
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'File deleted successfully'})

@app.route('/download/<int:file_id>')
def download_file(file_id):
    """Download a file"""
    file = UploadedFile.query.get_or_404(file_id)
    return send_from_directory(
        app.config['UPLOAD_FOLDER'],
        file.filename,
        as_attachment=True,
        download_name=file.original_filename
    )

@app.route('/search')
def search_files():
    """Search files by filename or description"""
    query = request.args.get('q', '')
    
    if not query:
        return jsonify({'files': [], 'total': 0})
    
    files = UploadedFile.query.filter(
        db.or_(
            UploadedFile.original_filename.like(f'%{query}%'),
            UploadedFile.description.like(f'%{query}%')
        )
    ).order_by(UploadedFile.upload_date.desc()).all()
    
    return jsonify({
        'files': [file.to_dict() for file in files],
        'total': len(files),
        'query': query
    })

@app.route('/stats')
def get_stats():
    """Get upload statistics"""
    total_files = UploadedFile.query.count()
    total_size = db.session.query(db.func.sum(UploadedFile.file_size)).scalar() or 0
    
    # Get file type distribution
    file_types = db.session.query(
        UploadedFile.file_type,
        db.func.count(UploadedFile.id)
    ).group_by(UploadedFile.file_type).all()
    
    return jsonify({
        'total_files': total_files,
        'total_size': total_size,
        'total_size_readable': format_bytes(total_size),
        'file_types': {ft: count for ft, count in file_types}
    })

def format_bytes(size):
    """Convert bytes to human readable format"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return f"{size:.2f} {unit}"
        size /= 1024.0
    return f"{size:.2f} PB"

def extract_text_from_pdf(file_path):
    """Extract text from PDF file"""
    try:
        text = ""
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text()
        return text
    except Exception as e:
        return f"Error extracting text: {str(e)}"

def extract_text_from_txt(file_path):
    """Extract text from text file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"

def encode_image_to_base64(file_path):
    """Encode image to base64 for OpenAI Vision API"""
    try:
        with open(file_path, 'rb') as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except Exception as e:
        return None

@app.route('/ai/analyze', methods=['POST'])
def ai_analyze_file():
    """Analyze file content using OpenAI"""
    data = request.json
    file_id = data.get('file_id')
    api_key = data.get('api_key')
    prompt = data.get('prompt', 'Analyze this content and provide a summary')
    
    if not file_id or not api_key:
        return jsonify({'error': 'Missing file_id or api_key'}), 400
    
    file = UploadedFile.query.get_or_404(file_id)
    
    try:
        # Set OpenAI API key
        openai.api_key = api_key
        
        # Extract content based on file type
        content = ""
        file_type = file.file_type.lower()
        
        if file_type == 'pdf':
            content = extract_text_from_pdf(file.file_path)
        elif file_type in ['txt', 'md', 'csv']:
            content = extract_text_from_txt(file.file_path)
        elif file_type in ['png', 'jpg', 'jpeg', 'gif']:
            # Use Vision API for images
            base64_image = encode_image_to_base64(file.file_path)
            if base64_image:
                response = openai.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": prompt},
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/{file_type};base64,{base64_image}"
                                    }
                                }
                            ]
                        }
                    ],
                    max_tokens=1000
                )
                return jsonify({
                    'success': True,
                    'analysis': response.choices[0].message.content,
                    'model': 'gpt-4o-mini',
                    'file_type': 'image'
                })
        else:
            return jsonify({'error': f'File type {file_type} not supported for AI analysis'}), 400
        
        # For text-based files, use standard completion
        if content and not content.startswith('Error'):
            # Truncate content if too long (max ~3000 words)
            max_chars = 12000
            if len(content) > max_chars:
                content = content[:max_chars] + "...\n[Content truncated]"
            
            response = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that analyzes documents and provides insightful summaries and analysis."},
                    {"role": "user", "content": f"{prompt}\n\nContent:\n{content}"}
                ],
                max_tokens=1000,
                temperature=0.7
            )
            
            return jsonify({
                'success': True,
                'analysis': response.choices[0].message.content,
                'model': 'gpt-4o-mini',
                'file_type': file_type,
                'content_length': len(content)
            })
        else:
            return jsonify({'error': content}), 500
            
    except Exception as e:
        return jsonify({'error': f'AI analysis failed: {str(e)}'}), 500

@app.route('/ai/chat', methods=['POST'])
def ai_chat():
    """General AI chat endpoint"""
    data = request.json
    api_key = data.get('api_key')
    message = data.get('message')
    file_id = data.get('file_id')  # Optional: context from a file
    
    if not api_key or not message:
        return jsonify({'error': 'Missing api_key or message'}), 400
    
    try:
        openai.api_key = api_key
        
        # Build context if file_id provided
        context = ""
        if file_id:
            file = UploadedFile.query.get(file_id)
            if file:
                file_type = file.file_type.lower()
                if file_type == 'pdf':
                    context = extract_text_from_pdf(file.file_path)
                elif file_type in ['txt', 'md', 'csv']:
                    context = extract_text_from_txt(file.file_path)
                
                # Truncate if too long
                if len(context) > 8000:
                    context = context[:8000] + "...\n[Content truncated]"
        
        # Create message with or without context
        if context:
            full_message = f"Based on this document:\n\n{context}\n\nQuestion: {message}"
        else:
            full_message = message
        
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant that helps users understand and work with their uploaded documents."},
                {"role": "user", "content": full_message}
            ],
            max_tokens=1000,
            temperature=0.7
        )
        
        return jsonify({
            'success': True,
            'response': response.choices[0].message.content,
            'model': 'gpt-4o-mini',
            'has_context': bool(context)
        })
        
    except Exception as e:
        return jsonify({'error': f'Chat failed: {str(e)}'}), 500

@app.route('/ai/suggest-tags', methods=['POST'])
def ai_suggest_tags():
    """Suggest tags for a file using AI"""
    data = request.json
    file_id = data.get('file_id')
    api_key = data.get('api_key')
    
    if not file_id or not api_key:
        return jsonify({'error': 'Missing file_id or api_key'}), 400
    
    file = UploadedFile.query.get_or_404(file_id)
    
    try:
        openai.api_key = api_key
        
        # Extract content
        content = ""
        file_type = file.file_type.lower()
        
        if file_type == 'pdf':
            content = extract_text_from_pdf(file.file_path)[:5000]
        elif file_type in ['txt', 'md', 'csv']:
            content = extract_text_from_txt(file.file_path)[:5000]
        else:
            # For other files, use filename and description
            content = f"Filename: {file.original_filename}\nDescription: {file.description or 'N/A'}"
        
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that suggests relevant tags for documents. Provide 5-10 single-word or short-phrase tags separated by commas."},
                {"role": "user", "content": f"Suggest tags for this content:\n\n{content}"}
            ],
            max_tokens=100,
            temperature=0.5
        )
        
        tags = response.choices[0].message.content.strip()
        tag_list = [tag.strip() for tag in tags.split(',')]
        
        return jsonify({
            'success': True,
            'tags': tag_list,
            'model': 'gpt-4o-mini'
        })
        
    except Exception as e:
        return jsonify({'error': f'Tag suggestion failed: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
