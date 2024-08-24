To Run Locally 


1. Install python 

2. Create a virtual environment using python 

```
python -m venv venv 

```
3. activate venv 

for windows 
```
venv\Scripts\activate
``` 
in cmd prompt 

```
source venv/Scripts/activate 
``` 
in bash 

for linux 

```
source venv/bin/activate 
```

4. Install poetry package after activating venv 

```
pip install poetry 
```

5. Clone this repo 

```
git clone https://github.com/abhi2596/DocoToc_chatbot.git
```
6. After cloning repo run this command to install other packages 

```
poetry install 

```
then run 
```
cd chatbot 
```
create a folder .streamlit in that add a file secrets.toml in which add 

OPENAI_API_KEY = "your-api-key"

then to run streamlit 

use this command 

```
streamlit run app.py 
```