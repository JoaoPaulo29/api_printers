from flask import Flask, jsonify, request
import cups
import os
 
app = Flask(__name__)
conn = cups.Connection()

UPLOAD_FOLDER = '/files'
if not os.path.exists(UPLOAD_FOLDER) :
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/get/printers', methods=['GET'])
def get_printers():
    if conn :
        return jsonify({'printers':conn.getPrinters(), 'status': 200})
    else:
        return jsonify({'error':"Erro ao ligar a CUPS!", 'status':500})

@app.route('/print', methods=['POST'])
def print_pdf():
    if 'file' not in request.files :
        return jsonify({'error': 'No file part', 'status':400})
    file = request.files['file']
    printer_name = request.form['printer']
    
    if not printer_name or not file.filename :
        return jsonify({'error': 'O nome da impressoara ou o arquivo são necessarios!', 'status':400})
    try: 
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        conn.printFile(printer_name, file_path, file.filename, {}) 
        return jsonify({'message': f'Arquivo {file.filename} impresso com sucesso na impressora {printer_name}!', 'status':200})
    except Exception as e:
        return jsonify({'error': f'Erro ao imprimir o arquivo {file.filename}  : {e}', 'status': 500})

 
@app.route('/')
def hello():
    return 'Hello, World!'

 
if __name__ == '__main__':
    app.run(debug=True, host='192.168.0.31')