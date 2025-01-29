""" 
Author      : Seunghwan Shin 
Create date : 2024-07-12 
Description : Code that can perform various functions through Telegram
    
History     : 2024-07-12 Seunghwan Shin       # first creat
              2024-08-27 Seunghwan Shin       # Modified so that only integers can be represented on the x-axis of the graph.
              2024-11-05 Seunghwan Shin       # Create Test api
              2025-01-29 Seunghwan Shin       # Change code configuration to make system settings easier to manage using '.env' files
"""
from controller import *

if __name__ == "__main__":
    """
    Code to load ".env" file.
    """
    load_dotenv()
    
    """
    Function to start the "Flask" server
    Route functions exist below "controller.py"
    """ 
    RUNNING_PORT = os.getenv('RUNNING_PORT')
    app.run(debug=True, port=RUNNING_PORT)