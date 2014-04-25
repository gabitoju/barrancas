# barrancas

By Juan Gabito ([@gabitoju](https://twitter.com/gabitoju))

**barrancas** is a simple document generator that uses Markdown and Jinja2
to format and generate HTML documents or static web sites. It's inspired in 
[Jekyll](http://jekyllrb.com/) and written in Python.

## Dependencies

barrancas has the following dependencies:

+ [path.py](https://pypi.python.org/pypi/path.py)
+ [PyYAML](http://pyyaml.org/)
+ [Markdown](https://pypi.python.org/pypi/Markdown)
+ [Jinja2](http://jinja.pocoo.org/)

## Usage

### Directory structure

barracas uses the following directory structure:


    .                        // directory that contains the md files
    |-- templates           // directory that contains the html templates files
        |-- general.html   // basic templates
    |-- file1.md
    |-- file2.md

### Templates

barrancas use Jinja2 templates to generate html files. This templates are located in the *templates* directory and you must have at least the *general.html* template.

The following variables are available to use inside the templates:

+ ${title}: the article or page title
+ ${content}: thiw varible would be replaced with the content that it's generated from the md files. It also can be used inside the general template to include other templates.
+ ${menu}: this variable can be replaced with the content of a special template that contains the site or documentation menu. The name of this template must be *menu.html*.
+ ${quick\_menu}: It allows to have a small menu to link to document or page items (like an article section). The template file for this option is *quick_menu.html*.

This is a simple *general.html* template example: 


    <html>
        <head>
            <title>${title}</title>
        </head>
        <body>
            ${content}
         </body>
    </html>

The following examples uses an aditional template *article.html* (the file name does not matter):

    <!-- general.html -->
    <html>
        <head>
            <title>My Site</title>
        </head>
        <body>
            ${content}
         </body>
    </html>

    <!-- article.html -->
    <h1>${title}</h1>
    ${content}


The ${content} in *general.html* will bi replaces with the content of *article.html* and the md file will be included in the article template.

### Writing

barrancas read .md files and generates a .html file. For example, the post1.md will be generated as post1.html.

You can write the md file using Markdown, html or a combination of both. 

Also, you can use  the following yaml properties:

+ title: the article or document title.
+ template: the name of the template that will be used to generate this document. For example, if the template is *article.html* the property value will be *article*.
+ order: the order of the document in the menu.

This is an md example:

    ---
    title: "Example Article"    
    template: article
    order: 1
    ---
    # My first article

    *This* is an article showing the usage of barrancas.

### Generating the files

To generate the files you have to run *barrancas.py* in the directory that contains the md files. You can run *barrancas.py* with no arguments or with the *--generate* option.