# Welcome to CNED-API
## An API to get your CNED Homeworks

### How to make it work ?  
- Install python
- Run ```pip install -r requirements.txt``` in the folder
- Create a credentials file, put your username in 1st line and Password in 2nd
- Go to vars.py, change creds.txt to yout file path (leave it to creds.txt if your file is in the folder of the project, named creds.txt)
- Run the app
- Go to ``` http://your-ip:5000/hws```  to get the data !


### How to use it ?  
- Go the vars file, replace creds for your creds file (txt, username in 1st line, password in 2nd).
- When you go / fetch ```http://ip:5000/hws```, it returns :
  - If you have no data file (which should not happen):
  ```
      { 
        "old_data": {
          "corrected": "None",
          "given_homeworks": "None",
          "in_correction": "None"
        }
        "new_data": { 
          "given_homeworks": "x",
          "in_correction": "x", 
          "corrected": "x"
        }
      }
  ```
  - If the data file exists: 
  ```
      { 
        "old_data": {
          "corrected": "x",
          "given_homeworks": "x",
          "in_correction": "x"
        }
        "new_data": { 
          "given_homeworks": "x",
          "in_correction": "x", 
          "corrected": "x"
        }
      }
  ```

You can easily integrate this with discord bot or anything to run the endpoint and get data.
  
Any ideas ? Create a **pull request** !
