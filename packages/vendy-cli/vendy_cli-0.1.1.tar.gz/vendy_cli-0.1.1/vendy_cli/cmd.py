import typer
from typing_extensions import Annotated
import yaml
from pathlib import Path
from cookiecutter.main import cookiecutter
from rich.console import Console
from rich.table import Table

app = typer.Typer()
home = Path.home()
console = Console()


def get_template_loc(name: str) -> str:
    with open(f"{home}/.vendy/config.yaml") as stream:
        try:
            templates = yaml.safe_load(stream)
            for template in templates["templates"]:
                if name == template["name"]:
                    return template["path"], template["version"]
            return None
        except yaml.YAMLError as exc:
            print(exc)


@app.command("list", help="List install templates.(also 'ls')")
@app.command("ls", hidden=True)
def list():
    table = Table(title="Configured Templates")
    table.add_column("Name")
    table.add_column("Version")
    table.add_column("Path")
    with open(f"{home}/.vendy/config.yaml") as stream:
        try:
            templates = yaml.safe_load(stream)
            for template in templates["templates"]:
                table.add_row(template["name"], template["version"], template["path"])
        except yaml.YAMLError as exc:
            print(exc)

    console.print(table)


@app.command("add", help="Add a new template")
def add(name: str, path: str, version: Annotated[str, typer.Argument()] = "main"):
    config_file = Path(f"{home}/.vendy/config.yaml")
    entry = {"name": name, "path": path, "version": version}

    if config_file.exists():
        with open(f"{home}/.vendy/config.yaml") as conf_file:
            config = yaml.safe_load(conf_file)
            if entry not in config["templates"]:
                config["templates"].append(entry)
                with open(f"{home}/.vendy/config.yaml", "w") as conf_file_new:
                    yaml.dump(config, conf_file_new)
            else:
                print("Item Already Configured")
    else:
        config = {"templates": []}
        config["templates"].append(entry)
        with open(f"{home}/.vendy/config.yaml", "w") as conf_file:
            yaml.dump(config, conf_file)

    table = Table(title="Added Template")
    table.add_column("Name")
    table.add_column("Version")
    table.add_column("Path")
    table.add_row(entry["name"], entry["version"], entry["path"])
    console.print(table)


@app.command("remove", help="Remove a template. (also 'rm')")
@app.command("rm", hidden=True)
def remove(name: str):
    config_file = Path(f"{home}/.vendy/config.yaml")
    if config_file.exists():
        with open(f"{home}/.vendy/config.yaml") as conf_file:
            config = yaml.safe_load(conf_file)
            conf_file.close()
            config["templates"] = [
                template
                for template in config["templates"]
                if template.get("name") != name
            ]
            with open(f"{home}/.vendy/config.yaml", "w") as conf_file:
                yaml.dump(config, conf_file)


@app.command("deploy", help="Deploy a new instance of a given template")
def deploy(name: str):
    print(f"Deploying {name}: ")
    path, version = get_template_loc(name)
    cookiecutter(path, checkout=version)


def main():
    app()


if __name__ == "__main__":
    main()
