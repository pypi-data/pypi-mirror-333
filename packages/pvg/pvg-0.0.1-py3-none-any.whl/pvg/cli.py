import click
import os
import subprocess
import tempfile
import shutil
from pathlib import Path
import re
import hashlib
import json

def is_git_url(url):
    """Check if the input is a git URL."""
    git_url_patterns = [
        r'^https?://.*\.git$',
        r'^git@.*:.*\.git$',
        r'^git://.*\.git$',
        r'^ssh://.*\.git$'
    ]
    return any(re.match(pattern, url) for pattern in git_url_patterns)

def get_cache_dir():
    """Get the cache directory path.
    
    The cache directory can be configured using the PVG_CACHE_DIR environment variable.
    If not set, defaults to ~/.pvg-cache/
    """
    return os.environ.get('PVG_CACHE_DIR') or os.path.expanduser("~/.pvg-cache")

def safe_path(url):
    """Convert a URL to a safe directory name using SHA-256."""
    return hashlib.sha256(url.encode()).hexdigest()

def ensure_cache_dir():
    """Ensure the cache directory exists."""
    cache_dir = get_cache_dir()
    os.makedirs(cache_dir, exist_ok=True)
    return cache_dir

def write_meta_info(package_dir, git_url):
    """Write metadata information to meta.json."""
    meta_file = os.path.join(package_dir, "meta.json")
    meta_info = {
        "git_url": git_url,
        "installed_at": str(Path(package_dir).stat().st_mtime),
        "last_updated": str(Path(package_dir).stat().st_mtime)
    }
    with open(meta_file, "w") as f:
        json.dump(meta_info, f, indent=2)

def clone_or_pull(git_url, force=False):
    """Clone a new repository or pull if it exists."""
    cache_dir = ensure_cache_dir()
    package_dir = os.path.join(cache_dir, safe_path(git_url))
    repo_dir = os.path.join(package_dir, "repo")

    if os.path.exists(repo_dir):
        if force:
            click.echo("Force flag used. Removing existing repository...")
            shutil.rmtree(package_dir)
        else:
            click.echo(f"Repository cache exists at {repo_dir}")
            click.echo("Pulling latest changes...")
            try:
                subprocess.run(
                    ["git", "pull"],
                    cwd=repo_dir,
                    check=True,
                    capture_output=True,
                    text=True
                )
                # Update last_updated in meta.json
                write_meta_info(package_dir, git_url)
                return repo_dir
            except subprocess.CalledProcessError as e:
                click.echo(f"Pull failed: {e.stderr}", err=True)
                if click.confirm("Would you like to force delete and clone again?"):
                    shutil.rmtree(package_dir)
                else:
                    raise click.Abort()

    # Clone if directory doesn't exist or was deleted
    if not os.path.exists(repo_dir):
        os.makedirs(package_dir, exist_ok=True)
        click.echo(f"Cloning repository to {repo_dir}")
        subprocess.run(
            ["git", "clone", git_url, repo_dir],
            check=True,
            capture_output=True,
            text=True
        )
        # Write initial meta.json
        write_meta_info(package_dir, git_url)

    return repo_dir

@click.group()
def cli():
    """PVG - pip-via-git: Install Python packages directly from Git repositories."""
    pass

@cli.command()
@click.argument('package')
@click.option('--use-ssh', is_flag=True, default=False, help='Use SSH URL instead of HTTPS for git clone')
@click.option('--force', is_flag=True, default=False, help='Force delete and clone the repository even if it exists in cache')
def install(package, use_ssh, force):
    """Install a package from the specified source.
    
    Example: pvg install hello/world
            pvg install https://github.com/username/repo.git
            pvg install git@github.com:username/repo.git
    
    This will clone the git repository and install the package using pip.
    The repository can be cloned using either HTTPS (default) or SSH URLs.
    For GitHub repositories, you can specify either the repository name or the full URL.
    Repositories are cached in ~/.pvg-cache/ and updated using git pull unless --force is used.
    """
    # Determine if the package is a URL or a GitHub repository name
    if is_git_url(package):
        git_url = package
        click.echo(f"Using provided git URL: {git_url}")
    else:
        # Convert package name to git URL based on protocol choice
        if use_ssh:
            git_url = f"git@github.com:{package}.git"
        else:
            git_url = f"https://github.com/{package}.git"
        click.echo(f"Using {'SSH' if use_ssh else 'HTTPS'} GitHub URL: {git_url}")
    
    try:
        # Clone or pull the repository
        repo_path = clone_or_pull(git_url, force)
        
        click.echo(f"Installing package from {repo_path}")
        # Run pip install -e in the cloned repository
        result = subprocess.run(
            ["pip", "install", "-e", "."],
            cwd=repo_path,
            check=True,
            capture_output=True,
            text=True
        )
        click.echo("Installation successful!")
        
    except subprocess.CalledProcessError as e:
        click.echo(f"Error: {e.stderr}", err=True)
        raise click.Abort()
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        raise click.Abort()

@cli.command()
def clean_cache():
    """Clean the package cache directory (~/.pvg-cache)."""
    cache_dir = get_cache_dir()
    if os.path.exists(cache_dir):
        if click.confirm(f"Are you sure you want to delete all cached repositories in {cache_dir}?"):
            shutil.rmtree(cache_dir)
            click.echo("Cache cleaned successfully!")
        else:
            click.echo("Cache cleaning cancelled.")
    else:
        click.echo("Cache directory doesn't exist.")

@cli.command()
def list_cache():
    """List all cached repositories and their metadata."""
    cache_dir = get_cache_dir()
    if not os.path.exists(cache_dir):
        click.echo("Cache directory doesn't exist.")
        return

    for package_hash in os.listdir(cache_dir):
        package_dir = os.path.join(cache_dir, package_hash)
        meta_file = os.path.join(package_dir, "meta.json")
        if os.path.exists(meta_file):
            with open(meta_file) as f:
                meta = json.load(f)
                click.echo(f"\nPackage: {meta['git_url']}")
                click.echo(f"Cache location: {package_dir}")
                click.echo(f"Last updated: {meta['last_updated']}")

if __name__ == '__main__':
    cli()
