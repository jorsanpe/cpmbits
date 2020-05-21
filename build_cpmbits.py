#!/usr/bin/env python3
import os
import glob
import subprocess
from dataclasses import dataclass
import shutil

from jinja2 import Template


DOCS_DIRECTORY = 'docs'
OUTPUT_DIRECTORY = 'output'
DOCS_OUTPUT_DIRECTORY = 'docs_output'


@dataclass
class MenuItem:
    text: str
    highlighted: bool
    href: str


@dataclass
class DocumentPage:
    title: str
    href: str
    page_contents: str


def main():
    empty_directory(OUTPUT_DIRECTORY)
    empty_directory(DOCS_OUTPUT_DIRECTORY)

    with open(f'{OUTPUT_DIRECTORY}/index.html', 'w+') as stream:
        stream.write(render_index_page())

    with open(f'{OUTPUT_DIRECTORY}/documentation.html', 'w+') as stream:
        stream.write(render_documentation_index_page())

    shutil.copytree('resources/css', f'{OUTPUT_DIRECTORY}/css')
    shutil.copytree('resources/js', f'{OUTPUT_DIRECTORY}/js')
    shutil.copytree('resources/img', f'{OUTPUT_DIRECTORY}/img')


def empty_directory(directory):
    try:
        shutil.rmtree(f'{directory}')
    except:
        pass
    os.mkdir(f'{directory}')


def render_index_page():
    menu_items = [
        MenuItem('Documentation', False, "documentation.html"),
        MenuItem('Browse', False, "browse.html"),
        MenuItem('Blog', False, "blog.html"),
    ]
    head = render_head()
    navbar = render_navbar(menu_items)
    footer = render_footer()

    with open('templates/views/index.html') as stream:
        contents = stream.read()
    return Template(contents).render(head=head, navbar=navbar, footer=footer)


def render_documentation_index_page():
    menu_items = [
        MenuItem('Documentation', True, "documentation.html"),
        MenuItem('Browse', False, "browse.html"),
        MenuItem('Blog', False, "blog.html"),
    ]
    head = render_head()
    navbar = render_navbar(menu_items)
    aside_menu = render_documentation_aside_menu()
    footer = render_footer()

    with open('templates/views/documentation.html') as stream:
        contents = stream.read()
    return Template(contents).render(head=head, navbar=navbar, aside_menu=aside_menu, footer=footer)


def render_documentation_pages():
    converted_docs = glob.glob(f'{DOCS_OUTPUT_DIRECTORY}/*.html')


def all_documentation_pages():
    converted_docs = glob.glob(f'{DOCS_OUTPUT_DIRECTORY}/*.html')



def convert_docs():
    docs = glob.glob(f'{DOCS_DIRECTORY}/*.md')
    for doc in docs:
        subprocess.run(
            ['pandoc', '-f', 'markdown', '-t', 'html5', doc, '-o', f'{DOCS_OUTPUT_DIRECTORY}/{os.path.basename(doc)}.html']
        )


def render_head():
    with open('templates/components/head.html') as stream:
        head_payload = stream.read()
        head = Template(head_payload).render()
    return head


def render_navbar(menu_items):
    with open('templates/components/navbar.html') as stream:
        navbar_payload = stream.read()
        navbar = Template(navbar_payload).render(menu_items=menu_items)
    return navbar


def render_footer():
    with open('templates/components/footer.html') as stream:
        footer_payload = stream.read()
        footer = Template(footer_payload).render()
    return footer


def render_documentation_aside_menu():
    with open('templates/components/documentation_aside_menu.html') as stream:
        documentation_aside_menu_payload = stream.read()
        documentation_aside_menu = Template(documentation_aside_menu_payload).render()
    return documentation_aside_menu


if __name__ == '__main__':
    main()
