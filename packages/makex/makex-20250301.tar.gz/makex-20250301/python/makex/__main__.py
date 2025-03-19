import dataclasses
import importlib.resources
import logging
import operator
import os
import platform
import signal
import sys
import traceback
from argparse import (
    SUPPRESS,
    Action,
    ArgumentError,
    ArgumentParser,
    Namespace,
)
from enum import Enum
from os.path import normpath
from pathlib import Path
from typing import (
    Any,
    Literal,
    Optional,
    Sequence,
    Union,
)

from makex._logging import (
    debug,
    initialize_logging,
    trace,
)
from makex.build_path import get_build_path
from makex.colors import (
    Colors,
    ColorsNames,
    NoColors,
)
from makex.commands.fix import main_fix_parser
from makex.configuration import (
    collect_configurations,
    evaluate_configuration_environment,
    read_configuration,
)
from makex.constants import (
    ABSOLUTE_WORKSPACE,
    CONFIGURATION_ARGUMENT_ENABLED,
    DIRECT_REFERENCES_TO_MAKEX_FILES,
    SYNTAX_2025,
    TASK_PATH_NAME_SEPARATOR,
    WORKSPACE_ARGUMENT_ENABLED,
)
from makex.context import (
    Context,
    detect_shell,
)
from makex.errors import (
    CacheError,
    ConfigurationError,
    Error,
    ExecutionError,
    ExternalExecutionError,
    GenericSyntaxError,
    MultipleErrors,
)
from makex.executor import Executor
from makex.flags import (
    MAKEX_SYNTAX_VERSION,
    VARIANTS_ENABLED,
)
from makex.locators import format_locator
from makex.makex_file import MakexFileCycleError
from makex.makex_file_parser import (
    TargetGraph,
    parse_makefile_into_graph,
)
from makex.makex_file_types import TaskReference
from makex.python_script import (
    PythonScriptError,
    PythonScriptFileError,
)
from makex.run import (
    get_running_process_ids,
    run,
)
from makex.ui import (
    UI,
    is_ansi_tty,
    pretty_makex_file_exception,
)
from makex.version import VERSION
from makex.workspace import (
    current_workspace,
    get_workspace,
    which_workspace,
)

COMPLETE_TARGET = {
    "bash": "_shtab_makex_compgen_paths",
    "zsh": "_shtab_makex_complete_target",
}


class GlobalArgs:
    pass


class AffectedArgs(GlobalArgs):
    """
        affected --scope //* paths or stdin

    """

    # list of paths that are marked as changed to find dependent tasks.
    # paths may be relative, absolute, or workspace
    paths: list[str]

    # list of paths to change scope of makex file searches
    scope: list[str]


class ScopePart(Enum):
    RECURSIVE = "..."


@dataclasses.dataclass
class ParsedScope:
    path: Path
    type: ScopePart = None


def is_color_enabled(color_argument: Literal["no", "auto", "off", "on", "yes"]):
    color_argument = color_argument.lower()
    if color_argument == "auto":
        return is_ansi_tty()
    elif color_argument in {"no", "off"}:
        return False
    elif color_argument in {"yes", "on"}:
        return True

    return None


class Verbosity(Action):
    def __init__(self, *args, default_none=3, **kwargs):
        super().__init__(*args, **kwargs)
        self.default_none = default_none

    def __call__(
        self,
        parser: ArgumentParser,
        namespace: Namespace,
        values: Union[str, Sequence[Any], None],
        option_string: Union[str, None] = ...
    ) -> None:
        """
        --verbose == 3
        --verbose=3 is 3
        --verbose=2 is 2
        --verbose=0 is off
        :param parser:
        :param namespace:
        :param values:
        :param option_string:
        :return:
        """
        value = None
        print("parse values", values, namespace)
        if values is not None:
            try:
                value = int(values)
            except Exception as e:
                raise ArgumentError(
                    self, f"Error parsing verbosity argument. Must be a number. Got {value}"
                )
        else:
            value = self.default_none

        if value is not None:
            namespace.verbose = value
        else:
            namespace.verbose = False

        sys.exit(0)


def _add_global_arguments(base_parser, cache: Path = None, documentation: bool = True, help=None):
    # Allow supressing help so the arguments work before and after the specified command.
    # all arguments should be optional for sphinx
    # documentation = True by default to ease automatic documentation by sphinx

    base_parser.add_argument(
        #"-v",
        "--verbose",
        default=0,
        action="count",
        help=help or
        "Verbosity of makex messaging. Specify multiple times or set to a number between 0 and 3. (The default is 0 and the maximum is 3)."
    )

    if WORKSPACE_ARGUMENT_ENABLED:
        base_parser.add_argument(
            #"-W",
            "--workspace",
            action="store_true",
            default=False,
            help=help or "Path to the current workspace. This should not be used unless necessary."
        )

    base_parser.add_argument(
        # "-d",
        "--debug",
        action="store_true",
        default=False,
        help=help or "Enable debug and logging to the maximum level."
    )

    base_parser.add_argument(
        "--profile-mode",
        choices=["cprofile", "yappi"],
        default="yappi",
        help=SUPPRESS,
        #help="Enable profiling. Specify file name to write stats to a file. - to write to stdout."
    )

    if documentation is False:
        # Hide from documentation
        base_parser.add_argument(
            "--profile",
            #help="Enable profiling. Specify file name to write stats to a file. - to write to stdout.",
            help=SUPPRESS,
        )

    if CONFIGURATION_ARGUMENT_ENABLED:
        base_parser.add_argument(
            #"-C",
            "--configuration",
            action="store_true",
            default=False,
            help=help or "Path to a Makex configuration file. This is not normally required."
        )

    base_parser.add_argument(
        "--color",
        choices=["off", "auto", "on"],
        default="auto",
        help=help or "Print colored messaging."
    )
    #parser.add_argument("--define", nargs="*", action="append", help="define a variable")

    help_text = "The unified external cache/build path."
    if cache:
        help_text += f"[default={cache}]"

    base_parser.add_argument(
        "--cache",
        default=False,
        help=help or help_text,
    )

    if documentation is False:
        base_parser.add_argument(
            # "-d",
            "--python-audit",
            nargs="?",
            action="append",
            help=help or
            "Enable auditing of python audit hooks. Pass a identifier. May be passed multiple times.",
        )
    return base_parser


def parser(cache: Path = None, documentation: bool = True):

    #base_parser = ArgumentParser(add_help=False)
    #base_parser = _base_parser(base_parser, cache, documentation)

    system = platform.system()
    if documentation: # XXX: Documentation mode. For sphinx. Don't calculate cpus default.
        cpus = 1
    elif system in {"Linux"}:
        cpus = max(len(os.sched_getaffinity(0)), 1)
    elif system == "windows":
        # Windows
        cpus = psutil.Process().cpu_affinity()
    else:
        # assume at least one cpu is available
        cpus = 1

    # TODO: most of the subcommands use threads in some way.
    def add_threads_argument(subparser):
        subparser.add_argument(
            #"-t",
            "--cpus",
            type=int,
            help=f"Worker CPUs to use for parsing, evaluating and running tasks in parallel. (Default: {cpus})",
            default=cpus
        )

    parser = ArgumentParser(
        prog="makex",
        description="""Makex command line program.\n\nSee https://meta.company/go/makex for the latest documentation.""",
        epilog="""""", #parents=[base_parser],
    )
    _add_global_arguments(parser, cache, documentation)

    base_parser = ArgumentParser(prog="makex", add_help=False)
    _add_global_arguments(base_parser, cache, documentation, help=SUPPRESS)

    # XXX: help argument must be specified otherwise shtab will not see the sub-commands (specifically in the zsh generator)
    #   see: https://github.com/iterative/shtab/blob/eb12748b7068848ddd7b570abcd180df7264332a/shtab/__init__.py#L136
    #   see: https://github.com/python/cpython/blob/58f883b91bd8dd4cac38b58a026397363104a129/Lib/argparse.py#L1220
    #    ("help" in kwargs, if not specified, self._choices_actions will not be filled.)
    subparsers = parser.add_subparsers(
        dest='command',
        title="commands",
        description="Valid commands",
        help="Commands you may enter.",
        required=True,
    )

    ######### run
    subparser = subparsers.add_parser(
        "run",
        help="Run a task or list of tasks.",
        description="Run a task or list of tasks.",
        parents=[base_parser],
    )
    subparser.set_defaults(command_function=main_run)

    action = subparser.add_argument(
        "tasks",
        nargs="+",
    )
    action.complete = COMPLETE_TARGET
    subparser.add_argument(
        "--directory",
        help="Change to directory before evaluating tasks.",
    ) #"-C",

    subparser.add_argument(
        "--force",
        action="store_true",
        help="Always run all tasks even if they don't need to be.",
    ) #"-f",

    subparser.add_argument(
        "--dry",
        action="store_true",
        default=False,
        help="Do a dry run. Nothing will be executed.",
    )

    if VARIANTS_ENABLED:
        subparser.add_argument(
            "--variants",
            nargs="*",
            action="append",
            help="specify variants. name=value command separated. or specify multiple times."
        )

    if False:
        subparser.add_argument(
            "--ignore",
            nargs="*",
            action="append",
            help="Specify file ignore patterns for input/output files.",
        )

    add_threads_argument(subparser)

    ######## path
    subparser = subparsers.add_parser(
        "path",
        help="Get the output path of a task.",
        description="Get the output path of a task.",
        parents=[base_parser],
    )
    subparser.add_argument(
        "task", help="Name and optional path of a task. //path:name, //:name, :name are all valid."
    )
    subparser.add_argument(
        "--real",
        action="store_true",
        help="Return cache path. This may be slower as it must resolve Workspaces.",
        default=False,
    ) #"-r",
    subparser.set_defaults(command_function=main_get_path)

    ######## dot
    subparser = subparsers.add_parser(
        "dot",
        help="Create a dot dependency graph of tasks. Printed to standard output.",
        parents=[base_parser],
    )
    subparser.add_argument("targets", nargs="+")
    subparser.add_argument(
        "--files",
        help="Include/evaluate files/globs. May be slow.",
    ) # "-f", "-f",

    # TODO: this could be a global
    subparser.add_argument(
        "--ignore",
        nargs="*",
        action="append",
        help="Specify file ignore patterns for input/output files.",
    )
    add_threads_argument(subparser)

    ######## affected
    subparser = subparsers.add_parser(
        "affected",
        help="Return a list of tasks affected by changes to the specified files.",
        parents=[base_parser],
    )
    subparser.set_defaults(command_function=main_affected)
    subparser.add_argument("files", nargs="+")
    subparser.add_argument(
        "--scope",
        nargs="+",
        help="expand/narrow the scope of the search. +/- may be added to prefix includes/excludes."
    )

    add_threads_argument(subparser)

    ######## inputs
    subparser = subparsers.add_parser(
        "inputs",
        help="Return the input files of a task. Evaluates the file.",
        parents=[base_parser],
    )
    subparser.set_defaults(command_function=main_get_inputs)
    subparser.add_argument(
        "--ignore",
        nargs="*",
        action="append",
        help="Specify file ignore patterns.",
    )
    subparser.add_argument("targets", nargs="+")
    add_threads_argument(subparser)

    ######## outputs
    subparser = subparsers.add_parser(
        "outputs",
        help="Return the output files of a task. Evaluates the file.",
        parents=[base_parser],
    )
    subparser.set_defaults(command_function=main_get_outputs)
    subparser.add_argument(
        "--ignore",
        nargs="*",
        action="append",
        help="Specify file ignore patterns.",
    )
    subparser.add_argument("output_names", nargs="+")

    add_threads_argument(subparser)

    ######## evaluate
    subparser = subparsers.add_parser(
        "evaluate",
        help="Evaluate the specified Makex File (or paths with Makex Files) for the specified variable.",
        parents=[base_parser],
    )
    subparser.add_argument("file_or_directory")
    subparser.add_argument(
        "variable_name",
        help="Name of the variable to evaluate. Can be target(name).* to evaluated variables of named targets  in the file.",
    )

    ######### targets subcommand
    subparser = subparsers.add_parser(
        "tasks",
        aliases=["targets"], # TODO: remove this.
        parents=[base_parser],
        help="Generate list of targets parsed from the makex file found in path.",
    )
    subparser.set_defaults(command_function=main_targets)
    subparser.add_argument(
        "path",
        nargs="?",
        help="Path to a makex file or directory. The current directory is the default.",
    )
    subparser.add_argument(
        "--paths",
        choices=["absolute", "workspace", "relative"],
        default="workspace",
        help="How to output paths of tasks. `relative` is relative to the current folder.",
    )
    subparser.add_argument(
        "--prefix",
        default=False,
        action="store_true",
        help="May be used to prefix all paths.",
    )

    ######### completions command
    subparser = subparsers.add_parser(
        "completions",
        parents=[base_parser],
        description="Generate completion files for shells.",
        help="Generate completion files for shells.",
    )
    subparser.set_defaults(command_function=main_completions)

    #if HAS_SHTAB:
    #    shtab.add_argument_to(
    #        subparser, option_string=["--shell"], parent=parser, preamble=PREAMBLE
    #    ) # magic!
    #else:
    subparser.add_argument("--shell", choices=["bash", "zsh"])
    subparser.add_argument("--internal", action="store_true", default=False)

    subparser.add_argument(
        "file",
        nargs="?",
        help="The output file to write the completions to. If not specified, will the completion will be written to standard out.",
    )

    ######### workspace command
    subparser = subparsers.add_parser(
        "workspace",
        parents=[base_parser],
        description="Print the current workspace, or the workspace detected at path.",
        help="Print the current workspace, or the workspace detected at path.",
    )
    subparser.set_defaults(command_function=main_workspace)

    subparser.add_argument(
        "path",
        nargs="?",
        help="Path representing a workspace, or inside a workspace.",
    )

    ######### complete command
    subparser = subparsers.add_parser(
        "complete",
        parents=[base_parser],
        help="Print completions for the specified input. This is used for shell completions.",
    )
    subparser.set_defaults(command_function=main_complete)

    subparser.add_argument(
        "string",
        nargs="?",
        help="May be a complete/partial path. May include a target name.",
    )

    ######### version command
    subparser = subparsers.add_parser(
        "version",
        help="Print the makex version",
    )
    subparser.set_defaults(command_function=main_version)

    ######### fix command
    main_fix_parser(subparsers)

    return parser


def _kill_running_processes():
    # XXX: send a signal to any processes we created.
    for pid in get_running_process_ids():
        os.killpg(os.getpgid(pid), signal.SIGKILL)


def _handle_signal_interrupt(_signal, frame):
    # TODO: attempt to shutdown pool gracefully
    # self.pool.shutdown()
    # self.pool.shutdown(cancel_futures=True)
    print('You pressed Ctrl+C or the process was interrupted!')
    _kill_running_processes()
    sys.exit(-1)


def _handle_signal_terminate(_signal, frame):
    # TODO: attempt to shutdown pool gracefully
    # self.pool.shutdown()
    # self.pool.shutdown(cancel_futures=True)
    print('You pressed Ctrl+C or the process was interrupted!')

    # send a kill because it's more reliable.
    _kill_running_processes()

    sys.exit(-1)


def parse_scope(scope):
    type = None
    if scope.startswith(ABSOLUTE_WORKSPACE):
        workspace = get_workspace()
        if workspace is None:
            raise Exception("Workspace prefix // used but no WORKSPACE defined.")
        path = workspace / Path(scope[2:])
        name = path.name

        if name == "...":
            type = ScopePart.RECURSIVE

        return ParsedScope(path, type)
    else:
        path = Path(scope)
        if not path.is_absolute():
            path = Path.cwd() / path

    if not path.exists():
        raise Exception(f"Path in scope {scope} does not exist (Expected: {path}).")

    return ParsedScope(path, type)


def print_errors(ctx: Context, errors: Union[Exception, MultipleErrors]):
    if errors:
        print(f"{ctx.colors.ERROR+ctx.colors.BOLD}The execution had errors:{ctx.colors.RESET}\n")

    for error in errors:
        print("---------------")
        print_error(ctx, error)


def print_error(ctx: Context, error):
    if isinstance(error, (PythonScriptFileError, PythonScriptError)):
        print(pretty_makex_file_exception(error, error.location, colors=ctx.colors))
    elif isinstance(error, MakexFileCycleError):
        print(error.pretty(ctx))
    elif isinstance(error, MultipleErrors):
        for error in error.errors:
            print_error(ctx, error)
    elif isinstance(error, (ExecutionError, ExternalExecutionError)):
        if error.location:
            print(pretty_makex_file_exception(error.error, error.location, colors=ctx.colors))
        else:
            print("Execution Error:", error)
    else:
        print(f"{type(error)} Error:")
        print(error)


def _find_files(path, names: set[str]):
    # XXX: use os.scandir for performance
    for entry in os.scandir(path):
        if entry.is_file():
            if entry.name in names:
                yield Path(entry.path, entry.name)
        elif entry.is_dir():
            yield from _find_files(entry, names)


def find_makex_files(path, names):
    for name in names:
        file = path.joinpath(name)
        if file.exists():
            return file

    return None


def early_ui_printer(max_level: int, colors: ColorsNames):
    # we need an early ui before configuration/context is loaded
    def f(message, level=1, error=False):
        if error:
            print(f"{colors.ERROR}ERROR:{colors.RESET} {message}")
            return
        if level <= max_level:
            print(f"{colors.MAKEX}[makex]{colors.RESET} {message}")

    return f


def init_context_standard(cwd, args):
    colors = Colors if args.color else NoColors

    verbosity = args.verbose
    if args.debug:
        verbosity = 3

    # Show early ui if verbose OR debug.
    early_ui = early_ui_printer(verbosity, colors)
    early_ui("Loading configuration files...")

    try:
        files = collect_configurations(cwd, verbose=early_ui)
    except GenericSyntaxError as e:
        print(e.pretty(colors))
        sys.exit(-1)

    if CONFIGURATION_ARGUMENT_ENABLED:
        if args.configuration:
            # append the argument provided configuration file last so it takes priority
            try:
                path = Path(args.configuration).resolve()
            except Exception:
                early_ui(
                    f"Error loading configuration file specified with --configuration argument: {args.configuration}",
                    error=True
                )
                sys.exit(-1)

            path = path.resolve()

            if not path.exists():
                early_ui(
                    f"Configuration file specified with --configuration argument does not exist at {path}",
                    error=True
                )
                sys.exit(-1)

            configuration = read_configuration(path)
            files.configuration_files.append(configuration)

    configuration = files.merged()

    early_ui(f"Merged Configuration: {configuration!r}", level=3)

    current_enviroment = os.environ.copy()

    if False and "VIRTUAL_ENV" in current_enviroment:
        # Fix a bug with getting recursive with venv.
        # TODO: We need to strip the PATH too.
        current_enviroment.pop("VIRTUAL_ENV")

    if configuration.environment:
        early_ui(
            f"Evaluating environment from configuration: {configuration.environment}...", level=1
        )
        try:
            configuration_environment = evaluate_configuration_environment(
                shell=configuration.shell or detect_shell(),
                env=configuration.environment,
                current_enviroment=current_enviroment,
                cwd=cwd,
                run=run,
            )
        except ConfigurationError as e:
            early_ui(e, error=True)
            sys.exit(-1)

        if configuration_environment:
            early_ui(f"Environment from configuration: {configuration_environment}", level=1)
            current_enviroment.update(configuration_environment)

    argument = args.workspace if WORKSPACE_ARGUMENT_ENABLED else None
    workspace = current_workspace(
        cwd,
        files=files,
        argument=argument,
        environment=get_workspace(),
    )

    early_ui(f"Current workspace: {workspace.path}", level=1)

    ctx = Context(
        environment=current_enviroment,
        workspace_object=workspace,
        debug=args.debug,
        color=args.color,
        colors=colors,
        ui=UI(verbosity=verbosity, colors=colors),
        dry_run=getattr(args, "dry", False),
        cpus=args.cpus,
    )
    ctx.workspace_cache.add(workspace)
    try:
        ctx = ctx.with_configuration(configuration, early_ui)
    except CacheError as e:
        early_ui(e, error=True)
        sys.exit(-1)

    return ctx


def try_change_cwd(cwd: str):
    cwd = Path(cwd)
    if not cwd.exists():
        print(f"Error changing to specified directory: Path {cwd} doesn't exist.")
        sys.exit(-1)
    os.chdir(cwd)
    return cwd


def parse_target(
    ctx,
    base: Path,
    string: str,
    check=True,
    syntax=MAKEX_SYNTAX_VERSION,
) -> Optional[TaskReference]:
    """
    A variation of parse target which prints errors
    :param base:
    :param string:
    :param check:
    :return:
    """

    # resolve the path/makefile?:target_or_build_path name
    # return name/Path
    # TODO: SYNTAX_2025: must be fixed here.
    parts = string.split(TASK_PATH_NAME_SEPARATOR, 1)
    check_upwards = False
    if len(parts) == 2:
        if syntax == SYNTAX_2025:
            task_name, _path = parts
        else:
            _path, task_name = parts
        path = Path(_path)

        if not task_name:
            ctx.ui.print(f"Invalid task name {task_name!r} in argument: {string!r}.", error=True)
            sys.exit(-1)

        if path.parts and path.parts[0] == ABSOLUTE_WORKSPACE:
            trace("Translate workspace path %s %s", path, ctx.workspace_object.path)
            path = ctx.workspace_object.path.joinpath(*path.parts[1:])
        elif not path.is_absolute():
            path = base / path
        elif path.is_symlink():
            path = path.readlink()
    else:
        task_name = parts[0]
        path = base
        check_upwards = True

    #trace("Parse target %s -> %s:%s %s %s", string, target, path, parts, path.parts)
    if path.is_dir():
        #if check:
        # check for Build/Makexfile in path
        file = find_makex_files(path, names=ctx.makex_file_names)
        if file is None:
            if check_upwards:
                # task path was omitted; search upwards for makex file
                if not path.is_relative_to(ctx.workspace_path):
                    raise Error(f"Can't run task. Current folder ({path}) is not in workspace.")

                found = None
                for parent in [path] + list(path.parents):
                    file = find_makex_files(parent, names=ctx.makex_file_names)
                    if file is None:
                        continue

                    if parent == ctx.workspace_path:
                        break

                    found = file

                if found is None:
                    raise Error(f"No makex file found in {path} or parent folders.")

                file = found

            else:

                ctx.ui.print(
                    f"Makex file does not exist for task specified: {task_name}", error=True
                )
                for check in ctx.makex_file_names:
                    ctx.ui.print(f"- Checked in {path/check}")
                sys.exit(-1)
    elif path.is_file():
        if DIRECT_REFERENCES_TO_MAKEX_FILES is False:
            raise Error(
                f"Direct references to Makex files not permitted. Path to task is not a folder. Got {path}."
            )
        file = path
    else:
        raise NotImplementedError(f"Unknown file type {path}")

    return TaskReference(task_name, path=file)


def main_clean(args, extra):
    """
    - Clean the specified targets in the makex file in the current working directory
    - (support recursive target specifier ... or //...)
    - or, clean all of them
    """
    targets = args.targets

    to_clean: list[tuple[TaskReference, Path]] = []

    if targets:
        for target in targets:
            pass
    else:
        # simply remove the contents of the children of _output_ directory, and all of its children.
        pass


def main_affected(args: AffectedArgs, extra_args):
    """
    Return all the targets affected by a change in the specified files.

    Allow output to tree format which can be "executed" in dependency order, or a list.

    - name: ""
      path: ""
      requires:
      - name: ""
        path: ""
      - ...

    - name: ""
      path: ""
      requires:
      - name: ""
        path: ""

    :param args:
    :param extra_args:
    :return:
    """
    # find all the makexfile under path
    # add them all to the graph

    # for the specified targets, return the reverse dependencies
    # eg. we change a project, we want to query all dependents and their dependents to rebuild them

    scopes: list[ParsedScope] = [parse_scope(scope) for scope in args.scope or []]

    cwd = Path.cwd()
    ctx = Context()
    ctx.graph = graph = TargetGraph()
    ctx.ui.print(f"Current working directory: {ctx.colors.BOLD}{cwd}{ctx.colors.RESET}")

    for scope in scopes:
        for makefile in _find_files(scope.path, names={"Makexfile"}):
            result = parse_makefile_into_graph(ctx, makefile, graph)

    if len(args.paths) == 1 and args.paths[0] == "-":
        paths = [Path(line) for line in sys.stdin.readlines()]
    else:
        paths = [Path(path) for path in args.paths]

    # start an executor in analysis mode to evaluate tasks
    executor = Executor(ctx, workers=args.threads, force=True, analysis=True)

    # evaluate all the targets we've collected into graph 2.
    executor.execute_targets(ctx.graph.get_all_tasks())

    # query the evaluated task graph for the specified paths and which targets they are required by
    graph = executor.graph_2
    affected_tasks = list(
        graph.get_affected(paths, scopes=list(map(operator.attrgetter("path"), scopes)))
    )

    for task in affected_tasks:
        print(task)


def main_get_path(args, extra):
    """
    Return build path of specified of target
    :param args:
    :return:
    """
    cwd = Path.cwd()
    ctx = init_context_standard(cwd, args)
    ref = parse_target(ctx, cwd, args.task)

    #debug("Current environment: %s", pformat(os.environ.__dict__, indent=2))

    if ref is None:
        print(f"Invalid task reference: {args.task!r}")
        sys.exit(-1)

    target_input = ref.path

    # assume the default/detected
    workspace = ctx.workspace_object

    if args.real:
        workspace = which_workspace(workspace.path, target_input)

    obj = get_build_path(
        objective_name=ref.name,
        variants=[],
        input_directory=target_input.parent,
        build_root=ctx.cache,
        workspace=workspace.path,
        workspace_id=workspace.id,
        output_folder=ctx.output_folder_name,
    )

    # TODO: allow getting the path of a specific output file

    path, link = obj

    if args.real:
        print(path)
        sys.exit(0)

    print(link)
    sys.exit(0)


def main_get_inputs(args):
    """
    return the [file] inputs of targets (and optionally recursively)
    :param args:
    :return:
    """
    pass


def main_get_outputs(args):
    """
    Return the output files of target/path (optionally recursively).

    :param args:
    :return:
    """
    cwd = Path.cwd()
    ctx = init_context_standard(cwd, args)

    target = parse_target(ctx, cwd, args.target)
    ctx.graph = graph = TargetGraph()
    ctx.ui.print(f"Current working directory: {ctx.colors.BOLD}{cwd}{ctx.colors.RESET}")

    ctx.ui.print(f"Loading makex file at {target.path}")

    result = parse_makefile_into_graph(ctx, target.path, graph)

    if result.errors:
        print_errors(ctx, result.errors)
        sys.exit(-1)

    t = graph.get_target(target)
    if t is None:
        ctx.ui.print(
            f"Task \"{ctx.colors.BOLD}{target.name}{ctx.colors.RESET}\" not found in {target.path}",
            error=True
        )
        sys.exit(-1)

    # XXX: don't execute anything, evaluate the target outputs manually
    executor = Executor(ctx, workers=1, force=args.force)
    evaluated, errors = executor._evaluate_target(t)

    if len(errors):
        print_errors(ctx, errors)
        sys.exit(-1)

    if args.output_names:
        paths = []
        for output_name in args.output_names:
            output = evaluated.outputs.get(output_name)
            paths.append(output.path)
        print(" ".join(paths))
    else:
        for output in evaluated.outputs:
            print(output.path)


def main_targets(args, extra_args):
    # Fast function to print targets of specified directory or makex file.
    cwd = Path.cwd()

    #if args.directory:
    #    cwd = try_change_cwd(args.directory)

    ctx = init_context_standard(cwd, args)

    targets = []

    path = args.path

    # TODO: SYNTAX_2025: fix here.
    target_name = None
    if path:
        if path.find(TASK_PATH_NAME_SEPARATOR) > -1:
            path, target_name = path.rsplit(TASK_PATH_NAME_SEPARATOR, 1)

        if path.startswith("//"):
            _path = ctx.workspace_path / path[2:]
        elif not path and target_name:
            _path = cwd
        else:
            _path = Path(path)
            if not _path.is_absolute():
                _path = cwd / _path
    else:
        _path = cwd

    file = find_makex_files(_path, ctx.makex_file_names)

    if not file:
        return sys.exit(-1)

    ctx.graph = graph = TargetGraph()

    directory = file.parent
    workspace_path = directory.relative_to(ctx.workspace_path)
    cwd_relative_path = _path.relative_to(cwd)
    if cwd_relative_path.name == "":
        cwd_relative_path = ""

    #result = parse_makefile_into_graph(ctx, file, ctx.graph)

    prefix = ""
    if args.prefix:
        prefix = ":"
    end = "\n"

    for name, target in _yield_targets(ctx, file, ctx.graph):
        #for name, target in result.makex_file.targets.items():
        if args.paths == "workspace":
            #workspace_path = target.path_input()
            print(f"//{workspace_path}:{name}", end=end)
        elif args.paths == "absolute":
            #workspace_path = target.path_input().resolved.relative_to(target.workspace.path)
            print(f"ABS:{target.path_input()}:{name}", end=end)
        elif args.paths == "relative":
            #workspace_path = target.path_input().resolved.relative_to(target.workspace.path)
            print(f"REL:{cwd_relative_path}:{name}", end=end)
        elif args.paths is None:
            print(format_locator(name, syntax=ctx.makex_syntax_version), end=end)


def _yield_targets(ctx, file, graph):
    result = parse_makefile_into_graph(ctx, file, graph)

    for name, target in result.makex_file.targets.items():
        yield name, target


def _find_makefile_and_yield(ctx, directory):
    file = find_makex_files(directory, ctx.makex_file_names)

    if not file:
        return None

    yield from _yield_targets(ctx, file, ctx.graph)


def main_workspace(args, extra_args):
    # Fast function to print targets.
    # XXX: this is used in bash completions and should return early.
    cwd = Path.cwd()

    if args.path:
        # change to the path and let initialization detect the workspace.
        cwd = try_change_cwd(args.path)

    ctx = init_context_standard(cwd, args)
    print(ctx.workspace_path)


def main_complete(args, extra_args):
    """
    TODO: rename to shell-complete

    Complete the specified argument (path/target/etc).

    :param args:
    :param extra_args:
    :return:
    """
    # XXX: this is used in bash completions and should return fast/early.
    cwd = Path.cwd()

    #if args.directory:
    #    cwd = try_change_cwd(args.directory)

    ctx = init_context_standard(cwd, args)
    ctx.graph = graph = TargetGraph()

    string = args.string or ""

    parts = string.rsplit(TASK_PATH_NAME_SEPARATOR, 1)

    target_name = ""

    has_target_marker = False
    if len(parts) == 2:
        if ctx.makex_syntax_version == SYNTAX_2025:
            target_name, path = parts
        else:
            path, target_name = parts
        has_target_marker = True
    else:
        if ctx.makex_syntax_version == SYNTAX_2025:
            path = parts[0]
        else:
            target_name = parts[0]
            path = cwd

    def escape_print(string):
        print(f'''{string}''')

    # TODO: SYNTAX_2025: fix here.
    def print_task(name, path=None):
        locator = format_locator(name, path)
        print(locator)

    escape_print(f"mark:{string.replace('/','__')}")
    if not path:

        if target_name:
            for name, target in _find_makefile_and_yield(ctx, cwd):
                if has_target_marker:
                    if name.startswith(target_name):
                        print_task(name)
                else:
                    print_task(name)
        else:
            for name, target in _find_makefile_and_yield(ctx, cwd):
                print_task(name)
        # checking the cwd
        #print(f":NOPATH_TARGETS-{target}-{len(target)}")

        if has_target_marker:
            pass
        else:
            for entry in sorted(os.scandir(cwd), key=lambda x: x.name):
                if not entry.is_dir():
                    continue
                print_task(f"{entry.name}")
    elif path.startswith("//"):

        workspace_path_string = path[2:]
        normalized_path = normpath(workspace_path_string)
        has_ending_slash = workspace_path_string.endswith("/") is True
        workspace_path = Path(normalized_path)
        is_root = len(workspace_path.parts) == 0

        if is_root:
            # print targets at root of workspace
            #print("Targets of ", ctx.workspace_path)
            workspace_absolute_path = ctx.workspace_path
        else:
            workspace_absolute_path = ctx.workspace_path / workspace_path

        if workspace_absolute_path.exists():

            # print any targets
            target_prefix = f"//{workspace_path}" if not is_root else "//"

            if not has_ending_slash:
                #print(f"{prefix}:EXXI")
                # check the path for any default makexfiles/targets
                if target_name:
                    for name, target in _find_makefile_and_yield(ctx, workspace_absolute_path):
                        if has_target_marker:
                            if name.startswith(target_name):
                                print_task(name, target_prefix)
                        else:
                            print_task(name, target_prefix)

                if is_root is False and target_prefix:
                    escape_print(f"{target_prefix}/")

            # print any subdirectories
            if has_ending_slash or is_root:
                target_prefix = f"//{workspace_path}" if workspace_path.name else "/"
                for entry in os.scandir(workspace_absolute_path):
                    if not entry.is_dir():
                        continue
                    escape_print(f"{target_prefix}/{entry.name}")

        else:
            name = workspace_absolute_path.name
            search_parent = workspace_absolute_path.parent
            parent = workspace_path.parent

            if is_root:
                prefix = "//"
            else:
                prefix = f"//{parent}" if parent.name else "/"

            # try to complete the directory
            for entry in os.scandir(search_parent):
                if not entry.is_dir():
                    continue

                if entry.name.startswith(name):
                    escape_print(f"{prefix}/{entry.name}")

    elif path.startswith("/"):
        # we have an absolute path
        has_ending_slash = path[1:].endswith("/") is True
        absolute_path = normpath(path)
        absolute_path = Path(absolute_path)
        absolute_path_parent = absolute_path.parent
        is_root = len(absolute_path.parts) == 1

        if is_root:
            absolute_path_parent = Path("/")

        if absolute_path.exists():
            target_prefix = f"{absolute_path}" if is_root is False else ""
            if is_root is False and has_ending_slash is False:
                escape_print(f"{target_prefix}/")

            if target_name:
                for name, target in _find_makefile_and_yield(ctx, absolute_path):
                    if has_target_marker:
                        if name.startswith(target_name):
                            print_task(name, target_prefix)
                    else:
                        print_task(name, target_prefix)

            if has_ending_slash or is_root:
                # list the specific subdirectory
                for entry in os.scandir(absolute_path):
                    if not entry.is_dir():
                        continue

                    escape_print(f"{target_prefix}/{entry.name}")

        else:
            # list the parent
            for entry in _scandir_check_prefix(absolute_path_parent, absolute_path.name):
                print(entry.path)

    else:
        # we have a relative path
        has_ending_slash = path.endswith("/")
        path = normpath(path)
        relative_path = Path(path)
        absolute_path = cwd / relative_path
        absolute_path_parent = absolute_path.parent

        if has_ending_slash:
            # print the subdirectory
            for entry in os.scandir(absolute_path):
                if not entry.is_dir():
                    continue
                escape_print(f"{relative_path}/{entry.name}")
            pass
        else:
            if absolute_path.exists():
                target_prefix = relative_path.as_posix()
                escape_print(f"{target_prefix}/")
                # print any targets
                for name, target in _find_makefile_and_yield(ctx, absolute_path):
                    if has_target_marker:
                        if name.startswith(target_name):
                            print_task(name, target_prefix)
                    else:
                        print_task(name, target_prefix)
            else:
                for entry in _scandir_check_prefix(absolute_path_parent, absolute_path.name):
                    escape_print(f"{entry.name}")


def main_completions(args, extra_args):
    # XXX: Performance: Do a late import shtab because we probably don't need most of the time.
    HAS_SHTAB = False
    try:
        import shtab
        HAS_SHTAB = True
    except ImportError:
        pass

    if args.file:
        file = Path(args.file).expanduser().resolve(strict=False)
    else:
        file = None

    output = sys.stdout
    if file:
        file.parent.mkdir(parents=True, exist_ok=True)
        try:
            output = file.open("w")
        except PermissionError:
            print(f"Error opening the output file. Permission denied: {file}")
            sys.exit(-1)

    if args.internal is False and HAS_SHTAB is False:
        COMPLETIONS_PACKAGE = "makex.data.completions"
        resource_name = f"makex.{args.shell}"
        # load static completions from data directory
        if not importlib.resources.is_resource(COMPLETIONS_PACKAGE, resource_name):
            print(
                f"Error: Could not find static shell script for {resource_name} in {COMPLETIONS_PACKAGE}."
            )
            sys.exit(-1)
        print(importlib.resources.read_text(COMPLETIONS_PACKAGE, resource_name), file=output)
        sys.exit(-1)
    else:
        if HAS_SHTAB is False:
            print("shtab is not installed. pip install shtab")
            sys.exit(-1)

        from makex._shtab import PREAMBLE
        shell = args.shell
        _parser = parser(documentation=False)
        script = shtab.complete(_parser, shell=shell, preamble=PREAMBLE)
        print(script, file=output)

    return 0


def _scandir_check_prefix(path, prefix):
    for entry in os.scandir(path):
        if not entry.is_dir():
            continue

        if entry.name.startswith(prefix):
            yield entry


def main_version(args, extra_args):
    print(VERSION)


def main_run(args, extra_args):
    cwd = Path.cwd()

    if args.directory:
        cwd = try_change_cwd(args.directory)

    ctx = init_context_standard(cwd, args)

    debug("Current content: %s", ctx)

    targets = []

    for target in args.tasks:
        ref = parse_target(ctx, cwd, target)
        targets.append(ref)

    ctx.graph = graph = TargetGraph()
    ctx.ui.print(f"Current working directory: {ctx.colors.BOLD}{cwd}{ctx.colors.RESET}")
    for target in targets:

        ctx.ui.print(f"Loading makex file at {target.path}")

        result = parse_makefile_into_graph(ctx, target.path, graph)

        if result.errors:
            print_errors(ctx, result.errors)
            sys.exit(-1)

    targets_to_run = []

    for target in targets:
        t = graph.get_target(target)
        if t is None:
            ctx.ui.print(
                f"Task \"{ctx.colors.BOLD}{target.name}{ctx.colors.RESET}\" not found in {target.path!r}",
                error=True
            )
            sys.exit(-1)

        targets_to_run.append(t)

    ctx.ui.print(f"Executing {len(targets_to_run)} tasks...")

    # TODO: SYNTAX_2025: fix here
    for target in targets_to_run:
        input = target.path_input()

        if input.is_relative_to(ctx.workspace_path):
            input = input.relative_to(ctx.workspace_path)
            input = ABSOLUTE_WORKSPACE + input.as_posix()
            ctx.ui.print(f"- {format_locator(target.name, input, syntax=ctx.makex_syntax_version)}")
        else:
            input = ABSOLUTE_WORKSPACE + input.as_posix()
            ctx.ui.print(f"- {format_locator(target.name, input, syntax=ctx.makex_syntax_version)}")

    # XXX: Currently set to one to avoid much breakage. Things are fast enough, for now.
    workers = args.cpus
    executor = Executor(ctx, workers=workers, force=args.force)

    try:
        executed, errors = executor.execute_targets(*targets_to_run)

        if len(errors):
            print_errors(ctx, errors)
            sys.exit(-1)

    except KeyboardInterrupt as e:
        executor.stop.set()
        _kill_running_processes()
        sys.exit(-1)

    except IOError as e:
        exc_info = sys.exc_info()
        traceback.print_exception(*exc_info)
        ctx.ui.print(f"There was an IO Error: {e} ({e.filename})", error=True)
        sys.exit(-1)

    except Exception as e:
        exc_info = sys.exc_info()
        traceback.print_exception(*exc_info)
        sys.exit(-1)


COMMANDS = {
    "run": main_run,
    "path": main_get_path,
    "tasks": main_targets,
    "workspace": main_workspace,
    "complete": main_complete,
    "completions": main_completions,
    "version": main_version,
    "outputs": main_get_outputs
}


def main():

    signal.signal(signal.SIGINT, _handle_signal_interrupt)
    signal.signal(signal.SIGTERM, _handle_signal_terminate)

    args, extra_args = parser(documentation=False).parse_known_args()

    if args.python_audit:
        events = set(args.python_audit)

        def audit(event, args):
            if event in events:
                print(f'audit: {event} with args={args}')

        sys.addaudithook(audit)

    level = logging.NOTSET

    #if args.verbose >= 1:
    #    level = logging.INFO

    if args.debug:
        level = logging.TRACE

    args.color = is_color_enabled(args.color)

    initialize_logging(level=level, color=args.color)

    profile_output = None
    if args.profile:
        if args.profile != "-":
            profile_output = Path(args.profile)

        if args.profile_mode == "cprofile":
            import cProfile

            #import pstats
            profiler = cProfile.Profile()
            profiler.enable()
        elif args.profile_mode == "yappi":
            import yappi
            yappi.set_clock_type("wall") # Use set_clock_type("wall") for wall time
            yappi.start()

    try:
        if TASK_PATH_NAME_SEPARATOR in args.command:
            # handle running a target with the second argument to makex
            # e.g. makex :target
            function = main_run
            extra_args = args.command + extra_args
        else:
            function = args.command_function

        function(args, extra_args)
    finally:
        if args.profile:
            if args.profile_mode == "cprofile":
                profiler.disable()
            elif args.profile_mode == "yappi":
                yappi.stop()

            #return pstats.Stats(profiler)
            if profile_output:
                if args.profile_mode == "cprofile":
                    profiler.dump_stats(profile_output)
                elif args.profile_mode == "yappi":
                    if profile_output.name.endswith(".callgrind"):
                        yappi.get_func_stats().save(profile_output, "callgrind")
                    else:
                        yappi.get_func_stats().save(profile_output, "pstat")
            else:
                if args.profile_mode == "cprofile":
                    profiler.print_stats()
                elif args.profile_mode == "yappi":
                    yappi.get_func_stats().print_all()
                    yappi.get_thread_stats().print_all()


if __name__ == "__main__":
    main()
