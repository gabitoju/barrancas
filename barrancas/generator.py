from path import path
from string import Template
from jinja2 import Environment, FileSystemLoader
import markdown
import yaml
import re
import sys, traceback


TEMPLATE_NOT_FOUND_ERROR = 'Template file {0} could not be found'

class Generator():

    def __init__(self, properties):
        self.properties = properties

    def generate(self):
        
        try:
            general_template = Template(path('templates/general.html').text(encoding='UTF-8'))
        except Exception as e:
            sys.stderr.write(TEMPLATE_NOT_FOUND_ERROR.format('templates/general.html'))
            sys.exit(1)

        current_dir = path('.')
        menu_items = []
        content_list = []
        links = {}
        for f in current_dir.files('*.md'):
            print 'Generating: {0}'.format(f)
            content = f.text(encoding='UTF-8')            

            parts = re.match(r'---(.*?)---', content, re.DOTALL)
            properties = yaml.load(parts.group(1))
            properties.update(self.properties)
            content = content.replace(parts.group(0), '')
            html_content = markdown.markdown(content, output_format='html5', extensions=['markdown.extensions.extra'])			
            
            if 'template' in properties:
                template_path = 'templates/{0}.html'.format(properties['template'])
                try:                    
                    template_f = Template(path(template_path).text(encoding='UTF-8'))
                    html_content = template_f.safe_substitute(properties, content=html_content)    
                except Exception as e:
                    sys.stderr.write(TEMPLATE_NOT_FOUND_ERROR.format(template_path))
                    sys.exit(1)                    
            if 'order' in properties:
                menu_items.append({'order': int(properties['order'] - 1),'title': properties['title'], 'link': f.replace('.md', '.html')})
                order = int(properties['order'])
            else:
                menu_items.append({'order': 0,'title': properties['title'], 'link': f.replace('.md', '.html')})
                order = 0
            final_content = general_template.safe_substitute(properties, content=html_content)

            file_name = f.replace('.md', '.html')
            links[order] = (file_name.replace('./', ''), properties['title'], properties.get('lang', ''))
            content_list.append((file_name, final_content, order, properties.get('lang', '')))
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
            
            order = c[2]
            if order != 0:
                link_p = u'<a class="previous" href="{0}">{1} >></a>'
                try:
                    previous = links[order - 1][0]                  
                    name = links[order - 1][1]            
                    if c[3] == links[order - 1][2]:
                        link_p = link_p.format(previous, name)                    
                    else:
                        link_p = ''
                except Exception as e:                
                    link_p = ''

                link_n = u'<a class="next" href="{0}"><< {1}</a>'
                try:
                    next_p = links[order + 1][0]                  
                    name = links[order + 1][1]
                    if c[3] == links[order + 1][2]:
                        link_n = link_n.format(next_p, name)                    
                    else:
                        link_n = ''
                except Exception as e:                                           
                    link_n = ''
                content = content.replace('${previous}', link_p).replace('${next}', link_n)

            path(c[0]).write_text(content, encoding='UTF-8')
   
