# from flask import Flask, request, jsonify
# import pandas as pd
# import sweetviz as sv
# import os
# import tempfile
# from flask_cors import CORS

# app = Flask(__name__)
# CORS(app)  # Enable CORS for all routes

# @app.route('/generate-report', methods=['POST'])
# def generate_report():
#     if 'file' not in request.files:
#         return jsonify({"error": "No file part"}), 400
    
#     file = request.files['file']
    
#     if file.filename == '':
#         return jsonify({"error": "No selected file"}), 400
    
#     if file:
#         try:
#             # Load the CSV file into a DataFrame
#             df = pd.read_csv(file)
            
#             # Create a temporary directory and file for the report
#             temp_dir = tempfile.gettempdir()
#             report_path = os.path.join(temp_dir, "sweetviz_report.html")
            
#             # Generate the Sweetviz report
#             report = sv.analyze(df)
#             report.show_html(report_path, open_browser=False, scale=0.7)
            
#             # Ensure the report file exists
#             if not os.path.isfile(report_path):
#                 return jsonify({"error": "Report generation failed"}), 500
            
#             # Read the report content
#             with open(report_path, 'r') as file:
#                 report_content = file.read()
            
#             # Return the report content as HTML
#             return report_content, 200, {'Content-Type': 'text/html'}
        
#         except Exception as e:
#             return jsonify({"error": str(e)}), 500
    
#     return jsonify({"error": "An unknown error occurred"}), 500

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', port=5000, debug=True)

from flask import Flask, request, jsonify
import pandas as pd
import sweetviz as sv
import os
import tempfile
import uuid
import matplotlib
matplotlib.use('Agg')  # Use Agg backend for Matplotlib
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/generate-report', methods=['POST'])
def generate_report():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if file:
        try:
            # Load the CSV file into a DataFrame
            df = pd.read_csv(file)
            
            # Create a unique temporary file for the report
            temp_dir = tempfile.gettempdir()
            unique_filename = f"sweetviz_report_{uuid.uuid4().hex}.html"
            report_path = os.path.join(temp_dir, unique_filename)
            
            # Generate the Sweetviz report
            report = sv.analyze(df)
            report.show_html(report_path, open_browser=False, scale=0.7)
            
            # Ensure the report file exists
            if not os.path.isfile(report_path):
                return jsonify({"error": "Report generation failed"}), 500
            
            # Read the report content
            with open(report_path, 'r') as file:
                report_content = file.read()
            
            # Clean up the report file
            os.remove(report_path)
            
            # Return the report content as HTML
            return report_content, 200, {'Content-Type': 'text/html'}
        
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    return jsonify({"error": "An unknown error occurred"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


