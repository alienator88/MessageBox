import http.server, socketserver, json, signal, sys, os, subprocess

class MyHandler(http.server.SimpleHTTPRequestHandler):
    
    
    def do_POST(self):
        if self.path == '/sleep-screen':
            self.handle_sleep_screen()
        else:
            self.handle_form_submission()

    def handle_form_submission(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')

        # Parse the JSON data
        try:
            json_data = json.loads(post_data)
            message = json_data.get('message', '')

            server_directory = os.path.dirname(os.path.realpath(__file__))
            root_directory = os.path.abspath(os.path.join(server_directory, os.pardir))
            scripts_directory = os.path.join(root_directory, 'scripts')
            
            file_path = os.path.join(scripts_directory, 'current.txt')
            

            # Save the message to a file or process it as needed
            with open(file_path, 'w') as file:
                file.write(message)

            # Update screen with message
            display_message_script = os.path.join(scripts_directory, 'displayMessage.py')
            subprocess.run(["python", display_message_script, message], cwd=scripts_directory, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            # Respond to the POST request
            self.send_response(200)
            self.end_headers()
            self.wfile.write(bytes("Form submitted successfully", 'utf-8'))
        except json.JSONDecodeError:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(bytes("Invalid JSON data", 'utf-8'))

    def handle_sleep_screen(self):
        try:
            server_directory = os.path.dirname(os.path.realpath(__file__))
            root_directory = os.path.abspath(os.path.join(server_directory, os.pardir))
            scripts_directory = os.path.join(root_directory, 'scripts')
            # You can adjust this command based on your system and how you want to run sleepScreen.py
            subprocess.run(["python", "sleepScreen.py"], cwd=scripts_directory, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(bytes("Sleep screen command sent successfully", 'utf-8'))
        except subprocess.CalledProcessError as e:
            print(f"Error executing sleepScreen.py: {e}")
            self.send_response(500)
            self.end_headers()
            self.wfile.write(bytes("Error sending sleep screen command", 'utf-8'))

# Set up the web server
port = 3000
handler = MyHandler

with socketserver.TCPServer(("", port), handler) as httpd:
    print(f"Server started on port {port}. Navigate to http://localhost:{port}/index.html")

    # Handle Ctrl+C to gracefully shut down the server
    def signal_handler(sig, frame):
        print('\nShutting down the server...')
        httpd.server_close()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    # Keep the server running
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
