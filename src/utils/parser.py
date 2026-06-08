import os

import numpy as np
import pandas as pd
import peppi_py as pp


def parse_slp(file_path):
    """
    Parses a single .slp file using peppi-py and returns a DataFrame
    containing the relevant state and action information.
    """
    try:
        game = pp.read_slippi(file_path)
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None

    # Identify ports
    players = game.start["players"]
    if len(players) != 2:
        return None  # Only 1v1 for now

    ports = [p["port"] for p in players]

    # We'll create a list of dictionaries, one per frame, per player
    # But for Behavioral Cloning, we want to train for BOTH players (doubling our data)
    # as long as they are "good" players. For now, let's just extract all frames.

    frames_data = []
    num_frames = len(game.frames)

    for i in range(1, num_frames):
        # Frame i-1 (Post) -> State
        # Frame i (Pre) -> Action

        prev_frame = game.frames[i - 1]
        curr_frame = game.frames[i]

        for p_idx, port in enumerate(ports):
            other_port = ports[1 - p_idx]

            p_post_prev = prev_frame["ports"][port]["leader"]["post"]
            o_post_prev = prev_frame["ports"][other_port]["leader"]["post"]

            p_pre_curr = curr_frame["ports"][port]["leader"]["pre"]

            # Basic state features
            row = {
                "frame": i,
                "port": port,
                "char": players[p_idx]["character"],
                "stage": game.start["stage"],
                # Self State (Post-frame i-1)
                "self_x": p_post_prev["position"]["x"].as_py(),
                "self_y": p_post_prev["position"]["y"].as_py(),
                "self_percent": p_post_prev["percent"].as_py(),
                "self_state": p_post_prev["state"].as_py(),
                "self_stocks": p_post_prev["stocks"].as_py(),
                "self_direction": p_post_prev["direction"].as_py(),
                "self_jumps": p_post_prev["jumps_used"].as_py(),
                # Opponent State (Post-frame i-1)
                "opp_x": o_post_prev["position"]["x"].as_py(),
                "opp_y": o_post_prev["position"]["y"].as_py(),
                "opp_percent": o_post_prev["percent"].as_py(),
                "opp_state": o_post_prev["state"].as_py(),
                "opp_stocks": o_post_prev["stocks"].as_py(),
                "opp_direction": o_post_prev["direction"].as_py(),
                # Action (Pre-frame i) - Targets
                "target_joy_x": p_pre_curr["joystick"]["x"].as_py(),
                "target_joy_y": p_pre_curr["joystick"]["y"].as_py(),
                "target_c_x": p_pre_curr["cstick"]["x"].as_py(),
                "target_c_y": p_pre_curr["cstick"]["y"].as_py(),
                "target_buttons": p_pre_curr["buttons"].as_py(),
                "target_l": p_pre_curr["triggers"][
                    "logical"
                ].as_py(),  # Logical trigger value
            }
            frames_data.append(row)

    return pd.DataFrame(frames_data)


if __name__ == "__main__":
    # Test with a dummy path if needed
    pass
