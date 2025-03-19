"""Parser module to parse gear config.json."""

from typing import Tuple

from flywheel_gear_toolkit import GearToolkitContext

from fw_gear_deid_inplace.utils import RunConfig


# This function mainly parses gear_context's config.json file and returns relevant
# inputs and options.
def parse_config(
    gear_context: GearToolkitContext,
) -> Tuple[str, str, str, str, bool, str, RunConfig]:
    """Parses the gear context

    Returns:
        str: Input file path
        str: Input file flywheel ID
        str: deid_profile path
        str: subject_csv path
        bool: if gear log debugging is true or false.
        str: tag prefix to append to file
        RunConfig: Contains the run config
    """

    debug = gear_context.config.get("debug")
    subject_csv_path = gear_context.get_input_path("subject-csv")
    tag = gear_context.config.get("tag")

    input_file_object = gear_context.get_input("input-file")

    deid_profile = gear_context.get_input_path("deid-profile")
    input_file_path = gear_context.get_input_path("input-file")

    input_file_id = input_file_object.get("object", {}).get("file_id", "")

    delete_original = gear_context.config.get("delete-original")

    run_config = RunConfig(
        delete_original=delete_original, output_dir=gear_context.output_dir
    )

    return (
        input_file_path,
        input_file_id,
        deid_profile,
        subject_csv_path,
        debug,
        tag,
        run_config,
    )
