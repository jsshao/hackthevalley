from app import app
import os

dir_path = os.path.dirname(os.path.realpath(__file__))

context = (dir_path + '/cert/cert.pem', dir_path + '/cert/key.pem')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
