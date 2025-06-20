"""
quart_uploads.file_ext
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Tuple


@dataclass(frozen=True)
class FileExtensions:
    """
    A dataclass for holding file extensions for different file types.
    """
    #: This just contains plain text files (.txt).
    Text: tuple = ('txt',)

    #: This contains various office document formats (.rtf, .odf, .ods,
    # .gnumeric, .abw, .doc, .docx, .xls, .xlsx and .pdf). Note that the
    # macro-enabled versions of Microsoft Office 2007 files are not included.
    Documents = tuple('rtf odf ods gnumeric abw doc docx xls xlsx pdf'.split())

    #: This contains basic image types that are viewable from most browsers
    # (.jpg, .jpe, .jpeg, .png, .gif, .svg, .bmp and .webp).
    Images = tuple('jpg jpe jpeg png gif svg bmp webp'.split())

    #: This contains audio file types (.wav, .mp3, .aac, .ogg,
    # .oga, and .flac).
    Audio = tuple('wav mp3 aac ogg oga flac'.split())

    #: This is for structured data files (.csv, .ini, .json, .plist,
    # .xml, .yaml, and .yml).
    Data = tuple('csv ini json plist xml yaml yml'.split())

    #: This contains various types of scripts (.js, .php, .pl,
    # .py .rb, and .sh). If your Web server has PHP installed
    # and set to auto-run, you might want to add ``php`` to the
    # DENY setting.
    Scripts = tuple('js php pl py rb sh'.split())

    #: This contains archive and compression formats (.gz, .bz2,
    # .zip, .tar, .tgz, .txz, and .7z).
    Archives = tuple('gz bz2 zip tar tgz txz 7z'.split())

    #: This contains nonexecutable source files - those which need to be
    #: compiled or assembled to binaries to be used. They are generally safe to
    #: accept, as without an existing RCE vulnerability, they cannot be
    # compiled, assembled, linked, or executed. Supports C, C++, Ada, Rust, Go
    # (Golang), FORTRAN, D, Java, C Sharp, F Sharp (compiled only), COBOL,
    # Haskell, and assembly.
    Source = (
        'c',
        'cpp',
        'c++',
        'h',
        'hpp',
        'cxx',
        'hxx',
        'hdl',  # C/C++
        'ada',  # ADA
        'rs',  # Rust
        'go',  # Go
        'f',
        'for',
        'f90',
        'f95',
        'f03',  # FORTRAN
        'd',
        'dd',
        'di',   # D
        'java',  # Java
        'hs',  # Haskell
        'cs',  # C Sharp
        'fs',  # F Sharp
        'cbl',
        'cob',  # COBOL
        'asm',
        's'  # Assembly
    )

    #: This contains shared libraries and executable files
    # (.so, .exe and .dll). Most of the time, you will not
    # want to allow this - it's better suited for use with
    # `AllExcept`.
    Executables = tuple('so exe dll'.split())

    @property
    def Defaults(self) -> Tuple[str]:
        """
        Returns the default allowed file extensions.
        It is a combination of text, documents, and
        images.
        """
        return self.Text + self.Documents + self.Images


FILE_EXTENSIONS = FileExtensions()


class All:
    """
    This type can be used to allow all extensions. There is a predefined
    instance named `ALL`.
    """
    def __contains__(self, item: Any) -> bool:
        return True


#: This "contains" all items. You can use it to allow all extensions to be
#: uploaded.
ALL = All()
