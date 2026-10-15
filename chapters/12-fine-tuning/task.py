"""Chapter 12's fine-tuning task: extract a payment (date, amount, currency) from a messy message into exact JSON.

Generated programmatically, so labels are exact and data is free:
    from task import dataset, messages, score
"""
import json
import random
import re
from datetime import date, timedelta

SYSTEM = ('Extract the payment from the message. Reply with JSON only, exactly: '
          '{"date": "YYYY-MM-DD", "amount": <number>, "currency": "PEN" | "USD" | "EUR"}')

CURRENCY_WORDS = {"PEN": ["soles", "S/", "PEN"], "USD": ["dollars", "US$", "USD", "$"], "EUR": ["euros", "€", "EUR"]}
MONTHS_EN = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
MONTHS_ES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]

TEMPLATES_EN = [
    "I paid {amt} on {date} for the internet bill.",
    "On {date} we transferred {amt} to the landlord.",
    "Receipt: {date} — total {amt}",
    "{date}: team lunch, {amt}",
    "hey can u log {amt} i spent {date} at the pharmacy",
    "Payment of {amt} was received {date}. Thanks!",
    "Netflix charged me {amt} ({date})",
]
TEMPLATES_ES = [
    "Pagué {amt} el {date} por la luz.",
    "Transferencia realizada el {date} por {amt}.",
    "{date} - mercado, {amt}",
    "me cobraron {amt} el {date} en la farmacia",
]


def _amount_text(value, currency, rng):
    word = rng.choice(CURRENCY_WORDS[currency])
    num = rng.choice([f"{value:,.2f}", f"{value:.2f}", f"{value:g}"]) if value != int(value) else rng.choice([f"{int(value):,}", f"{int(value)}", f"{value:.2f}"])
    return f"{word}{num}" if word in ("S/", "US$", "$", "€") else f"{num} {word}"


def _date_text(d, spanish, rng):
    if spanish:
        return rng.choice([f"{d.day} de {MONTHS_ES[d.month - 1]} de {d.year}", f"{d.day:02d}/{d.month:02d}/{d.year}", d.isoformat()])
    return rng.choice([f"{MONTHS_EN[d.month - 1]} {d.day}, {d.year}", f"{MONTHS_EN[d.month - 1][:3]} {d.day} {d.year}", d.isoformat()])


def make_example(rng):
    spanish = rng.random() < 0.35
    currency = rng.choice(list(CURRENCY_WORDS))
    value = round(rng.uniform(1, 3000), rng.choice([0, 2]))
    d = date(2025, 1, 1) + timedelta(days=rng.randint(0, 600))
    text = rng.choice(TEMPLATES_ES if spanish else TEMPLATES_EN).format(amt=_amount_text(value, currency, rng), date=_date_text(d, spanish, rng))
    return {"text": text, "target": {"date": d.isoformat(), "amount": value, "currency": currency}}


def dataset(n, seed=0):
    rng = random.Random(seed)
    return [make_example(rng) for _ in range(n)]


def messages(text, target=None):
    """Chat messages for one example; include the target as the assistant turn for training."""
    msgs = [{"role": "system", "content": SYSTEM}, {"role": "user", "content": text}]
    return msgs + ([{"role": "assistant", "content": json.dumps(target)}] if target else [])


def parse(output):
    m = re.search(r"\{.*?\}", output or "", flags=re.S)
    try:
        return json.loads(m.group(0)) if m else None
    except json.JSONDecodeError:
        return None


def score(output, target):
    """{'valid_json', 'date', 'amount', 'currency', 'exact'} for one model output."""
    p = parse(output)
    if not isinstance(p, dict):
        return {"valid_json": False, "date": False, "amount": False, "currency": False, "exact": False}
    try:
        amount_ok = abs(float(p.get("amount")) - target["amount"]) < 0.005
    except (TypeError, ValueError):
        amount_ok = False
    s = {"valid_json": True, "date": p.get("date") == target["date"], "amount": amount_ok, "currency": p.get("currency") == target["currency"]}
    s["exact"] = s["date"] and s["amount"] and s["currency"]
    return s


if __name__ == "__main__":  # self-check
    ex = dataset(3, seed=1)
    for e in ex:
        print(e["text"], "->", e["target"])
    t = ex[0]["target"]
    assert score(json.dumps(t), t)["exact"]
    assert not score('{"date": "2020-01-01", "amount": 1, "currency": "USD"}', t)["exact"]
    assert score("Sure! " + json.dumps(t) + " hope that helps", t)["exact"]
    assert not score("no json here", t)["valid_json"]
    print("ok")
