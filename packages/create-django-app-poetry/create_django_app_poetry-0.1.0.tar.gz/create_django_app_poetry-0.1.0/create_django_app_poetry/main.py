#!/usr/bin/env python3

import argparse
import os
import re
import shutil
import subprocess
from pathlib import Path
import tempfile

REPO_URL = "https://github.com/Sergio-prog/just-a-django-template"
COMMIT_MSG = "Initial commit"

def pascal_case(s):
    """Convert a string to PascalCase"""
    s = re.sub(r'[^a-zA-Z0-9]', ' ', s)
    return ''.join(word.capitalize() for word in s.split())


def snake_case(s):
    """Convert a string to snake_case"""
    s = re.sub(r'[^a-zA-Z0-9]', ' ', s.lower())
    return '_'.join(s.split())


def replace_placeholders(directory, project_name):
    """Replace {{project_name}} placeholders in all files"""
    project_name_pascal = pascal_case(project_name)
    project_name_snake = snake_case(project_name)

    # Rename the project directory
    old_project_dir = os.path.join(directory, "{{project_name}}")
    new_project_dir = os.path.join(directory, project_name_snake)

    if os.path.exists(old_project_dir):
        os.rename(old_project_dir, new_project_dir)

    # Replace placeholders in files
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(('.py', '.toml', '.ini', '.yml', '.yaml', 'Dockerfile', 'Makefile', '.example')):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath, 'r') as f:
                        content = f.read()

                    content = content.replace("{{project_name}}", project_name_snake)

                    with open(filepath, 'w') as f:
                        f.write(content)
                except UnicodeDecodeError:
                    # Skip binary files
                    pass


def setup_git(directory):
    """Initialize a git repository"""
    subprocess.run(['git', 'init'], cwd=directory, check=True)
    subprocess.run(['git', 'add', '.'], cwd=directory, check=True)
    subprocess.run(['git', 'commit', '-m', COMMIT_MSG], cwd=directory, check=True)


def create_virtual_env(directory):
    """Create a virtual environment and install dependencies"""
    subprocess.run(['poetry', 'install'], cwd=directory, check=True)


def clone_template(template_url, temp_dir):
    """Clone the template repository"""
    subprocess.run(['git', 'clone', template_url, temp_dir], check=True)

    # Remove .git directory
    git_dir = os.path.join(temp_dir, '.git')
    if os.path.exists(git_dir):
        shutil.rmtree(git_dir)


def main():
    parser = argparse.ArgumentParser(description='Create a new Django project from template')
    parser.add_argument('project_name', help='Name of the project')
    parser.add_argument('--dir', '-d', help='Directory to create the project in', default='.')
    parser.add_argument('--template', '-t',
                        help='Template URL or path',
                        default=REPO_URL)
    parser.add_argument('--no-git', action='store_true', help='Skip git initialization')
    parser.add_argument('--no-install', action='store_true', help='Skip dependency installation')

    args = parser.parse_args()

    project_name = args.project_name
    project_dir = os.path.join(os.path.abspath(args.dir), project_name)

    # Create project directory
    os.makedirs(project_dir, exist_ok=True)

    print(f"Creating new Django project: {project_name}")
    print(f"Project directory: {project_dir}")

    with tempfile.TemporaryDirectory() as temp_dir:
        # Clone template
        print("Downloading template...")
        clone_template(args.template, temp_dir)

        # Copy template files to project directory
        print("Setting up project files...")
        for item in os.listdir(temp_dir):
            src = os.path.join(temp_dir, item)
            dst = os.path.join(project_dir, item)
            if os.path.isdir(src):
                shutil.copytree(src, dst, dirs_exist_ok=True)
            else:
                shutil.copy2(src, dst)

        # Replace placeholders
        print("Configuring project...")
        replace_placeholders(project_dir, project_name)

        # Initialize git repository
        if not args.no_git:
            print("Initializing git repository...")
            setup_git(project_dir)

        # Install dependencies
        if not args.no_install:
            print("Installing dependencies (this may take a while)...")
            create_virtual_env(project_dir)

    print(f"\n✅ Project {project_name} created successfully!")
    print(f"\nNext steps:")
    print(f"  cd {project_name}")
    print(f"  cp .env.example .env  # Update with your settings")
    print(f"  poetry shell")
    print(f"  make run  # Or: make build (for Docker)")


if __name__ == "__main__":
    main()