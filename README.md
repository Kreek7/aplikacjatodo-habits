# aplikacjatodo-habits

W tym projekcie stworzyłem aplikację webową, która pozwala użytkownikowi tworzyć zadania do wykonania oraz pomaga użytkownikowi utrwalić swoje nawyki. Aplikacja jest napisana w języku Python, w tworzeniu aplikacji użyłem frameworka Flask oraz do zapisywania danych posłużyła mi baza danych utworzona w MySql. 

Główne operacje oraz działania, które wykonuje aplikacje zostały zapisane w pliku app.py. Znajdziemy tam poszczególne funkcje, które odpowiadają za poszczególne działanie każdej podstrony. Wszelkie szablony stron, znajdziemy w folderze templates. Większość funkcji korzysta z metod GET oraz POST w celu nawiązania kontaktu z poszególnymi dokumentami sieciowymi oraz w wielu przypadkach funkcja wymaga połączenia się z bazą danych np. w celu pobrania informacji z tabeli oraz wyświetlenia jej na stronie czy też, żeby zapisać podane przez użytkownika dane w konretnej tabeli w bazie.

Aplikacja umożliwia użytkownikowi takie opcje jak: rejestracja użytkownika oraz zalogowanie się, tworzenie zadań do zrobienia, usuwanie zadań całkowicie z bazy danych, dołączenie zadania do listy zadań wykonanych oraz edycja zadań. Użytkownik może wyszukiwać zadania w aplikacji po określonej w aplikacji jednej z 6 kategorii. 
Oprócz tego aplikacja pozwala użytkownikowi również tworzyć nawyki, które użytkownik chciałby utrwalać. Pomóc może mu w tym opcja kalendarza, w której użytkownik podaje dzień, w którym wykonał daną czynność oraz opcja historii w której widać w jakich dniach w danym odstępie czasu użytkownik daną czynność wykonał.
