### Requirement
 - Task 1. Install llama
 - Task2. Write a Python script that accept user questions
 - Task 3. Send the user question from Python to Llama 
    - Example:  what's the capital of India
 - Task 4. Update SOLR Index with student scores in a class (SOLR index is like Elastic)
 - Task 5. Have the Python send the question to Llama > Have Llama convert that to SOLR query > Take 
    - Llama's response and send it to SOLR
 - Task 6. Send SOLR response to Llama for formatting
 - Task 7. Show the response to user in a nice way (Python)



### Initial Setup to setup the project
- Step 1: 
    - Open powershell:
        - run: `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`
        - ref url: https://docs.astral.sh/uv/getting-started/installation/#standalone-installer
            ![After UV installed](images/uv_installed.png)
- Step 2:
    - Check if UV installed
        - Run: `uv --version`
        - Run: `uv --help`
- Step 3:
    - Go to your project directory
        - Run: `uv init`
- Step 4:
    - To install dependencies
        - Run: `uv init`
- Step 4:
    - To install dependencies
        - Run: `uv add solrpy`
        - else all the dependencies into `pyproject.toml` file as dependencies with version
- Step 5:
    - To run python script
        - Run: `uv run main.py`


#### To Access The solr UI

-Step 1: Find or Download Solr
  -If you don’t already have Solr:
    -Download it from the official site:
       👉 https://solr.apache.org/downloads.html

 -Extract it somewhere, e.g., D:\solr-9.5.0

 -Extract the .tgz file using a tool like 7-Zip (Right-click → Extract).

#### if you don't have java installed in your system  then follow these steps 

###✅ Step-by-Step: Fix JAVA_HOME on Windows
git
-1. Install Java
    -If Java isn't installed yet, download and install one of the following:

    -Adoptium JDK 17 (Recommended)
    -https://adoptium.net/en-GB/temurin/releases/
    -Make sure to choose the Windows x64 MSI Installer.

-2. Find Java Installation Path
   -After installing, the Java path will be something like:

    - C:\Program Files\Eclipse Adoptium\jdk-17.0.9

-3. Set JAVA_HOME
    -Press Win + R, type sysdm.cpl, press Enter.
    -Go to Advanced → Environment Variables.

    -Under System variables, click New:

       -Variable name: JAVA_HOME

    -Variable value: paste the Java path, e.g.,

       -C:\Program Files\Eclipse Adoptium\jdk-17.0.9

    -Click OK.

-4. Verify the Setup
    -Close your command prompt. Open a new one, then run:

        -java -version
        echo %JAVA_HOME%

    -You should see your Java version and the correct path.


-Step 2: Start Solr (on Windows)
   -Open Command Prompt (not Git Bash), and run:

     -cd D:\solr-9.5.0\bin
     -solr.cmd start

    - Now you should see output like:

    -Waiting up to 180 seconds to see Solr running on port 8983
    -Started Solr server on port 8983

Step 3: Check if it Works
    -Then, open your browser and go to:

    -http://localhost:8983/solr/
    -You should see the Solr admin UI. 


##### flow digram ###########

+----------------+
|  User (Gradio) |
|   Input:       |
| Natural Language|
|   Question     |
+-------+--------+
        |
        | (1. User enters question)
        v
+-------+--------+
|   Python Backend  |
|  (forwards query) |
+-------+--------+
        |
        | (2. Forwards to LLaMA)
        v
+-------+--------+
|  LLaMA Model   |
| (Interprets &  |
|  Generates Solr |
|   Query)       |
+-------+--------+
        |
        | (3. Generates Solr query)
        v
+-------+--------+
|   Python Backend  |
|  (executes query)|
+-------+--------+
        |
        | (4. Executes query on Solr)
        v
+-------+--------+
|   Solr Database |
| (Returns Relevant|
|   Results)     |
+-------+--------+
        |
        | (5. Returns results)
        v
+-------+--------+
|   Python Backend  |
|  (formats response)|
+-------+--------+
        |
        | (6. Formats & sends to Gradio)
        v
+-------+--------+
|  Gradio UI     |
|   Output:      |
| Formatted Answer|
+----------------+

![AI Query System Flow](docs/ai_query_system_flow.png)
