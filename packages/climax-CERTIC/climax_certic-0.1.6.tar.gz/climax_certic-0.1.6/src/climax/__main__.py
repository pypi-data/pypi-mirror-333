import subprocess
from pathlib import Path
from typing import Optional, Union, Dict
from typing_extensions import Annotated
import gettext

locales_dir = Path(__file__).parent / "locales"
gettext.bindtextdomain("messages", str(locales_dir))
gettext.textdomain("messages")
_ = gettext.gettext

from bs4 import BeautifulSoup  # noqa: E402
from .eggs import get_yolk  # noqa: E402
import geler  # noqa: E402
import requests  # noqa: E402
import os  # noqa: E402
import hashlib  # noqa: E402
import platform  # noqa: E402
import typer  # noqa: E402
from rich import print  # noqa: E402
from rich.progress import track  # noqa: E402
from rich.console import Console  # noqa: E402
from rich.table import Table  # noqa: E402
import shutil  # noqa: E402
from functools import lru_cache  # noqa: E402
import socket  # noqa: E402


WELCOME_PAGE = """
<h1>Bienvenue dans MaX !</h1>
<p>
    Vous pouvez personnaliser cette page en éditant le fichier content_html/fr/index.html
</p>
<p>
    Retrouvez la documentation de MaX à l'adresse suivante: 
    <a href="https://pdn-certic.pages.unicaen.fr/max-documentation/">
        https://pdn-certic.pages.unicaen.fr/max-documentation/
    </a>
</p>
"""

USER_MAX_DIR = os.getenv("CLIMAX_HOME") or Path(Path.home(), ".climax")
USER_MAX_DIR = Path(USER_MAX_DIR)
USER_MAX_DIR.mkdir(exist_ok=True)
CACHE_DIR = Path(USER_MAX_DIR, "cache")
CACHE_DIR.mkdir(exist_ok=True)
MAX_CONFIG_FILE = "config.xml"
BASEX_DISTRO = "https://files.basex.org/releases/11.1/BaseX111.zip"
SAXON_DISTRO = (
    "https://repo1.maven.org/maven2/net/sf/saxon/Saxon-HE/10.8/Saxon-HE-10.8.jar"
)

MAX_DISTRO = "https://git.unicaen.fr/pdn-certic/max-v2/-/archive/0.0.2-alpha/max-v2-0.0.2-alpha.zip"


CURRENT_MAX_DISTRO_DIR = os.path.splitext(os.path.basename(MAX_DISTRO))[0]
JAVA_DISTROS = {
    "darwin/arm64": "https://download.java.net/java/GA/jdk22.0.2/c9ecb94cd31b495da20a27d4581645e8/9/GPL/openjdk-22.0.2_macos-aarch64_bin.tar.gz",
    "linux/x86_64": "https://download.java.net/java/GA/jdk22.0.2/c9ecb94cd31b495da20a27d4581645e8/9/GPL/openjdk-22.0.2_linux-x64_bin.tar.gz",
    "windows/amd64": "https://download.java.net/java/GA/jdk22.0.2/c9ecb94cd31b495da20a27d4581645e8/9/GPL/openjdk-22.0.2_windows-x64_bin.zip",
}
WEB_PORT = 8080
WEB_HOST = "localhost"
BASEX_PORT = 1984
STOP_PORT = 8081
CONFIG_INIT_TEMPLATE = """<?xml version="1.0" encoding="UTF-8"?>
<configuration xmlns="http://certic.unicaen.fr/max/ns/1.0" env="dev" vocabulary-bundle="max-dumb-xml">
    <languages>
        <language>fr</language>
        <language>en</language>
    </languages>
    <title>mon Corpus Numérique</title>
    <bundles>    
        <bundle name="max-dumb-xml"/>
        <bundle name="max-export"/>
        <bundle name="max-dev"/>
    </bundles>
</configuration>
"""


def _free_port() -> int:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("localhost", 0))
    port = s.getsockname()[1]
    s.close()
    return port


class MaXProjectConfig:
    def __init__(self, path_to_config_file: Union[str, Path]):
        self.config_file_path = Path(path_to_config_file).resolve()
        if os.path.isfile(self.config_file_path):
            with open(self.config_file_path, "r") as f:
                self.xml_soup = BeautifulSoup(f, "xml")
        else:
            self.xml_soup = BeautifulSoup(CONFIG_INIT_TEMPLATE, "xml")
        first = self.xml_soup.find()
        if first and first.name != "configuration":
            raise ValueError(
                _("{} is not a MaX configuration file").format(self.config_file_path)
            )
        conf = self.xml_soup.find("configuration")
        if not conf:
            conf = self.xml_soup.new_tag("configuration")
            conf["env"] = "dev"
            conf["vocabulary-bundle"] = "max-dumb-xml"
            conf["xmlns"] = "http://certic.unicaen.fr/max/ns/1.0"
            self.xml_soup.append(conf)

    @property
    def available_bundles(self) -> Dict[str, Dict]:
        active_bundles = self.bundles
        available_bundles = {}
        available_bundles_xml = Path(
            os.path.dirname(self.config_file_path),
            ".max",
            "resources",
            "available-bundles.xml",
        )
        if available_bundles_xml.is_file():
            with open(available_bundles_xml, "r") as file_handle:
                soup = BeautifulSoup(file_handle.read(), "xml")
                for b in soup.find_all("bundle"):
                    available_bundles[b["name"]] = {
                        "name": b["name"],
                        "url": b["url"] if b.has_attr("url") else "",
                        "description": b["description"]
                        if b.has_attr("description")
                        else "",
                        "active": b["name"] in active_bundles.keys(),
                        "vocabulary": True
                        if (
                            b.has_attr("vocabulary-bundle")
                            and b["vocabulary-bundle"] == "true"
                        )
                        else False,
                    }
        return dict(sorted(available_bundles.items()))

    @property
    def max_version(self) -> str:
        expath_pkg = Path(
            os.path.dirname(self.config_file_path),
            ".max",
            "resources",
            "expath-pkg.xml",
        )
        if expath_pkg.is_file():
            with open(expath_pkg, "r") as expath_handle:
                soup = BeautifulSoup(expath_handle.read(), "xml")
                package = soup.find("package")
                if package:
                    return package["version"]
        return ""

    @property
    def env(self) -> str:
        conf = self.xml_soup.find("configuration")
        val = conf.get("env", "dev")
        return str(val)

    @env.setter
    def env(self, value: str):
        conf = self.xml_soup.find("configuration")
        conf["env"] = value

    @property
    def vocabulary_bundle(self) -> str:
        conf = self.xml_soup.find("configuration")
        val = conf.get("vocabulary-bundle", "max-dumb-xml")
        return str(val)

    @vocabulary_bundle.setter
    def vocabulary_bundle(self, value):
        conf = self.xml_soup.find("configuration")
        conf["vocabulary-bundle"] = value

    @property
    def title(self) -> str:
        val = "untitled"
        conf = self.xml_soup.find("configuration")
        xml_node = conf.find("title")
        if xml_node:
            val = xml_node.text.strip()
        return str(val)

    @title.setter
    def title(self, value):
        conf = self.xml_soup.find("configuration")
        xml_node = conf.find("title")
        if not xml_node:
            xml_node = self.xml_soup.new_tag("title")
            conf.append(xml_node)
        xml_node.string = value

    @property
    def languages(self) -> list[str]:
        vals = []
        conf = self.xml_soup.find("configuration")
        nodes = conf.find("languages")
        if nodes:
            for language in nodes.find_all("language"):
                vals.append(language.text.strip())
        return vals

    @languages.setter
    def languages(self, languages: list[str]):
        conf = self.xml_soup.find("configuration")
        nodes = conf.find("languages")
        if not nodes:
            nodes = self.xml_soup.new_tag("languages")
            conf.append(nodes)
        nodes.clear()
        for language in languages:
            language_tag = self.xml_soup.new_tag("language")
            language_tag.string = language
            nodes.append(language_tag)

    @property
    def bundles(self) -> Dict[str, Dict]:
        vals = {}
        conf = self.xml_soup.find("configuration")
        nodes = conf.find("bundles")
        if nodes:
            for bundle in nodes.find_all("bundle"):
                vals[bundle["name"]] = {
                    "name": bundle["name"],
                    "url": bundle["url"] if bundle.has_attr("url") else "",
                }
        return vals

    @bundles.setter
    def bundles(self, bundles: Dict[str, Dict]):
        conf = self.xml_soup.find("configuration")
        nodes = conf.find("bundles")
        if not nodes:
            nodes = self.xml_soup.new_tag("languages")
            conf.append(nodes)
        nodes.clear()
        for bundle_name, bundle_dict in bundles.items():
            bundle_tag = self.xml_soup.new_tag("bundle")
            bundle_tag["name"] = bundle_dict["name"]
            if bundle_dict.get("url"):
                bundle_tag["url"] = bundle_dict["url"]
            nodes.append(bundle_tag)

    def __str__(self):
        return self.xml_soup.prettify()

    def write(self):
        with open(self.config_file_path, "w") as f:
            f.write(str(self))


@lru_cache()
def current_system() -> str:
    return f"{platform.system()}/{platform.machine()}".lower()


@lru_cache
def class_path_separator() -> str:
    separator = ":"
    current_os = current_system().split("/")[0]
    if current_os == "windows":
        separator = ";"
    return separator


@lru_cache
def cp_paths() -> str:
    basex_dir_path = Path(os.getcwd(), ".max", "basex")
    paths = class_path_separator().join([
        str(Path(basex_dir_path, "BaseX.jar")),
        str(Path(basex_dir_path, "lib", "custom", "*")),
        str(Path(basex_dir_path, "lib", "*")),
    ])
    return paths


@lru_cache()
def find_jdk(cur_sys: str = None) -> Optional[str]:
    if not cur_sys:
        cur_sys = current_system()
    return JAVA_DISTROS.get(cur_sys, None)


def dir_is_max(directory: Path = None) -> bool:
    if directory is None:
        directory = os.getcwd()
    directory = Path(directory)
    config_file = Path(directory, "config.xml")
    if config_file.exists():
        with open(config_file, "r") as f:
            soup = BeautifulSoup(f, "xml")
            conf = soup.find("configuration")
            if conf:
                ns = conf.get("xmlns")
                if ns == "http://certic.unicaen.fr/max/ns/1.0":
                    return True
    return False


def check_cwd_is_max():
    if not dir_is_max():
        print(
            "[red]{}[/red]".format(_("Le dossier n'est pas une installation de MaX."))
        )
        raise typer.Exit(code=1)


def max_config() -> MaXProjectConfig:
    return MaXProjectConfig(Path(os.getcwd(), MAX_CONFIG_FILE))


def unzip(source: Union[Path, str], destination: Union[Path, str]) -> bool:
    shutil.unpack_archive(source, destination)
    os.remove(source)
    return True


def cached_download(
    source: str, destination: Union[Path, str], chunk_size: int = 1024
) -> bool:
    cache_path = Path(CACHE_DIR, hashlib.sha1(source.encode("utf-8")).hexdigest())
    if cache_path.exists():
        shutil.copy(cache_path, destination)
    else:
        response = requests.get(source, stream=True)
        if response.status_code != 200:
            print("[red]{}[/red] {}".format(_("Impossible de télécharger"), source))
            raise typer.Exit(code=1)
        try:
            total_size = int(response.headers["Content-length"])
            seq_len = total_size // chunk_size
        except KeyError:
            # missing Content-length
            seq_len = 100
        with open(cache_path, "wb") as f:
            for data in track(
                response.iter_content(chunk_size=chunk_size),
                total=seq_len,
                description=os.path.basename(source),
            ):
                f.write(data)
        shutil.copy(cache_path, destination)
    return True


@lru_cache()
def ensure_java() -> Path:
    java_bin = shutil.which("java")
    if not java_bin:
        cur_sys = current_system()
        suitable_jdk = find_jdk(cur_sys)
        if suitable_jdk:
            destination_folder = Path(USER_MAX_DIR, "jdk")
            if not destination_folder.exists():
                destination_archive = Path(USER_MAX_DIR, os.path.basename(suitable_jdk))
                cached_download(suitable_jdk, destination_archive)
                unzip(destination_archive, destination_folder)
            if cur_sys in ["linux/x86_64", "linux/amd64"]:
                java_bin = Path(destination_folder, "jdk-22.0.2", "bin", "java")
            if cur_sys in ["windows/x86_64", "windows/amd64"]:
                java_bin = Path(destination_folder, "jdk-22.0.2", "bin", "java.exe")
            if cur_sys == "darwin/arm64":
                java_bin = Path(
                    destination_folder,
                    "jdk-22.0.2.jdk",
                    "Contents",
                    "Home",
                    "bin",
                    "java",
                )
    if not java_bin:
        print(
            "[red]"
            + _("Java est requis pour utiliser MaX: https://openjdk.org/install/")
            + "[/red]"
        )
        raise typer.Exit(code=1)
    return java_bin


def ensure_max_distro() -> Path:
    destination_folder = Path(USER_MAX_DIR, "max")
    if not destination_folder.exists():
        destination_archive = Path(USER_MAX_DIR, "max.zip")
        cached_download(MAX_DISTRO, destination_archive)
        unzip(destination_archive, destination_folder)
    return destination_folder


def ensure_available_max_directory(directory: Optional[Path]) -> tuple[Path, bool]:
    if not directory:
        directory = os.getcwd()
    directory = Path(directory)
    if not directory.exists():
        directory.mkdir(parents=True, exist_ok=False)
    directory = directory.resolve()
    is_empty = not any(directory.iterdir())
    is_max = dir_is_max(directory)
    if not is_empty and not is_max:
        print(
            "[red]{}[/red]".format(
                _(
                    "Le dossier n'est pas vide et n'est pas un projet MaX valide, veuillez en choisir un autre."
                )
            )
        )
        raise typer.Exit(code=1)
    return directory, is_max


app = typer.Typer(
    help=_("Utilitaire en ligne de commande pour la gestion des projets MaX")
)


def _sync_bundles(root_directory: Path):
    ignore_file = ".ignore"
    dot_max_dir = Path(root_directory, ".max")
    bundles_dir = Path(dot_max_dir, "basex", "webapp", "max", "bundles")
    # first deactivate everything
    for item in os.listdir(bundles_dir):
        if os.path.isdir(Path(bundles_dir, item)):
            Path(bundles_dir, item, ignore_file).touch()
    config = MaXProjectConfig(Path(root_directory, "config.xml"))
    # then activate or install what is in config file
    for bundle_name, bundle in config.bundles.items():
        bundle_dir = Path(bundles_dir, bundle_name)
        if os.path.isdir(bundle_dir):
            Path(bundle_dir, ignore_file).unlink(missing_ok=True)
        else:
            if str(bundle["url"]).startswith("http://") or str(
                bundle["url"]
            ).startswith("https://"):
                bundle_archive_path = Path(bundles_dir, f"{bundle_name}.zip")
                cached_download(bundle["url"], bundle_archive_path)
                shutil.unpack_archive(bundle_archive_path, bundles_dir)
                dir_name, _ = os.path.splitext(os.path.basename(bundle["url"]))
                Path(bundles_dir, dir_name).rename(bundle_dir)
                bundle_archive_path.unlink()
            if str(bundle["url"]).startswith("local://"):
                zip_name = str(bundle["url"]).lstrip("local://")
                bundle_archive_path = Path(
                    dot_max_dir, "resources", "local_bundles", f"{zip_name}"
                )
                shutil.unpack_archive(bundle_archive_path, bundles_dir)
                dir_name, _ = os.path.splitext(os.path.basename(bundle["url"]))
                Path(bundles_dir, dir_name).rename(bundle_dir)
                bundle_archive_path.unlink()


def _install_new_max_instance(root_directory: Path):
    print(
        "[bold]"
        + _("Initialisation d'une nouvelle instance de MaX dans {}").format(
            root_directory
        )
        + "[/bold]"
    )
    config_file_path = Path(root_directory, "config.xml")
    dot_max_dir = Path(root_directory, ".max")
    dot_max_dir.mkdir(parents=True, exist_ok=False)

    basex_zip_destination = Path(dot_max_dir, "BaseX.zip")
    cached_download(BASEX_DISTRO, basex_zip_destination)
    unzip(basex_zip_destination, dot_max_dir)
    saxon_zip_destination = Path(
        dot_max_dir, "basex", "lib", "custom", "Saxon-HE-10.8.jar"
    )
    cached_download(SAXON_DISTRO, saxon_zip_destination)

    with open(Path(root_directory, ".gitignore"), "w") as f:
        f.write(".max\n")

    shutil.copytree(
        Path(USER_MAX_DIR, "max", CURRENT_MAX_DISTRO_DIR, "src", "main", "core"),
        Path(dot_max_dir, "basex", "webapp", "max", "core"),
    )
    shutil.copytree(
        Path(USER_MAX_DIR, "max", CURRENT_MAX_DISTRO_DIR, "src", "main", "bundles"),
        Path(dot_max_dir, "basex", "webapp", "max", "bundles"),
    )

    shutil.copytree(
        Path(USER_MAX_DIR, "max", CURRENT_MAX_DISTRO_DIR, "src", "resources"),
        Path(dot_max_dir, "resources"),
    )

    shutil.copy(Path(dot_max_dir, "resources", "config.xml.sample"), config_file_path)

    _sync_bundles(root_directory)

    Path(root_directory, "content_html", "fr").mkdir(exist_ok=True, parents=True)
    welcome_page = Path(root_directory, "content_html", "fr", "index.html")
    with open(welcome_page, "w") as f:
        f.write(WELCOME_PAGE)

    print(
        "[bold]"
        + _("La nouvelle instance de MaX est prête dans {}").format(root_directory)
        + "[/bold]"
    )
    print(
        _(
            'Vous pouvez éventuellement installer un projet de démonstration avec "climax demo".'
        )
    )


def _sync_max_instance(root_directory: Path, verbose=True):
    if verbose:
        print(
            "[bold]"
            + _("Initialisation de l'instance de MaX existant dans {}").format(
                root_directory
            )
            + "[/bold]"
        )
    MaXProjectConfig(Path(root_directory, "config.xml"))
    dot_max_dir = Path(root_directory, ".max")
    if not os.path.isdir(dot_max_dir):
        dot_max_dir.mkdir(parents=True, exist_ok=True)
        basex_zip_destination = Path(dot_max_dir, "BaseX.zip")
        cached_download(BASEX_DISTRO, basex_zip_destination)
        unzip(basex_zip_destination, dot_max_dir)
        saxon_zip_destination = Path(
            dot_max_dir, "basex", "lib", "custom", "Saxon-HE-10.8.jar"
        )
        cached_download(SAXON_DISTRO, saxon_zip_destination)

        shutil.copytree(
            Path(USER_MAX_DIR, "max", CURRENT_MAX_DISTRO_DIR, "src", "main", "core"),
            Path(dot_max_dir, "basex", "webapp", "max", "core"),
        )
        shutil.copytree(
            Path(USER_MAX_DIR, "max", CURRENT_MAX_DISTRO_DIR, "src", "main", "bundles"),
            Path(dot_max_dir, "basex", "webapp", "max", "bundles"),
        )

        shutil.copytree(
            Path(USER_MAX_DIR, "max", CURRENT_MAX_DISTRO_DIR, "src", "resources"),
            Path(dot_max_dir, "resources"),
        )

    _sync_bundles(root_directory)
    if verbose:
        print(
            "[bold]"
            + _("L'instance de MaX est prête dans {}").format(root_directory)
            + "[/bold]"
        )


@app.command(help=_("Initialisation d'une instance existante de MaX"))
def sync(
    directory: Annotated[
        Optional[Path], typer.Argument(help=_("chemin vers un dossier"))
    ] = os.getcwd(),
):
    ensure_java()
    ensure_max_distro()
    root_directory, is_max = ensure_available_max_directory(directory)

    if is_max:
        _sync_max_instance(root_directory)
    else:
        print(
            _(
                "Le dossier ne contient pas une instance de MaX. Utiliser la commande new"
            )
        )
        raise typer.Exit()


@app.command(help=_("Création d'une nouvelle instance de MaX"))
def new(
    directory: Annotated[
        Optional[Path], typer.Argument(help=_("chemin vers un dossier"))
    ] = os.getcwd(),
):
    ensure_java()
    ensure_max_distro()
    root_directory, is_max = ensure_available_max_directory(directory)
    if is_max:
        print(_("Le dossier contient une instance de MaX. Utiliser la commande sync"))
        raise typer.Exit()
    else:
        _install_new_max_instance(root_directory)


@app.command(
    help=_("Installe une édition de démonstration dans l'instance de MaX en cours")
)
def demo():
    check_cwd_is_max()
    if typer.confirm(
        _("Voulez-vous installer une édition de démonstration ?"), default=False
    ):
        cur_dir = os.getcwd()

        shutil.copytree(  ## BaseX databases
            Path(USER_MAX_DIR, "max", CURRENT_MAX_DISTRO_DIR, "fixtures", "max"),
            Path(cur_dir, ".max", "basex", "data", "max"),
            dirs_exist_ok=True,
        )
        shutil.copytree(
            Path(
                USER_MAX_DIR, "max", CURRENT_MAX_DISTRO_DIR, "fixtures", "content_html"
            ),
            Path(cur_dir, "content_html"),
            dirs_exist_ok=True,
        )
        shutil.copytree(
            Path(USER_MAX_DIR, "max", CURRENT_MAX_DISTRO_DIR, "fixtures", "templates"),
            Path(cur_dir, "templates"),
            dirs_exist_ok=True,
        )
        shutil.copytree(
            Path(USER_MAX_DIR, "max", CURRENT_MAX_DISTRO_DIR, "fixtures", "autoroute"),
            Path(cur_dir, "autoroute"),
            dirs_exist_ok=True,
        )

        shutil.copy(
            Path(USER_MAX_DIR, "max", CURRENT_MAX_DISTRO_DIR, "fixtures", "config.xml"),
            Path(cur_dir, "config.xml"),
        )

        print("[green]" + _("édition de démonstration installée") + "[/green]")
        print(_("Vous pouvez démarrer MaX avec la commande [bold]climax start[/bold]"))


@app.command(help=_("Arrête l'instance de MaX du dossier en cours"))
def stop(http_stop_port: int = STOP_PORT):
    check_cwd_is_max()
    java_bin_path = ensure_java()
    process_args = [
        str(java_bin_path),
        "-cp",
        cp_paths(),
        "-Xmx2g",
        "org.basex.BaseXHTTP",
        f"-s{http_stop_port}",
        "stop",
    ]
    subprocess.run(process_args)


@app.command(help=_("Démarre l'instance de MaX du dossier en cours"))
def start(
    http_host: str = WEB_HOST,
    http_port: int = WEB_PORT,
    basex_port: int = BASEX_PORT,
    http_stop_port: int = STOP_PORT,
    service: Annotated[
        bool,
        typer.Option(
            help=_(
                'Démarrer MaX en tant que service. Utilisez "climax stop" pour arrêter le service.'
            )
        ),
    ] = False,
):
    check_cwd_is_max()
    java_bin_path = ensure_java()
    process_args = [
        str(java_bin_path),
        "-cp",
        cp_paths(),
        "-Xmx2g",
        "org.basex.BaseXHTTP",
        f"-p{basex_port}",
        f"-h{http_port}",
        f"-n{http_host}",
    ]
    if service:
        process_args.append("-S")
        process_args.append(f"-s{http_stop_port}")
    print(
        "[green]"
        + _("Démarrage de MaX sur http://{}:{}").format(http_host, http_port)
        + "[/green]"
    )
    subprocess.run(process_args)


@app.command(help=_("Efface le cache de climax"))
def cache_clear():
    for p in CACHE_DIR.iterdir():
        if p.is_file():
            p.unlink(missing_ok=True)
    shutil.rmtree(Path(USER_MAX_DIR, "max"), ignore_errors=True)


@app.command(help=_("Affiche la configuration de MaX"))
def config():
    check_cwd_is_max()
    config = max_config()
    print(f"MaX version: {config.max_version}\n")
    print("Project configuration:\n")
    print(max_config())


@app.command(help=_("Fait une copie HTML statique du projet dans le dossier"))
def freeze(
    directory: Annotated[
        Optional[Path], typer.Argument(help=_("chemin vers un dossier"))
    ] = Path(os.getcwd(), "output"),
    debug: bool = False,
):
    max_config()
    # start server on specific port
    port_number = _free_port()
    stop_port = port_number + 1
    start(WEB_HOST, port_number, http_stop_port=stop_port, service=True)
    # copy website
    try:
        # for lang in config.languages:
        # start_url = f"http://localhost:{port_number}/{lang}/tdm.html"
        start_url = f"http://localhost:{port_number}/"
        geler.freeze(start_url, directory)
    except Exception as e:
        stop(stop_port)
        raise e
    # stop server
    stop(stop_port)
    print("[green]" + _("Site copié dans {}").format(str(directory)) + "[/green]")


@app.command(help=_("Supprime un bundle pour l'instance de Max en cours"))
def bundles_remove(bundle_name: str):
    check_cwd_is_max()
    config = max_config()
    keep_bundles = {}
    bundle_name = bundle_name.lower().strip()
    if bundle_name not in config.bundles.keys():
        print(_("[red]{} n'est pas un bundle actif[/red]").format(bundle_name))
        raise typer.Exit(code=1)
    for active_bundle_name, active_bundle_url in config.bundles.items():
        if active_bundle_name.strip() != bundle_name.strip():
            keep_bundles[active_bundle_name] = active_bundle_url
    config.bundles = keep_bundles
    config.write()
    bundles_list()


@app.command(help=_("Liste les bundles disponibles"))
def bundles_list():
    check_cwd_is_max()
    config = max_config()
    console = Console()
    table = Table(_("Nom"), _("Installé"), _("Description"), show_lines=True)
    bundles_done = {}

    for bundle_name, bundle in config.available_bundles.items():
        bundles_done[bundle_name] = [
            "[bold]{}[/bold]".format(bundle["name"]),
            "[green]{}[/green]".format(_("oui"))
            if bundle["active"]
            else "[red]{}[/red]".format(_("non")),
            bundle["description"],
        ]

    for bundle_name, bundle in config.bundles.items():
        if bundle_name not in bundles_done.keys():
            bundles_done[bundle_name] = [
                "[bold]{}[/bold]".format(bundle_name),
                "[green]{}[/green]".format(_("oui")),
                _("(bundle local sans description)"),
            ]
    for k, row in dict(sorted(bundles_done.items())).items():
        table.add_row(*row)
    console.print(table)


@app.command(help=_("Ajoute un bundle pour l'instance de Max en cours"))
def bundles_add(bundle_name: str):
    from_archive = None
    check_cwd_is_max()
    config = max_config()
    current_bundles_config = config.bundles
    # bundle_name is a local archive
    if bundle_name.endswith(".zip") and Path(bundle_name).is_file():
        from_archive = bundle_name
        bundle_name = os.path.splitext(os.path.basename(bundle_name))[0]
        print(bundle_name, from_archive)
    if from_archive is not None:  # todo install from archive
        if type(from_archive) is str:
            from_archive = Path(from_archive)
        if not from_archive.is_file():
            print(
                _("[red][bold]{}[/bold] n'est pas un chemin valide[/red]").format(
                    from_archive
                )
            )
            raise typer.Exit(code=1)
        fname, extension = os.path.splitext(from_archive)
        if extension != ".zip":
            print(_("[red]{} n'est pas un bundle[/red]").format(from_archive))
            raise typer.Exit(code=1)
        local_destination = Path(
            os.getcwd(),
            ".max",
            "resources",
            "local_bundles",
            os.path.basename(from_archive),
        )
        Path(os.path.dirname(local_destination)).mkdir(exist_ok=True, parents=True)
        shutil.copy(from_archive, local_destination)
        current_bundles_config[bundle_name] = {
            "name": bundle_name,
            "url": f"local://{os.path.basename(local_destination)}",
        }
        config.bundles = current_bundles_config
        config.write()
        _sync_max_instance(os.getcwd(), verbose=False)
        bundles_list()
    else:
        if bundle_name not in config.available_bundles.keys():
            print(_("[red]{} n'est pas un bundle disponible[/red]").format(bundle_name))
            raise typer.Exit(code=1)
        else:
            for (
                available_bundle_name,
                available_bundle,
            ) in config.available_bundles.items():
                if available_bundle_name == bundle_name:
                    if available_bundle["vocabulary"]:
                        config.vocabulary_bundle = bundle_name
                    current_bundles_config[bundle_name] = available_bundle["url"]
                    config.bundles = current_bundles_config
                    config.write()
                    _sync_max_instance(os.getcwd(), verbose=False)
                    bundles_list()


@app.command(help=_("Ajoute un fichier XML à l'instance de Max en cours"))
def feed(xml_file: Path):
    xml_file = Path(xml_file)
    if not xml_file.is_file():
        print(_("[red]{} n'est pas un fichier XML[/red]").format(xml_file))
        raise typer.Exit(code=1)
    check_cwd_is_max()
    java_bin_path = ensure_java()
    # "if(not(db:exists('max'))) then db:create('max') else ()"
    process_args = [
        str(java_bin_path),
        "-cp",
        cp_paths(),
        "-Xmx2g",
        "org.basex.BaseX",
        "if(not(db:exists('max'))) then db:create('max') else ()",
    ]
    subprocess.run(process_args)
    process_args = [
        str(java_bin_path),
        "-cp",
        cp_paths(),
        "-Xmx2g",
        "org.basex.BaseX",
        f"-cOPEN max; ADD {xml_file.resolve()}",
    ]
    subprocess.run(process_args)


@app.command(help=_("Lance le client de BaseX"))
def basex():
    check_cwd_is_max()
    java_bin_path = ensure_java()
    # "if(not(db:exists('max'))) then db:create('max') else ()"
    process_args = [
        str(java_bin_path),
        "-cp",
        cp_paths(),
        "-Xmx2g",
        "org.basex.BaseX",
    ]
    subprocess.run(process_args)


get_yolk()

if __name__ == "__main__":
    app()
