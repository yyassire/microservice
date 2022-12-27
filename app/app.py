from fastapi import FastAPI,Depends,HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets
import os
from app.scraping import TwitterScraping,Youtube

# Creating an app object
app = FastAPI()
security = HTTPBasic()
load_dotenv()
origins = [
    #  origins will be added here
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8080",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)
   

# auth
def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    current_username_bytes = credentials.username.encode("utf8")
    # correct_username_bytes =b(os.environ['LOGIN'])
    correct_username_bytes = b"istardatalab"
    is_correct_username = secrets.compare_digest(
        current_username_bytes, correct_username_bytes
    )
    current_password_bytes = credentials.password.encode("utf8")
    # correct_password_bytes = b(os.environ['PASSWORD'])
    correct_password_bytes = b"istar"
    is_correct_password = secrets.compare_digest(
        current_password_bytes, correct_password_bytes
    )
    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return True


# download twit
@app.post("/twitter", tags=['twitter'])
async def twitter(body:dict,username: bool = Depends(get_current_username)):
    tweet = TwitterScraping(word=body.get("word"),
    limit= body.get("limit"),since=body.get("since"),
    until=body.get("until"),hashtag=body.get("hashtag"),
    account=body.get("user_account"))
    if body.get("word"):
        data = tweet.search_keyword()
    elif body.get("user_account"):
        data = tweet.search_user()
    elif body.get("hashtag"):
        data = tweet.search_hashtag()  
    return data
# youtube scraping
@app.post("/youtube", tags=['youtube'])
async def youtube(body:dict,username: bool = Depends(get_current_username)):
    print(body)
    data= Youtube(body.get("url"),body.get("limit")).main()
    return data   
  
