import pytest
from urus_api.v1.ris_gov.views import IDcardValidator


class TestIDcardValidator:

    def test_get_captcha_key(self):
        # Arrange
        base_url = "https://www.ris.gov.tw/apply-idCard/app/idcard/IDCardReissue/"
        # Act
        captcha_key = IDcardValidator().get_captcha_key(base_url)
        # Assert
        assert captcha_key != None

    def test_get_captcha_image(self):
        # Arrange
        current_time = "1546930816894"
        captcha_key = "test_captcha_key"
        captcha_url = "https://www.ris.gov.tw/apply-idCard/captcha/image?"

        # Act
        captcha_image_url = IDcardValidator().get_captcha_image_url(current_time, captcha_key,
                                                                    captcha_url)
        # Assert
        assert captcha_image_url == "https://www.ris.gov.tw/apply-idCard/captcha/image?CAPTCHA_KEY=test_captcha_key&time=1546930816894"

    def test_validate_idcard(self):
        # Arrange
        idcard_validate_url = "https://www.ris.gov.tw/apply-idCard/app/idcard/IDCardReissue/query"
        request_data = {
            "idnum": "A123456789",
            "applyTWY": "99",
            "applyMM": "7",
            "applyDD": "16",
            "siteId": "10001",
            "applyReason": "3"
        }
        captcha_key = "test_captcha_key"
        captcha_code = "ABCDE"
        # Act
        rep = IDcardValidator().validate_idcard(idcard_validate_url, request_data, captcha_key,
                                                captcha_code)

        # Assert
        assert rep.status_code == 200
