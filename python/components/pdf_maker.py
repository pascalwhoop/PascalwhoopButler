import json
import os
import pdfkit
import re
from subprocess import call
import markdown
import logging
from components import config
LOGGER = logging.getLogger(__name__)

def mercury_summary_to_pdf(summary):
    """converts a mercury summary into a pdf file.
    """
    title     = summary['title']
    content   = summary['content']
    name_template = re.sub('[^0-9a-zA-Z]+', '_', title) + '.{}'
    name_template= name_template.strip()
    
    body = """
           <a href="{url}"><h1>{title}</h1></a>
           <h2>Author: {author}, Date: {date}</h2>
           <img src="{lead_image_url}" class="lead"/>
           <hr>
           {content}
    """.format(title          = summary['title'],
               author         = summary['author'],
               date           = summary['date_published'],
               lead_image_url = summary['lead_image_url'],
               word_count     = summary['word_count'],
               url            = summary['url'],
               content        = summary['content'])
    html_full = html_tmp.format(body)

    save_html(html_full, name_template.format("html"))
    #save_pdf(html_full,  name_template.format("pdf"))
    save_pdf_original(summary['url'],  name_template.format("pdf"))
    return name_template

def save_html(html: str, file_name: str):
    try:
        target_path = config.get_config()['html_target_path']
        os.makedirs(target_path, exist_ok=True)
        file_path = os.path.join(target_path,file_name)
        LOGGER.info("saving html file with name {}".format(file_name))
        with open(file_path, mode='w') as f:
            f.write(html)
    except Exception as e:
        LOGGER.error(e)

def save_website(url, file_name):
    try:
        target_path = config.get_config()['pdf_target_path']
        os.makedirs(target_path, exist_ok=True)
        file_path = os.path.join(target_path,file_name)
        LOGGER.info("generating PDF file with name {}".format(file_name))
        tmplt = config.get_config()['puppeteer_template']
        cmd_arr = tmplt.format(url, file_name).split(' ')
        return_code = call(cmd_arr)
        if return_code
    except Exception as e:
        LOGGER.error(e)

        


def save_pdf(html, file_name):
    try:
        target_path = config.get_config()['pdf_target_path']
        os.makedirs(target_path, exist_ok=True)
        file_path = os.path.join(target_path,file_name)
        LOGGER.info("generating PDF file with name {}".format(file_name))
        pdfkit.from_string(html, file_name)
    except Exception as e:
        LOGGER.error(e)

# OLD, DON'T USE
def save_pdf_original(url, file_name):
    try:
        target_path = config.get_config()['pdf_target_path']
        os.makedirs(target_path, exist_ok=True)
        file_path = os.path.join(target_path,file_name)
        LOGGER.info("generating PDF file with name {}".format(file_name))
        pdfkit.from_url(url, file_name)
    except Exception as e:
        LOGGER.error(e)


html_tmp = """
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <link rel="stylesheet" href="css/styles.css">
</head>

<body>
    {}
</body>
</html>
"""
