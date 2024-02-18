from flask import Blueprint, request, jsonify
from app.services import SimpleFileSystemService

file_system_blueprint = Blueprint('file_system', __name__)
fs_service = SimpleFileSystemService()

@file_system_blueprint.route('/folder/create', methods=['POST'])
def create_folder():
    data = request.json

    if not data or 'name' not in data or 'path' not in data:
        return jsonify({"message": "Missing name or path"}), 400

    result = fs_service.create_folder(data['name'], data['path'])
    if result:
        return jsonify({"message": "Folder created successfully"}), 200
    else:
        return jsonify({"message": "Folder already exists"}), 403

@file_system_blueprint.route('/file/create', methods=['POST'])
def create_file():
    data = request.json
    result = fs_service.create_file(data['name'], data['path'], data['content'])
    if result:
        return jsonify({"message": "File created successfully"}), 200
    else:
        return jsonify({"message": "File already exists"}), 403

@file_system_blueprint.route('/file/read', methods=['GET'])
def read_file():
    file_path = request.args.get('file_path')
    file_name = request.args.get('file_name')
    file = fs_service.read_file(file_path, file_name)
    if file is not None:
        return jsonify(file)
    else:
        return jsonify({"message": "File not found"}), 404

@file_system_blueprint.route('/file/update', methods=['PUT'])
def update_file():
    data = request.json
    fs_service.update_file(data['name'], data['path'], data['content'])
    return jsonify({"message": "File updated successfully"})

@file_system_blueprint.route('/file/delete', methods=['DELETE'])
def delete_file():
    file_path = request.args.get('file_path')
    file_name = request.args.get('file_name')

    result = fs_service.delete_file(file_path, file_name)
    if result:
        return jsonify({"message": "File deleted successfully"})
    else:
        return jsonify({"message": "File not found"}), 404

@file_system_blueprint.route('/files', methods=['GET'])
def list_files():
    files = fs_service.list_files()
    return jsonify({"files": files})

@file_system_blueprint.route('/folder/<path:path>', methods=['GET'])
def get_folder_content(path):
    data = fs_service.get_folder_content(path)
    return jsonify(data)