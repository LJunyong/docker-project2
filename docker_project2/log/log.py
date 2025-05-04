from flask import Flask, request

app = Flask(__name__)

@app.route('/log', methods=['POST'])
def log():
    log = request.json.get('message', 'No message')
    with open('logs.txt', 'a', encoding='utf-8') as p:
        p.write(log + '\n')
    return 'Logged', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=6000)
