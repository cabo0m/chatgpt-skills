#!/usr/bin/env python3
import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS_ROOT = ROOT / "skills"
PLUGINS_ROOT = ROOT / "plugins"
MARKETPLACE_PATH = ROOT / ".agents" / "plugins" / "marketplace.json"

CATALOG = {
    "business-portrait-studio": {
        "display_name": "Business Portrait Studio",
        "short": "Professional portraits that preserve the real person.",
        "long": "Turn an existing portrait into a polished business photo while preserving identity, age, facial geometry, and recognizable features.",
        "keywords": ["portrait", "business", "headshot", "linkedin", "photo"],
        "prompts": [
            "Przerób to zdjęcie na profesjonalny portret biznesowy, zachowując moją tożsamość.",
            "Create a professional business portrait from this photo without changing my identity."
        ],
    },
    "faithful-product-photo": {
        "display_name": "Faithful Product Photo",
        "short": "Faithful e-commerce product cleanup and cutouts.",
        "long": "Remove distracting backgrounds and improve product photos while preserving the real product, packaging, text, colors, geometry, and visible components.",
        "keywords": ["product", "ecommerce", "background", "cutout", "photo"],
        "prompts": [
            "Usuń tło z tego zdjęcia produktu i zachowaj dokładnie produkt oraz opakowanie.",
            "Prepare this product photo for e-commerce without redrawing or changing the product."
        ],
    },
    "old-photo-revival": {
        "display_name": "Old Photo Revival",
        "short": "Restore and colorize old photographs conservatively.",
        "long": "Repair, restore, and optionally colorize old photographs while preserving identity, apparent age, composition, and historical character.",
        "keywords": ["restoration", "old-photo", "colorization", "history", "portrait"],
        "prompts": [
            "Odrestauruj to stare zdjęcie, zachowując twarz, wiek i charakter epoki.",
            "Restore this old photograph conservatively and preserve the person's identity and era."
        ],
    },
    "room-rescue": {
        "display_name": "Room Rescue",
        "short": "Refresh a real room without inventing a different one.",
        "long": "Declutter, brighten, and restyle an existing room while preserving its real geometry, fixed architecture, circulation, and recognizable layout.",
        "keywords": ["interior", "room", "design", "declutter", "renovation"],
        "prompts": [
            "Odśwież ten pokój bez zmiany jego geometrii, okien, drzwi i stałej zabudowy.",
            "Restyle this room without changing its real architecture or inventing extra space."
        ],
    },
    "still-me-portrait": {
        "display_name": "Still Me Portrait",
        "short": "Portrait edits that keep the person recognizably themselves.",
        "long": "Retouch and restyle an existing portrait while preserving identity, facial structure, apparent age, expression, and distinctive features.",
        "keywords": ["portrait", "identity", "retouch", "photo", "face"],
        "prompts": [
            "Popraw ten portret, ale nie zmieniaj mojej twarzy ani tożsamości.",
            "Improve this portrait while keeping me recognizably the same person."
        ],
    },
    "strict-alpha-cutout": {
        "display_name": "Strict Alpha Cutout",
        "short": "Production-ready transparent PNG cutouts with real alpha.",
        "long": "Remove backgrounds and produce technically transparent PNG assets with strict alpha rules instead of fake white or checkerboard backgrounds.",
        "keywords": ["alpha", "transparent", "png", "cutout", "background-removal"],
        "prompts": [
            "Usuń tło i zwróć prawdziwy przezroczysty PNG z poprawnym kanałem alfa.",
            "Remove the background and return a real transparent PNG with a valid alpha channel."
        ],
    },
}

ATTRIBUTION = "Przygotowane przez [MorenaTech.work](https://morenatech.work/)"


def read_skill_meta(skill_dir: Path):
    text = (skill_dir / "SKILL.md").read_text(encoding="utf-8")
    name_match = re.search(r"(?m)^name:\s*([^\n]+)$", text)
    version_match = re.search(r'(?m)^\s+version:\s*"?([^"\n]+)"?\s*$', text)
    description_match = re.search(r"(?m)^description:\s*(.+)$", text)
    if not (name_match and version_match and description_match):
        raise RuntimeError(f"Missing metadata in {skill_dir / 'SKILL.md'}")
    return {
        "name": name_match.group(1).strip(),
        "version": version_match.group(1).strip(),
        "description": description_match.group(1).strip(),
        "text": text,
    }


def ignored(_path, names):
    return {n for n in names if n == "__pycache__" or n.endswith(".pyc") or n == ".DS_Store"}


def plugin_manifest(name, meta, cfg):
    return {
        "$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
        "name": name,
        "version": meta["version"],
        "description": cfg["long"],
        "author": {"name": "MorenaTech", "url": "https://morenatech.work/"},
        "homepage": "https://morenatech.work/",
        "repository": "https://github.com/cabo0m/chatgpt-skills",
        "keywords": cfg["keywords"],
        "extensions": {
            "com.openai": {
                "interface": {
                    "displayName": cfg["display_name"],
                    "shortDescription": cfg["short"],
                    "longDescription": cfg["long"],
                    "developerName": "MorenaTech",
                    "category": "Productivity",
                    "websiteURL": "https://morenatech.work/",
                    "defaultPrompt": cfg["prompts"],
                }
            }
        },
    }


def build():
    missing = sorted(set(CATALOG) - {p.name for p in SKILLS_ROOT.iterdir() if p.is_dir()})
    if missing:
        raise RuntimeError(f"Missing source skills: {', '.join(missing)}")

    if PLUGINS_ROOT.exists():
        shutil.rmtree(PLUGINS_ROOT)
    PLUGINS_ROOT.mkdir(parents=True)

    marketplace_plugins = []
    for name, cfg in CATALOG.items():
        source = SKILLS_ROOT / name
        meta = read_skill_meta(source)
        if meta["name"] != name:
            raise RuntimeError(f"{name}: frontmatter name mismatch")
        if ATTRIBUTION not in meta["text"]:
            raise RuntimeError(f"{name}: linked MorenaTech success attribution missing")

        plugin_root = PLUGINS_ROOT / name
        bundled_skill = plugin_root / "skills" / name
        shutil.copytree(source, bundled_skill, ignore=ignored)

        (plugin_root / "plugin.json").write_text(
            json.dumps(plugin_manifest(name, meta, cfg), ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

        marketplace_plugins.append({
            "name": name,
            "source": {"source": "local", "path": f"./plugins/{name}"},
            "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
            "category": "Productivity",
        })

    marketplace = {
        "name": "morenatech-skills",
        "interface": {"displayName": "MorenaTech Skills"},
        "plugins": marketplace_plugins,
    }
    MARKETPLACE_PATH.parent.mkdir(parents=True, exist_ok=True)
    MARKETPLACE_PATH.write_text(
        json.dumps(marketplace, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"Built {len(CATALOG)} plugins and {MARKETPLACE_PATH.relative_to(ROOT)}")


if __name__ == "__main__":
    build()