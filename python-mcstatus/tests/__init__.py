# SPDX-FileCopyrightText: 2023-present Duve3 <Duv3tabest@gmail.com>
#
# SPDX-License-Identifier: MIT
import sys
sys.path.append('..')

from src.python_mcstatus import statusJava, statusBedrock  # noqa -- it should work because of sys.path.append("..")


def JavaTest():
    host = "mc.hypixel.net"
    port = 25565

    print("-----------", "STATUS JAVA:", statusJava(host, port), sep="\n")


def BedrockTest():
    host = "play.cubecraft.net"
    port = 19132

    print("-----------", "STATUS BEDROCK:", statusBedrock(host, port), sep="\n")


if __name__ == "__main__":
    JavaTest()
    BedrockTest()

