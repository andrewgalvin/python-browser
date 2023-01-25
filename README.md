# python-browser

A simple web browser built with Python and PyQt5. Navigate, refresh, and duplicate pages. Perfect for learning PyQt5 and desktop app development in Python.

# How to run the code

## Requirements

- Python 3 installed on your system. You can download it from [here](https://www.python.org/downloads/)
  - For a guide to installing Python, visit the wiki [here](https://wiki.python.org/moin/BeginnersGuide/Download)

## Setup

1. Clone or download the repository
2. Open and extract the folder to a location of your choice
3. Open the command prompt and navigate to the location in which you extracted the repository to
4. Run the following command to install any needed libraries: `pip install -r requirements.txt` -- the libraries installed can be found in the `requirements.txt` file
5. Fill the following locations with the required data
   - The default location is below:
     - "./data/proxies.txt" -- add proxies to this file
     - "./data/links.txt" -- add links to this file (include `https://www.`)
       - Example: `https://www.google.com/`
6. Ensure the data located in the folder labeled "data" is not empty
   - This will require you to input proxies (default is **empty**) and links (default is Google)

## Execution

Run the following command in your terminal

```
python main.py
```

## Program Navigation

### Selecting a Proxy to Open

In order to open a browser, you must use your arrow keys to navigate through the program.

1. Use the **right arrow key** to select a proxy
2. Use the **down arrow key** to move down the list of proxies
3. Use the **TAB** button to select all proxies
4. Use the **ENTER** button to open the selected proxies

## Additional Notes

- If the file containing the proxies cannot be found or the file is empty, the program will raise an exception and stop running
- If you close a browser, you can re-open it by using your arrow keys to select the proxy it was hosted on
- If any other error occurs, it will be displayed in the command prompt or terminal window
- There may be erorr output as the browsers are open and running, if you need to open a new browser simply use your arrow keys and the error output will disappear
- If you want to stop the program, press CTRL+C on your keyboard
