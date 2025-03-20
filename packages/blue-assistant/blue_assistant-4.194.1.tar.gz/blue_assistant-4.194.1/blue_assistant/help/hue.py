from typing import List

from blue_options.terminal import show_usage, xtra

from blue_assistant import env


def help_set(
    tokens: List[str],
    mono: bool,
) -> str:
    options = xtra("dryrun", mono=mono)

    args = [
        f"[--bridge_ip <{env.HUE_BRIDGE_IP_ADDRESS}>]",
        "[--username <username>]",
        "[--light_id <light_id>]",
        "[--hue <65535>]",
        "[--saturation <254>]",
        "[--verbose 1]",
    ]
    return show_usage(
        [
            "@hue",
            "set",
            f"[{options}]",
        ]
        + args,
        "set hue lights.",
        mono=mono,
    )


help_functions = {
    "set": help_set,
}
