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

import os

from tqdm import trange
from swift_book_pdf.config import Config
from swift_book_pdf.latex import LaTeXConverter
from swift_book_pdf.pdf import PDFConverter
from swift_book_pdf.preamble import generate_preamble
from swift_book_pdf.toc import TableOfContents


class Book:
    def __init__(self, config: Config):
        self.config = config
        self.toc = TableOfContents(config.root_dir, config.toc_file_path)
        self.converter = LaTeXConverter(config)

    def process_files_in_order(self, latex_file_path: str):
        latex = generate_preamble(self.config.rendering_mode)
        # TODO: Use the version to generate a cover page
        toc_latex, _ = self.toc.generate_toc_latex(converter=self.converter)
        latex += toc_latex + "\n"
        for tag in self.toc.doc_tags:
            chapter_metadata = self.toc.chapter_metadata.get(tag.lower())
            if chapter_metadata:
                file_path = chapter_metadata.file_path
            if file_path:
                latex_content = self.converter.generate_latex(file_path)
                latex += latex_content + "\n"
            else:
                self.config.logger.warning(
                    f"Warning: No file found for tag <doc:{tag}>, skipping..."
                )
        latex += r"\end{document}"
        with open(latex_file_path, "w", encoding="utf-8") as f:
            f.write(latex)

    def process(self):
        latex_file_path = os.path.join(self.config.temp_dir, "inner_content.tex")
        self.process_files_in_order(latex_file_path)
        self.config.logger.info("Creating PDF...")
        converter = PDFConverter(self.config)
        for _ in trange(self.config.typesets, leave=False):
            converter.convert_to_pdf(latex_file_path)

        temp_pdf_path = os.path.join(self.config.temp_dir, "inner_content.pdf")
        if not os.path.exists(temp_pdf_path):
            self.config.logger.error(f"PDF file not found: {temp_pdf_path}")
            return

        os.rename(temp_pdf_path, self.config.output_path)
        self.config.logger.info(f"PDF saved to {self.config.output_path}")
