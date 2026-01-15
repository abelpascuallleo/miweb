import os
import shutil
from pathlib import Path

import markdown as md
from jinja2 import Environment, FileSystemLoader


PROJECT_ROOT = Path(__file__).parent
TEMPLATES_DIR = PROJECT_ROOT / "templates"
STATIC_DIR = PROJECT_ROOT / "static"
MARKDOWN_DIR = PROJECT_ROOT / "markdown"
OUTPUT_DIR = PROJECT_ROOT / "docs"


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def copy_static() -> None:
    dest = OUTPUT_DIR / "static"
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(STATIC_DIR, dest)


def make_nojekyll() -> None:
    (OUTPUT_DIR / ".nojekyll").write_text("")


def build_pages(env: Environment) -> None:
    # Utilidad de url_for para plantillas estáticas
    def url_for(endpoint: str, **values) -> str:
        if endpoint == "static":
            filename = values.get("filename", "")
            return f"static/{filename}"
        if endpoint == "proyectos":
            return "proyectos.html"
        if endpoint == "contacto":
            return "contacto.html"
        if endpoint == "mostrar_post":
            nombre = values.get("nombre")
            return f"posts/{nombre}.html"
        if endpoint == "inicio":
            return "index.html"
        # Fallback
        return "#"

    posts = get_posts()
    context = {"url_for": url_for, "posts": posts}

    # Render páginas principales
    for template_name in ["index.html", "proyectos.html", "contacto.html"]:
        template = env.get_template(template_name)
        if template_name == "index.html":
            html = template.render(**context)
        else:
            html = template.render(url_for=url_for)
        (OUTPUT_DIR / template_name).write_text(html, encoding="utf-8")


def build_posts() -> None:
    posts_out = OUTPUT_DIR / "posts"
    ensure_dir(posts_out)

    for md_file in sorted(MARKDOWN_DIR.glob("*.md")):
        nombre = md_file.stem
        contenido_md = md_file.read_text(encoding="utf-8")
        contenido_html = md.markdown(contenido_md)

        page_html = f"""
<!DOCTYPE html>
<html lang=\"es\">
<head>
  <meta charset=\"utf-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
  <title>{nombre}</title>
  <style>
    body {{
      background-color: #ffffff;
      color: #1f2937;
      font-family: system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
      line-height: 1.6;
      max-width: 700px;
      margin: 0 auto;
      padding: 2rem 1rem;
    }}
    a {{ color: #2563eb; text-decoration: none; font-weight: 500; }}
    a:hover {{ text-decoration: underline; color: #1d4ed8; }}
    h1, h2, h3, h4, h5, h6 {{ color: #111827; margin-top: 2em; margin-bottom: 0.75em; font-weight: 700; line-height: 1.2; }}
    h1 {{ font-size: 2.25rem; margin-top: 0.5em; }}
    hr {{ border: 0; border-top: 1px solid #e5e7eb; margin: 3rem 0; }}
    img {{ max-width: 100%; height: auto; border-radius: 0.5rem; }}
    pre {{ background: #1f2937; color: #f9fafb; padding: 1.25rem; border-radius: 0.5rem; overflow-x: auto; }}
    code {{ background: #f3f4f6; padding: 0.2em 0.4em; border-radius: 0.25rem; font-family: monospace; font-size: 0.9em; }}
    pre code {{ background: transparent; padding: 0; color: inherit; }}
    blockquote {{ border-left: 4px solid #e5e7eb; padding-left: 1rem; color: #4b5563; font-style: italic; }}
  </style>
  <link rel=\"preconnect\" href=\"https://fonts.googleapis.com\" />
  <link rel=\"preconnect\" href=\"https://fonts.gstatic.com\" crossorigin />
  <link rel=\"stylesheet\" href=\"../static/styles.css\" />
  <link rel=\"icon\" href=\"data:,\" />
  <meta name=\"robots\" content=\"noindex\" />
  </head>
<body>
  {contenido_html}
</body>
</html>
"""
        (posts_out / f"{nombre}.html").write_text(page_html, encoding="utf-8")


def get_posts():
    posts = []
    for md_file in sorted(MARKDOWN_DIR.glob("*.md")):
        nombre = md_file.stem
        contenido_md = md_file.read_text(encoding="utf-8")
        contenido_html = md.markdown(contenido_md)
        posts.append({"nombre": nombre, "contenido_html": contenido_html})
    return posts


def main() -> None:
    ensure_dir(OUTPUT_DIR)
    env = Environment(loader=FileSystemLoader(str(TEMPLATES_DIR)))
    copy_static()
    make_nojekyll()
    build_pages(env)
    build_posts()
    print(f"Sitio estático generado en: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
