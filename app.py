"""Create entry."""
# pylint: disbale=invalid-name
import gradio as gr
import pandas as pd

from about_time import about_time
from aset2pairs import aset2pairs
from cmat2aset import cmat2aset
from logzero import logger
from typing import List, Optional, Union
from hf_model_s_cpu import model_s

from radio_mlbee import __version__
from radio_mlbee.gen_cmat import gen_cmat
from radio_mlbee.utils import text1, text2


def greet(name):
    """Greet."""
    if not name:
        name = "world"
    return "Hello " + name + "!! (coming sooooon...)"


def ml_fn(
    text1: str,
    text2: str,
    split_to_sents: bool = False
) -> pd.DataFrame:
    """Align text1 text2"""
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

    # if split_to_sents: ...  # TODO

    with about_time() as t:
        cmat = gen_cmat(paras1, paras2)
        aset = cmat2aset(cmat)

    _ = len(paras1) + len(paras2)
    av = t.duration / _ * 1000
    logger.info(" %s blocks, took %s, av. %s s/1000 blk", _, t.duration_human, av)

    pairs = aset2pairs(paras1, paras2, aset)
    df = pd.DataFrame(pairs, columns=["text1", "text2", "llh"])

    # return pd.DataFrame([["", "", ""]])
    # return df.to_html()
    return df


mlbee = gr.Interface(
    fn=ml_fn,
    inputs=[
        "textarea",
        "textarea",
        # gr.Checkbox(label="Split to sents?"),
    ],
    outputs="dataframe",
    # outputs="html",
    title=f"radio-mlbee {__version__}",
    description="mlbee rest api on dev ",
    examples=[
        # ["a b", "cd", False],
        # [text1, text2, False],
        [text1[:len(text1//2], text2[:len(text2//2], False],
    ]
)

mlbee.launch(
    show_error=True,
    enable_queue=True,
)
