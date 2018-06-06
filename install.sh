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
echo " >>>> Setting 775 permissions to scripts"
chmod 775 /usr/local/bin/cli.py
chmod 775 /usr/local/bin/nita
echo ""

if [[ "$OSTYPE" == "linux-gnu" ]]; then
    # Linux
    echo " >>>> Generating bash completion script"
    python autocomplete
    echo ""
    echo " >>>> Copying bash_completion.d/nita to /etc/bash_completion.d/"
    cp bash_completion.d/nita /etc/bash_completion.d/
    . /etc/bash_completion.d/nita

elif [[ "$OSTYPE" == "darwin"* ]]; then
    # Mac OSX
    echo " >>>> Generating bash completion script"
    python autocomplete
    echo ""
    echo " >>>> Copying bash_completion.d/nita to $(brew --prefix)/etc/bash_completion.d/"
    cp bash_completion.d/nita $(brew --prefix)/etc/bash_completion.d/
    . $(brew --prefix)/etc/bash_completion.d/nita

elif [[ "$OSTYPE" == "cygwin" ]]; then
    # Cygwin on Windows
    echo " >>>> Generating bash completion script"
    python autocomplete
    echo ""
    echo " >>>> Copying bash_completion.d/nita to /etc/bash_completion.d/"
    cp bash_completion.d/nita /etc/bash_completion.d/
    . /etc/bash_completion.d/nita

else
    # Unknown.
    echo " This is an unknown OS!!!"
fi

echo ""
echo " >>>> NITA CLI has been successfully installed!"
echo ""
