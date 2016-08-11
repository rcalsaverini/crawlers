from list_of_speeches import parse


def test_result_is_list():
    html = open('./tests/fixtures/list_of_speeches.html', 'r').read()
    list_of_speeches = parse.list_of_speeches(html)
    assert isinstance(list_of_speeches, list)
    assert len(list_of_speeches) == 5


def test_contains_dicts():
    html = open('./tests/fixtures/list_of_speeches.html', 'r').read()
    list_of_speeches = parse.list_of_speeches(html)
    for speech in list_of_speeches:
        assert isinstance(speech, dict)

def test_fields():
    html = open('./tests/fixtures/list_of_speeches.html', 'r').read()
    list_of_speeches = parse.list_of_speeches(html)
    for speech in list_of_speeches:
        assert 'date' in speech
        assert 'session' in speech
        assert 'phase' in speech
        assert 'speech_url' in speech
        assert 'orator' in speech
        assert 'party' in speech
        assert 'state' in speech
        assert 'hour' in speech
        assert 'publication' in speech
