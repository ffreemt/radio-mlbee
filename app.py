"""Create entry."""
# pylint: disbale=invalid-name
import os
import time
from pathlib import Path

import gradio as gr
import pandas as pd
from about_time import about_time
from aset2pairs import aset2pairs
from cmat2aset import cmat2aset
from logzero import logger
from seg_text import seg_text

from radio_mlbee import __version__
from radio_mlbee.gen_cmat import gen_cmat
from radio_mlbee.utils import text1, text2

os.environ["TZ"] = "Asia/Shanghai"
try:
    time.tzset()  # type: ignore
except Exception as _:
    logger.warning("time.tzset() error: %s. Probably running Windows, we let it pass.", _)


def greet(name):
    """Greet."""
    if not name:
        name = "world"
    return "Hello " + name + "!! (coming sooooon...)"


def ml_fn(
    text1: str,
    text2: str,
    split_to_sents: bool = False,
    preview: bool = False,
    download_csv: bool = False,
) -> pd.DataFrame:
    """Align multilingual (50+ pairs) text1 text2."""
    text1 = str(text1)
    text2 = str(text2)
    try:
        paras1 = text1.splitlines()
        paras1 = [_.strip() for _ in paras1 if _.strip()]
    except Exception as exc:
        logger.error(" praras.slpitlines() erros: %s, setting to ['']", exc)
        paras1 = [""]
    try:
        paras2 = text2.splitlines()
        paras2 = [_.strip() for _ in paras2 if _.strip()]
    except Exception as exc:
        logger.error(" praras slpitlines erros: %s, setting to ['']", exc)
        paras2 = [""]

    if split_to_sents:  # TODO
        try:
            paras1 = seg_text(paras1)
        except Exception as exc:
            logger.error(exc)
        try:
            paras2 = seg_text(paras2)
        except Exception as exc:
            logger.error(exc)

    with about_time() as t:
        cmat = gen_cmat(paras1, paras2)
        aset = cmat2aset(cmat)

    _ = len(paras1) + len(paras2)
    av = t.duration / _ * 1000
    logger.info(" %s blocks, took %s, av. %s s/1000 blk", _, t.duration_human, av)

    pairs = aset2pairs(paras1, paras2, aset)
    df = pd.DataFrame(pairs, columns=["text1", "text2", "llh"])

    html = None
    if preview:
        html = df.to_html()

    dl_csv = None
    if download_csv:
        filepath = Path("aligned-blocks.csv")
        _ = df.to_csv(index=False)
        dl_csv = filepath.write_text(_, encoding="utf8")

    # return pd.DataFrame([["", "", ""]])
    # return df.to_html()
    return df, html, dl_csv


mlbee = gr.Interface(
    fn=ml_fn,
    inputs=[
        "textarea",
        "textarea",
        gr.Checkbox(label="Split to sents?"),
        gr.Checkbox(label="Preview?"),
        gr.Checkbox(label="Download csv?"),
    ],
    outputs=["dataframe", "html", gr.outputs.File(
        label="Click to download csv",
    )],
    # outputs="html",
    title=f"radio-mlbee {__version__}",
    description="mlbee rest api on dev ",
    examples=[
        # [text1, text2, False],
        [text1[: len(text1) // 5], text2[: len(text2) // 5], False, False, False],
    ],
)

mlbee.launch(
    show_error=True,
    enable_queue=True,
)
