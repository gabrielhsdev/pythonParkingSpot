from app import create_app

def run_app():
    """
    Initialize and start the Flask application.

    This function creates the Flask app instance using the factory function, 
    and runs it on all available network interfaces (host='0.0.0.0') binding it to port 5001.
    
    Do not remove the host and port parameters, as they are required for the application to run in the container.
    """
    
    app = create_app()
    app.run(host="0.0.0.0", port=5001, debug=True)

if __name__ == "__main__":
    """
    Entry point for the application when the script is executed directly.
    """

    run_app()
