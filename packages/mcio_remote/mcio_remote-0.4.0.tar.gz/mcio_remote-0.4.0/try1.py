import typing

import mcio_remote as mcio

# vars_info = {
#     "MCIO_MODE": MCioMode,
#     "MCIO_FRAME_TYPE": FrameType,
#     "MCIO_UNLIMITED_FPS": bool,
#     "MCIO_ACTION_PORT": int,
#     "MCIO_OBSERVATION_PORT": int,
#     "MCIO_HIDE_WINDOW": bool,
#     "MCIO_DO_RETINA_HACK": bool,
#     "MCIO_SYNC_SPEED_TEST": bool,
#     "MCIO_EXP1": bool,
# }


def main() -> None:
    x = typing.get_type_hints(mcio.types.EnvConfig)
    print(x)


if __name__ == "__main__":
    main()
