"""

(c) Copyright 2019, ayivima@hotmail.com 

"""


from token import NEWLINE, STRING, OP, NL, COMMENT, ENDMARKER


__name__ = "flake8-lineleak"
__version__ = "0.9.7"


# Warnings & Messages
LLI200 = (
    "LLI200 [INFO] Live code count: "
	"{} logical and {} physical lines.\n"
)
	
LLW404 = (
    "LLW404 Maximum number of logical live "
    "code lines ({}) exceeded.\n"
)
LLW405 = (
    "LLW405 Maximum number of physical "
    "live code lines ({}) exceeded.\n"
)


class screener(object):
    name = __name__
    version = __version__

    LOGICAL = False
    LIVE_CODE_COUNT = False
    MAX_LINE_COUNT = 500

    def __init__(self, tree, file_tokens, filename):
        self.leak_line = None
        self.LIMIT_REACHED = False
        self.logical_line_count = None
        self.physical_line_count = None
        self.tokens = file_tokens

    def _analyse(self):
        """
        Counts code lines, and gets the line
        which exceeds limit if applicable.
        """

        prev_token_type = None
        prev_line_no = None
        log_line_count = 0

        physical_line_deductions = 0

        for token_type, token_value, start, end, line in self.tokens:

            start_line_num = start[0]
            end_line_num, end_line_end = end
            phy_line_count = start_line_num - physical_line_deductions

            # making necessary adjustments for physical 
            # and logical line counts exclude blank lines
            # and comments from count.
            if token_type == NEWLINE:
                log_line_count += 1

            elif ((token_type == NL and start_line_num != prev_line_no)
                    or token_type == COMMENT
                    or token_type == ENDMARKER):

                physical_line_deductions += 1

            # exclude docstrings from count
            elif (token_type == STRING
                    and token_value.startswith(('"""', "'''"))
                    and prev_token_type != OP):

                log_line_count -= 1
                if end_line_num == start_line_num:
                    physical_line_deductions += 1
                else:
                    physical_line_deductions += (
                        end_line_num - start_line_num + 1
                    )

            # checking for leak line while limit is not reached.
            # check stops if limit has been reached
            if not self.LIMIT_REACHED:
                if ((log_line_count > self.MAX_LINE_COUNT and self.LOGICAL)
                        or (phy_line_count > self.MAX_LINE_COUNT
                        and not self.LOGICAL)
                        and token_type not in (NL, COMMENT, STRING)):
                    self.LIMIT_REACHED = True
                    self.leak_line = start_line_num

            prev_token_type = token_type
            prev_line_no = start_line_num
        
        self.last_line, self.last_cell = end_line_num, end_line_end
        self.physical_line_count = (
             self.last_line - physical_line_deductions
        )

        self.logical_line_count = log_line_count

    @classmethod
    def add_options(cls, parser):
        """Registers optional arguments"""
        parser.add_option(
            '--lineleak-logical', action='store_true',
            parse_from_config=False,
            help="Applies line count limit to logical lines."
        )

        parser.add_option(
            '--max-line-count', type=int,
            parse_from_config=False,
            help="Changes the maximum limit for live code line count."
        )

        parser.add_option(
            '--live-code-count', action='store_true',
            parse_from_config=False,
            help="Displays the number of physical"
                 "and logical lines containing live code."
        )

    @classmethod
    def parse_options(cls, options):
        """Parses command-line arguments"""
        if options.max_line_count:
            cls.MAX_LINE_COUNT = options.max_line_count

        if options.lineleak_logical:
            cls.LOGICAL = True

        if options.live_code_count:
            cls.LIVE_CODE_COUNT = True

    def run(self):
        """
        Runs line count and gets the first
        line that breaks the limit.
        """
        self._analyse()

        # requesting live code count overrides limit check
        # and displays the number of live code lines
        if self.LIVE_CODE_COUNT:
            yield (
                self.last_line, self.last_cell,
                LLI200.format(
                    self.logical_line_count,
                    self.physical_line_count
                ), type(self)
            )
        else:
            leak_warning = LLW404 if self.LOGICAL else LLW405

            if self.LIMIT_REACHED:
                yield (
                    self.leak_line, 0,
                    leak_warning.format(self.MAX_LINE_COUNT),
                    type(self)
                )
