from __future__ import annotations

import os
import pathlib
import subprocess

from rich.markdown import Markdown
from rich.prompt import Prompt
from rich.rule import Rule
from rich.syntax import Syntax

import coiled

from ..utils import live_panel_print, log_interactions


def xarray_nwm() -> bool | None:
    text1 = Markdown(
        """
## Example: Aggregate 2 TB of geospatial data

NOAA hosts their National Water Model (NWM) on AWS in this bucket

```
s3://noaa-nwm-retrospective-2-1-zarr-pds
```

Let's use Xarray, Dask, and Coiled to churn through this data
and compute a spatial average.\n
"""
    )

    script_basename = "xarray_nwm.py"
    script_path = pathlib.Path(__file__).parent.parent / "scripts" / script_basename
    example_code = Syntax.from_path(str(script_path))

    text2 = """
Next we'll drop you into an IPython terminal to run this code yourself.
When you're done type "exit" to come back here.
"""

    live_panel_print(text1, Rule(style="grey"), example_code, Rule(style="grey"), text2)

    try:
        choice = Prompt.ask(
            "Ready to run this example?",
            choices=["y", "n"],
            default="y",
            show_choices=True,
        )
    except KeyboardInterrupt:
        coiled.add_interaction(action="cli-hello:KeyboardInterrupt", success=False)
        return False

    if choice == "y":
        with log_interactions("example-xarray-nwm"):
            fill = pathlib.Path(__file__).parent.parent / "scripts" / "fill_ipython.py"
            subprocess.run(
                ["ipython", "-i", fill, str(script_path)],
                env={**os.environ, **{"DASK_COILED__TAGS": '{"coiled-hello": "xarray-nwm"}'}},
                check=True,
            )
    else:
        return None

    return True
