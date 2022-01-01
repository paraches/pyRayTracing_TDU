from unittest import TestCase
from PVector import PVector


class TestPVector(TestCase):
    def test_theme_1_6(self):
        v1 = PVector(3, 4, 5)
        v2 = PVector(6, 7, 8)
        v3 = PVector(9, 10, 11)

        # 1
        print(f'1. {v1}')
        # 2
        print(f'2. {v2}')
        # 3
        print(f'3. {v3}')

        # 4
        v4 = v1.add(v2)
        print(f'4. {v4}')
        self.assertEqual(PVector(9, 11, 13), v4)

        # 5
        v5 = PVector.sigma(3, v1, 4, v2)
        print(f'5. {v5}')
        self.assertEqual(PVector(33, 40, 47), v5)

        # 6
        v1 = v3.copy()
        print(f'6. {v1}')
        self.assertEqual(PVector(9, 10, 11), v1)

        # 7
        v1.y = 0
        print(f'7. {v1}')
        self.assertEqual(PVector(9, 0, 11), v1)

        # 8
        v8 = PVector.sigma(2, v1, -5, v2, 10, v3)
        print(f'8. {v8}')
        self.assertEqual(PVector(78, 65, 92), v8)

        # 9
        v9 = v2.dot(v3)
        print(f'9. {v9}')
        self.assertEqual(212, v9)

        # 10
        v10 = v2.cross(v3)
        print(f'10. {v10}')
        self.assertEqual(PVector(-3, 6, -3), v10)
