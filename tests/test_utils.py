from setup_mock import TestDB
from DefiOSPython.utils import isfloat, remove_dups_by_id


class TestISFloat(TestDB):
    def test_success_float(self):
        self.assertEqual(isfloat(3.6), True)

    def test_success_int(self):
        self.assertEqual(isfloat(3), True)

    def test_success_string(self):
        self.assertEqual(isfloat("3.5"), True)

    def test_fail_json(self):
        req = {"number": "3"}
        self.assertEqual(isfloat(req), False)

    def test_fail_string(self):
        self.assertEqual(isfloat("Hi!"), False)


class TestRemoveDups(TestDB):
    def test_no_dulpicates(self):
        req = [{"_id": 1, "number": 2}, {"_id": 4, "number": 6}]
        res = remove_dups_by_id(req)
        self.assertEqual(req, res)

    def test_no_duplicate_id(self):
        req = [{"_id": 1, "number": 2}, {"_id": 4, "number": 2}]
        res = remove_dups_by_id(req)
        self.assertEqual(req, res)

    def test_duplicates(self):
        req = [
            {"_id": 1, "number": 2},
            {"_id": 1, "number": 6},
            {"_id": 3, "number": 2},
            {"_id": 2, "number": 6},
        ]
        ideal_res = [
            {"_id": 1, "number": 2},
            {"_id": 3, "number": 2},
            {"_id": 2, "number": 6},
        ]
        res = remove_dups_by_id(req)
        self.assertEqual(res, ideal_res)

    def test_empty(self):
        req = []
        res = remove_dups_by_id(req)
        self.assertEqual(req, res)
