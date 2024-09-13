# SPDX-FileCopyrightText: 2023-present Duve3 <Duv3tabest@gmail.com>
#
# SPDX-License-Identifier: MIT
"""
Sorry for how atrocious this code is. It is here to ensure that the package is working correctly.
"""
import os
os.environ["BASE_MCSTATUS_URL"] = "https://api.mcstatus.io/v2"

import sys
sys.path.append('..')

from src.python_mcstatus import JavaServer, BedrockServer  # noqa -- it should work because of sys.path.append("..")



def JavaTest():
    host = "mc.hypixel.net"
    port = 25565

    hypixl = JavaServer(host, port)

    print("-----------", "STATUS JAVA:", hypixl.get_status(), hypixl.lastValidResponse, sep="\n")

    host = "demo.mcstatus.io"
    query = False
    
    secondary = JavaServer(host, query=query)

    print("-----------", "STATUS JAVA SECONDARY:", secondary.get_status(), secondary.lastValidResponse, sep="\n")

    return hypixl


def BedrockTest():
    host = "play.cubecraft.net"
    port = 19132

    cube = BedrockServer(host, port)
    print("-----------", "STATUS BEDROCK:", cube.get_status(), cube.lastValidResponse, sep="\n")

    host = "demo.mcstatus.io"

    secondary = 

    print("-----------", "STATUS BEDROCK SECONDARY:", statusBedrock(host), sep="\n")

    return cube


if __name__ == "__main__":
    jres = JavaTest()
    bres = BedrockTest()

    print("-----------", "jres vars", vars(jres), sep="\n")
    print("-----------", "bres vars", vars(bres), sep="\n")
