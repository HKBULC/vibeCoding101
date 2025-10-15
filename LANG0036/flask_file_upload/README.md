# Flask File Upload Manager with Database

A complete file upload system with drag-and-drop interface, database storage, and file management capabilities.

## 🌟 Features

- **Drag & Drop Upload**: Intuitive drag-and-drop interface
- **Database Integration**: SQLite database stores file metadata
- **File Management**: Upload, download, delete files
- **Search Functionality**: Search files by name or description
- **Statistics Dashboard**: View total files and storage usage
- **File Type Support**: Support for multiple file types (images, documents, archives, etc.)
- **Duplicate Handling**: Automatic handling of duplicate filenames
- **File Hashing**: SHA256 hash calculation for file integrity
- **Responsive Design**: Modern, gradient-based UI

## 📁 Project Structure

```
flask_file_upload/
├── app.py                 # Flask backend application
├── templates/
│   └── upload.html       # Frontend HTML/CSS/JS
├── uploads/              # Directory for uploaded files (auto-created)
├── files.db              # SQLite database (auto-created)
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## 🚀 Installation

### 1. Install Dependencies

```bash
cd /workspaces/vibeCoding101/LANG0036/flask_file_upload
pip install -r requirements.txt
```

### 2. Run the Application

```bash
python app.py
```

The server will start on `http://localhost:5000`

## 📊 Database Schema

### Table: `uploaded_files`

| Column | Type | Description |
|--------|------|-------------|
| id | INTEGER | Primary key |
| filename | STRING | Secure filename on server |
| original_filename | STRING | Original filename from upload |
| file_path | STRING | Full path to file |
| file_size | INTEGER | File size in bytes |
| file_type | STRING | File extension |
| file_hash | STRING | SHA256 hash |
| upload_date | DATETIME | Upload timestamp |
| description | TEXT | Optional description |

## 🔌 API Endpoints

### Upload File
```
POST /upload
Content-Type: multipart/form-data

Parameters:
- file: File object
- description: Optional text description

Returns:
{
  "success": true,
  "message": "File uploaded successfully",
  "file": { file_object }
}
```

### Get All Files
```
GET /files

Returns:
{
  "files": [ array_of_files ],
  "total": count
}
```

### Get File by ID
```
GET /files/<file_id>

Returns: file_object
```

### Delete File
```
DELETE /files/<file_id>

Returns:
{
  "success": true,
  "message": "File deleted successfully"
}
```

### Download File
```
GET /download/<file_id>

Returns: File download
```

### Search Files
```
GET /search?q=query

Returns:
{
  "files": [ matching_files ],
  "total": count,
  "query": search_term
}
```

### Get Statistics
```
GET /stats

Returns:
{
  "total_files": count,
  "total_size": bytes,
  "total_size_readable": "X.XX MB",
  "file_types": { type: count }
}
```

## 💻 Usage

### Upload Files

1. **Drag and Drop**: Drag files onto the upload zone
2. **Click to Browse**: Click the upload zone to select files
3. **Add Description**: Optionally add a description
4. **Multiple Files**: Upload multiple files at once

### Manage Files

- **Search**: Use search box to find files by name or description
- **Download**: Click download button to get the file
- **Delete**: Click delete button to remove file (with confirmation)

### View Statistics

- Total number of uploaded files
- Total storage used
- File type distribution

## ⚙️ Configuration

Edit `app.py` to customize:

```python
# Maximum file size (default: 50MB)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024

# Upload folder location
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')

# Allowed file extensions
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', ...}

# Secret key (change in production!)
app.config['SECRET_KEY'] = 'your-secret-key-here'
```

## 🔒 Security Features

- **Secure Filenames**: Uses `secure_filename()` to sanitize uploads
- **File Type Validation**: Only allowed extensions accepted
- **File Size Limits**: Configurable maximum file size
- **Hash Verification**: SHA256 hash for file integrity
- **Duplicate Prevention**: Automatic filename conflict resolution

## 🎨 Frontend Features

- **Modern UI**: Gradient-based design with smooth animations
- **Responsive Layout**: Works on desktop and mobile
- **Real-time Feedback**: Progress bars and status messages
- **File Type Badges**: Color-coded badges for different file types
- **Empty States**: Helpful messages when no files exist
- **Loading States**: Spinners during async operations

## 📝 Example Usage

### Python/Command Line

```python
import requests

# Upload a file
files = {'file': open('document.pdf', 'rb')}
data = {'description': 'Important document'}
response = requests.post('http://localhost:5000/upload', files=files, data=data)

# Get all files
response = requests.get('http://localhost:5000/files')
files = response.json()['files']

# Search files
response = requests.get('http://localhost:5000/search?q=document')
results = response.json()['files']

# Delete file
response = requests.delete(f'http://localhost:5000/files/{file_id}')
```

### JavaScript/Fetch API

```javascript
// Upload file
const formData = new FormData();
formData.append('file', fileObject);
formData.append('description', 'My file');

const response = await fetch('/upload', {
    method: 'POST',
    body: formData
});

const data = await response.json();
```

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Use a different port
python app.py --port 5001
```

### Permission Errors
```bash
# Ensure upload directory is writable
chmod 755 uploads/
```

### Database Locked
```bash
# Close other connections or delete and recreate
rm files.db
python app.py  # Database will be recreated
```

## 🔄 Database Migration

To reset the database:

```bash
rm files.db
python -c "from app import app, db; app.app_context().push(); db.create_all()"
```

## 📈 Performance Considerations

- **File Size**: Large files may take time to upload
- **Storage**: Monitor disk space in `uploads/` directory
- **Database**: SQLite suitable for small to medium usage
- **Scalability**: For production, consider PostgreSQL/MySQL

## 🚀 Production Deployment

For production use:

1. **Change SECRET_KEY**: Use a secure random key
2. **Use Production WSGI Server**: Gunicorn or uWSGI
3. **Enable HTTPS**: Use reverse proxy (nginx)
4. **Database**: Migrate to PostgreSQL
5. **File Storage**: Consider cloud storage (S3, Azure Blob)
6. **Add Authentication**: Implement user login
7. **Rate Limiting**: Prevent abuse
8. **Monitoring**: Add logging and error tracking

### Example with Gunicorn

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## 📦 Additional Features to Add

- [ ] User authentication and authorization
- [ ] File sharing with public/private links
- [ ] Image thumbnails and preview
- [ ] Batch operations (delete multiple, download as ZIP)
- [ ] File versioning
- [ ] Storage quotas per user
- [ ] Email notifications
- [ ] Virus scanning integration
- [ ] Cloud storage integration (S3, Google Drive)
- [ ] File categories/tags

## 🤝 Contributing

Feel free to extend and customize this application for your needs!

## 📄 License

Part of the vibeCoding101 educational project.

---

**Last Updated**: October 15, 2025
**Version**: 1.0.0
