import os
from pathlib import Path
import openai
from git import Repo

#print(os.getcwd())
PATH_TO_BLOG_REPO= Path("C:\\Users\\srgur\\OneDrive\\Desktop\\Guru\\LLM\\gforgurups.github.io\\.git")
PATH_TO_BLOG = PATH_TO_BLOG_REPO.parent
PATH_TO_CONTENT = PATH_TO_BLOG/"content"
PATH_TO_CONTENT.mkdir(exist_ok=True, parents=True)

def update_blog(commit_msg='Updates blog'):
    repo = Repo(PATH_TO_BLOG_REPO)
    # git add .
    repo.git.add(all=True)
    #git commit -m commit_msg
    repo.index.commit(commit_msg)
    #git push
    origin = repo.remote(name="origin")
    origin.push()

random_text_string ="Testing git connection"

with open(PATH_TO_BLOG/"index.html",'w') as f:
    f.write(random_text_string)

update_blog()