__version = "v1.0.15"

version: str = "v0.0.0" if __version == "{{STABLE_GIT_DESCRIPTION}}" else __version
