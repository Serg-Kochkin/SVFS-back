from datetime import datetime
from app.models import SystemType

class SimpleFileSystemService:
    def __init__(self):
        self.fileSystem = []

    def is_exist_item(self, name, path):
        return any(item for item in self.fileSystem if item["name"] == name and item["path"] == path)

    def create_file(self, name, path, content):
        if not self.is_exist_item(name, path):
            timestamp = datetime.utcnow().isoformat() + 'Z'
            self.fileSystem.append({'name': name,
                                    'path': path,
                                    'content': content,
                                    'type': SystemType.FILE.name,
                                    'created_at': timestamp,
                                    'modified_at': timestamp,
                                    'size': len(content.encode('utf-8'))
                                    })
            return True
        else:
            return False

    def create_folder(self, name, path):
        if not self.is_exist_item(name, path):
            timestamp = datetime.utcnow().isoformat() + 'Z'
            self.fileSystem.append({'name': name,
                                    'path': path,
                                    'content': None,
                                    'type': SystemType.FOLDER.name,
                                    'created_at': timestamp,
                                    'modified_at': timestamp,
                                    'size': 0,
                                    })
            return True
        else:
            return False

    def read_file(self, file_path, file_name):
        file = next((item for item in self.fileSystem if item["path"] == file_path and item["name"] == file_name), None)
        if file is not None:
            file_info = {'name': file['name'], 'content': file['content']}
        else:
            file_info = None
        return file_info
    
    def get_folder_content(self, path):
        result = [item for item in self.fileSystem if item["path"] == path]
        return {"files": result}

    def update_file(self, file_name, file_path, content):
        timestamp = datetime.utcnow().isoformat() + 'Z'
        for file in self.fileSystem:
            if file['name'] == file_name and file['path'] == file_path:
                file['content'] = content
                file['modified_at'] = timestamp
                file['size'] = len(content.encode('utf-8'))
                return True
        return False

    def delete_file(self, file_path, file_name):
        file_index = next((index for index, item in enumerate(self.fileSystem) 
                            if item["path"] == file_path and item["name"] == file_name), None)
        
        if file_index is not None:
            del self.fileSystem[file_index]
            return True
        else:
            return False

    def list_files(self):
        return [{'name': file['name'],
                 'path': file['path'],
                 'type': file['type'],
                 'created_at': file['created_at'],
                 'modified_at': file['modified_at'],
                 'size': file['size'],
                 'content': file['content'],
                 }  for file in self.fileSystem]
