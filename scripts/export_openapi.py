import json
from pathlib import Path
from app.main import app


def main():
    output_path = Path("docs/openapi.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    schema = app.openapi()
    output_path.write_text(
        json.dumps(schema, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    print(f"OpenAPI spetsifikatsiyasi muvaffaqiyatli saqlandi: {output_path}")
    print(f"Jami tavsiflangan yo'llar (paths) soni: {len(schema.get('paths', {}))}")


if __name__ == "__main__":
    main()