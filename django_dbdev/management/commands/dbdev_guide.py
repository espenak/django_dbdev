from ._base import BaseDbdevCommand


class Command(BaseDbdevCommand):
    help = 'Print a guide of useful database specific commands to stdout.'

    def dbdev_handle(self):
        self.stdout.write('')
        self.stdout.write(self.dbdev_backend.guide())
        self.stdout.write('')