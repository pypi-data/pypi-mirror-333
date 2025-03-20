import requests

from blueness import module

from blue_assistant import NAME
from blue_assistant import env
from blue_assistant.logger import logger

NAME = module.name(__file__, NAME)


def set_light_color(
    username: str,
    light_id: str,
    hue: int,  # 0 to 65535
    saturation: int,  # 0 to 254
    bridge_ip: str = env.HUE_BRIDGE_IP_ADDRESS,
    verbose: bool = False,
) -> bool:
    logger.info(
        "{}.set_light_color({}@{}:{}) -> hue=0x{:x}, saturation=0x{:x}".format(
            NAME,
            username,
            bridge_ip,
            light_id,
            hue,
            saturation,
        )
    )

    # hue-2025-03-13-1xjr1z

    # Construct the API endpoint URL
    url = f"http://{bridge_ip}/api/{username}/lights/{light_id}/state"

    # Prepare the payload with the desired hue and saturation
    payload = {
        "hue": hue,
        "sat": saturation,
    }

    response = requests.put(url, json=payload)

    # https://chat.openai.com/c/6deb94d0-826a-48de-b5ef-f7d8da416c82
    # response.raise_for_status()
    if response.status_code // 100 != 2:
        logger.error(response)
        return False

    if verbose:
        logger.info(response.json())

    return True
