"""Not @generated code, but it belongs to the upstream lowerquality/gentle project."""
import os
import shutil
import sys

ENV_VAR = "GENTLE_RESOURCES_ROOT"


class CustomResolver:
    def __init__(self):
        thisfile = os.path.abspath(__file__)
        thisdir = os.path.dirname(thisfile)
        gentledir = os.path.dirname(thisdir)
        all_files = []
        all_dirs = []
        for root, dirs, files in os.walk(gentledir):
            for idir in dirs:
                all_dirs.append(os.path.join(root, idir))
            for ifile in files:
                all_files.append(os.path.join(root, ifile))
        self.all_files = sorted(x for x in all_files if "__pycache__" not in x)
        self.all_dirs = sorted(x for x in all_dirs if "__pycache__" not in x)

    def get_binary(self, name):
        return shutil.which(name) or self.get_match(name, self.all_files)

    def get_match(self, name, candidates):
        matching_files = [x for x in candidates if x.endswith(name)]
        if not matching_files:
            raise AssertionError("Couldn't find {}".format(name))
        if 1 < len(matching_files):
            raise AssertionError("{} was not unique found: {}".format(name, matching_files))
        return matching_files[0]

    def get_resource(self, name):
        if name.endswith("/"):
            return self.get_match(name.rstrip("/"), self.all_dirs) + "/"
        return self.get_match(name, self.all_files + self.all_dirs)

    def get_datadir(self, name):
        return self.get_match(name, self.all_dirs)


class SourceResolver:
    def __init__(self):
        self.project_root = os.path.abspath(
            os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir, os.pardir)
        )

    def get_binary(self, name):
        path_in_project = os.path.join(self.project_root, name)
        if os.path.exists(path_in_project):
            return path_in_project
        else:
            return name

    def get_resource(self, name):
        root = os.environ.get(ENV_VAR) or self.project_root
        return os.path.join(root, name)

    def get_datadir(self, name):
        return self.get_resource(name)


class PyinstallResolver:
    def __init__(self):
        self.root = os.path.abspath(
            os.path.join(getattr(sys, "_MEIPASS", ""), os.pardir, "Resources")
        )

    def get_binary(self, name):
        return os.path.join(self.root, name)

    def get_resource(self, name):
        rpath = os.path.join(self.root, name)
        if os.path.exists(rpath):
            return rpath
        else:
            return get_datadir(
                name
            )  # DMG may be read-only; fall-back to datadir (ie. so language models can be added)

    def get_datadir(self, path):
        return os.path.join(os.environ["HOME"], ".gentle", path)


RESOLVER = CustomResolver()


def get_binary(name):
    return RESOLVER.get_binary(name)


def get_resource(path):
    return RESOLVER.get_resource(path)


def get_datadir(path):
    return RESOLVER.get_datadir(path)
