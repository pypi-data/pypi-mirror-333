# !/usr/bin/env python3
# -*- coding: UTF-8 -*-
#
# Copyright (c) 2022 Baidu.com, Inc. All Rights Reserved
#
"""
modify input train parameter yaml
Authors: wanggaofei(wanggaofei03@baidu.com)
Date:    2023-02-29
"""
import os

import bcelogger

from gaea_operator.config.config import KEY_NETWORK_ARCHITECTURE, set_multi_args
from gaea_operator.utils import write_yaml_file

KEY_EPOCH = "num_train_epochs"
KEY_BATCH_SIZE = "per_device_train_batch_size"
KEY_WORKER_NUM = "dataloader_num_workers"


def generate_train_config(
        advanced_parameters: dict,
        pretrain_model_uri: str,
        train_config_name: str
):
    """
    modify parameter by template config
    """
    # 1. modify uncertain parameters
    network_architecture2model_type = {"yijian-mllm-lite": "internvl2"}
    network_architecture = advanced_parameters.pop(KEY_NETWORK_ARCHITECTURE)
    assert network_architecture in network_architecture2model_type, \
        "network_architecture {} is not supported".format(network_architecture)
    advanced_parameters["model_type"] = network_architecture2model_type[network_architecture]
    advanced_parameters["model"] = pretrain_model_uri
    advanced_parameters["train_type"] = "full"

    # 2. save yaml
    bcelogger.info('begin to save yaml. {}'.format(train_config_name))
    args = set_multi_args(advanced_parameters)
    write_yaml_file({"args": args}, os.path.dirname(train_config_name), os.path.basename(train_config_name))
    bcelogger.info('write train config finish.')