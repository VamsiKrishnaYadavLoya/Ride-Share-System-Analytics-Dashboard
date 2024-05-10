# Ride-Share-System-Analytics-Dashboard
The Ride Share Analytics Dashboard project is designed to provide a comprehensive overview of ride-sharing activities within urban environments. By integrating and visualizing data from multiple ride-sharing platforms, this dashboard aims to offer actionable insights for improving traffic management, enhancing user experiences, and supporting sustainable urban mobility strategies.

# Steps to setup the project

Install Python:
• If Python is not already installed on your system, download and install Python from the official website: Python Downloads.
• Follow the installation instructions provided on the website for your operating system.

Clone the Project Repository:
• Clone the project repository containing the dashboard code to your local machine. You can do this using Git or by downloading the repository as a ZIP file and extracting it.

Navigate to the Project Directory:
• Open a command-line interface (e.g., Command Prompt, Terminal).
• Use the cd command to navigate to the directory where you cloned or extracted the project repository.

Create and Activate a Virtual Environment (Optional but Recommended):
• It's a good practice to work within a virtual environment to isolate the project dependencies. This step is optional but recommended.
• Create a virtual environment by running the following command:
  python -m venv myenv
• Activate the virtual environment:
• On Windows: myenv\Scripts\activate
• On macOS/Linux: source myenv/bin/activate

Install Required Python Libraries:
• Once inside the project directory, install the required Python libraries specified in the requirements.txt file using pip:
pip install -r requirements.txt
• This command will install the necessary libraries such as Streamlit, pandas, matplotlib, seaborn, and numpy.
Run the Streamlit Application:
• After installing the dependencies, you can run the Streamlit application by executing the following command in the command-line interface:
streamlit run app.py
• This command will start the Streamlit server locally, and you will see output indicating that the server is running.
• Open a web browser and navigate to the URL provided in the output (usually http://localhost:8501) to access the dashboard interface.
