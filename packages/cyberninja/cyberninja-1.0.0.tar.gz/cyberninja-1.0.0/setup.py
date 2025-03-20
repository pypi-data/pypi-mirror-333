from setuptools import setup, find_packages

# Read README.md for long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="cyberninja",
    version="1.0.0",
    description="Advanced Social Media Intelligence Tool for username reconnaissance",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Vimal",
    author_email="2004.vimald@gmail.com",
    url="https://github.com/Vimal007Vimal/CyberNinja",
    project_urls={
        "Bug Tracker": "https://github.com/Vimal007Vimal/CyberNinja/issues",
        "Documentation": "https://github.com/Vimal007Vimal/CyberNinja/blob/main/README.md",
    },
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'cyberninja': ['resources/*', 'removed_sites.json'],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Information Technology",
        "Topic :: Security",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords="osint, security, social-media, username, reconnaissance, cybersecurity",
    python_requires='>=3.6',
    install_requires=[
        'beautifulsoup4>=4.9.3',
        'bs4',
        'certifi',
        'colorama',
        'lxml',
        'PySocks',
        'requests>=2.25.1',
        'requests-futures>=1.0.0',
        'soupsieve',
        'stem>=1.8.0',
        'torrequest>=0.1.0',
        'pyfiglet>=0.8.post1',
        'term_image>=0.7.2',
        'timg>=1.1.6',
        'pillow>=9.1,<11'
    ],
    entry_points={
        'console_scripts': [
            'cyberninja=cyberninja.cyberninja:main',
        ],
    },
)
