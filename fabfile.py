from fabric.api import sudo, task


@task
def pipy():
    """
    Deploy the newest version of the PiPy service.

    """

    sudo("pypy -m pip install --upgrade git+https://github.com/Julian/PiPy")
    sudo("service pipy restart")
