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
        return jsonify(conn.getPrinters())
    else:
        return "Erro ao ligar a CUPS!"

@app.route('/print', methods=['POST'])
def print_pdf():
    data = request.json
    printer_name = data.get('printer')
    file_name = data.get(f'file_name')
    settings = data.get('settings')
    #return jsonify(data)
    if not printer_name or not file_name :
        return jsonify({'error': 'O nome da impressoara ou o arquivo são necessarios!'})
    try:
        file = request.files['file']
        file_path = os.path.join(app.config['UPLOAD_FOLDER', file_name])
        file.save()
        conn.printFile(printer_name, file_path, file_name, settings)
        os.remove(file_path)
        return jsonify({'message': f'Arquivo {file_name} impresso com sucesso na impressora {printer_name}!'})
    except Exception as e:
        return jsonify({'error': f'Erro ao imprimir o arquivo {file_name}  : {e}'})

 
@app.route('/')
def hello():
    return 'Hello, World!'

 
if __name__ == '__main__':
    app.run(debug=True, host='192.168.0.31')