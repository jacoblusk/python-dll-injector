# DLL Injector

A simple Python DLL Injector that utilizes `ctypes` and the WIN32 API.

Currently only supports the most basic style of DLL injection, using `LoadLibraryA` and `CreateRemoteThread`.

Depending on whether you run this with 64bit or 32bit Python will change which processes you may inject into.

![Python DLL Injector](https://i.imgur.com/w2AZbll.png)
# Installation
You can install directly from GitHub using the command below,
```sh
pip install git+https://github.com/jacoblusk/python-dll-injector.git
```
Or you can clone the repo and install from the repository itself.
```sh
git clone https://github.com/jacoblusk/python-dll-injector.git
cd python-dll-injector
pip install .
```
To run the program,
```sh
pydllinjector
```
