# python-gmail-helper
This is a simple repository to develop an application to utilize the Google API using Python for Gmail operations.

## Prerequisites
### Python
For Brief and custom installation including more linux disto you can follow this [Python 3 Installation & Setup Guide](https://realpython.com/installing-python/) from Real Python.
For basic and quick installation guide follow below:
##### Windows
**Step 1:** Download windows installer (32/64 bit based on your system) Python 3.8.8 from [here](https://www.python.org/downloads/windows/) (While Developing this version was used)
**Step 2:** Run the windows installer
**Step 3:** Press install now and install in default directory.
##### Linux
**Step 1:** Open terminal
**Step 2:** Run this commands:
- **Ubuntu 18.04, Ubuntu 20.04 and above:** 
    ```console
    sudo apt-get update
    sudo apt-get install python3.8 python3-pip
    ```
- **Linux Mint and Ubuntu 17 and below:**
    ```console
    sudo add-apt-repository ppa:deadsnakes/ppa
    sudo apt-get update
    sudo apt-get install python3.8 python3-pip
    ```
##### Mac
**Step 1:** Download installer Python 3.8.8 from [here](https://www.python.org/downloads/macos/) (While Developing this version was used)
**Step 2:** Run the installer
**Step 3:** Press continue and agree and finish the installation.

### Gmail API Installation and Configuration
**Step 1:** Install the Google client library or for more alternate option checkout [here](https://github.com/googleapis/google-api-python-client#installation).
```console
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```
**Step 2:** Configure the OAuth consent screen:
- Open the [Google Cloud console](https://console.cloud.google.com/)
- At the top-left, click **Menu > APIs & Services > OAuth consent screen.**
- Click top left drop down, then click **New Project**.
- Type in desired project name and click **Create**.
- Go to https://console.developers.google.com/apis/api/gmail.googleapis.com/overview?project=<your Project ID here> and enable Gmail API
- Then go to your newly created project from [console page](https://console.cloud.google.com/welcome) and clicking **"<Project name> API & Services"**
- Click ** OAuth consent screen** from the left panel
- Choose user type External/Internal based on your requirement, in this case we choose External and click **Create**
- In next screen
    - Give an app name
    - Choose Support email
    - Add logo if you have any
    - At the bottom add Developer email and create
- In next Screen
    - Save and continue
- In next Screen
    - Add a test user with valid email id
    - Save and continue
- Click **Credentials** from the left panel
- Hit the **+ CREATE CREDENTIALS** button on top bar.
    - Select **OAuth client ID**
    - Application type **Desktop App**
    - Create
    - Download the json and rename it as credential.json and paste it inside projetc folder

## Software Usage guide
### Initial Setup
- Clone the repository
- First time Click "helper.py" and validate the provided url to autorize this application. Links look like this "Please visit this URL to authorize this application: https://accounts.google.com/o/oauth2/auth?response_type=code&client_id=<clientId here>.apps.googleusercontent.com&redirect_uri=<redirectUri here>&access_type=offline"
- Choose the account you added as test user and press **Continue** two times
- Once it is enabled you will see "The authentication flow has completed. You may close this window." IN that window as confirmation.
- A toke.json will be generated in project folder. You need to delete it if you update SCOPE of the project
- Now you are set with all pre-requisites.

### Run
- Before Running the program Initial setup is necessary. Make sure you have both working credentials.json and token.json both inside the project folder.

Project can be used as a library or from command line. Making this as a package WIP. 
#### Library
You can import gmail_helper class from helper.py and utilize. 
###### Current available actions
- Send email
    ```python
    from helper import my_gmail
    worker = my_gmail()
    worker.send_email("<your email here>@email.com", "<Subject Line goes here>", "<Subject body goes here>")
    ```
    **Note:** If you are using your own email, credential and token remember to change default sender EMAIL on the script
- Search email
    ```python
    from helper import my_gmail
    worker = my_gmail()
    # Supports Gmail Advanced Search Features & Create Filters
    emails_matched = worker.search_emails("<search keywords goes here>")
    ```
#### Command line application
Here is the Help for the command line application
```console
python helper-updated.py --help
```
```console
usage: helper-updated.py [-h] [--manual] [-o {search,email,none}] [-e E] [-s S] [-b B] [-k K]
Gmail Helper
optional arguments:
  -h, --help            show this help message and exit
  --manual              specifies if the script is running in manual mode
  -o {search,email,none}
                        Send Email, Search Email, Do Nothing
  -e E                  Email address of recipient
  -s S                  Subject line
  -b B                  Body of email
  -k K                  Search keyword
```

###### To send an email:
```console
python helper.py --manual -o email -e "md.rashedul.amin@gmail.com" -s "galaxy" -b "hello universe"
```
**Note:** recipient email is mandatory if operation choosen to sent email. Failing providing this argument, system will abort saying "Error on dependency for manual mode"
**To send an email with or without subject line or body:**
- Without Body
    ```console
    python helper.py --manual -o email -e "md.rashedul.amin@gmail.com" -s "galaxy"
    Want to send email without body? [y/N]
    y
    ```
- Without Subject
    ```console
    python helper.py --manual -o email -e "md.rashedul.amin@gmail.com" -b "hello universe"
    Want to send email without subject? [y/N]
    y
    ```
**Note:** If you choose **N** in any case, application will abort.

###### To search in email:
```console
python helper.py --manual -o search -k "hello world" 
```