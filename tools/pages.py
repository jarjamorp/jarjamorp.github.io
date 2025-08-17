from pathlib import Path
from datetime import datetime
from jinja2 import Environment, FileSystemLoader, select_autoescape

def make_env(templates_dir: Path) -> Environment:
    return Environment(
        loader=FileSystemLoader(str(templates_dir)),
        autoescape=select_autoescape(["html"])
    )

def render_to_file(env: Environment, template_name: str, context: dict, out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    html = env.get_template(template_name).render(**context)
    tmp = out_path.with_suffix(out_path.suffix + ".tmp")
    tmp.write_text(html, encoding="utf-8")
    tmp.replace(out_path)

def build_index(cfg: dict) -> Path:
    env = make_env(Path(cfg["paths"]["templates"]))
    out = Path(cfg["paths"]["output"]) / "index.html"
    ctx = {
        "site_title": cfg.get("site_title", "My Site"),
        "build_time": datetime.now().isoformat(timespec="seconds"),
    }
    render_to_file(env, "index.html", ctx, out)
    return out
