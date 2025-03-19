import subprocess
from pathlib import Path

from hipercow.environment_engines.base import EnvironmentEngine, Platform
from hipercow.root import Root
from hipercow.util import subprocess_run


class Empty(EnvironmentEngine):
    def __init__(self, root: Root, name: str, platform: Platform | None = None):
        super().__init__(root, name, platform)

    def exists(self) -> bool:
        return True

    def path(self) -> Path:
        msg = "The empty environment has no path"
        raise Exception(msg)

    # These "unused argument" errors from ruff are probably a bug?
    def create(self, **kwargs) -> None:  # noqa: ARG002
        msg = "Can't create the empty environment!"
        raise Exception(msg)

    def provision(
        self, cmd: list[str] | None, **kwargs  # noqa: ARG002
    ) -> None:
        msg = "Can't provision the empty environment!"
        raise Exception(msg)

    def run(
        self,
        cmd: list[str],
        *,
        env: dict[str, str] | None = None,
        **kwargs,
    ) -> subprocess.CompletedProcess:
        return subprocess_run(cmd, env=env, **kwargs)
