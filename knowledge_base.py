# Knowledge base per risposte di programmazione

knowledge = {
    'Python': {
        'variables': """In Python, le variabili sono contenitori per memorizzare dati. Non è necessario dichiarare il tipo:

x = 5           # intero
name = "HAL"    # stringa
pi = 3.14       # float
is_active = True # boolean

Python usa il duck typing - il tipo viene determinato automaticamente dal valore assegnato.""",
        
        'functions': """Le funzioni in Python si definiscono con 'def':

def greet(name):
    return f"Hello, {name}"

# Con parametri di default
def power(base, exp=2):
    return base ** exp

# Lambda functions
square = lambda x: x ** 2""",

        'loops': """Python supporta diversi tipi di loop:

# For loop
for i in range(5):
    print(i)

# While loop
while condition:
    # codice

# List comprehension
squares = [x**2 for x in range(10)]""",

        'classes': """Le classi in Python usano la parola chiave 'class':

class Robot:
    def __init__(self, name):
        self.name = name
    
    def speak(self):
        return f"I am {self.name}"

hal = Robot("HAL 9000")"""
    },
    
    'Java': {
        'variables': """In Java, le variabili devono essere dichiarate con un tipo:

int x = 5;
String name = "HAL";
double pi = 3.14;
boolean isActive = true;

Java è fortemente tipizzato - il tipo deve essere specificato esplicitamente.""",
        
        'functions': """I metodi in Java devono specificare il tipo di ritorno:

public int add(int a, int b) {
    return a + b;
}

public void greet(String name) {
    System.out.println("Hello, " + name);
}""",

        'classes': """Le classi in Java:

public class Robot {
    private String name;
    
    public Robot(String name) {
        this.name = name;
    }
    
    public String speak() {
        return "I am " + name;
    }
}"""
    },
    
    'JavaScript': {
        'variables': """JavaScript ha tre modi per dichiarare variabili:

let x = 5;        // variabile modificabile (block-scoped)
const name = "HAL"; // costante (block-scoped)
var old = "legacy"; // vecchio stile (function-scoped)

Usa 'let' per variabili che cambiano, 'const' per costanti.""",
        
        'functions': """JavaScript supporta diversi stili di funzioni:

// Function declaration
function greet(name) {
    return `Hello, ${name}`;
}

// Arrow function
const square = (x) => x ** 2;

// Function expression
const add = function(a, b) {
    return a + b;
};""",

        'async': """JavaScript gestisce operazioni asincrone con Promises e async/await:

// Promise
fetch('/api/data')
    .then(response => response.json())
    .then(data => console.log(data));

// Async/await
async function getData() {
    const response = await fetch('/api/data');
    const data = await response.json();
    return data;
}"""
    },
    
    'C': {
        'variables': """In C, le variabili devono essere dichiarate con tipo:

int x = 5;
char name[] = "HAL";
float pi = 3.14f;
double precise = 3.14159265359;

C richiede gestione manuale della memoria.""",
        
        'pointers': """I puntatori in C sono fondamentali:

int x = 10;
int *ptr = &x;  // puntatore a x

printf("%d", *ptr);  // dereferenziazione
*ptr = 20;  // modifica il valore di x""",

        'functions': """Le funzioni in C:

int add(int a, int b) {
    return a + b;
}

void greet(char *name) {
    printf("Hello, %s\\n", name);
}"""
    },
    
    'C++': {
        'variables': """C++ estende C con features object-oriented:

int x = 5;
std::string name = "HAL";
auto value = 42;  // type inference

// References
int &ref = x;  // reference a x""",
        
        'classes': """Le classi in C++:

class Robot {
private:
    std::string name;
public:
    Robot(std::string n) : name(n) {}
    
    std::string speak() {
        return "I am " + name;
    }
};""",

        'templates': """I template permettono programmazione generica:

template<typename T>
T max(T a, T b) {
    return (a > b) ? a : b;
}

int result = max<int>(5, 10);"""
    },
    
    'Go': {
        'variables': """Go usa inferenza di tipo con ':=':

var x int = 5
name := "HAL"  // tipo inferito
const pi = 3.14

Go è fortemente tipizzato ma con inferenza.""",
        
        'functions': """Le funzioni in Go possono ritornare multipli valori:

func divide(a, b float64) (float64, error) {
    if b == 0 {
        return 0, errors.New("division by zero")
    }
    return a / b, nil
}

result, err := divide(10, 2)""",

        'goroutines': """Go gestisce concorrenza con goroutines:

// Avvia goroutine
go func() {
    fmt.Println("Running in background")
}()

// Channels per comunicazione
ch := make(chan int)
go func() { ch <- 42 }()
value := <-ch"""
    }
}

def find_answer(language, query):
    """Cerca una risposta nella knowledge base"""
    query_lower = query.lower()
    
    if language not in knowledge:
        return None
    
    lang_kb = knowledge[language]
    
    # Cerca keywords nella query
    for topic, answer in lang_kb.items():
        keywords = topic.lower().split()
        if any(keyword in query_lower for keyword in keywords):
            return answer
    
    # Cerca keywords comuni
    common_keywords = {
        'variabili': 'variables',
        'variable': 'variables',
        'funzioni': 'functions',
        'function': 'functions',
        'metodi': 'functions',
        'method': 'functions',
        'loop': 'loops',
        'cicli': 'loops',
        'class': 'classes',
        'classe': 'classes',
        'oggetti': 'classes',
        'pointer': 'pointers',
        'puntatori': 'pointers',
        'async': 'async',
        'asincrono': 'async',
        'template': 'templates',
        'goroutine': 'goroutines',
    }
    
    for keyword, topic in common_keywords.items():
        if keyword in query_lower and topic in lang_kb:
            return lang_kb[topic]
    
    return None
