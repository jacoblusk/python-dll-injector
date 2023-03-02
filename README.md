# DLL Injector

A simple Python DLL Injector that utilizes `ctypes` and the WIN32 API.

Currently only supports the most basic style of DLL injection, using `LoadLibraryA` and `CreateRemoteThread`.

Depending on whether you run this with 64bit or 32bit Python will change which processes you may inject into.

![Python DLL Injector](https://i.imgur.com/w2AZbll.png)

# How to Run

Just clone the repository and run with `python main.py` as there are no other dependencies.
