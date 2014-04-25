from path import path
from string import Template
import markdown
import yaml
import re
from jinja2 import Environment, FileSystemLoader

class Generator():

    def __init__(self, properties):
        self.properties = properties

    def generate(self):
        
        general_template = Template(path('templates/general.html').text(encoding='UTF-8'))
        current_dir = path('.')
        menu_items = []
        content_list = []
        for f in current_dir.files('*.md'):
            print 'Generating: {0}'.format(f)
            content = f.text(encoding='UTF-8')            

            parts = re.match(r'---(.*?)---', content, re.DOTALL)
            properties = yaml.load(parts.group(1))
            properties.update(self.properties)
            content = content.replace(parts.group(0), '')
            html_content = markdown.markdown(content, output_format='html5')			
            
            if 'template' in properties:
                template_f = Template(path('templates/{0}.html'.format(properties['template'])).text(encoding='UTF-8'))
                html_content = template_f.safe_substitute(properties, content=html_content)    
            if 'order' in properties:
                menu_items.append({'order': int(properties['order'] - 1),'title': properties['title'], 'link': f.replace('.md', '.html')})
            else:
                menu_items.append({'order': 0,'title': properties['title'], 'link': f.replace('.md', '.html')})

            final_content = general_template.safe_substitute(properties, content=html_content)

            file_name = f.replace('.md', '.html')
            content_list.append((file_name, final_content))
        menu_items = sorted(menu_items, key = lambda k: k['order'])
        
        for c in content_list:
            env = Environment(loader=FileSystemLoader('templates'))
            temp = env.get_template('menu.html')
            menu = temp.render(items=menu_items, current=c[0])            
            
            content = c[1].replace('${menu}', menu)
            quick_menu_items = re.compile('<h3>(.*?)</h3>', re.DOTALL |  re.IGNORECASE).findall(content)
            i = 1
            for item in quick_menu_items:
                link = '<h3><a name="' + str(i) + '"></a>' + item + '</h3>'
                content = content.replace('<h3>' + item + '</h3>', link)
                i = i + 1
            if len(quick_menu_items) > 0:
                temp = env.get_template('quick_menu.html')
                quick_menu = temp.render(items=quick_menu_items, current=c[0])
                content = content.replace('${quick_menu}', quick_menu)
            else:
                content = content.replace('${quick_menu}', '')
            
            path(c[0]).write_text(content, encoding='UTF-8')
   
