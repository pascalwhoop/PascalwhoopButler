import logging
import os
import pdfkit
import re
from subprocess import call
from urllib.parse import urlparse

from components import config

LOGGER = logging.getLogger(__name__)


def mercury_summary_to_pdf(summary):
    """converts a mercury summary into a pdf file.
    """
    title = summary['title']
    content = summary['content']
    name_template = re.sub('[^0-9a-zA-Z]+', '_', title) + '.{}'
    name_template = name_template.strip()

    body = """
           <a href="{url}"><h1>{title}</h1></a>
           <h2>Author: {author}, Date: {date}</h2>
           <img src="{lead_image_url}" class="lead"/>
           <hr>
           {content}
    """.format(title=summary['title'],
               author=summary['author'],
               date=summary['date_published'],
               lead_image_url=summary['lead_image_url'],
               word_count=summary['word_count'],
               url=summary['url'],
               content=summary['content'])
    html_full = html_tmp.format(body)

    save_html(html_full, name_template.format("html"))
    save_website(summary['url'], name_template.format("pdf"))
    # save_pdf(html_full,  name_template.format("pdf"))
    # save_pdf_original(summary['url'],  name_template.format("pdf"))
    return name_template


def save_html(html: str, file_name: str):
    """Saves given html as such, directly as html file"""
    try:
        target_path = config.get_config()['html_target_path']
        os.makedirs(target_path, exist_ok=True)
        file_path = os.path.join(target_path, file_name)
        LOGGER.info("saving html file with name {}".format(file_name))
        with open(file_path, mode='w') as f:
            f.write(html)
    except Exception as e:
        LOGGER.error(e)


def save_website(url, file_name):
    """Takes a screenshot with puppeteer and saves it as a PDF"""
    try:
        LOGGER.info("puppeteer print for {}".format(url))
        target_path = config.get_config()['pdf_target_path']
        os.makedirs(target_path, exist_ok=True)
        file_path = os.path.join(target_path, file_name)
        LOGGER.info("generating PDF file with name {}".format(file_name))
        tmplt = config.get_config()['puppeteer_template']
        cmd = tmplt.format(url, str(file_path)).split(' ')
        LOGGER.info("calling puppeteer script as -- {}".format(cmd))
        return_code = call(cmd)
        return return_code
    except Exception as e:
        LOGGER.error(e)


def save_pdf(html, file_name):
    """Save Markdown variant as PDF"""
    try:
        target_path = config.get_config()['pdf_target_path']
        os.makedirs(target_path, exist_ok=True)
        file_path = os.path.join(target_path, file_name)
        LOGGER.info("generating PDF file with name {}".format(file_name))
        pdfkit.from_string(html, file_name)
    except Exception as e:
        LOGGER.error(e)


def save_pdf_directly(response):
    target_path = config.get_config()['pdf_target_path']
    os.makedirs(target_path, exist_ok=True)
    title = re.sub("[\W]", "", response.url.strip())
    file_name = get_fn_from_header(response)
    if file_name is None:
        file_name = "{}.pdf".format(title)

    # making it host specific
    host = urlparse(response.url).netloc
    file_name = host + file_name
    file_path = os.path.join(target_path, file_name)
    if os.path.exists(file_path):
        return
    else:
        print('Saving PDF {}'.format(file_path))
        with open(file_path, 'wb') as f:
            f.write(response.body)


def get_fn_from_header(response):
    cd = response.headers.get('Content-Disposition')
    if cd is not None:
        cd = cd.decode('ascii')
        fn = re.search("filename=(.*)", cd).group(1)
        if fn:
            file_name = re.sub("[\W]", "", fn)
            file_name = file_name[:-3] + ".pdf"
            return file_name


# OLD, DON'T USE
# def save_pdf_original(url, file_name):
#    try:
#        target_path = config.get_config()['pdf_target_path']
#        os.makedirs(target_path, exist_ok=True)
#        file_path = os.path.join(target_path,file_name)
#        LOGGER.info("generating PDF file with name {}".format(file_name))
#        pdfkit.from_url(url, file_name)
#    except Exception as e:
#        LOGGER.error(e)


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
