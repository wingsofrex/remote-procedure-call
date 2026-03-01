# remote-procedure-call
This lab demonstrates Remote Procedure Call used in Distributed Computing Environment

# Tools
Programming Language: Python
IDE / Platform: VSCode
Framework: Flask
CLI: PIP

# What are we trying to do here
Here, we implement a simple distributed system with one client (CLIENT) and two servers (SERVER1 and SERVER 2). Two servers SERVER1 and SERVER 2 are used as file servers and contains same set of files (one is replica of another).  Note that there may be delay in updating the servers. 
The above distributed system must perform the following:
o	CLIENT sends a file request with a “pathname” to SERVER 1. 
o	SERVER 1 checks its own file system for the file and sends the same file request to SERVER 2. 
o	SERVER 2 returns the file if available. 
o	SERVER 1 then compares the contents of file it found in its directory and the file that is received from SERVER 2.
o	If there is no difference between the file contents, SERVER1 sends the file to client.
o	If there is a difference between the file contents, SERVER1 sends both the files to client.
o	If file is available on one of the servers, then the file is returned to client via SERVER 1.
o	If the file is not available, SERVER 1 should send appropriate message to CLIENT

# Project Structure
Here we have two folders namely server1_files and server2_files which contain empty text files. server1_files folder contain two files data.txt and hello.txt. server2_files contain data_1.txt and hello.txt. 

# Note
The text files in the folder are completely empty and will not have any effect on the outcome of the project

# Implementation

After we complete the writing of the code for server1.py (which traverses server1_files), server2.py (for server2_files) and client.py, you need to open 3 terminals.

In the first terminal, type the below command:

# python server1.py #

In the second terminal:

# python server2.py #

In the third terminal, type:

# python client.py #

Once you run client.py, here is what you may see. Note that I have used Python Virtual Environment for this task. You are free to use whichever tool you want to use.
# ------------------------------------------------------------------------------------#

(.venv) $ python client.py
Enter file pathname: hello.txt
=== FILE RECEIVED (both servers matched) ===

(.venv) $ python client.py
Enter file pathname: data.txt
=== FILE RECEIVED (from one server) ===

(.venv) $ python client.py
Enter file pathname: hero.txt
File not found on any server.

# -------------------------------------------------------------------------------------- #

# Note #
Converted the process into a Web App

(.venv) $ python client.py
Enter file pathname: hello.txt
=== FILE RECEIVED (both servers matched) ===

