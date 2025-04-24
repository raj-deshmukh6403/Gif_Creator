from flask import Flask, render_template, request, send_from_directory, redirect, url_for, flash, after_this_request, session
import os
import imageio
from PIL import Image
import numpy as np
import uuid
import shutil
import time
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'rajhd6403'  # Required for flash messages and sessions

# Enable sessions
app.config['SESSION_TYPE'] = 'filesystem'

# Folder for uploaded images and generated GIFs
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'uploads')
GIF_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'gifs')

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['GIF_FOLDER'] = GIF_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload size
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'}

# Ensure directories exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(GIF_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Helper function to resize images
def resize_image(image, size):
    return image.resize(size, Image.LANCZOS)

# Helper function to create GIF from images
def create_gif_from_images(image_paths, gif_name, duration=0.5, loop=0):
    try:
        image_paths.sort()  # Sort images by name to maintain order
        images = []
        first_image = Image.open(image_paths[0]).convert('RGB')
        image_size = first_image.size
        
        for filename in image_paths:
            img = Image.open(filename).convert('RGB') 
            img_resized = resize_image(img, image_size)
            images.append(np.array(img_resized))

        gif_path = os.path.join(GIF_FOLDER, gif_name)
        # If the file already exists, remove it first to prevent permission issues
        if os.path.exists(gif_path):
            try:
                os.remove(gif_path)
            except PermissionError:
                # If we can't remove it, generate a new filename
                gif_name = f"{uuid.uuid4().hex}_{gif_name}"
                gif_path = os.path.join(GIF_FOLDER, gif_name)
                
        imageio.mimsave(gif_path, images, duration=float(duration), loop=int(loop))
        return gif_name, None
    except Exception as e:
        return None, str(e)

# Clean up function to remove files safely
def cleanup_files(file_paths, gif_path=None):
    # Remove uploaded images
    for file_path in file_paths:
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except Exception as e:
                print(f"Error removing {file_path}: {e}")
    
    # We no longer try to remove the GIF file here
    # This avoids the permission error when the GIF is being downloaded

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/reset', methods=['POST'])
def reset():
    # This route clears session data and redirects to the index
    return redirect(url_for('index'))

@app.route('/upload', methods=['POST'])
def upload_files():
    print("Upload route called")  # Debug print
    file_paths = []  # Initialize list to store file paths
    
    try:
        print("Form data keys:", request.form.keys())  # Debug print
        print("Files keys:", request.files.keys())  # Debug print
        
        # Check if individual files were uploaded - check both forms of the name
        if 'files' in request.files:
            print("Processing files input")  # Debug print
            files = request.files.getlist('files')
            if files and files[0].filename:
                # Validate that we have at least 2 images for a meaningful GIF
                valid_files = [f for f in files if f and f.filename and allowed_file(f.filename)]
                if len(valid_files) < 2:
                    flash('Please upload at least 2 valid image files')
                    return redirect(url_for('index'))
                
                # Save the valid files
                for file in valid_files:
                    original_filename = secure_filename(file.filename)
                    filename = f"{uuid.uuid4().hex}_{original_filename}"
                    file_path = os.path.join(UPLOAD_FOLDER, filename)
                    file.save(file_path)
                    file_paths.append(file_path)
        elif 'files[]' in request.files:
            print("Processing files[] input")  # Debug print
            files = request.files.getlist('files[]')
            if files and files[0].filename:
                # Validate that we have at least 2 images for a meaningful GIF
                valid_files = [f for f in files if f and f.filename and allowed_file(f.filename)]
                if len(valid_files) < 2:
                    flash('Please upload at least 2 valid image files')
                    return redirect(url_for('index'))
                
                # Save the valid files
                for file in valid_files:
                    original_filename = secure_filename(file.filename)
                    filename = f"{uuid.uuid4().hex}_{original_filename}"
                    file_path = os.path.join(UPLOAD_FOLDER, filename)
                    file.save(file_path)
                    file_paths.append(file_path)
        
        # Check if a folder was uploaded (directory isn't directly supported in HTML, but we can use a directory input)
        elif 'folder' in request.files:
            print("Processing folder input")  # Debug print
            files = request.files.getlist('folder')
            if files and files[0].filename:
                valid_files = [f for f in files if f and f.filename and allowed_file(f.filename)]
                if len(valid_files) < 2:
                    flash('Please select a folder with at least 2 valid image files')
                    return redirect(url_for('index'))
                
                # Save the valid files from the folder
                for file in valid_files:
                    original_filename = secure_filename(file.filename)
                    filename = f"{uuid.uuid4().hex}_{original_filename}"
                    file_path = os.path.join(UPLOAD_FOLDER, filename)
                    file.save(file_path)
                    file_paths.append(file_path)
        
        else:
            flash('No files or folder selected')
            return redirect(url_for('index'))
        
        # If we have file paths, create the GIF
        if file_paths:
            print(f"Files saved: {len(file_paths)}")  # Debug print
            
            # Get parameters from the form
            gif_name = secure_filename(request.form.get('gif_name', 'my_gif')) + '.gif'
            duration = request.form.get('duration', 0.5)
            loop = request.form.get('loop', 0)
            
            print(f"Creating GIF with name: {gif_name}, duration: {duration}, loop: {loop}")  # Debug print
            
            gif_filename, error = create_gif_from_images(file_paths, gif_name, duration, loop)
            
            if error:
                flash(f'Error creating GIF: {error}')
                cleanup_files(file_paths)  # Clean up uploaded files on error
                return redirect(url_for('index'))
            
            # Store file paths in session for cleanup after download
            session['file_paths'] = file_paths
            session['gif_path'] = os.path.join(GIF_FOLDER, gif_filename)
            
            print(f"GIF created successfully: {gif_filename}")  # Debug print
            
            # Pass the gif filename to the template
            return render_template('index.html', gif_path=gif_filename, session_data={'file_paths': file_paths, 'gif_path': os.path.join(GIF_FOLDER, gif_filename)})
        
        else:
            flash('No valid images found')
            return redirect(url_for('index'))
            
    except Exception as e:
        flash(f'An error occurred: {str(e)}')
        # Clean up any files that might have been saved before the error
        cleanup_files(file_paths)
        return redirect(url_for('index'))

@app.route('/download/<filename>')
def download(filename):
    # Get the full path of the gif
    gif_path = os.path.join(GIF_FOLDER, filename)
    
    # Check if the file exists
    if not os.path.exists(gif_path):
        flash('File not found')
        return redirect(url_for('index'))
    
    # Get file paths from query parameters
    file_paths = request.args.getlist('file_paths')
    
    # Clean up only the uploaded files, not the GIF
    if file_paths:
        cleanup_files(file_paths)
    
    # Return the file without trying to delete it during download
    return send_from_directory(
        directory=GIF_FOLDER, 
        path=filename, 
        as_attachment=True
    )

# Add a scheduled cleanup task for old GIFs (optional)
def cleanup_old_gifs(max_age_days=1):
    """Clean up GIFs older than max_age_days"""
    now = time.time()
    for filename in os.listdir(GIF_FOLDER):
        filepath = os.path.join(GIF_FOLDER, filename)
        if os.path.isfile(filepath):
            # Get file's age in days
            file_age_days = (now - os.path.getmtime(filepath)) / (24 * 3600)
            if file_age_days > max_age_days:
                try:
                    os.remove(filepath)
                    print(f"Removed old GIF: {filename}")
                except Exception as e:
                    print(f"Failed to remove {filename}: {e}")

if __name__ == '__main__':
    app.run(debug=True)