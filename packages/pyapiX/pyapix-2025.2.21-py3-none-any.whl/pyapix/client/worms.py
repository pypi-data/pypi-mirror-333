# Copyright (c) 2024-2025 Cary Miller
#
# Permission to use, copy, modify, and/or distribute this software for any purpose
# with or without fee is hereby granted, provided that the above copyright notice
# and this permission notice appear in all copies.
# 
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
# REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
# FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT,
# INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS
# OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER
# TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF
# THIS SOFTWARE.

# WoRMS: World Register of Marine Species

from pyapix.tool.api_tools import dynamic_validator, dynamic_call
from .info import local


class config:
    swagger_path = local.swagger.worms
    api_base = local.api_base.worms
    alt_swagger = lambda x: x 
    head_func = lambda endpoint, verb: {}
    validate = lambda params: None


_validator = dynamic_validator(config)
call = dynamic_call(config)
