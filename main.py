import os
from pathlib import Path
import openai
from git import Repo
import shutil
from bs4 import BeautifulSoup as Soup
import requests
import datetime

#print(os.getcwd())
PATH_TO_BLOG_REPO= Path("C:\\Users\\srgur\\OneDrive\\Desktop\\Guru\\LLM\\gforgurups.github.io\\.git")
PATH_TO_BLOG = PATH_TO_BLOG_REPO.parent
PATH_TO_CONTENT = PATH_TO_BLOG/"content"
PATH_TO_CONTENT.mkdir(exist_ok=True, parents=True)
openai.api_key = os.getenv("OPENAI_API_KEY")

def update_blog(commit_msg='Updates blog'):
    repo = Repo(PATH_TO_BLOG_REPO)
    # git add .
    repo.git.add(all=True)
    #git commit -m commit_msg
    repo.index.commit(commit_msg)
    #git push
    origin = repo.remote(name="origin")
    origin.push()

def create_new_blog(title, content, cover_img):
    img_path = Path(cover_img)
    files_count = len(list(PATH_TO_CONTENT.glob("*.html")))
    new_file=f"{files_count+1}.html"
    path_to_new_content = PATH_TO_CONTENT/new_file
    #shutil.copy(img_path,PATH_TO_CONTENT)

    # create new content
    if os.path.exists(path_to_new_content):
        raise FileExistsError("File already exists !")
    else:
        # create new content
        with open(path_to_new_content, "w") as f:
            f.write("<!DOCTYPE html>\n")
            f.write("<html>\n")
            f.write("<head>\n")
            f.write(f"<title> {title} </title>\n")
            f.write("</head>\n")

            f.write("<body>\n")
            f.write(f"<img src='{img_path.name}' alt='Cover Image'> <br />\n")
            f.write(f"<h1> {title} </h1>")
            f.write(content.replace("\n", "<br />\n"))
            f.write("</body>\n")
            f.write("</html>\n")
            print("Blog created")
        with open(PATH_TO_BLOG/"index.html") as index:
            soup = Soup(index.read())
            links = soup.find_all("a")
            last_link = links[-1]
            link_to_new_blog = soup.new_tag("a",href=Path(*path_to_new_content.parts[-2:]))
            link_to_new_blog.string = path_to_new_content.name.split('.')[0]
            last_link.insert_after(link_to_new_blog)
        with open(PATH_TO_BLOG / "index.html", "w") as index:
            index.write(str(soup.prettify(formatter='html')))
            print("Index updated")

def create_prompt(title):
    prompt="""
    Biography:
    My name is Guru and I work as Associate Director for Wayfare India.
    
    Blog
    Title: {}
    Tags: Tech, Python, AI, GenAI, LLM, LangChain
    Summary: I talk about applications of GenAI in real world scenarios
    Full Text: """.format(title)
    return prompt

def dalle2_prompt(title):
    prompt =f"Pixel digital art showing {title}"
    return prompt

def generateOpenAIContent(title):
    response = openai.Completion.create(
        model='text-davinci-003',
        prompt=create_prompt(title),
        temperature=0.7,
        max_tokens=1000
     )

    img_response = openai.Image.create(
        prompt=dalle2_prompt(title),
        n=1,
        size='256x256'
    )

    img_url = img_response['data'][0]['url']
    img_res = requests.get(img_url, stream=True)
    if img_res.status_code == 200:
        img = "img_"+str(datetime.datetime.now().second)+".png"
        img_name=PATH_TO_CONTENT/img
        with open(img_name, 'wb') as f:
            shutil.copyfileobj(img_res.raw, f)
    else:
        print("Error")

    print("Image saved successfully")
    return response.choices[0].text,img_name
    

content,img = generateOpenAIContent("Applications of LangChain in real world")
create_new_blog("Test Title", content, img)
update_blog()