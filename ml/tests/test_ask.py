from app.llm.prompts import load_prompt


def test_ask_returns_the_model_answer(client, fake_llm):
    fake_llm.reply_text = "Париж"

    response = client.post("/api/v1/ask", json={"question": "Столица Франции?"})

    assert response.status_code == 200
    assert response.json() == {"answer": "Париж"}
    sent = fake_llm.requests[0]["body"]
    assert sent["messages"][0]["content"] == "Столица Франции?"
    assert sent["system"] == load_prompt("ask")


def test_ask_returns_502_when_the_model_fails(client, fake_llm):
    fake_llm.statuses = [500, 500, 500]

    response = client.post("/api/v1/ask", json={"question": "Столица Франции?"})

    assert response.status_code == 502


def test_ask_rejects_an_empty_question(client):
    response = client.post("/api/v1/ask", json={"question": ""})

    assert response.status_code == 422
