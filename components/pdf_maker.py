import json
import os
import re
import pypandoc
import logging
from components import config
LOGGER = logging.getLogger(__name__)

#https://pypi.org/project/pypandoc/
def mercury_summary_to_pdf(summary):
    """converts a mercury summary into a pdf file.
    """
    title     = summary['title']
    content   = summary['content']
    json_dump = json.dumps(summary, indent=4, sort_keys=True)
    file_name = re.sub('[^0-9a-zA-Z]+', '_', title) + '.pdf'
    file_name = file_name.strip()
    if file_name[-4:] != '.pdf':
        LOGGER.error('filename issues')
    
    markdown_text = pypandoc.convert_text(content, 'md',format='html')
    markdown_output = """
# {title}
## Author: {author}, Date: {date}
![]({lead_image_url})

Words: {word_count}

URL: {url}
    
----

{content}

----

```
{json_dump}
```
    """.format(title          = title,
               author         = summary['author'],
               date           = summary['date_published'],
               lead_image_url = summary['lead_image_url'],
               word_count     = summary['word_count'],
               url            = summary['url'],
               content        = markdown_text,
               json_dump      = json_dump)

    save_markdown(markdown_output, file_name)
    save_pdf(markdown_output, file_name)
    #save_tex(markdown_output, file_name)
    return file_name

def save_markdown(markdown: str, file_name: str):
    try:
        target_path = config.get_config()['md_target_path']
        os.makedirs(target_path, exist_ok=True)
        file_name = file_name + ".md"
        file_path = os.path.join(target_path,file_name)
        LOGGER.info("generating markdown file with name {}".format(file_name))
        with open(file_path, mode='w') as f:
            f.write(markdown)
    except Exception as e:
        LOGGER.error(e)
    
def save_pdf(markdown, file_name):
    try:
        target_path = config.get_config()['pdf_target_path']
        os.makedirs(target_path, exist_ok=True)
        file_path = os.path.join(target_path,file_name)
        extra_args = [
                '--latex-engine=xelatex'
                ]
        LOGGER.info("generating PDF file with name {}".format(file_name))
        pypandoc.convert_text(markdown, 'pdf',format='md', outputfile=file_path, extra_args=extra_args)
    except Exception as e:
        LOGGER.error(e)

def save_tex(markdown, file_name):
    LOGGER.info("generating tex file with name {}".format(file_name))
    target_path = config.get_config()['pdf_target_path']
    os.makedirs(target_path, exist_ok=True)
    file_path = os.path.join(target_path,file_name + '.tex')
    pypandoc.convert_text(markdown, 'tex',format='md', outputfile=file_path)
