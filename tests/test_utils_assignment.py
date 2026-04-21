from restfly._utils import assign_annotations


def test_assign_annotations():
    class Test:
        def __init__(self, obj):
            self.obj = obj

        a: int = 1

    class Base:
        t: Test
        _t: Test
        x: int
        z: int = 1

    b = Base()
    assign_annotations(b, Test)
    assert hasattr(b, "t")
    assert hasattr(b.t, "obj") and b.t.obj == b
    assert not hasattr(b, "_t")
    assert not hasattr(b, "x")
    assert hasattr(b, "z") and b.z == 1
