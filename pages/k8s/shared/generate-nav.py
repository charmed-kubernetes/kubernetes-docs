import jinja2
import re

item = re.compile(r"\s*\-\s\[(.*)\]\((.*)\)")
subhead = re.compile(r"-\s*\*\*(.*)\*\*")
indent = 2
templateLoader = jinja2.FileSystemLoader(searchpath="./")
templateEnv = jinja2.Environment(loader=templateLoader)
TEMPLATE_FILE = "nav-section.j2"
section_template = templateEnv.get_template(TEMPLATE_FILE)
TEMPLATE_FILE = "nav-page.j2"
page_template = templateEnv.get_template(TEMPLATE_FILE)

def add_section(line):
    ctx = {}
    ctx['title'] = line[3:].strip()
    indent = 2
    ctx['indent'] = ' '*indent
    output = section_template.render(ctx)
    indent = 4
    return output

def add_page(line):
    ctx = {}
    m = item.search(line)
    ctx['title'] = m.group(1)
    ctx['url'] = m.group(2)[16:]
    if line[:2] == '  ':
        ctx['indent'] = ' '*(indent+2)
    else:
        ctx['indent'] = ' '*indent
    output = page_template.render(ctx)
    return output

def add_subhead(line):
    ctx = {}
    s = subhead.search(line)
    ctx['title'] = s.group(1)
    indent = 4
    ctx['indent'] = ' '*indent
    output = section_template.render(ctx)
    indent = 6
    return output

def main():
    output = """
# This is your sidebar TOC. The sidebar code loops through sections here and provides the appropriate formatting.

entries:
- title: sidebar
  items:
"""
    with open('_side-navigation.md','r') as f:
        content = f.readlines()
    for line in content:
        if line[:2] == '##':
            newblock = add_section(line)
            output += newblock +'\n'
        elif item.search(line):
            newblock = add_page(line)
            output += newblock +'\n'
        elif subhead.search(line):
            newblock = add_subhead(line)
            output += newblock +'\n'        
        else:
            print('not processed - '+line)
    print(output)
if __name__ == "__main__":
    main()

