"""Payment payload validation and GUI integration checks."""
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from urllib.parse import parse_qs, urlsplit
from PIL import Image
from qr_core import QRGenerator
from qr_generator_gui import QRGeneratorGUI


class UPITests(unittest.TestCase):
    def setUp(self):
        self.generator = QRGenerator()

    def test_recipient_amount_and_encoded_name(self):
        uri = self.generator.create_upi_data(' shop@bank ', '150.5', 'Shop & Sons + Cafe')
        parsed = urlsplit(uri)
        self.assertEqual((parsed.scheme, parsed.netloc), ('upi', 'pay'))
        self.assertEqual(parse_qs(parsed.query), {
            'pa': ['shop@bank'], 'pn': ['Shop & Sons + Cafe'],
            'am': ['150.50'], 'cu': ['INR'],
        })

    def test_invalid_amounts_and_ids(self):
        for amount in ['', '0', '-1', '1.001', 'NaN', 'Infinity', '1e3', '1,000', '1&pa=other@bank']:
            with self.subTest(amount=amount), self.assertRaises(ValueError):
                self.generator.create_upi_data('shop@bank', amount)
        for upi_id in ['', 'shop', '@bank', 'shop@', 'shop @bank', 'shop@bank&pa=other@bank']:
            with self.subTest(upi_id=upi_id), self.assertRaises(ValueError):
                self.generator.create_upi_data(upi_id, '1')

    def test_gui_uses_payment_payload_and_reports_validation(self):
        def entry(value):
            return SimpleNamespace(get=lambda: value)
        gui = SimpleNamespace(qr_gen=self.generator, qr_type=entry('upi'),
                              upi_id_entry=entry('shop@bank'),
                              upi_amount_entry=entry('0.01'), upi_name_entry=entry(''))
        data = QRGeneratorGUI.get_qr_data(gui)
        self.assertEqual(parse_qs(urlsplit(data).query)['am'], ['0.01'])
        gui.upi_amount_entry = entry('0')
        with self.assertRaises(ValueError):
            QRGeneratorGUI.get_qr_data(gui)

    def test_saves_payment_image(self):
        with tempfile.TemporaryDirectory() as directory:
            path = self.generator.create_upi_qr('shop@bank', '150.50', output_dir=directory)
            self.assertTrue(Path(path).is_file())
            with Image.open(path) as image:
                self.assertEqual(image.format, 'PNG')
                self.assertGreater(image.width, 0)


if __name__ == '__main__':
    unittest.main()
