# Copyright 2025 Evangelos Kassos
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
import subprocess

logger = logging.getLogger(__name__)

SANS_FONT = "Helvetica Neue"
SANS_FONT_BOLD = "Helvetica Neue Bold"
MONO_FONT = "Menlo"
EMOJI_FONT = "Apple Color Emoji"
UNICODE_FONT = "Arial Unicode MS"
HEADER_FOOTER_FONT = "SF Compact Display"
FONT_TROUBLESHOOTING_URL = (
    "https://github.com/ekassos/swift-book-pdf/wiki/Troubleshooting"
)


class FontConfig:
    def __init__(
        self,
        sans_font: str = SANS_FONT,
        sans_font_bold: str = SANS_FONT_BOLD,
        mono_font: str = MONO_FONT,
        emoji_font: str = EMOJI_FONT,
        unicode_font: str = UNICODE_FONT,
        header_footer_font: str = HEADER_FOOTER_FONT,
    ):
        self.sans_font = sans_font
        self.sans_font_bold = sans_font_bold
        self.mono_font = mono_font
        self.emoji_font = emoji_font
        self.unicode_font = unicode_font
        self.header_footer_font = header_footer_font

    def check_font_availability(self) -> None:
        fonts = [
            self.sans_font,
            self.sans_font_bold,
            self.mono_font,
            self.emoji_font,
            self.unicode_font,
            self.header_footer_font,
        ]
        try:
            result = subprocess.run(
                ["luaotfload-tool", "--list=*"], capture_output=True, text=True
            )
            logger.debug(f"Available fonts:\n{result.stdout}")
            available_fonts = result.stdout.lower()
            for font in fonts:
                if font.lower() not in available_fonts:
                    logger.debug(f'Font "{font}" is not accessible by LuaTeX.')
                    raise ValueError(
                        f'Can\'t build The Swift Programming Language book: Font "{font}" is not accessible by LuaTeX. See: {FONT_TROUBLESHOOTING_URL}'
                    )
                else:
                    logger.debug(f'Font "{font}" is accessible by LuaTeX.')
        except FileNotFoundError:
            raise ValueError(
                "Can't build The Swift Programming Language book: luaotfload-tool not found. Ensure LuaTeX is installed."
            )
