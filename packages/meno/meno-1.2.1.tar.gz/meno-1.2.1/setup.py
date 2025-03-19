"""Setup script for the meno package."""

from setuptools import setup, find_packages

setup(
    name="meno",
    version="1.2.1",
    description="Topic modeling toolkit for messy text data",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Stephen Oates",
    author_email="stephen.oates@example.com",
    url="https://github.com/srepho/meno",
    packages=find_packages(),
    include_package_data=True,
    package_data={"meno": ["default_config.yaml", "config/*.yaml"]},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Text Processing :: Linguistic",
    ],
    python_requires=">=3.8,<3.14",
    install_requires=[
        "pandas>=2.0.0,<3.0.0",
        "pyarrow>=11.0.0",
        "scikit-learn>=1.2.0,<2.0.0",
        "pydantic>=2.0.0,<3.0.0",
        "pyyaml>=6.0,<7.0",
        "jinja2>=3.1.2,<4.0.0",
        "thefuzz>=0.20.0,<0.21.0",
        "argparse>=1.4.0,<2.0.0",
    ],
    extras_require={
        # Simplified installation options
        "lightweight": [
            "scikit-learn>=1.2.0,<2.0.0",
            "plotly>=5.14.0,<6.0.0",
            "wordcloud>=1.9.0,<2.0.0",
        ],
        "cpu": [
            "sentence-transformers>=2.2.2,<3.0.0", 
            "transformers>=4.28.0,<5.0.0",
            "torch>=2.0.0,<3.0.0",
            "plotly>=5.14.0,<6.0.0",
            "umap-learn>=0.5.3,<0.6.0",
            "hdbscan>=0.8.29,<0.9.0", 
            "bertopic>=0.15.0,<0.16.0",
            "gensim>=4.3.0,<5.0.0",
            "spacy>=3.5.0,<4.0.0",
            "wordcloud>=1.9.0,<2.0.0",
            "en_core_web_sm>=3.5.0,<4.0.0",
        ],
        "gpu": [
            "sentence-transformers>=2.2.2,<3.0.0", 
            "transformers>=4.28.0,<5.0.0",
            "torch>=2.0.0,<3.0.0",
            "plotly>=5.14.0,<6.0.0",
            "umap-learn>=0.5.3,<0.6.0",
            "hdbscan>=0.8.29,<0.9.0", 
            "bertopic>=0.15.0,<0.16.0",
            "gensim>=4.3.0,<5.0.0",
            "spacy>=3.5.0,<4.0.0",
            "wordcloud>=1.9.0,<2.0.0",
            "en_core_web_sm>=3.5.0,<4.0.0",
            "bitsandbytes>=0.41.0,<1.0.0",
            "accelerate>=0.20.0,<1.0.0",
            "safetensors>=0.3.1,<0.4.0",
        ],
        
        # Legacy options (maintained for backwards compatibility)
        "minimal": [
            "sentence-transformers>=2.2.2,<3.0.0", 
            "transformers>=4.28.0,<5.0.0",
            "torch>=2.0.0,<3.0.0",
            "plotly>=5.14.0,<6.0.0",
            "umap-learn>=0.5.3,<0.6.0",
            "hdbscan>=0.8.29,<0.9.0", 
            "bertopic>=0.15.0,<0.16.0",
            "gensim>=4.3.0,<5.0.0",
            "spacy>=3.5.0,<4.0.0",
            "wordcloud>=1.9.0,<2.0.0",
        ],
        "spacy_model": [
            "en_core_web_sm>=3.5.0,<4.0.0",
        ],
        "full": [
            "sentence-transformers>=2.2.2,<3.0.0",
            "transformers>=4.28.0,<5.0.0",
            "torch>=2.0.0,<3.0.0",
            "gensim>=4.3.0,<5.0.0",
            "plotly>=5.14.0,<6.0.0",
            "umap-learn>=0.5.3,<0.6.0",
            "hdbscan>=0.8.29,<0.9.0",
            "spacy>=3.5.0,<4.0.0",
            "en_core_web_sm>=3.5.0,<4.0.0",
            "cleanlab>=2.3.0,<3.0.0",
            "polars>=1.11.0,<1.15.0",
            "bertopic>=0.15.0,<0.16.0",
            "top2vec>=1.0.27,<2.0.0",
            "wordcloud>=1.9.0,<2.0.0",
            "openai>=1.0.0,<2.0.0",
            "tqdm>=4.65.0,<5.0.0",
        ],
        "llm": [
            "transformers>=4.28.0,<5.0.0",
            "torch>=2.0.0,<3.0.0",
            "tqdm>=4.65.0,<5.0.0",
            "accelerate>=0.20.0,<0.22.0",
        ],
        "llm_openai": [
            "openai>=1.0.0,<2.0.0",
            "tqdm>=4.65.0,<5.0.0",
        ],
        "embeddings": [
            "sentence-transformers>=2.2.2,<3.0.0",
            "transformers>=4.28.0,<5.0.0",
            "torch>=2.0.0,<3.0.0",
        ],
        "openai": [
            "openai>=1.0.0,<2.0.0",
            "tqdm>=4.65.0,<5.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "meno-config=meno.cli.team_config_cli:main",
            "meno-web=meno.cli.web_interface_cli:main",
        ],
    },
    license="MIT",
)