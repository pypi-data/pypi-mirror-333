import ai_cloud_sdk_4pd.client as ai_cloud_sdk_4pd_client
import ai_cloud_sdk_4pd.models as ai_cloud_sdk_4pd_models


def test_translate():
    print('-------------test client-------------')
    token = "eyJhbGciOiJIUzI1NiJ9.eyJ0ZW5hbnRfaWQiOjksInRva2VuX2NyZWF0ZWRfYXQiOjE3NDExNTkzNDkxNzIsImlhdCI6MTc0MTE1OTM0OSwicGxhbl9pZCI6bnVsbH0.FNiuEELfmV3DenOjp9I_nHXkVSyK3en8ChOLyzZ4Nco"
    call_token = "eyJhbGciOiJIUzI1NiJ9.eyJ0ZW5hbnRfaWQiOjksInVzZXJfaWQiOjE1LCJ0b2tlbl9jcmVhdGVkX2F0IjoxNzQxMTU5MzcyNDgzLCJpYXQiOjE3NDExNTkzNzJ9.TmManMkK970sUdKvD6z2tiALZGhh58cgumkuqilD0HQ"

    region = 'debug'
    config = ai_cloud_sdk_4pd_models.Config(
        token=token,
        call_token=call_token,
        region=region,
    )
    client = ai_cloud_sdk_4pd_client.Client(config=config)
    request = ai_cloud_sdk_4pd_models.TranslateTextRequest(
        text=["为什么全部语言这么奇怪", "我来检查一下", "全部语言"],
        source="zh",
        target="fa",
    )
    response = client.translate_text(request=request)
    print(response.code)
    print(response.data)
    print(response.message)
    print('-------------------------------------')


if __name__ == '__main__':
    test_translate()
