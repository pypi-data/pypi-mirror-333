import os
from setuptools import setup, find_packages

VERSION = '0.0.46'
DESCRIPTION = 'eazyml-image-xai provides APIs for explainable AI (XAI)'

# Setting up
setup(
    name="eazyml-xai-image",
    version=VERSION,
    author="Eazyml",
    author_email="admin@ipsoftlabs.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=open("README.md", encoding="utf-8").read(),
    package_dir={"eazyml_xai_image":"./eazyml_xai_image"},
    # Includes additional non-Python files in the package.
    package_data={'' : ['*.py', '*.so', '*.dylib', '*.pyd']},
    install_requires=[
                      'tensorflow==2.13',
                      'segmentation-models==1.0.1',
                      'lime',
                      'opencv-python>=4.10',
                      'flask',
                      'cryptography',
                      'pyyaml',
                      'pytz',
                      'cachetools',
                      'matplotlib'
                      ],
    extras_require={
        ':python_version<="3.7"': ['pandas==1.3.*', 'scikit-learn==1.0.*', 'numpy==1.21.*'],
        ':python_version=="3.8"': ['pandas>=2.0.3', 'scikit-learn==1.3.*', 'numpy==1.24.*'],
        ':python_version=="3.9"': ['pandas>=2.2.3', 'scikit-learn==1.3.*', 'numpy==1.24.*'],
        ':python_version=="3.10"': ['pandas>=2.2.3', 'scikit-learn==1.3.*', 'numpy==1.24.*'],
        ':python_version=="3.11"': ['pandas>=2.2.3', 'scikit-learn==1.3.*', 'numpy==1.24.*'],
        ':python_version>"3.11"': ['pandas>=2.2.3', 'scikit-learn==1.3.*', 'numpy']
    },
    keywords=['python'],
    url="https://eazyml.com/",
    project_urls={
        "Documentation": "https://docs.eazyml.com/",
        "Homepage": "https://eazyml.com/",
        "Contact Us": "https://eazyml.com/trust-in-ai",
        "eazyml-automl": "https://pypi.org/project/eazyml-automl/",
        "eazyml-counterfactual": "https://pypi.org/project/eazyml-counterfactual/",
        "eazyml-xai": "https://pypi.org/project/eazyml-xai/",
        "eazyml-xai-image": "https://pypi.org/project/eazyml-xai-image/",
        "eazyml-insight": "https://pypi.org/project/eazyml-insight/",
        "eazyml-data-quality": "https://pypi.org/project/eazyml-data-quality/",
    },
    similar_projects={
        'eazyml-data-quality' : "https://pypi.org/project/eazyml-data-quality/",
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: Other/Proprietary License",
        "Intended Audience :: Education",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Intended Audience :: System Administrators",
        "Intended Audience :: Information Technology",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Operating System :: Unix",
        "Operating System :: MacOS",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires=">=3.7"
)
