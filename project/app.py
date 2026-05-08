from flask import Flask, render_template, request, jsonify
from datetime import datetime

app = Flask(__name__)
app.secret_key = "studymind-secret-2024"



KNOWLEDGE_BASE = [
    {
        "keywords": ["newton", "law of motion", "force", "inertia", "acceleration"],
        "answer": """**Newton's Laws of Motion** physics ki bunyad hain:

**1st Law (Inertia):**
Koi cheez apni halat nahi badlti jab tak koi force na lage.
*Misal:* Car mein brakes lagane par aap aage jhuk jaate ho.

**2nd Law (F = ma):**
Force = Mass × Acceleration
*Misal:* Football ko zyada zor se maaro toh zyada tez jayegi.

**3rd Law (Action-Reaction):**
Har action ki barabar aur ulti reaction hoti hai.
*Misal:* Rocket gas neeche phenikta hai, rocket upar jaata hai."""
    },
    {
        "keywords": ["photosynthesis", "plant food", "chlorophyll", "sunlight", "glucose", "oxygen", "carbon dioxide"],
        "answer": """**Photosynthesis** woh process hai jis se plants apna khana banati hain.

**Formula:** 6CO₂ + 6H₂O + Sunlight → C₆H₁₂O₆ + 6O₂

**Steps:**
1. Roots se paani (H₂O) absorb hota hai
2. Patti stomata se CO₂ leta hai
3. Chlorophyll sunlight absorb karta hai
4. Glucose banta hai — plant ki energy
5. Oxygen release hoti hai — hamari saans

**Important:** Photosynthesis sirf din mein hoti hai!"""
    },
    {
        "keywords": ["pythagoras", "pythagorean", "right angle", "hypotenuse", "triangle sides"],
        "answer": """**Pythagoras Theorem:**

**Formula:** a² + b² = c²

- **a, b** = do sides (base aur perpendicular)
- **c** = hypotenuse (sabse lamba side)

**Example:**
a=3, b=4 → 9 + 16 = 25 → c = **5** ✅

**3-4-5, 5-12-13, 8-15-17** — famous Pythagorean triplets

**Use:** Construction, GPS, engineering mein."""
    },
    {
        "keywords": ["dna", "replication", "genes", "chromosome", "double helix", "genetic", "rna", "nucleotide"],
        "answer": """**DNA** hamari genetic information store karta hai.

**Structure:** Double Helix — 2 chains
**Bases:** A-T, G-C (sirf yahi pair karte hain)

**Replication (Copy banana):**
1. Helicase enzyme DNA kholta hai
2. DNA Polymerase naye nucleotides add karta hai
3. 2 identical DNA molecules ban jaate hain

**Kyun zaroori hai:** Cell division mein naye cells ko same DNA milta hai."""
    },
    {
        "keywords": ["ohm", "voltage", "current", "resistance", "electric circuit", "volt", "ampere"],
        "answer": """**Ohm's Law:** V = I × R

- **V** = Voltage (Volts) — electric pressure
- **I** = Current (Amperes) — electrons ka flow
- **R** = Resistance (Ohms) — rukawat

**Example:** V=12V, R=4Ω → I = 12/4 = **3A**

**Yaad karo:** VIR triangle!
- V = I×R
- I = V/R
- R = V/I"""
    },
    {
        "keywords": ["mitosis", "meiosis", "cell division", "prophase", "metaphase", "anaphase", "telophase"],
        "answer": """**Mitosis** — Body cells ki division (2 identical cells banti hain)

**Stages:**
1. **Prophase** — Chromosomes visible, nuclear membrane toot ti hai
2. **Metaphase** — Chromosomes middle mein align
3. **Anaphase** — Chromosomes alag hote hain
4. **Telophase** — 2 naye nuclei bante hain

**Mitosis vs Meiosis:**
- Mitosis → 2 cells, same DNA (body growth)
- Meiosis → 4 cells, half DNA (reproduction)"""
    },
    {
        "keywords": ["gravity", "gravitational force", "free fall", "weight", "g=9.8", "falling object"],
        "answer": """**Gravity** woh force hai jo cheezein zameen ki taraf kheenchti hai.

**Earth ki Gravity:** g = 9.8 m/s²

**Formula:** F = m × g
**Example:** 60kg insaan ka weight = 60 × 9.8 = **588 N**

**Mass vs Weight:**
- Mass = matter ki miqdar (kg) — nahi badlti
- Weight = gravity force (N) — jagah se badlti hai

**Chaand par:** g = 1.6 m/s² — isliye wahan halka lagta hai!"""
    },
    {
        "keywords": ["atom", "electron", "proton", "neutron", "nucleus", "atomic number", "element", "molecule"],
        "answer": """**Atom** matter ki sabse choti unit hai.

**Structure:**
- **Nucleus:** Protons (+) aur Neutrons (neutral)
- **Electron Cloud:** Electrons (-) bahar chakkar lagate hain

**Important:**
- Atomic Number = Protons
- Mass Number = Protons + Neutrons

**Carbon example:** 6 protons, 6 neutrons, 6 electrons

**Ions:**
- Electron gain → Negative ion (Anion)
- Electron khona → Positive ion (Cation)"""
    },
    {
        "keywords": ["python", "programming", "code", "function", "variable", "loop", "list", "class", "object"],
        "answer": """**Python** — sabse aasan programming language!

**Variables:**
```
name = "Ali"
age = 20
```

**If-Else:**
```
if marks >= 80:
    print("A Grade!")
```

**Loop:**
```
for i in range(5):
    print(i)
```

**Function:**
```
def greet(name):
    return "Hello " + name
```

**Python use:** AI, Web Dev, Data Science, Automation"""
    },
    {
        "keywords": ["world war", "ww1", "ww2", "first world war", "second world war", "1914", "1939", "hitler"],
        "answer": """**World War 1 (1914-1918)**
- Cause: MAIN — Militarism, Alliances, Imperialism, Nationalism
- Trigger: Archduke Franz Ferdinand ka qatl
- Result: Germany haara, Treaty of Versailles

**World War 2 (1939-1945)**
- Cause: WW1 ka badla, Hitler ka rise, Poland par hamla
- Events: Holocaust, Pearl Harbor, D-Day, Atomic bombs
- Result: Germany + Japan haare, UN bani"""
    },
    {
        "keywords": ["covalent bond", "ionic bond", "chemical bond", "valence", "sharing electrons"],
        "answer": """**Chemical Bonds:**

**Covalent Bond:**
- Electrons share hote hain
- Non-metals ke darmiyan
- Example: H₂O, CO₂, CH₄

**Ionic Bond:**
- Electron transfer hota hai
- Metal + Non-metal
- Example: NaCl (namak)

**Metallic Bond:**
- Metals mein free electrons
- Bijli conduct karte hain"""
    },
    {
        "keywords": ["photosynthesis", "respiration", "difference", "comparison"],
        "answer": """**Photosynthesis vs Respiration:**

| | Photosynthesis | Respiration |
|---|---|---|
| Kahan | Plants | Sab organisms |
| Kab | Din mein | Har waqt |
| Input | CO₂ + H₂O | Glucose + O₂ |
| Output | Glucose + O₂ | CO₂ + H₂O + Energy |
| Energy | Store hoti hai | Release hoti hai |"""
    },
    {
        "keywords": ["periodic table", "elements", "groups", "periods", "metals", "non-metals"],
        "answer": """**Periodic Table** — sabhi elements ki list!

**Structure:**
- **Periods** (Rows) — 7 periods hain
- **Groups** (Columns) — 18 groups hain

**Groups:**
- Group 1: Alkali Metals (Na, K, Li)
- Group 17: Halogens (F, Cl, Br)
- Group 18: Noble Gases (He, Ne, Ar)

**Metals:** Left side (conductors)
**Non-metals:** Right side
**Metalloids:** Middle (Si, Ge)

**Atomic number** left se right badhta hai."""
    },
    {
        "keywords": ["big o", "algorithm", "complexity", "time complexity", "data structure", "binary search", "sorting"],
        "answer": """**Big O Notation** — algorithm ki speed batata hai

**Common Complexities:**
- **O(1)** — Constant: Array element access
- **O(log n)** — Binary Search
- **O(n)** — Linear Search
- **O(n log n)** — Merge Sort
- **O(n²)** — Bubble Sort

**Binary Search:**
Sorted list mein middle check karo, half eliminate karo
1000 items → sirf 10 steps!

**Rule:** Chhota Big O = Tez algorithm"""
    },
    {
        "keywords": ["recursion", "recursive", "function calling itself", "base case", "stack"],
        "answer": """**Recursion** — function khud ko call karta hai!

**Structure:**
```
def factorial(n):
    if n == 1:        # Base case
        return 1
    return n * factorial(n-1)  # Recursive call
```

**Kaise kaam karta hai:**
factorial(4) = 4 × factorial(3)
             = 4 × 3 × factorial(2)
             = 4 × 3 × 2 × factorial(1)
             = 4 × 3 × 2 × 1 = **24**

**Zaroori:** Hamesha Base Case hona chahiye warna infinite loop!"""
    },
]


def find_answer(question, subject):
    question_lower = question.lower()

    # Search knowledge base by keywords
    for entry in KNOWLEDGE_BASE:
        for kw in entry["keywords"]:
            if kw.lower() in question_lower:
                return entry["answer"]

    # Subject-specific fallback
    subject_fallbacks = {
        "Mathematics": "**Mathematics:**\nSpecific sawaal likho jaise:\n- 'Pythagoras theorem kya hai?'\n- 'Quadratic equation solve karo'\n- 'Derivative kya hoti hai?'\n\nMain step-by-step samjhaunga!",
        "Physics": "**Physics:**\nYeh topics available hain:\n- Newton's Laws\n- Ohm's Law\n- Gravity\n- Atom structure\n\nSpecific topic ka naam likho!",
        "Chemistry": "**Chemistry:**\nYeh topics available hain:\n- Covalent/Ionic bonds\n- Periodic table\n- Atoms & molecules\n\nAur specific sawaal karo!",
        "Biology": "**Biology:**\nYeh topics available hain:\n- Photosynthesis\n- DNA & Replication\n- Mitosis vs Meiosis\n- Cell structure\n\nKoi ek topic choose karo!",
        "Computer Science": "**Computer Science:**\nYeh topics available hain:\n- Python programming\n- Big O notation\n- Recursion\n- Data structures\n\nSpecific topic poocho!",
        "History": "**History:**\nYeh topics available hain:\n- World War 1 & 2\n- Major historical events\n\nKoi specific event poocho!",
    }

    if subject in subject_fallbacks:
        return subject_fallbacks[subject]

    return """**Jawab nahi mila!**

Main abhi yeh topics samjha sakta hoon:

**Physics:** Newton's Laws, Ohm's Law, Gravity, Atom
**Biology:** Photosynthesis, DNA, Mitosis/Meiosis
**Math:** Pythagoras Theorem
**Chemistry:** Chemical Bonds, Periodic Table
**CS:** Python, Big O, Recursion
**History:** World Wars

Inhi topics mein se koi sawaal karo, main detail mein samjhaunga! 😊"""


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    question = data.get("question", "").strip()
    subject = data.get("subject", "All Subjects")

    if not question:
        return jsonify({"error": "Question nahi likha!"}), 400

    try:
        answer = find_answer(question, subject)
        return jsonify({
            "answer": answer,
            "subject": subject,
            "timestamp": datetime.now().strftime("%H:%M"),
            "tokens_used": len(answer.split())
        })
    except Exception as e:
        return jsonify({"error": f"Error: {str(e)}"}), 500


@app.route("/subjects", methods=["GET"])
def get_subjects():
    subjects = [
        {"id": "all", "name": "All Subjects", "emoji": "📚"},
        {"id": "math", "name": "Mathematics", "emoji": "🔢"},
        {"id": "physics", "name": "Physics", "emoji": "⚛️"},
        {"id": "chemistry", "name": "Chemistry", "emoji": "🧪"},
        {"id": "biology", "name": "Biology", "emoji": "🧬"},
        {"id": "cs", "name": "Computer Science", "emoji": "💻"},
        {"id": "history", "name": "History", "emoji": "🏛️"},
        {"id": "english", "name": "English", "emoji": "📝"},
        {"id": "urdu", "name": "Urdu", "emoji": "✍️"},
        {"id": "islamiat", "name": "Islamiat", "emoji": "☪️"},
    ]
    return jsonify(subjects)


if __name__ == "__main__":
    print("✅ StudyMind AI chal raha hai!")
    print("🔑 Koi API key nahi chahiye!")
    print("🌐 Browser mein kholein: http://127.0.0.1:5000")
    app.run(debug=True, port=5000)
