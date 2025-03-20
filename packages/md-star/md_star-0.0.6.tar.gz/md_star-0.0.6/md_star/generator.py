"""
A Python static site generator that converts Markdown files to HTML websites.
"""

import json
import locale
import shutil
from datetime import datetime
from pathlib import Path
from xml.dom import minidom
from xml.etree import ElementTree as ET

import arrow
import frontmatter
import markdown
import yaml
from jinja2 import Environment, FileSystemLoader, select_autoescape
from markdown_it import MarkdownIt
from slugify import slugify


class MarkdownSiteGenerator:
    """
    Core class for static site generation.
    Handles Markdown conversion, template rendering, and static file generation.
    """

    X_CARD_TYPE_SUMMARY = "summary"

    ARTICLE_TYPE_ARTICLE = "Article"
    ARTICLE_TYPE_NEWS = "NewsArticle"
    ARTICLE_TYPE_BLOG = "BlogPosting"
    VALID_ARTICLE_TYPES = [ARTICLE_TYPE_ARTICLE, ARTICLE_TYPE_NEWS, ARTICLE_TYPE_BLOG]

    def __init__(self, config_path: str = "config.yaml"):
        """Initialize the static site generator."""

        self.config_path = Path(config_path).absolute()
        self.project_dir = self.config_path.parent

        # Load and parse the YAML site configuration file
        with open(config_path, "r", encoding="utf-8") as f:
            self.config = yaml.safe_load(f)

        if "site" not in self.config:
            self.config["site"] = {}

        self.config["site"].setdefault("timezone", "UTC")
        self.config["site"].setdefault("locale", "en")
        self.config["site"].setdefault("article_type", self.ARTICLE_TYPE_ARTICLE)

        if self.config["site"].get("article_type") not in self.VALID_ARTICLE_TYPES:
            print(
                f"Warning: Invalid article_type: {self.config['site'].get('article_type')}. "
                f"Must be one of: {', '.join(self.VALID_ARTICLE_TYPES)}. "
                f"Automatically using default: {self.ARTICLE_TYPE_ARTICLE}"
            )
            self.config["site"]["article_type"] = self.ARTICLE_TYPE_ARTICLE

        default_lang = self.config["site"].get("locale")
        try:
            locale.setlocale(locale.LC_TIME, default_lang)
        except locale.Error:
            try:
                locale.setlocale(locale.LC_TIME, f"{default_lang}.UTF-8")
            except locale.Error:
                try:
                    locale.setlocale(locale.LC_TIME, f"{default_lang}.utf8")
                except locale.Error:
                    locale.setlocale(locale.LC_TIME, "")

        # Setup Jinja2 template environment
        templates_dir = self.project_dir / "templates"
        self.jinja_env = Environment(
            loader=FileSystemLoader(str(templates_dir)), autoescape=select_autoescape()
        )

        # Setup Markdown converter
        self.md = markdown.Markdown(
            extensions=[
                "fenced_code",
                "def_list",
                "pymdownx.tasklist",
                "pymdownx.superfences",
                "pymdownx.fancylists",
                "pymdownx.saneheaders",
                "toc",
            ]
        )
        self.md_parser = MarkdownIt("commonmark")

    def run(self):
        """Entry point for static site generation."""

        content_dir = Path(self.config["paths"]["content"])
        output_dir = Path(self.config["paths"]["output"])
        drafts_dir = content_dir / self.config["paths"]["drafts"]

        # Clean and create output directory
        if output_dir.exists():
            shutil.rmtree(output_dir)
        output_dir.mkdir(parents=True)

        # Create posts directory
        posts_dir = output_dir / "posts"
        posts_dir.mkdir(exist_ok=True)

        # Process all posts
        posts = []
        for md_file in content_dir.rglob("*.md"):
            # Skip draft files
            if drafts_dir in md_file.parents:  #
                print(f"Skipping draft: {md_file.relative_to(content_dir)}")
                continue

            # Process post data.
            post_data = self.build_post_data(md_file)
            posts.append(post_data)

            # Render post page
            template = self.jinja_env.get_template("post.html")
            html = template.render(
                site={
                    **self.config["site"],
                },
                page={
                    "lang": post_data["lang"],
                    "description": post_data["description"],
                    "keywords": post_data["keywords"],
                    "title": post_data["title"],
                },
                post=post_data,
                x_card_html=post_data["x_card_html"],
                canonical_link_html=post_data["canonical_link_html"],
            )

            # Save post page
            output_file = output_dir / post_data["file_path"].lstrip("/")
            output_file.parent.mkdir(exist_ok=True)
            output_file.write_text(html, encoding="utf-8")

        # Generate index page
        self.generate_index(posts, output_dir)

        # Generate about page
        self.generate_about(output_dir)

        # Generate sitemap
        self.generate_sitemap(posts, output_dir)

        # Copy static files
        self.copy_public_files()

        print(f"Site generation completed! Processed {len(posts)} posts.")

    def build_post_data(self, file_path: Path) -> dict:
        """Build a post data dictionary from a Markdown file."""

        # Get language
        file_stem = file_path.stem
        lang_parts = file_stem.split(".")
        lang = lang_parts[-1] if len(lang_parts) > 1 else self.config["site"]["locale"]

        # Load post.md content
        post = frontmatter.load(str(file_path), disable_yaml_loader=True)

        # Convert markdown to html
        html_content = self.md.convert(post.content)

        # Get title
        title = post.metadata.get("title", "Untitled")

        # Slug
        slug_source = None
        if post.metadata.get("slug") and post.metadata["slug"].strip():
            slug_source = post.metadata["slug"]
        elif post.metadata.get("title") and post.metadata["title"].strip():
            slug_source = post.metadata["title"]
        else:
            slug_source = self.config["name"].get("name", "untitled")
        slug = slugify(slug_source)

        created = (
            str(post.metadata.get("created", ""))
            if post.metadata.get("created")
            else ""
        )
        updated = (
            str(post.metadata.get("updated", ""))
            if post.metadata.get("updated")
            else ""
        )

        created_data = self.parse_datetime(created, lang)
        updated_data = self.parse_datetime(updated, lang)
        schema_article = {
            "@context": "https://schema.org",
            "@type": self.config["site"].get("article_type"),
            "headline": title,
        }

        author = []
        if self.config["site"].get("author", ""):
            author.append({"@type": "Person", "name": self.config["site"]["author"]})

        if author:
            schema_article["author"] = author
        if created_data["iso"]:
            schema_article["datePublished"] = created_data["iso"]
        if updated_data["iso"]:
            schema_article["dateModified"] = updated_data["iso"]

        description = post.metadata.get("description", "")
        if not description:
            text_content = self.get_plain_text(post.content)
            if len(text_content) > 157:
                description = text_content[:157] + "..."
            else:
                description = text_content[:160]

        path = f"/posts/{slug}"
        return {
            "content": html_content,
            "title": title,
            "created": created_data["original"],
            "updated": updated_data["original"],
            "created_humanized": created_data["humanized"],
            "updated_humanized": updated_data["humanized"],
            "created_iso": created_data["iso"],
            "updated_iso": updated_data["iso"],
            "url": path,
            "file_path": f"{path}.html",
            "lang": lang,
            "description": description,
            "keywords": post.metadata.get("keywords", []),
            "schema_article": json.dumps(schema_article, ensure_ascii=False),
            "x_card_html": self.generate_x_card(
                card_type=self.X_CARD_TYPE_SUMMARY,
                title=title,
                description=description,
            ),
            "canonical_link_html": self.generate_canonical_link(
                path=path,
            ),
        }

    def generate_index(self, posts: list, output_dir: Path):
        """Generate index page"""
        sorted_posts = posts

        sort_by = self.config["site"].get("sort_by")
        if sort_by:
            sorted_posts = sorted(
                posts,
                key=lambda x: str(x.get(sort_by)) if x.get(sort_by) is not None else "",
                reverse=True,
            )

        template = self.jinja_env.get_template("index.html")
        html = template.render(
            site={**self.config["site"]},
            posts=sorted_posts,
            schema_site_name=self.generate_schema_site_name(),
            x_card_html=self.generate_x_card(
                card_type=self.X_CARD_TYPE_SUMMARY,
                title=self.config["site"]["name"],
                description=self.config["site"]["description"],
            ),
            canonical_link_html=self.generate_canonical_link(
                path="/",
            ),
        )

        output_file = output_dir / "index.html"
        output_file.write_text(html, encoding="utf-8")

    def generate_about(self, output_dir: Path):
        """Generate about page"""

        if self.config["site"]["about"].get("name", ""):
            schema_profile_page = {
                "@context": "https://schema.org",
                "@type": "ProfilePage",
                "mainEntity": {
                    "@type": self.config["site"]["about"].get("type"),
                    "name": self.config["site"]["about"].get("name"),
                },
            }

            if self.config["site"]["about"].get("alternate_name"):
                schema_profile_page["mainEntity"]["alternateName"] = self.config[
                    "site"
                ]["about"]["alternate_name"]

            if self.config["site"]["about"].get("description"):
                schema_profile_page["mainEntity"]["description"] = self.config["site"][
                    "about"
                ].get("description")

            if self.config["site"]["about"].get("same_as"):
                same_as = self.config["site"]["about"].get("same_as")
                schema_profile_page["mainEntity"]["sameAs"] = (
                    [same_as] if isinstance(same_as, str) else same_as
                )
        else:
            schema_profile_page = {}

        template = self.jinja_env.get_template("about.html")
        html = template.render(
            site={**self.config["site"]},
            page={
                "title": "About",
                "description": "About me",
                "keywords": ["About", "Bio"],
            },
            projects=self.config.get("projects", []),
            x_card_html=self.generate_x_card(
                card_type=self.X_CARD_TYPE_SUMMARY,
                title="About",
                description="About me",
            ),
            canonical_link_html=self.generate_canonical_link(
                path="/about",
            ),
            schema_profile_page=json.dumps(schema_profile_page, ensure_ascii=False),
        )

        output_file = output_dir / "about.html"
        output_file.write_text(html, encoding="utf-8")

    def generate_sitemap(self, posts: list, output_dir: Path):
        """Generate sitemap"""

        # Create root element, add namespace
        urlset = ET.Element("urlset")
        urlset.set("xmlns", "http://www.sitemaps.org/schemas/sitemap/0.9")

        # Add home page
        url = ET.SubElement(urlset, "url")
        loc = ET.SubElement(url, "loc")
        loc.text = self.config["site"]["url"]

        # Add all posts
        for post in posts:
            url = ET.SubElement(urlset, "url")
            loc = ET.SubElement(url, "loc")
            loc.text = self.config["site"]["url"] + post["url"]
            # last modified
            if post["updated_iso"]:
                lastmod = ET.SubElement(url, "lastmod")
                lastmod.text = post["updated_iso"]
            elif post["created_iso"]:
                lastmod = ET.SubElement(url, "lastmod")
                lastmod.text = post["created_iso"]

        # Add about page
        url = ET.SubElement(urlset, "url")
        loc = ET.SubElement(url, "loc")
        loc.text = self.config["site"]["url"] + "/about"

        # Write to file, add XML declaration and correct indentation
        output_file = output_dir / "sitemap.xml"
        xml_str = minidom.parseString(
            ET.tostring(urlset, encoding="utf-8")
        ).toprettyxml(indent="  ", encoding="utf-8")
        output_file.write_bytes(xml_str)

    def generate_schema_site_name(self):
        """Generate schema site name"""
        site_name = self.config["site"].get("name").strip()
        site_url = self.config["site"].get("url").strip()

        if site_name and site_url:
            schema_site_name = {
                "@context": "https://schema.org",
                "@type": "WebSite",
                "name": site_name,
            }
            site_alternate_name = self.config["site"].get("alternate_name")
            if site_alternate_name:
                schema_site_name["alternateName"] = site_alternate_name
            schema_site_name["url"] = site_url.rstrip("/") + "/"
            return json.dumps(schema_site_name, ensure_ascii=False)
        return None

    def generate_x_card(self, card_type, title, description):
        """Generate X card"""
        processed_title = title
        if len(title) > 70:
            processed_title = title[:67] + "..."

        processed_description = description
        if len(description) > 200:
            processed_description = description[:197] + "..."

        x_account = self.config["site"]["socials"].get("x", "")
        template = self.jinja_env.get_template("components/x_card.html")
        html = template.render(
            x_card={
                "card_type": card_type,
                "site": x_account,
                "title": processed_title,
                "description": processed_description,
            }
        )
        return html

    def generate_canonical_link(self, path: str) -> str:
        """Generate canonical link"""
        site_url = self.config["site"].get("url", "")
        if not site_url:
            return ""

        url = site_url.rstrip("/") + "/" + path.lstrip("/")
        return f'<link rel="canonical" href="{url}">'

    def copy_public_files(self):
        """Copy static files"""

        def ignore_files(_, names):
            return [
                n
                for n in names
                if n.startswith(".DS_Store") or n.endswith((".swp", ".swo"))
            ]

        public_dir = self.project_dir / self.config["paths"]["public"]
        output_dir = self.project_dir / self.config["paths"]["output"]

        shutil.copytree(public_dir, output_dir, dirs_exist_ok=True, ignore=ignore_files)

    def parse_datetime(self, date_str: str, lang: str = None) -> dict:
        """
        Parse datetime string and return various formatted versions.
        """
        result = {
            "original": date_str,
            "datetime": None,
            "iso": "",
            "humanized": date_str,
        }

        if not date_str:
            return result

        try:
            try:
                dt = arrow.get(date_str)
            except (ValueError, TypeError):
                formats = ["%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%d"]
                for fmt in formats:
                    try:
                        parsed = datetime.strptime(date_str, fmt)
                        dt = arrow.get(parsed)
                        break
                    except ValueError:
                        continue
                else:
                    return result

            dt = dt.to(self.config["site"]["timezone"])
            result["datetime"] = dt.datetime

            if " " in date_str:
                base = date_str.replace(" ", "T")
                result["iso"] = f"{base}{dt.format('Z')}"
            elif "T" in date_str:  # ISO 格式
                if "+" in date_str or "-" in date_str[10:]:
                    result["iso"] = date_str
                else:
                    result["iso"] = f"{date_str}{dt.format('Z')}"
            else:
                result["iso"] = f"{date_str}{dt.format('Z')}"

            now = arrow.now(self.config["site"]["timezone"])
            if (now - dt).days <= 30:
                locale_to_use = lang or self.config["site"].get("locale")
                try:
                    result["humanized"] = dt.humanize(locale=locale_to_use.lower())
                except (ValueError, NotImplementedError):
                    result["humanized"] = date_str
            else:
                result["humanized"] = date_str

        except (ValueError, TypeError):
            pass
        return result

    def get_plain_text(self, markdown_content: str) -> str:
        """Get plain text from markdown content"""
        tokens = self.md_parser.parse(markdown_content)
        text_content = []
        for token in tokens:
            if token.type == "inline":
                text_content.append(token.content)
        return " ".join(" ".join(text_content).split())


if __name__ == "__main__":
    MarkdownSiteGenerator().run()
