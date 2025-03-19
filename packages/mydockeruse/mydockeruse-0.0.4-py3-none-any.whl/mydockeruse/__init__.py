__all__, __version__ = ['__main__', 'install', 'uninstall'], '0.0.4'
from docker import from_env as _docker_
from martialaw.martialaw import martialaw as _clsr
import builtins as __builtin__
__builtin__.default_docker_environment = _docker_()
__F = [(_clsr(_clsr(default_docker_environment.containers.run)(stdin_open=1, tty=1, detach=1)), default_docker_environment.images)]
(lambda x=__F[0][1]:__F.append([staticmethod(f) for f in (x.pull, _clsr(x.remove)(force=1))]))()
__builtin__.default_docker_environment_manager = type('',(), dict(install = __F[1][0], uninstall = __F[1][1], __call__ = lambda self, x : __F[0][0](x)("/bin/bash")))()