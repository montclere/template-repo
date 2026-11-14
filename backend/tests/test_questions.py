def test_ask_returns_the_answer_and_saves_it(client):
    response = client.post("/api/v1/questions", json={"text": "Что такое RAG?"})

    assert response.status_code == 201
    created = response.json()
    assert created["text"] == "Что такое RAG?"
    assert created["answer"] == "ответ на: Что такое RAG?"

    history = client.get("/api/v1/questions").json()
    assert history[0] == created


def test_history_is_newest_first(client):
    client.post("/api/v1/questions", json={"text": "первый"})
    client.post("/api/v1/questions", json={"text": "второй"})

    texts = [q["text"] for q in client.get("/api/v1/questions").json()]

    assert texts.index("второй") < texts.index("первый")


def test_ask_returns_502_and_saves_nothing_when_ml_is_down(client, assistant):
    assistant.down = True

    response = client.post("/api/v1/questions", json={"text": "не сохранится"})

    assert response.status_code == 502
    texts = [q["text"] for q in client.get("/api/v1/questions").json()]
    assert "не сохранится" not in texts


def test_ask_rejects_empty_text(client):
    response = client.post("/api/v1/questions", json={"text": ""})

    assert response.status_code == 422
