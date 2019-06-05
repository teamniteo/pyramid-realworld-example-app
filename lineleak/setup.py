from setuptools import setup


def long_description():
	with open('README.rst') as f:
		return f.read()


setup(
    name="flake8-lineleak",
    version='0.9.7',
    description="Lineleak is a flake8 plugin that counts the"
	"lines containing live code in a script, and 'yells' if"
    "a set limit is exceeded. It is meant to help enforce"
    "short scripts and modular python programming.",
	long_description=long_description(),
    keywords=["flake8", "lineleak", "counter", "lines"],
    author="Victor Ayi",
    author_email="ayivima@hotmail.com",
    url="https://github.com/ayivima/lineleak",
    license="MIT",
	py_modules=['lineleak'],
	zip_safe=False,
    python_requires=">=3.4",
    install_requires=["flake8>=3.3.0,<3.7.0"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Framework :: Flake8",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Quality Assurance",
    ],
    entry_points={
        "flake8.extension": [
            "LL = lineleak:screener",
        ],
    },
)
