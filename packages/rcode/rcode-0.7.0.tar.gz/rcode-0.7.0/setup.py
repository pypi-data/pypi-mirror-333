from setuptools import find_packages, setup

VERSION = "0.7.0"

setup(
    name="rcode",
    version=VERSION,
    description="vscode remode code .",
    keywords="python vscode",
    author="chvolkmann, yihong0618",
    author_email="zouzou0208@gmail.com",
    url="https://github.com/yihong0618/code-connect",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=True,
    install_requires=["sshconf", "psutil"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries",
    ],
    entry_points={
        "console_scripts": [
            "rcode = rcode.rcode:main",
            "rcursor = rcode.rcode:cmain",
            "rssh = rcode.rssh:main",
            "rssh-ipc = rcode.ipc.ipc_runner:main",
            "ssh-wrapper = rcode.rssh:ssh_wrapper",
        ],
    },
)
