import json
import openai
import time


DRY_RUN = False

MODEL = "gpt-3.5-turbo-16k" # "gpt-4"

DEFAULT_SYSTEM_MESSAGE = (
"""
Jesteś ekspertem w dziedzinie Psychologii Społecznej. Zostałeś poproszony o
udzielenie odpowiedzi na pytania dotyczące wybranych zagadnień tej dziedziny.
Przykłady i definicje udzielaj o ile to możliwe na podstawie książki Bogdana 
Wojciszke pt. Psychologia Społeczna. Gdziekolwiek to możliwe, udzielaj odpowiedzi 
w formie krótkich zdań, które są zrozumiałe dla osoby, która nie jest ekspertem 
w tej dziedzinie. Jeśli nie jesteś w stanie udzielić odpowiedzi na pytanie, 
napisz "Nie wiem". Jeśli nie jesteś pewien swojej odpowiedzi, napisz "Nie jestem 
pewien".
"""
).replace('\n', ' ').strip()


def do_setup():
    with open('secrets.json') as f:
        secrets = json.load(f)
    openai.api_key = secrets['openai_api_key']


def write_line_to_file(content, filename='odpowiedzi.md'):
    with open(filename, 'a', encoding='utf-8') as f:
        f.write(content + '\n')


def get_answers(question, how_many=1, system_message=DEFAULT_SYSTEM_MESSAGE, dry_run=DRY_RUN, model=MODEL):
    try:
        response = "Odp..." if dry_run else openai.ChatCompletion.create(
            model=model,
            messages=[
                {
                "role": "system",
                "content": system_message
                },
                {
                "role": "user",
                "content": question
                }
            ],
            temperature=0.5,
            max_tokens=9128,
            top_p=1,
            n=how_many,
            frequency_penalty=0,
            presence_penalty=0
        )
        return ( answer.message.content for answer in response.choices )
    except openai.error.RateLimitError as e:
        wait_time = 15
        print(f"Rate limit exceeded. Waiting {wait_time} seconds before retrying...")
        time.sleep(wait_time)
        return get_answers(question, how_many, system_message, dry_run)


def main():
    do_setup()
    write_line_to_file('# Zagadnienia na test wiedzy 28.10.2023\n')
    questions = [
        # '9. Czym jest podstawowy błąd atrybucji?',
        # '10. Czym jest egotyzm, a czym egocentryzm atrybucyjny?',
        '11. Czym jest efekt aureoli?',
        '12. Czym jest efekt czystej ekspozycji?',
        '13. Podaj przykład porównań społecznych "w dół".',
        '14. Podaj przykład porównań społecznych "w górę".',
        '15. Co zwiększa naszą skłonność do pozytywnej autoprezentacji?',
        '16. Czym jest autowaloryzacja Ja?',
        '17. Z jakich komponentów składa się postawa?',
        '18. Wymień elementy procesualnego modelu perswazji.',
        '19. Wymień trzy główne mechanizmy wpływu społecznego i zdefiniuj każdy z nich. Podaj przykład obrazujący mechanizm każdego z nich.',
        '20. Czym jest społeczny dowód słuszności?',
        '21. Czym jest zjawisko obojętnego przechodnia. Podaj przykład obrazujący jego mechanizm.',
        '22. Wymień rodzaje tożsamości grupowej. Zdefiniuj jeden z nich.',
        '23. Czym jest narcyzm kolektywny?',
        '24. Wyjaśnij czym jest zagrożenie stereotypem. Podaj definicję oraz przykład.',
        '25. Czym jest syndrom myślenia grupowego?'
    ]

    for question in questions:
        write_line_to_file("## " + question + "\n")
        answers = get_answers(question, how_many=2)
        answers_joined = '\n\n ----- \n\n'.join(answers)
        write_line_to_file(answers_joined + '\n')


if __name__ == '__main__':
    main()
