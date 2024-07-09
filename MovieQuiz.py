#pip install cinemagoer
#https://cinemagoer.readthedocs.io/en/latest/usage/quickstart.html
#Funzione di Cinemagoer (C_F)
#Funzione di Random (R_F)
import random
from imdb import Cinemagoer

class MovieQuiz:
    def __init__(mq): #MovieQuiz=mq 
        mq.cg = Cinemagoer() #(C_F)
        mq.total_score = 0
        mq.current_question_quantity = 0
        mq.num_questions = 5
        mq.movies = []
        mq.current_question_data = {}
        mq.difficulty_level = 1  # Default difficulty level
    
    def get_movies(mq, count=2000): #Top/bottom movies function non serve *ia.get_top250_movies()
        """
        Trova fino a "count" films casuali da Cinemagoer usando la parola chiave.
        """
        keyword = "movie"
        search_movies = mq.cg.search_movie(keyword) #(C_F)
        return random.sample(search_movies, count) #(R_F)
    
    def generate_question(mq, movie):
        """
        Crea domanda secondo la difficoltà scelta.
        """
        film_characteristics = mq.cg.get_movie(movie.movieID) #(C_F)
        
        if mq.difficulty_level == 1:
            # Difficoltà 1: Domanda-anno di uscita del film
            question = f"In che anno è uscito il film: '{film_characteristics['title']}'?" #f string
            answer = film_characteristics['year']
            wrong_answers = set() #Definire un set, per non ripetere risposte
            while len(wrong_answers) < 3:  # 3 risposte sbagliate vicine
                wrong_answer = answer + random.randint(-10, 10) #(R_F)
                if wrong_answer != answer:
                    wrong_answers.add(wrong_answer)    
            # Combina le risposte sbagliate con quella corretta
            options = list(wrong_answers) 
            options.append(answer)
            random.shuffle(options) #(R_F)
        elif mq.difficulty_level == 2:
            # Difficoltà 2: Domanda-direttore del film
            question = f"Chi è il direttore del film: '{film_characteristics['title']}'?" #f string
            if 'director' in film_characteristics and film_characteristics['director']:
                answer = film_characteristics['director'][0]['name'] #[0] prima lista di characteristics #secondo dizionario di CG
            else:
                answer = 'Direttore Sconosciuto'
            
            # Risposte casuali
            directors = [person['name'] for person in mq.cg.search_person('director')] #(C_F) #Creare una lista con tutti i direttori
            random_answers = random.sample([x for x in directors if x != answer], 3)  # 3 risposte sbagliate aleatorie #(R_F)
            options = random_answers + [answer] #opzioni (risposta giusta e sbagliate)
            random.shuffle(options) #(R_F)
        
        return question, str(answer), options 
    
    def display_question(mq, question_data):
        """
        Mostra la domanda e le opzioni nella console.
        """
        question = question_data['question']
        options = question_data['options']
        
        print(question) # Visualizza la domanda
        
        for i, option in enumerate(options): # Visualizza le opzioni
            print(f"{i + 1}. {option}") #f string per ogni opzione si enumera, aumentando 1

        while True:  # Chiede all'utente di rispondere #loop infinito mentre non si esce mediante il break
            try:
                user_input = int(input("Scegli una risposta (1-4): "))  # Utente seleziona la risposta nella console
                if 1 <= user_input <= 4: #risposta tra 1 e 4
                    user_answer = str(options[user_input - 1]) #sistema la risposta togliendo 1 per comparare con risposta *inizia da 0*
                    break #finisce il processo -> va a return
                else:
                    print("Inserisci un numero tra 1 e 4.")
            except ValueError: #se inserisce un carattere non valido
                print("Inserisci un numero valido.")
        
        return user_answer
    
    def show_final_score(mq):
        """
        Mostra il punteggio finale.
        """
        print(f"Il tuo punteggio totale: {mq.total_score}") #f string
    
    def selected_answer(mq, user_answer): #mette insieme tutti i parametri selezionati
        """
        Gestisce la risposta selezionata nella console. 
        """
        correct_answer = str(mq.current_question_data['answer']) #converte risposta in una string per il confronto
        difficulty = mq.current_question_data['difficulty']
        score = mq.calculate_score(correct_answer, user_answer, difficulty)
        mq.total_score += score #addiziona lo score al totale futuro
        
        # Visualizza il risultato dopo ogni domanda
        if user_answer == correct_answer:
            print(f"Risposta corretta! Punteggio ottenuto: {score} punti.") #f string
        else:
            print(f"Sbagliato. La risposta corretta era: {correct_answer}.") #f string
        
        # Passa alla prossima domanda o mostra il punteggio totale
        mq.current_question_quantity += 1
        if mq.current_question_quantity < len(mq.movies): #compara le domande con i film scelti
            mq.next_question()
        else:
            mq.show_final_score()
    
    def calculate_score(mq, correct_answer, user_answer, difficulty):
        """
        Calcola il punteggio secondo la difficoltà.
        """
        if user_answer == correct_answer:
            return difficulty * 10 #difficoltà 1:1*10, difficoltà 2:2*10
        return 0 #se risposta è sbagliata
    
    def choose_difficulty(mq):
        """
        Permette scegliere la difficoltà del quiz.
        """
        while True: #loop infinito mentre non si esce mediante il break
            try:
                mq.difficulty_level = int(input("Seleziona la difficoltà (1 o 2): "))
                if mq.difficulty_level in [1, 2]: #solo risposte amesse
                    break
                else:
                    print("Inserisci 1 per difficoltà 1 o 2 per difficoltà 2.") 
            except ValueError:
                print("Inserisci un numero valido.")
    
    def start_quiz(mq, num_questions=5): #condizioni iniziali per avviare il quiz
        """
        Inizia il quiz con 5 domande.
        """
        mq.choose_difficulty()
        mq.num_questions = num_questions
        mq.movies = mq.get_movies(num_questions)
        mq.total_score = 0
        mq.current_question_quantity = 0
        mq.next_question() #iniziano o continuano le domande
    
    def next_question(mq):
        """
        Mostra la domanda seguente.
        """
        if mq.current_question_quantity < len(mq.movies): #compara la quantità di domande attuale e la lunghezza della lista movies
            movie = mq.movies[mq.current_question_quantity]  #genera altre condizione per la nuova domanda
            question, answer, options = mq.generate_question(movie) 
            mq.current_question_data = {'question': question, 'answer': answer, 'options': options, 'difficulty': mq.difficulty_level}
            user_answer = mq.display_question(mq.current_question_data) 
            mq.selected_answer(user_answer)
        else:
            mq.show_final_score() #finisce gioco
          
# Inizializza il quiz e inizia
MovieQuiz().start_quiz() #classe MQ chiama start_quiz method
