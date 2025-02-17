import os
from flask import current_app

def get_unique_filename(filename):
    base, ext = os.path.splitext(filename)
    counter = 1
    while os.path.exists(os.path.join(current_app.config['UPLOAD_FOLDER'], filename)):
        filename = f"{base}_{counter}{ext}"
        counter += 1
    return filename

def delete_file(file_path):
    """Удаляет файл по указанному пути."""
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
            return True
        except Exception as e:
            print(f"Ошибка при удалении файла {file_path}: {str(e)}")
            return False
    return False
