from base_aux.aux_types.m2_info import *
from base_aux.versions.m1_block import *
from base_aux.aux_text.m6_nest_repr_clsname_str import *


# =====================================================================================================================
def _explore_other():
    # EXPLORE VARIANTS ----------------------------------------------
    # 1=PACKAGING.version ---------
    from packaging import version
    ObjectInfo(version.parse(str((1,2,3)))).print()

    result = version.parse("2.3.1") < version.parse("10.1.2")

    ObjectInfo(version.parse("1.2.3")).print()
    print(result)
    print()

    # 2=PKG_RESOURCES.parse_version ---------
    from pkg_resources import parse_version         # DEPRECATED!!!
    parse_version("1.9.a.dev") == parse_version("1.9a0dev")


    import sys
    print(sys.winver)
    print(sys.version_info)
    print(tuple(sys.version_info))

    result = sys.version_info > (2, 7)
    print(result)


# =====================================================================================================================
TYPE__VERSION_DRAFT = Union[TYPE__VERSION_BLOCK_ELEMENTS_DRAFT,  TYPE__VERSION_BLOCKS_FINAL, 'Version', Any]


# =====================================================================================================================
class Version(NestCmp, NestRepr__ClsName_SelfStr):
    """
    NOTE
    ----
    VERSION - SPLIT DOTS!
    BLOCK - SPLIT ELEMENTS!

    :ivar SOURCE: try to pass parsed value! it will try to self-parse in _prepare_string, but make it ensured on your own!
    """
    SOURCE: Any
    PREPARSE: str = None
    BLOCKS: TYPE__VERSION_BLOCKS_FINAL = ()

    RAISE: bool = True

    def __init__(self, source: Any, preparse: str = None, _raise: bool = None) -> None | NoReturn:
        if preparse is not None:
            self.PREPARSE = preparse

        if _raise is not None:
            self.RAISE = _raise

        self.SOURCE = source

        self._prepare_source()
        self._parse_blocks()

    # -----------------------------------------------------------------------------------------------------------------
    def _prepare_source(self) -> str:
        """
        ONLY PREPARE STRING FOR CORRECT SPLITTING BLOCKS - parsing blocks would inside VersionBlock
        """
        if isinstance(self.SOURCE, (list, tuple)):
            result = ".".join([str(block) for block in self.SOURCE])
        else:
            result = str(self.SOURCE)

        result = result.lower()

        # PREPARSE -----
        if self.PREPARSE:
            new = TextAux(result).search__group(self.PREPARSE)
            if new:
                result = new

        # CUT ---------
        for pattern in PatVersion.VERSION_IN_BRACKETS:
            match = re.search(pattern, result)
            if match:
                result = match[1]
                break

        if "," in result and "." in result and self.RAISE:
            raise Exx__Incompatible(result)
        # else:
        #     result = ""

        for pattern in PatVersion.VALID_BRACKETS:
            if re.search(pattern, result) and self.RAISE:
                raise Exx__Incompatible(f"{pattern=}/{result=}")

        result = re.sub(r"\A\D+", "", result)   # ver/version
        result = re.sub(r",+", ".", result)
        result = re.sub(r"\.+", ".", result)
        result = result.strip(".")

        self.SOURCE = result
        return self.SOURCE

    def _parse_blocks(self) -> TYPE__VERSION_BLOCKS_FINAL:
        blocks_list__str = str(self.SOURCE).split(".")

        # RESULT -----------
        result = []
        for item in blocks_list__str:
            if not item:
                continue

            try:
                block = VersionBlock(item)
                result.append(block)
            except Exception as exx:
                if self.RAISE:
                    raise Exx__Incompatible(exx)
                else:
                    return ()

        self.BLOCKS = tuple(result)
        return self.BLOCKS

    # -----------------------------------------------------------------------------------------------------------------
    def __str__(self):
        return ".".join([str(block) for block in self.BLOCKS])

    def __bool__(self):
        if len(self) == 0:
            return False
        for block in self.BLOCKS:
            if block != 0:
                return True
        return False
        # else:
        #     return self != "0"

    def __len__(self) -> int:
        return len(self.BLOCKS)

    def __getitem__(self, item: int) -> VersionBlock | None:
        try:
            return self.BLOCKS[item]
        except:
            return

    def __iter__(self):
        yield from self.BLOCKS

    # -----------------------------------------------------------------------------------------------------------------
    @property
    def MAJOR(self) -> VersionBlock | None:
        return self[0]

    @property
    def MINOR(self) -> VersionBlock | None:
        return self[1]

    @property
    def MICRO(self) -> VersionBlock | None:
        return self[2]

    # -----------------------------------------------------------------------------------------------------------------
    def __cmp__(self, other: TYPE__VERSION_DRAFT) -> int | NoReturn:
        if not bool(self) and not bool(other):
            return 0

        other = self.__class__(other, _raise=self.RAISE)

        if not bool(self) and not bool(other):
            return 0

        # equel ----------------------
        if str(self) == str(other):
            return 0

        # by elements ----------------
        for block_1, block_2 in zip(self, other):
            if block_1 == block_2:
                continue
            else:
                return int(block_1 > block_2) or -1

        # final - longest ------------
        return int(len(self) > len(other)) or -1


# =====================================================================================================================
