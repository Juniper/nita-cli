#!/bin/bash
# <*******************
#
# Copyright 2018 Juniper Networks, Inc. All rights reserved.
# Licensed under the Juniper Networks Script Software License (the "License").
# You may not use this script file except in compliance with the License, which is located at
# http://www.juniper.net/support/legal/scriptlicense/
# Unless required by applicable law or otherwise agreed to in writing by the parties, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#
# *******************>
echo ""
echo " >>>> Copying cli.py & nita to /usr/local/bin/"
cp cli.py nita /usr/local/bin/
echo ""
echo " >>>> Adding +x permissions to /usr/local/bin/nita"
echo ""
chmod +x /usr/local/bin/nita
echo " >>>> NITA CLI has been successfully installed!"
echo ""