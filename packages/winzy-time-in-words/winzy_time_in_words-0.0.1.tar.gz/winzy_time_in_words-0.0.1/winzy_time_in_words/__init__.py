import winzy
from winzy_time_in_words.time_in_words import mainrun


def create_parser(subparser):
    parser = subparser.add_parser("time", description="Simple program to say time in words")
    return parser


class WinzyPlugin:
    """ Simple program to say time in words """
    __name__ = "time"

    @winzy.hookimpl
    def register_commands(self, subparser):
        self.parser = create_parser(subparser)
        self.parser.set_defaults(func=self.run)

    def run(self, args):
        _ = mainrun()
    
    def hello(self, args):
        # this routine will be called when 'winzy time' is called.
        print("Hello! This is an example ``winzy`` plugin.")

time_plugin = WinzyPlugin()
