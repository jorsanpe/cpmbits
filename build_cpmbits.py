#!/usr/bin/env python3
import os
import glob
import subprocess
from dataclasses import dataclass
import shutil
from bs4 import BeautifulSoup
from jinja2 import Template


OUTPUT_DIRECTORY = 'docs'
DOCS_OUTPUT_DIRECTORY = 'docs_output'
DOCS_DIRECTORY = 'documentation'
POSTS_DIRECTORY = 'posts'
POSTS_OUTPUT_DIRECTORY = 'blog_output'


@dataclass
class MenuItem:
    text: str
    highlighted: bool
    href: str


@dataclass
class DocumentationPage:
    title: str = 'Untitled'
    href: str = ''
    contents: str = ''


@dataclass
class BlogPost:
    title: str = 'Untitled'
    href: str = ''
    contents: str = ''
    summary: str = ''


def main():
    empty_directory(OUTPUT_DIRECTORY)
    empty_directory(DOCS_OUTPUT_DIRECTORY)
    empty_directory(POSTS_OUTPUT_DIRECTORY)

    with open(f'{OUTPUT_DIRECTORY}/index.html', 'w+') as stream:
        stream.write(render_index_page())

    render_documentation()

    render_blog()

    render_registration_story()

    shutil.copytree('resources/css', f'{OUTPUT_DIRECTORY}/css')
    shutil.copytree('resources/js', f'{OUTPUT_DIRECTORY}/js')
    shutil.copytree('resources/img', f'{OUTPUT_DIRECTORY}/img')
    shutil.copy('resources/img/favicon.ico', f'{OUTPUT_DIRECTORY}')
    shutil.copy('resources/CNAME', f'{OUTPUT_DIRECTORY}')

    generate_css()


def empty_directory(directory):
    try:
        shutil.rmtree(f'{directory}')
    except:
        pass
    os.mkdir(f'{directory}')


def render_index_page():
    menu_items = [
        MenuItem('Documentation', False, "1_getting_started.html"),
        MenuItem('Browse', False, "#"),
        MenuItem('Blog', False, "blog_cover.html"),
    ]
    head = render_head()
    navbar = render_navbar(menu_items)
    footer = render_footer()

    with open('templates/views/index.html') as stream:
        contents = stream.read()
    return Template(contents).render(head=head, navbar=navbar, footer=footer)


def render_documentation():
    convert_docs()
    converted_docs = sorted(glob.glob(f'{DOCS_OUTPUT_DIRECTORY}/*.html'))
    documentation_pages = [as_documentation_page(converted_doc) for converted_doc in converted_docs]
    
    for documentation_page in documentation_pages:
        aside_menu = render_documentation_aside_menu(documentation_pages, active_page=documentation_page)
        with open(f'{OUTPUT_DIRECTORY}/{documentation_page.href}', 'w+') as stream:
            stream.write(render_documentation_page(documentation_page, aside_menu))


def as_documentation_page(converted_doc):
    documentation_page = DocumentationPage()
    documentation_page.title = document_page_title(converted_doc)
    documentation_page.href = f'{os.path.basename(converted_doc)}'
    with open(converted_doc, 'r') as stream:
        raw_contents = stream.read()
    documentation_page.contents = customize_documentation_page_html(raw_contents)
    return documentation_page


def render_documentation_index_page(aside_menu):
    menu_items = [
        MenuItem('Documentation', False, "1_getting_started.html"),
        MenuItem('Browse', False, "#"),
        MenuItem('Blog', False, "blog_cover.html"),
    ]
    head = render_head()
    navbar = render_navbar(menu_items)
    footer = render_footer()

    with open('templates/views/documentation.html') as stream:
        contents = stream.read()
    return Template(contents).render(head=head, navbar=navbar, aside_menu=aside_menu, footer=footer)


def render_documentation_page(documentation_page, aside_menu):
    menu_items = [
        MenuItem('Documentation', False, "1_getting_started.html"),
        MenuItem('Browse', False, "#"),
        MenuItem('Blog', False, "blog_cover.html"),
    ]
    head = render_head()
    navbar = render_navbar(menu_items)
    footer = render_footer()

    with open('templates/views/documentation_page.html', 'r') as stream:
        contents = stream.read()
    return Template(contents).render(head=head, navbar=navbar, aside_menu=aside_menu, doc=documentation_page, footer=footer)


def customize_documentation_page_html(contents):
    class_customization = {
        'h1': 'title is-2',
        'h2': 'subtitle is-3',
        'h3': 'subtitle is-4',
    }

    soup = BeautifulSoup(contents, 'html.parser')
    for c in class_customization:
        for tag in soup.find_all(c):
            tag['class'] = class_customization[c]
    return soup.encode("utf-8").decode()


def document_page_title(docfile):
    return file_basename(docfile).replace('_', ' ').title()


def convert_docs():
    docs = glob.glob(f'{DOCS_DIRECTORY}/*.md')
    for doc in docs:
        subprocess.run(
            ['pandoc', '-f', 'markdown', '-t', 'html5', doc, '-o', f'{DOCS_OUTPUT_DIRECTORY}/{file_basename(doc)}.html']
        )


def render_registration_story():
    with open(f'{OUTPUT_DIRECTORY}/registration_page.html', 'w+') as stream:
        stream.write(render_registration_page())

    with open(f'{OUTPUT_DIRECTORY}/registration_failure.html', 'w+') as stream:
        stream.write(render_registration_failure())

    with open(f'{OUTPUT_DIRECTORY}/registration_success.html', 'w+') as stream:
        stream.write(render_registration_success())


def render_registration_page():
    menu_items = [
        MenuItem('Documentation', False, "1_getting_started.html"),
        MenuItem('Browse', False, "#"),
        MenuItem('Blog', False, "blog_cover.html"),
    ]
    head = render_head()
    navbar = render_navbar(menu_items)
    footer = render_footer()

    with open('templates/components/registration_form.html') as stream:
        registration_form = stream.read()
    with open('templates/views/registration_page.html', 'r') as stream:
        contents = stream.read()

    return Template(contents).render(head=head, navbar=navbar, registration_form=registration_form, footer=footer)


def render_registration_failure():
    menu_items = [
        MenuItem('Documentation', False, "1_getting_started.html"),
        MenuItem('Browse', False, "#"),
        MenuItem('Blog', False, "blog_cover.html"),
    ]
    head = render_head()
    navbar = render_navbar(menu_items)
    footer = render_footer()

    with open('templates/views/registration_failure.html', 'r') as stream:
        contents = stream.read()
    return Template(contents).render(head=head, navbar=navbar, footer=footer)


def render_registration_success():
    menu_items = [
        MenuItem('Documentation', False, "1_getting_started.html"),
        MenuItem('Browse', False, "#"),
        MenuItem('Blog', False, "blog_cover.html"),
    ]
    head = render_head()
    navbar = render_navbar(menu_items)
    footer = render_footer()

    with open('templates/views/registration_success.html', 'r') as stream:
        contents = stream.read()
    return Template(contents).render(head=head, navbar=navbar, footer=footer)


def render_blog():
    convert_posts()
    converted_posts = sorted(glob.glob(f'{POSTS_OUTPUT_DIRECTORY}/*.html'))
    blog_posts = [as_blog_post(converted_post) for converted_post in converted_posts]

    with open(f'{OUTPUT_DIRECTORY}/blog_cover.html', 'w+') as stream:
        stream.write(render_blog_cover(blog_posts))

    for blog_post in blog_posts:
        aside_menu = render_blog_aside_menu(blog_posts, active_post=blog_post)
        with open(f'{OUTPUT_DIRECTORY}/{blog_post.href}', 'w+') as stream:
            stream.write(render_blog_post(blog_post, aside_menu))


def render_blog_cover(blog_posts):
    menu_items = [
        MenuItem('Documentation', False, "1_getting_started.html"),
        MenuItem('Browse', False, "#"),
        MenuItem('Blog', False, "blog_cover.html"),
    ]
    head = render_head()
    navbar = render_navbar(menu_items)
    footer = render_footer()
    aside_menu = render_blog_aside_menu(blog_posts, active_post=None)

    with open('templates/views/blog_cover.html', 'r') as stream:
        contents = stream.read()
    return Template(contents).render(head=head, navbar=navbar, aside_menu=aside_menu, posts=blog_posts, footer=footer)


def as_blog_post(converted_post):
    blog_post = BlogPost()
    blog_post.title = document_page_title(converted_post)
    blog_post.href = f'{os.path.basename(converted_post)}'
    with open(converted_post, 'r') as stream:
        raw_contents = stream.read()
    blog_post.contents = customize_documentation_page_html(raw_contents)
    blog_post.summary = blog_post_summary(blog_post)
    return blog_post


def blog_post_summary(blog_post):
    soup = BeautifulSoup(blog_post.contents, 'html.parser')
    for tag in soup.find_all('p'):
        first_paragraph = str(tag)
        summary = first_paragraph
        break
    return summary


def render_blog_post(blog_post, aside_menu):
    menu_items = [
        MenuItem('Documentation', False, "1_getting_started.html"),
        MenuItem('Browse', False, "#"),
        MenuItem('Blog', False, "blog_cover.html"),
    ]
    head = render_head()
    navbar = render_navbar(menu_items)
    footer = render_footer()

    with open('templates/views/blog_post.html', 'r') as stream:
        contents = stream.read()
    return Template(contents).render(head=head, navbar=navbar, aside_menu=aside_menu, post=blog_post, footer=footer)


def render_blog_aside_menu(blog_posts, active_post):
    with open('templates/components/blog_aside_menu.html') as stream:
        blog_aside_menu_payload = stream.read()
        blog_aside_menu = Template(blog_aside_menu_payload).render(posts=blog_posts, active_post=active_post)
    return blog_aside_menu


def convert_posts():
    docs = glob.glob(f'{POSTS_DIRECTORY}/*.md')
    for doc in docs:
        subprocess.run(
            ['pandoc', '-f', 'markdown', '-t', 'html5', doc, '-o', f'{POSTS_OUTPUT_DIRECTORY}/{file_basename(doc)}.html']
        )


def generate_css():
    subprocess.run(['sass', f'bulma-customization/cpmbits.scss:{OUTPUT_DIRECTORY}/css/cpmbits.css'])


def file_basename(path):
    return os.path.splitext(os.path.basename(path))[0]


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


def render_documentation_aside_menu(documentation_pages, active_page):
    with open('templates/components/documentation_aside_menu.html') as stream:
        documentation_aside_menu_payload = stream.read()
        documentation_aside_menu = Template(documentation_aside_menu_payload).render(documents=documentation_pages, active_page=active_page)
    return documentation_aside_menu


if __name__ == '__main__':
    main()
