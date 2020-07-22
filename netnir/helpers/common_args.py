def fetch_host(parser, required=False):
    parser.add_argument(
        "--host", help="specify a specific host", default=str(), required=required,
    )


def filter_hosts(parser, required=False):
    parser.add_argument(
        "--filter",
        "-f",
        help="filter inventory by key:value criteria",
        required=required,
        type=lambda x: x.split(","),
        default=dict(),
    )


def filter_group(parser, required=False):
    parser.add_argument(
        "--group",
        "-g",
        help="filter inventory by group",
        default=str(),
        required=required,
    )


def num_workers(parser, required=False):
    parser.add_argument(
        "--workers",
        "-w",
        help="number of workers to utilize",
        default=int(),
        required=required,
    )


def make_changes(parser, required=False):
    parser.add_argument(
        "-X",
        help="disables nornir dry-run",
        default=True,
        const=False,
        nargs="?",
        required=required,
    )


def verbose(parser, required=False):
    parser.add_argument(
        "--verbose",
        "-v",
        help="verbose logging",
        default=False,
        const=True,
        nargs="?",
        required=required,
    )


def output(parser, required=False):
    parser.add_argument(
        "--output", "-o", help="write output to file", required=required,
    )