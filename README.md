# Python Trading Robot

## Table of Contents

- [Overview](#overview)
- [Authentication Workflow](#Authentication Workflow)
- [Usage](#usage)

## Overview

A trading robot written in Python that can run automated strategies.
The robot is designed to mimic a few common scenarios:

1. Maintaining a portfolio of multiple instruments. The `Portfolio` object will be able
   to calculate common risk metrics related to a portfolio and give real-time feedback
   as you trade.

2. Define an order that can be used to trade a financial instrument. With the `Trade` object,
   you can define simple or even complex orders using Python. These orders will also help similify
   common scenarios like defining both a take profit and stop loss at the same time.

3. A real-time data table that includes both historical and real-time prices as they change. The
   `StockFrame` will make the process of storing your data easy and quick. Additionally, it will be
   setup so that way you can easily select your financial data as it comes in and do further analysis
   if needed.

4. Define and calculate indicators using both historical and real-time prices. The `Indicator` object
   will help you easily define the input of your indicators, calculate them, and then update their values
   as new prices come.
   
## Authentication Workflow

1. While in Visual Studio Code, right click anywhere in the code editor while in the file that contains your code. 
   From the dropdown, click Run Python file in Terminal, this will start the python script.

2. The TD Library will automatically generate the redirect URL that will navigate you to the TD website for
   you authentication. You can either copy the link and paste it into a browser manually or if you're using 
   Visual Studio Code you can press CTRL + Click to have Visual Studio Code navigate you to the URL immediately.

3. Once you've arrived at the login screen, you'll need to provide your credentials to authenticate the session. 
   Please provide your Account Username and Account Password in the userform and then press enter. As a reminder these, 
   are the same username/password combination you use to login to your regular TD Account.
   
4. Accept the Terms of the API by clicking Allow, this will redirect you.

5. After accepting the terms, you'll be taken to the URL that you provided as your redirect URI. However, at the end of 
   that URL will be authorization code. To complete the authentication workflow, copy the URL as it appears below. 
   Don't worry if the numbers don't match, as you will have a different code.

6. Take the URL and copy it into the Terminal, after you have pasted it, press Enter. The authentication workflow will 
   complete, and the script will start running. At this stage, we are exchanging your authorization code for an access 
   token. That access token is valid only for 30 minutes. However, a refresh token is also stored that will refresh your
   access token when it expires.
   
7. After, that the script should run. Additionally, if you go to the location you specified in the credentials_path 
   argument you will now see td_state.json file. This file contains all the info used during a session. Please DO NOT 
   DELETE THIS FILE OR ELSE YOU WILL NEED TO GO THROUGH THE STEPS ABOVE.
   
## Usage

To run the robot, you will need to provide a few pieces of information from your TD Ameritrade Developer account.
The following items are need for authentication:

- Client ID: Also, called your consumer key, this was provided when you registered an app with the TD Ameritrade
  Developer platform. An example of a client ID could look like the following `MMMMYYYYYA6444VXXXXBBJC3DOOOO`.

- Redirect URI: Also called the callback URL or redirect URL, this was specified by you when you registered your app with
  the TD Ameritrade Developer platform. Here is an example of a redirect URI <https://localhost/mycallback>

- Credentials Path: This is a file path that will point to a JSON file where your state info will be saved. Keep in mind
  that it is okay if it points to a non-existing file as once you run the script the file will be auto generated. For example,
  if I want my state info to be saved to my desktop, then it would look like the following: `C:\Users\Desktop\ts_state.json`

Once you've identified those pieces of info, you can run the robot. Here is a simple example that will create a new instance
of it:

```python
from pyrobot.robot import PyRobot

# Initialize the robot
trading_robot = PyRobot(
    client_id='XXXXXX111111YYYY22',
    redirect_uri='https://localhost/mycallback',
    credentials_path='path/to/td_state.json'
)
```