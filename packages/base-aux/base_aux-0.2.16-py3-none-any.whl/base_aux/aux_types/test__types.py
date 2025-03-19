import pytest
import sys

from base_aux.aux_types.m1_type_aux import *
from base_aux.base_statics.m3_primitives import *
from base_aux.aux_expect.m1_expect_aux import ExpectAux


# =====================================================================================================================
class Test__1:
    @pytest.mark.parametrize(
        argnames="source, _EXPECTED",
        argvalues=[
            (pytest,      (False, False, False, False, False, True, )),
            (sys,      (False, False, False, False, False, True, )),

            (None,      (True, True, True, False, False, False, )),
            (True,      (True, True, True, True, False, False, )),
            (False,     (True, True, True, True, False, False, )),
            (0,         (False, True, True, True, False, False, )),
            (111,       (False, True, True, True, False, False, )),
            (111.222,   (False, True, True, True, False, False, )),
            ("str",     (False, True, True, True, False, False, )),
            (b"bytes",  (False, True, True, True, False, False, )),

            ((111, ),        (False, True, False, False, True, False, )),
            ([111, ],        (False, True, False, False, True, False, )),
            ({111, },        (False, True, False, False, True, False, )),
            ({111: 222, },   (False, True, False, False, True, False, )),

            (int,       (False, False, False, False, False, False, )),
            (int(1),    (False, True, True, True, False, False, )),
            (str,       (False, False, False, False, False, False, )),
            (str(1),    (False, True, True, True, False, False, )),

            (Exception,     (False, False, False, False, False, False, )),
            (Exception(),   (False, False, False, False, False, False, )),
            (ClsException,  (False, False, False, False, False, False, )),
            (ClsException(), (False, False, False, False,False, False, )),

            (Cls,       (False, False, False, False, False, False, )),
            (Cls(),     (False, False, False, False, False, False, )),
            (ClsInt,    (False, False, False, False, False, False, )),
            (ClsInt(),  (False, True, True, True, False, False, )),    # int() == 0!!!

            (FUNC,                      (False, False, False, False, False, False, )),
            (LAMBDA,                    (False, False, False, False, False, False, )),
            (ClsCallNone,               (False, False, False, False, False, False, )),
            (ClsCallNone(),             (False, False, False, False, False, False, )),
            (ClsCallNone()(),           (True, True, True, False, False, False, )),
            (ClsCall().meth,            (False, False, False, False, False, False, )),
            (ClsFullTypes.attrNone,     (True, True, True, False, False, False, )),
            (ClsFullTypes().attrNone,   (True, True, True, False, False, False, )),

            *[
                (
                    class_i,
                    (False, False, False, False, False, False, )
                ) for class_i in CLASSES__AS_FUNC
            ]
        ]
    )
    def test__check__bool_none(self, source, _EXPECTED):
        victim = TypeAux(source)

        ExpectAux(victim.check__bool_none).check_assert(_EXPECTED[0])
        ExpectAux(victim.check__elementary).check_assert(_EXPECTED[1])
        ExpectAux(victim.check__elementary_single).check_assert(_EXPECTED[2])
        ExpectAux(victim.check__elementary_single_not_none).check_assert(_EXPECTED[3])
        ExpectAux(victim.check__elementary_collection).check_assert(_EXPECTED[4])
        ExpectAux(victim.check__module).check_assert(_EXPECTED[5])





    @pytest.mark.parametrize(
        argnames="source, _EXPECTED",
        argvalues=[
            (None, False),
            (True, False),
            (False, False),
            (0, False),
            (111, False),
            (111.222, False),
            ("str", False),
            (b"bytes", False),

            ((111, ), True),
            ([111, ], True),
            ({111, }, True),
            ({111: 222, }, False),

            (int, False),
            (int(1), False),
            (str, False),
            (str(1), False),

            (Exception, False),
            (Exception(), False),
            (ClsException, False),
            (ClsException(), False),

            (Cls, False),
            (Cls(), False),
            (ClsInt, False),
            (ClsInt(), False),    # int() == 0!!!

            (FUNC, False),
            (LAMBDA, False),
            (ClsCallNone, False),
            (ClsCallNone(), False),
            (ClsCallNone()(), False),
            (ClsCall.meth, False),
            (ClsCall().meth, False),
            (ClsFullTypes.attrNone, False),
            (ClsFullTypes().attrNone, False),

            *[(class_i, False) for class_i in CLASSES__AS_FUNC]
        ]
    )
    def test__check__elementary_collection_not_dict(self, source, _EXPECTED):
        func_link = TypeAux(source).check__elementary_collection_not_dict
        ExpectAux(func_link).check_assert(_EXPECTED)

    # -----------------------------------------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        argnames="source, args, _EXPECTED",
        argvalues=[
            ("str", (True, True), True),
            ("str", (True, False), False),

            (b"bytes", (True, True), True),
            (b"bytes", (True, False), False),

            # -----------------------
            (None, (), False),
            (True, (), False),
            (False, (), False),
            (0, (), False),
            (111, (), False),
            (111.222, (), False),
            ("str", (), True),
            (b"bytes", (), True),

            ((111, ), (), True),
            ([111, ], (), True),
            ({111, }, (), True),
            ({111: 222, }, (), True),
            ({111: 222, }, (True, True), True),
            ({111: 222, }, (False, True), False),

            (int, (), False),
            (int(1), (), False),
            (str, (), True),        # not clear!!!
            (str(1), (), True),

            (Exception, (), False),
            (Exception(), (), False),
            (ClsException, (), False),
            (ClsException(), (), False),

            (Cls, (), False),
            (Cls(), (), False),
            (ClsInt, (), False),
            (ClsInt(), (), False),

            (FUNC, (), False),
            (LAMBDA, (), False),
            (ClsCallNone, (), False),
            (ClsCallNone(),(),  False),
            (ClsCallNone()(), (), False),
            (ClsCall.meth, (), False),
            (ClsCall().meth, (), False),
            (ClsFullTypes.attrNone, (), False),
            (ClsFullTypes().attrNone, (), False),

            # *[(class_i, False) for class_i in CLASSES__AS_FUNC]
        ]
    )
    def test__iterable(self, source, args, _EXPECTED):
        func_link = TypeAux(source).check__iterable
        ExpectAux(func_link, args).check_assert(_EXPECTED)

    @pytest.mark.parametrize(
        argnames="source, _EXPECTED",
        argvalues=[
            (None, False),
            (True, False),
            (False, False),
            (0, False),
            (111, False),
            (111.222, False),
            ("str", False),
            (b"bytes", False),

            (((111, ),), True),
            (([111, ],), True),
            (({111, },), True),
            (({111: 222, },), True),

            (int, False),
            (int(1), False),
            (str, True),        # not clear!!!
            (str(1), False),

            (Exception, False),
            (Exception(), False),
            (ClsException, False),
            (ClsException(), False),

            (Cls, False),
            (Cls(), False),
            (ClsInt, False),
            (ClsInt(), False),

            (FUNC, False),
            (LAMBDA, False),
            (ClsCallNone, False),
            (ClsCallNone(), False),
            (ClsCallNone()(), False),
            (ClsCall.meth, False),
            (ClsCall().meth, False),
            (ClsFullTypes.attrNone, False),
            (ClsFullTypes().attrNone, False),

            # *[(class_i, False) for class_i in CLASSES__AS_FUNC]
        ]
    )
    def test__iterable_not_str(self, source, _EXPECTED):
        func_link = TypeAux(source).check__iterable_not_str
        ExpectAux(func_link).check_assert(_EXPECTED)

    # CALLABLE --------------------------------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        argnames="source, _EXPECTED",
        argvalues=[
            (None, False),
            (True, False),
            (False, False),
            (0, False),
            (111, False),
            (111.222, False),
            ("str", False),
            (b"bytes", False),

            (((111, ),), False),
            (([111, ],), False),
            (({111, },), False),
            (({111: 222, },), False),

            (int, True),
            (int(1), False),
            (str, True),
            (str(1), False),

            (Exception, False),
            (Exception(), False),
            (ClsException, False),
            (ClsException(), False),

            (Cls, False),
            (Cls(), False),
            (ClsInt, True),
            (ClsInt(), False),    # int() == 0!!!

            (FUNC, True),
            (LAMBDA, True),
            (ClsCallNone, False),
            (ClsCallNone(), True),
            (ClsCallNone()(), False),
            (ClsCall.meth, True),
            (ClsCall().meth, True),
            (ClsFullTypes.attrNone, False),
            (ClsFullTypes().attrNone, False),

            *[(class_i, True) for class_i in CLASSES__AS_FUNC]
        ]
    )
    def test__check__callable_func_meth_inst(self, source, _EXPECTED):
        func_link = TypeAux(source).check__callable_func_meth_inst
        ExpectAux(func_link).check_assert(_EXPECTED)

    @pytest.mark.parametrize(
        argnames="source, _EXPECTED",
        argvalues=[
            (None, False),
            (True, False),
            (False, False),
            (0, False),
            (111, False),
            (111.222, False),
            ("str", False),
            (b"bytes", False),

            (((111, ),), False),
            (([111, ],), False),
            (({111, },), False),
            (({111: 222, },), False),

            (int, True),
            (int(1), False),
            (str, True),
            (str(1), False),

            (Exception, False),
            (Exception(), False),
            (ClsException, False),
            (ClsException(), False),

            (Cls, False),
            (Cls(), False),
            (ClsInt, True),
            (ClsInt(), False),    # int() == 0!!!

            (FUNC, True),
            (LAMBDA, True),
            (ClsCallNone, False),
            (ClsCallNone(), False),
            (ClsCallNone()(), False),
            (ClsCall.meth, True),
            (ClsCall().meth, True),
            (ClsFullTypes.attrNone, False),
            (ClsFullTypes().attrNone, False),

            *[(class_i, True) for class_i in CLASSES__AS_FUNC]
        ]
    )
    def test__check__callable_func_meth(self, source, _EXPECTED):
        func_link = TypeAux(source).check__callable_func_meth
        ExpectAux(func_link).check_assert(_EXPECTED)

    @pytest.mark.parametrize(
        argnames="source, _EXPECTED",
        argvalues=[
            (None, False),
            (True, False),
            (False, False),
            (0, False),
            (111, False),
            (111.222, False),
            ("str", False),
            (b"bytes", False),

            (((111, ),), False),
            (([111, ],), False),
            (({111, },), False),
            (({111: 222, },), False),

            (int, True),
            (int(1), False),
            (str, True),
            (str(1), False),

            (Exception, False),
            (Exception(), False),
            (ClsException, False),
            (ClsException(), False),

            (Cls, False),
            (Cls(), False),
            (ClsInt, True),
            (ClsInt(), False),    # int() == 0!!!

            (FUNC, True),
            (LAMBDA, True),
            (ClsCallNone, False),
            (ClsCallNone(), False),
            (ClsCallNone()(), False),
            (ClsCall.meth, True),
            (ClsCall().meth, False),
            (ClsFullTypes.attrNone, False),
            (ClsFullTypes().attrNone, False),

            *[(class_i, True) for class_i in CLASSES__AS_FUNC]
        ]
    )
    def test__check__callable_func(self, source, _EXPECTED):
        func_link = TypeAux(source).check__callable_func
        ExpectAux(func_link).check_assert(_EXPECTED)

    @pytest.mark.parametrize(
        argnames="source, _EXPECTED",
        argvalues=[
            (None, False),
            (True, False),
            (False, False),
            (0, False),
            (111, False),
            (111.222, False),
            ("str", False),
            (b"bytes", False),

            (((111, ),), False),
            (([111, ],), False),
            (({111, },), False),
            (({111: 222, },), False),

            (int, False),
            (int(1), False),
            (str, False),
            (str(1), False),

            (Exception, False),
            (Exception(), False),
            (ClsException, False),
            (ClsException(), False),

            (Cls, False),
            (Cls(), False),
            (ClsInt, False),
            (ClsInt(), False),    # int() == 0!!!

            (FUNC, False),
            (LAMBDA, False),
            (ClsCallNone, False),
            (ClsCallNone(), False),
            (ClsCallNone()(), False),
            (ClsCall.meth, False),
            (ClsCall().meth, True),
            (ClsFullTypes.attrNone, False),
            (ClsFullTypes().attrNone, False),

            *[(class_i, False) for class_i in CLASSES__AS_FUNC]
        ]
    )
    def test__check__callable_meth(self, source, _EXPECTED):
        func_link = TypeAux(source).check__callable_meth
        ExpectAux(func_link).check_assert(_EXPECTED)

    @pytest.mark.parametrize(
        argnames="source, _EXPECTED",
        argvalues=[
            (None, False),
            (True, False),
            (False, False),
            (0, False),
            (111, False),
            (111.222, False),
            ("str", False),
            (b"bytes", False),

            (((111, ),), False),
            (([111, ],), False),
            (({111, },), False),
            (({111: 222, },), False),

            (int, False),
            (int(1), False),
            (str, False),
            (str(1), False),

            (Exception, False),
            (Exception(), False),
            (ClsException, False),
            (ClsException(), False),

            (Cls, False),
            (Cls(), False),
            (ClsInt, False),
            (ClsInt(), False),    # int() == 0!!!

            (FUNC, False),
            (LAMBDA, False),
            (ClsCallNone, False),
            (ClsCallNone(), True),
            (ClsCallNone()(), False),
            (ClsCall.meth, False),
            (ClsCall().meth, False),
            (ClsFullTypes.attrNone, False),
            (ClsFullTypes().attrNone, False),

            *[(class_i, False) for class_i in CLASSES__AS_FUNC]
        ]
    )
    def test__check__callable_inst(self, source, _EXPECTED):
        func_link = TypeAux(source).check__callable_inst
        ExpectAux(func_link).check_assert(_EXPECTED)

    @pytest.mark.parametrize(
        argnames="source, _EXPECTED",
        argvalues=[
            (None, False),
            (True, False),
            (False, False),
            (0, False),
            (111, False),
            (111.222, False),
            ("str", False),
            (b"bytes", False),

            (((111, ),), False),
            (([111, ],), False),
            (({111, },), False),
            (({111: 222, },), False),

            (int, True),
            (int(1), False),
            (str, True),
            (str(1), False),

            (Exception, False),
            (Exception(), False),
            (ClsException, False),
            (ClsException(), False),

            (Cls, False),
            (Cls(), False),
            (ClsInt, True),
            (ClsInt(), False),    # int() == 0!!!

            (FUNC, False),
            (LAMBDA, False),
            (ClsCallNone, False),
            (ClsCallNone(), False),
            (ClsCallNone()(), False),
            (ClsCall.meth, False),
            (ClsCall().meth, False),
            (ClsFullTypes.attrNone, False),
            (ClsFullTypes().attrNone, False),

            *[(class_i, True) for class_i in CLASSES__AS_FUNC]
        ]
    )
    def test__check__callable_cls_as_func_builtin(self, source, _EXPECTED):
        func_link = TypeAux(source).check__callable_cls_as_func_builtin
        ExpectAux(func_link).check_assert(_EXPECTED)

    # -----------------------------------------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        argnames="source, _EXPECTED",
        argvalues=[
            (None, False),
            (True, False),
            (False, False),
            (0, False),
            (111, False),
            (111.222, False),
            ("str", False),
            (b"bytes", False),

            (((111, ),), False),
            (([111, ],), False),
            (({111, },), False),
            (({111: 222, },), False),

            (int, True),
            (int(1), False),
            (str, True),
            (str(1), False),

            (Exception, True),
            (Exception(), False),
            (ClsException, True),
            (ClsException(), False),

            (Cls, True),
            (Cls(), False),
            (ClsInt, True),
            (ClsInt(), False),    # int() == 0!!!

            (FUNC, False),
            (LAMBDA, False),
            (ClsCallNone, True),
            (ClsCallNone(), False),
            (ClsCallNone()(), False),
            (ClsCall.meth, False),
            (ClsCall().meth, False),
            (ClsFullTypes.attrNone, False),
            (ClsFullTypes().attrNone, False),

            *[(class_i, True) for class_i in CLASSES__AS_FUNC]
        ]
    )
    def test__check__class(self, source, _EXPECTED):
        func_link = TypeAux(source).check__class
        ExpectAux(func_link).check_assert(_EXPECTED)

    @pytest.mark.parametrize(
        argnames="source, _EXPECTED",
        argvalues=[
            (None, True),
            (True, True),
            (False, True),
            (0, True),
            (111, True),
            (111.222, True),
            ("str", True),
            (b"bytes", True),

            (((111, ),), True),
            (([111, ],), True),
            (({111, },), True),
            (({111: 222, },), True),

            (int, False),
            (int(1), True),
            (str, False),
            (str(1), True),

            (Exception, False),
            (Exception(), True),
            (ClsException, False),
            (ClsException(), True),

            (Cls, False),
            (Cls(), True),
            (ClsInt, False),
            (ClsInt(), True),    # int() == 0!!!

            (FUNC, False),
            (LAMBDA, False),
            (ClsCallNone, False),
            (ClsCallNone(), True),
            (ClsCallNone()(), True),
            (ClsCall.meth, False),
            (ClsCall().meth, False),
            (ClsFullTypes.attrNone, True),
            (ClsFullTypes().attrNone, True),

            *[(class_i, False) for class_i in CLASSES__AS_FUNC]
        ]
    )
    def test__check__instance(self, source, _EXPECTED):
        func_link = TypeAux(source).check__instance
        ExpectAux(func_link).check_assert(_EXPECTED)

    @pytest.mark.parametrize(
        argnames="source, _EXPECTED",
        argvalues=[
            (None, False),
            (True, False),
            (False, False),
            (0, False),
            (111, False),
            (111.222, False),
            ("str", False),
            (b"bytes", False),

            (((111, ),), False),
            (([111, ],), False),
            (({111, },), False),
            (({111: 222, },), False),

            (int, False),
            (int(1), False),
            (str, False),
            (str(1), False),

            (Exception, False),
            (Exception(), True),
            (ClsException, False),
            (ClsException(), True),

            (Cls, False),
            (Cls(), True),
            (ClsInt, False),
            (ClsInt(), False),    # int() == 0!!!

            (FUNC, False),
            (LAMBDA, False),
            (ClsCallNone, False),
            (ClsCallNone(), True),
            (ClsCallNone()(), False),
            (ClsCall.meth, False),
            (ClsCall().meth, False),
            (ClsFullTypes.attrNone, False),
            (ClsFullTypes().attrNone, False),

            *[(class_i, False) for class_i in CLASSES__AS_FUNC]
        ]
    )
    def test__check__instance_not_elementary(self, source, _EXPECTED):
        func_link = TypeAux(source).check__instance_not_elementary
        ExpectAux(func_link).check_assert(_EXPECTED)

    # -----------------------------------------------------------------------------------------------------------------
    @pytest.mark.parametrize(
        argnames="source, _EXPECTED",
        argvalues=[
            (None, False),
            (True, False),
            (False, False),
            (0, False),
            (111, False),
            (111.222, False),
            ("str", False),
            (b"bytes", False),

            (((111, ),), False),
            (([111, ],), False),
            (({111, },), False),
            (({111: 222, },), False),

            (int, False),
            (int(1), False),
            (str, False),
            (str(1), False),

            (Exception, True),
            (Exception(), True),
            (ClsException, True),
            (ClsException(), True),

            (Cls, False),
            (Cls(), False),
            (ClsInt, False),
            (ClsInt(), False),    # int() == 0!!!

            (FUNC, False),
            (LAMBDA, False),
            (ClsCallNone, False),
            (ClsCallNone(), False),
            (ClsCallNone()(), False),
            (ClsCall.meth, False),
            (ClsCall().meth, False),
            (ClsFullTypes.attrNone, False),
            (ClsFullTypes().attrNone, False),

            *[(class_i, False) for class_i in CLASSES__AS_FUNC]
        ]
    )
    def test__check__exception(self, source, _EXPECTED):
        func_link = TypeAux(source).check__exception
        ExpectAux(func_link).check_assert(_EXPECTED)

    # =================================================================================================================
    @pytest.mark.parametrize(
        argnames="source, parent, _EXPECTED",
        argvalues=[
            ("str", "str", True),
            ("str", str, True),
            (str, "str", True),
            (str, str, True),

            (int, str, False),
            (int, "str", False),

            (111, 111, True),
            (int, 111, True),
            (111, int, True),
            (int, int, True),

            (Exception, Exception, True),
            (Exception(), Exception, True),
            (Exception, Exception(), True),
            (Exception(), Exception(), True),

            (ClsException, Exception, True),
            (ClsException(), Exception, True),
            (ClsException, Exception(), True),
            (ClsException(), Exception(), True),

            (Exception, ClsException, False),      # REMEMBER! not clear!
            (Exception(), ClsException, False),    # REMEMBER! not clear!
            (Exception, ClsException(), False),    # REMEMBER! not clear!
            (Exception(), ClsException(), False),  # REMEMBER! not clear!

            (Cls, Cls, True),
            (Cls, Cls(), True),
            (Cls(), Cls, True),
            (Cls(), Cls(), True),

            (FUNC, Cls, False),
            (FUNC, Cls(), False),
        ]
    )
    def test__check__nested__by_cls_or_inst(self, source, parent, _EXPECTED):
        func_link = TypeAux(source).check__nested__by_cls_or_inst
        ExpectAux(func_link, parent).check_assert(_EXPECTED)


# =====================================================================================================================
