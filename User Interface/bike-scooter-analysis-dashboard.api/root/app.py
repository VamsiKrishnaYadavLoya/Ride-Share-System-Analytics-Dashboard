import sys
import os
# Assuming your project structure requires adding the parent directory to sys.path to find the 'controllers' package
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from flask import Flask
from controllers.DataSummary import data_summary  # Adjusted import statement

app = Flask(__name__)

# Adjusting the route setup to use the more conventional decorator syntax
@app.route('/api/data-summary', methods=['GET'])
def summary():
    return data_summary()

if __name__ == '__main__':
    app.run(debug=True)



