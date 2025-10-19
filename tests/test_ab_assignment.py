from app.services.ab_test import ABTestController, ABPolicy


def test_sticky_assignment():
    ab = ABTestController(ABPolicy(v1_weight=0.5, sticky=True))
    a1 = ab.pick_arm("p1", "a1")
    a2 = ab.pick_arm("p1", "a1")
    assert a1 == a2  # sticky