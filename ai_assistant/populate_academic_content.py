"""
Populate Academic Content - Script to add educational content for VI students
Run this script to populate the offline database with academic subjects and topics
"""

import csv
import os
from datetime import datetime

# Academic content organized by subject
ACADEMIC_CONTENT = {
    "Mathematics": [
        {
            "question": "What is algebra?",
            "answer": "Algebra is a branch of mathematics that uses symbols and letters to represent numbers and quantities in formulas and equations. It allows us to solve problems by finding unknown values. For example, in the equation x plus 3 equals 7, we can solve for x to find that x equals 4. Algebra is fundamental to advanced mathematics and is used in science, engineering, and everyday problem-solving.",
            "keywords": "algebra,mathematics,equations,variables,solving"
        },
        {
            "question": "What is geometry?",
            "answer": "Geometry is the branch of mathematics concerned with shapes, sizes, positions, and properties of space. It studies points, lines, angles, surfaces, and solids. Geometry helps us understand spatial relationships and is used in architecture, art, engineering, and navigation. Basic concepts include triangles, circles, rectangles, and their properties like area, perimeter, and volume.",
            "keywords": "geometry,shapes,mathematics,angles,area,volume"
        },
        {
            "question": "What is the Pythagorean theorem?",
            "answer": "The Pythagorean theorem states that in a right triangle, the square of the length of the hypotenuse (the longest side) equals the sum of the squares of the other two sides. Written as a squared plus b squared equals c squared. This theorem is named after the ancient Greek mathematician Pythagoras and is one of the most important principles in geometry, used in construction, navigation, and computer graphics.",
            "keywords": "pythagorean,theorem,triangle,geometry,mathematics,hypotenuse"
        },
        {
            "question": "What is calculus?",
            "answer": "Calculus is an advanced branch of mathematics that studies continuous change. It has two main branches: differential calculus, which deals with rates of change and slopes of curves, and integral calculus, which deals with accumulation of quantities and areas under curves. Calculus is essential in physics, engineering, economics, and computer science. It helps us understand motion, optimization, and complex systems.",
            "keywords": "calculus,mathematics,derivatives,integrals,change,advanced"
        }
    ],
    "Physics": [
        {
            "question": "What is Newton's First Law of Motion?",
            "answer": "Newton's First Law of Motion, also called the Law of Inertia, states that an object at rest stays at rest, and an object in motion stays in motion with the same speed and direction, unless acted upon by an external force. This means objects resist changes to their state of motion. For example, a ball will not move unless you kick it, and a rolling ball will continue rolling unless friction or another force stops it.",
            "keywords": "newton,physics,motion,inertia,force,law"
        },
        {
            "question": "What is energy?",
            "answer": "Energy is the ability to do work or cause change. It exists in many forms including kinetic energy (energy of motion), potential energy (stored energy), thermal energy (heat), electrical energy, and chemical energy. Energy cannot be created or destroyed, only transformed from one form to another. This is known as the Law of Conservation of Energy. Understanding energy is fundamental to physics and affects everything from how cars move to how our bodies function.",
            "keywords": "energy,physics,kinetic,potential,conservation,work"
        },
        {
            "question": "What is gravity?",
            "answer": "Gravity is a fundamental force of nature that attracts all objects with mass toward each other. The more mass an object has, the stronger its gravitational pull. Earth's gravity keeps us on the ground and the Moon in orbit. Sir Isaac Newton first described gravity mathematically, showing that it decreases with distance squared. Gravity is responsible for the formation of stars, planets, and the structure of the universe.",
            "keywords": "gravity,physics,force,newton,mass,attraction"
        }
    ],
    "Biology": [
        {
            "question": "What is a cell?",
            "answer": "A cell is the basic structural and functional unit of all living organisms. It is the smallest unit of life that can function independently. Cells contain genetic material (DNA), produce energy, and can reproduce. There are two main types: prokaryotic cells (simple cells without a nucleus, like bacteria) and eukaryotic cells (complex cells with a nucleus, like plant and animal cells). Understanding cells is fundamental to biology because all living things are made of one or more cells.",
            "keywords": "cell,biology,life,organism,dna,structure"
        },
        {
            "question": "What is photosynthesis?",
            "answer": "Photosynthesis is the process by which plants, algae, and some bacteria convert light energy (usually from the sun) into chemical energy stored in glucose. Plants use carbon dioxide from the air and water from the soil, and with the help of chlorophyll in their leaves, they produce glucose and oxygen. The oxygen is released into the atmosphere, which is essential for animal life. Photosynthesis is crucial for life on Earth as it provides food and oxygen.",
            "keywords": "photosynthesis,plants,biology,sunlight,oxygen,glucose,chlorophyll"
        },
        {
            "question": "What is DNA?",
            "answer": "DNA, or deoxyribonucleic acid, is the molecule that carries genetic information in all living organisms. It consists of two long strands forming a double helix structure. DNA contains instructions for building and maintaining an organism, determining traits like eye color, height, and blood type. Genes are segments of DNA that code for specific proteins. DNA is passed from parents to offspring, which is why children resemble their parents. Understanding DNA is essential to genetics, medicine, and evolutionary biology.",
            "keywords": "dna,biology,genetics,heredity,genes,double helix"
        }
    ],
    "Chemistry": [
        {
            "question": "What is an atom?",
            "answer": "An atom is the smallest unit of matter that retains the properties of an element. It consists of a nucleus containing protons (positively charged) and neutrons (no charge), surrounded by electrons (negatively charged) in orbital shells. Different elements have different numbers of protons. For example, hydrogen has 1 proton, while oxygen has 8. Atoms combine to form molecules. Understanding atoms is fundamental to chemistry because all matter is made of atoms.",
            "keywords": "atom,chemistry,proton,neutron,electron,element,matter"
        },
        {
            "question": "What is a chemical reaction?",
            "answer": "A chemical reaction is a process where substances (reactants) are transformed into different substances (products) through breaking and forming of chemical bonds. During a reaction, atoms are rearranged but not created or destroyed. Chemical reactions are everywhere: burning wood, cooking food, rusting iron, and digestion in our bodies. Reactions can release energy (exothermic) or absorb energy (endothermic). Understanding chemical reactions is essential to chemistry and helps explain how matter changes.",
            "keywords": "chemical reaction,chemistry,reactants,products,bonds,transformation"
        },
        {
            "question": "What is the periodic table?",
            "answer": "The periodic table is an organized chart of all known chemical elements arranged by atomic number (number of protons). Elements are grouped into columns called groups, which share similar chemical properties, and rows called periods. The table was created by Dmitri Mendeleev and helps scientists predict how elements will behave and interact. It includes metals, nonmetals, and metalloids. The periodic table is one of the most important tools in chemistry and shows patterns in element properties.",
            "keywords": "periodic table,chemistry,elements,mendeleev,atomic number,organization"
        }
    ],
    "English": [
        {
            "question": "What is a noun?",
            "answer": "A noun is a word that names a person, place, thing, or idea. Nouns are one of the main parts of speech in English grammar. There are several types of nouns: common nouns (like dog, city, book), proper nouns (names like London, Shakespeare), abstract nouns (ideas like happiness, freedom), and collective nouns (groups like team, family). Nouns can be singular or plural, and they function as subjects or objects in sentences. Understanding nouns is fundamental to constructing sentences.",
            "keywords": "noun,english,grammar,language,parts of speech,word"
        },
        {
            "question": "What is a verb?",
            "answer": "A verb is a word that expresses an action, occurrence, or state of being. Verbs are essential to sentences because they tell us what is happening. Action verbs describe what someone or something does (run, write, think). Linking verbs connect the subject to additional information (is, am, seems). Helping verbs work with main verbs (can, will, have). Verbs change form based on tense (past, present, future) and subject. Every complete sentence needs a verb.",
            "keywords": "verb,english,grammar,action,language,sentence,tense"
        },
        {
            "question": "What is a metaphor?",
            "answer": "A metaphor is a figure of speech that directly compares two different things by stating that one thing is another, without using 'like' or 'as'. For example, 'Time is money' or 'Her voice is music to my ears'. Metaphors create vivid images and help readers understand complex ideas by comparing them to familiar things. They are common in poetry, literature, and everyday speech. Metaphors make language more interesting and expressive. Understanding metaphors improves comprehension and writing skills.",
            "keywords": "metaphor,english,literature,figurative language,comparison,poetry"
        }
    ],
    "History": [
        {
            "question": "What was the Industrial Revolution?",
            "answer": "The Industrial Revolution was a period of major technological, economic, and social change that began in Britain in the late 1700s and spread worldwide. It marked the transition from hand production to machine manufacturing. Key innovations included the steam engine, textile machinery, and iron production methods. Factories replaced small workshops, and people moved from rural areas to cities for work. The Industrial Revolution dramatically changed how goods were produced, increased economic productivity, and transformed society, though it also created challenges like poor working conditions and pollution.",
            "keywords": "industrial revolution,history,technology,factories,manufacturing,society"
        },
        {
            "question": "What was World War Two?",
            "answer": "World War Two was a global conflict from 1939 to 1945, involving most of the world's nations. It was the deadliest war in history, causing millions of deaths. The main opposing sides were the Allies (including Britain, United States, and Soviet Union) and the Axis powers (Germany, Italy, and Japan). The war began when Germany, led by Adolf Hitler, invaded Poland. Major events included the Holocaust, the bombing of Pearl Harbor, D-Day invasion, and the atomic bombings of Hiroshima and Nagasaki. The war ended with Allied victory and led to the formation of the United Nations.",
            "keywords": "world war two,history,war,allies,axis,hitler,conflict"
        }
    ],
    "Geography": [
        {
            "question": "What is climate?",
            "answer": "Climate is the average weather pattern in a region over a long period of time, typically 30 years or more. It includes patterns of temperature, humidity, rainfall, wind, and seasons. Climate is different from weather, which describes short-term atmospheric conditions. Different regions have different climate types, such as tropical, desert, temperate, and polar climates. Climate is influenced by factors like latitude, altitude, distance from oceans, and terrain. Understanding climate helps us predict seasonal patterns and understand ecosystems.",
            "keywords": "climate,geography,weather,temperature,environment,patterns"
        },
        {
            "question": "What is a continent?",
            "answer": "A continent is one of Earth's seven large, continuous landmasses. The seven continents are Africa, Antarctica, Asia, Australia (Oceania), Europe, North America, and South America. Continents are the largest geographical divisions of Earth's land. Each continent has its own unique features, climates, cultures, and ecosystems. Continents sit on tectonic plates and have been moving slowly over millions of years. Understanding continents is fundamental to geography and helps us organize knowledge about Earth's diverse regions.",
            "keywords": "continent,geography,landmass,earth,world,regions"
        }
    ]
}


def populate_knowledge_base(data_dir="offline_data"):
    """Populate the knowledge base with academic content"""
    csv_file = os.path.join(data_dir, "aivi_knowledge_base.csv")

    # Ensure directory exists
    os.makedirs(data_dir, exist_ok=True)

    # Read existing data to avoid duplicates
    existing_questions = set()
    if os.path.exists(csv_file):
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                existing_questions.add(row['question'])

    # Open file in append mode
    with open(csv_file, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)

        # Write header if file is new
        if not existing_questions:
            writer.writerow(['id', 'category', 'question', 'answer', 'keywords', 'source', 'timestamp', 'confidence'])

        entry_id = len(existing_questions) + 1

        # Add all academic content
        for subject, topics in ACADEMIC_CONTENT.items():
            for topic in topics:
                if topic['question'] not in existing_questions:
                    writer.writerow([
                        entry_id,
                        subject.lower(),
                        topic['question'],
                        topic['answer'],
                        topic['keywords'],
                        'academic_curriculum',
                        datetime.now().isoformat(),
                        0.95
                    ])
                    entry_id += 1
                    print(f"Added: {subject} - {topic['question']}")

    print(f"\nSuccessfully populated knowledge base with {entry_id - 1} entries!")
    print(f"Subjects available: {', '.join(ACADEMIC_CONTENT.keys())}")


if __name__ == "__main__":
    print("Populating AIVI knowledge base with academic content...")
    print("=" * 60)
    populate_knowledge_base()
    print("=" * 60)
    print("Done! You can now use voice commands like:")
    print("- 'List subjects'")
    print("- 'Learn Mathematics'")
    print("- 'Learn Biology'")
    print("- 'What is photosynthesis?'")
