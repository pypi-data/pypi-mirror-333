from bshlib.suffix_mgr import ObjId, SuffixMgr, is_suffix

from unittest import TestCase
from dataclasses import dataclass

@dataclass
class CreditCard:
    bank: str
    number: str
    balance: float


bundle_ls_0 = [
    ObjId(CreditCard('Banco Santander', '1231241243', 500.2), 'santander'),
    ObjId(CreditCard('Banco Santander', '5643373368', 1.0), 'santander'),
    ObjId(CreditCard('UniCredit', '9996431232', 12.0), 'unicredit_554'),
    ObjId(CreditCard('Banco Santander', '0500055441', 0.0), 'santander_21'),
    ObjId(CreditCard('Banco Santander', '0234023796', 66.7), 'santander_55'),
    ObjId(CreditCard('Banco Santander', '0000000000', 90.1), 'santander'),
    ObjId(CreditCard('UniCredit', '1196431232', 11.22), 'unicredit_2'),
    ObjId(CreditCard('UniCredit', '0140410667', 13.0), 'unicredit_112'),
    ObjId(CreditCard('BNP Paribas', '1196456232', 1200.5), 'paribas'),
    ObjId(CreditCard('Intesa Sanpaolo', '0988763312', 43.3), 'intesa_sanpaolo'),
    ObjId(CreditCard('Banco Santander', '9934799665', 69.7), 'santander_555')
]

bundle_ls_1 = [
    ObjId(CreditCard('Banco Santander', '1231241243', 500.2), 'santander'),
    ObjId(CreditCard('Banco Santander', '5643373368', 1.0), 'santander'),
    ObjId(CreditCard('Intesa Sanpaolo', '0988763312', 43.3), 'intesa_sanpaolo'),
    ObjId(CreditCard('Banco Santander', '9934799665', 69.7), 'santander')
]


class TestSfxMgr(TestCase):

    def test_init(self):
        SuffixMgr(bundle_ls_0)
        assert True

    def test_rearrange(self):
        # - PREPARE -
        # messy ids
        my_creds = [
            ObjId(CreditCard('Banco Santander', '0413657334', 100.0), 'santander'),
            ObjId(CreditCard('Banco Santander', '9595993393', 200.0), 'santander_12226'),
            ObjId(CreditCard('Banco Santander', '0189072346', 400.0), 'santander_245'),
            ObjId(CreditCard('BNP Paribas', '0000000000', 1.0), 'paribas'),
            ObjId(CreditCard('Banco Santander', '8205631544', 7700.0), 'santander'),
        ]
        # rearrange
        sfm = SuffixMgr(my_creds)

        # - TEST -
        # repeated name IDs get suffixes
        for ids in [bun.id for bun in my_creds if bun.obj.bank == 'Banco Santander']:
            self.assertTrue(is_suffix(ids))
        # unique IDs stay `basic`
        unq = [bun for bun in my_creds if bun.obj.number == '0000000000'][0]
        self.assertTrue(unq.id in sfm.basic)
        # verify amount of IDs with same name
        self.assertEqual(len(sfm.map['santander']), 4)
        self.assertEqual(len(sfm.find_base('santander')), 4)
