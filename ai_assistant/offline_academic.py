
import os

# Flag file to indicate offline/online mode
MODE_FLAG_FILE = 'assistant_mode.flag'

def set_mode(mode):
    """
    Set the assistant mode to 'offline' or 'online'.
    This creates or updates a flag file with the mode.
    """
    assert mode in ('offline', 'online'), "Mode must be 'offline' or 'online'"
    with open(MODE_FLAG_FILE, 'w') as f:
        f.write(mode)

def get_mode():
    """
    Get the current assistant mode ('offline' or 'online').
    Returns 'offline' if the flag file does not exist.
    """
    if not os.path.exists(MODE_FLAG_FILE):
        return 'offline'
    with open(MODE_FLAG_FILE, 'r') as f:
        return f.read().strip()

"""
Offline Academic Data Model
"""
offline_data = {
    # BASIC LEVEL (at least 35 entries)
    "basic": {
        "mathematics": {
            "addition": (
                "Addition is the process of finding the total or sum by combining two or more numbers. "
                "For example, 2 + 3 = 5. Addition is used in daily life when counting money or objects. "
                "Further reading: https://www.khanacademy.org/math/arithmetic/arith-review-add-subtract; Book: 'Mathematics for Elementary School' by Pearson."
            ),
            "subtraction": (
                "Subtraction is taking one number away from another. For example, 5 - 2 = 3. "
                "Subtraction is used to find out how much is left after taking some away. "
                "Further reading: https://www.khanacademy.org/math/arithmetic/arith-review-add-subtract; Book: 'Mathematics for Elementary School' by Pearson."
            ),
            "multiplication": (
                "Multiplication is repeated addition of the same number. For example, 3 x 4 = 12 means 3 added 4 times. "
                "It is used in calculating area, arrays, and groups. "
                "Further reading: https://www.khanacademy.org/math/arithmetic/arith-review-multiply-divide; Book: 'Mathematics for Elementary School' by Pearson."
            ),
            "division": (
                "Division is splitting a number into equal parts. For example, 12 ÷ 3 = 4. "
                "Division is used in sharing, grouping, and distributing items. "
                "Further reading: https://www.khanacademy.org/math/arithmetic/arith-review-multiply-divide; Book: 'Mathematics for Elementary School' by Pearson."
            ),
            "shapes": (
                "Basic shapes include circle, square, triangle, and rectangle. Each shape has unique properties: a square has 4 equal sides, a triangle has 3 sides, etc. "
                "Shapes are found everywhere, such as wheels (circles) and books (rectangles). "
                "Further reading: https://www.mathsisfun.com/geometry/plane-shapes.html; Book: 'Shapes and Geometry' by DK Publishing."
            ),
            "fractions": (
                "A fraction represents a part of a whole, like 1/2 means one out of two equal parts. "
                "Fractions are used in cooking, measuring, and dividing objects. "
                "Further reading: https://www.khanacademy.org/math/arithmetic/fraction-arithmetic; Book: 'Fractions, Decimals, and Percents' by David A. Adler."
            ),
            "place value": (
                "Place value is the value of each digit in a number, such as the 5 in 53 means 50. "
                "Understanding place value helps in reading and writing large numbers. "
                "Further reading: https://www.khanacademy.org/math/arithmetic/arith-review-place-value; Book: 'Place Value' by David A. Adler."
            ),
            "counting": (
                "Counting is listing numbers in order, usually starting from one. For example, 1, 2, 3, 4... "
                "Counting is the basis for all math and is used in daily life. "
                "Further reading: https://www.khanacademy.org/math/early-math/counting; Book: 'Counting' by DK Publishing."
            ),
            "even numbers": (
                "Even numbers are divisible by 2, such as 2, 4, 6, 8. "
                "Even numbers end in 0, 2, 4, 6, or 8. "
                "Further reading: https://www.mathsisfun.com/numbers/even-odd-numbers.html; Book: 'Numbers' by DK Publishing."
            ),
            "odd numbers": (
                "Odd numbers are not divisible by 2, such as 1, 3, 5, 7. "
                "Odd numbers end in 1, 3, 5, 7, or 9. "
                "Further reading: https://www.mathsisfun.com/numbers/even-odd-numbers.html; Book: 'Numbers' by DK Publishing."
            ),
            "number line": (
                "A number line is a straight line with numbers placed at equal intervals. It helps in addition, subtraction, and understanding negative numbers. "
                "For example, to add 2 + 3, start at 2 and move 3 steps right. "
                "Further reading: https://www.khanacademy.org/math/arithmetic/arith-review-negative-numbers/arith-review-number-line/v/number-line-intro; Book: 'Number Lines' by DK Publishing."
            ),
            "greater than": (
                "Greater than means bigger in value. For example, 7 is greater than 5. The symbol is >. "
                "Used in comparing numbers and quantities. "
                "Further reading: https://www.khanacademy.org/math/early-math/cc-early-math-compare-order-topic; Book: 'Comparing Numbers' by DK Publishing."
            ),
            "less than": (
                "Less than means smaller in value. For example, 3 is less than 8. The symbol is <. "
                "Used in comparing numbers and quantities. "
                "Further reading: https://www.khanacademy.org/math/early-math/cc-early-math-compare-order-topic; Book: 'Comparing Numbers' by DK Publishing."
            ),
            "equal to": (
                "Equal to means the same in value. For example, 4 + 2 is equal to 6. The symbol is =. "
                "Used in equations and comparisons. "
                "Further reading: https://www.khanacademy.org/math/early-math/cc-early-math-compare-order-topic; Book: 'Comparing Numbers' by DK Publishing."
            ),
            "tens and units": (
                "Tens and units are place values in numbers. In 34, 3 is tens and 4 is units. "
                "Understanding this helps in addition and subtraction. "
                "Further reading: https://www.khanacademy.org/math/arithmetic/arith-review-place-value; Book: 'Place Value' by David A. Adler."
            ),
            "hundreds": (
                "Hundreds is the third place value in a number. In 245, 2 is hundreds. "
                "Used in reading and writing large numbers. "
                "Further reading: https://www.khanacademy.org/math/arithmetic/arith-review-place-value; Book: 'Place Value' by David A. Adler."
            ),
            "skip counting": (
                "Skip counting is counting forward or backward by a number other than 1. For example, 2, 4, 6, 8... "
                "It helps in learning multiplication tables. "
                "Further reading: https://www.khanacademy.org/math/early-math/cc-early-math-counting-topic; Book: 'Counting' by DK Publishing."
            ),
            "ordinal numbers": (
                "Ordinal numbers show position or order, such as 1st, 2nd, 3rd. "
                "Used in races, lists, and rankings. "
                "Further reading: https://www.khanacademy.org/math/early-math/cc-early-math-counting-topic; Book: 'Counting' by DK Publishing."
            ),
            "money": (
                "Money is used to buy goods and services. Coins and notes have different values. "
                "Learning about money helps in shopping and saving. "
                "Further reading: https://www.khanacademy.org/math/early-math/cc-early-math-money-topic; Book: 'Money Math' by David A. Adler."
            ),
            "time": (
                "Time is measured in seconds, minutes, and hours. A clock shows time. "
                "Understanding time helps in daily routines and schedules. "
                "Further reading: https://www.khanacademy.org/math/early-math/cc-early-math-time-topic; Book: 'Telling Time' by Jules Older."
            ),
            "calendar": (
                "A calendar shows days, weeks, and months in a year. For example, January is the first month. "
                "Calendars help us plan events and remember important dates. "
                "Further reading: https://www.khanacademy.org/math/early-math/cc-early-math-time-topic; Book: 'Calendars' by David A. Adler."
            ),
            "measurement": (
                "Measurement is finding the length, size, or amount of something. We use rulers, scales, and cups to measure. "
                "Measurement is important in cooking, building, and science. "
                "Further reading: https://www.khanacademy.org/math/early-math/cc-early-math-measure-data-topic; Book: 'Measuring Penny' by Loreen Leedy."
            ),
            "weight": (
                "Weight is how heavy something is. We use kilograms and grams to measure weight. "
                "Knowing weight helps in shopping and cooking. "
                "Further reading: https://www.khanacademy.org/math/early-math/cc-early-math-measure-data-topic; Book: 'Measuring Penny' by Loreen Leedy."
            ),
            "capacity": (
                "Capacity is how much something can hold. We use liters and milliliters to measure capacity. "
                "Used in cooking and science experiments. "
                "Further reading: https://www.khanacademy.org/math/early-math/cc-early-math-measure-data-topic; Book: 'Measuring Penny' by Loreen Leedy."
            ),
            "temperature": (
                "Temperature tells how hot or cold something is. We use degrees Celsius or Fahrenheit. "
                "Thermometers are used to measure temperature. "
                "Further reading: https://www.khanacademy.org/math/early-math/cc-early-math-measure-data-topic; Book: 'What Is Temperature?' by Chris Arvetis."
            ),
            "patterns": (
                "Patterns are repeated designs or sequences, such as red-blue-red-blue. "
                "Patterns are found in art, music, and nature. "
                "Further reading: https://www.khanacademy.org/math/early-math/cc-early-math-patterns-topic; Book: 'Pattern Bugs' by Trudy Harris."
            ),
            "bar graph": (
                "A bar graph is a chart that uses bars to show data. Each bar shows a value. "
                "Bar graphs are used in surveys and science. "
                "Further reading: https://www.khanacademy.org/math/early-math/cc-early-math-measure-data-topic; Book: 'The Great Graph Contest' by Loreen Leedy."
            ),
            "pictogram": (
                "A pictogram uses pictures to show data. Each picture stands for a number of things. "
                "Pictograms are used in books and signs. "
                "Further reading: https://www.khanacademy.org/math/early-math/cc-early-math-measure-data-topic; Book: 'Picture Graphs' by Molly Blaisdell."
            ),
            "tally marks": (
                "Tally marks are used to count objects. Every fifth mark crosses the previous four. "
                "Tally marks are used in counting votes and scores. "
                "Further reading: https://www.khanacademy.org/math/early-math/cc-early-math-measure-data-topic; Book: 'Tally O'Malley' by Stuart J. Murphy."
            ),
            "word problems": (
                "Word problems use stories to describe math problems. For example, 'If you have 3 apples and get 2 more, how many do you have?' "
                "Solving word problems helps in real-life situations. "
                "Further reading: https://www.khanacademy.org/math/early-math/cc-early-math-add-subtract-topic; Book: 'Word Problems, Grade 1' by Spectrum."
            ),
            "basic probability": (
                "Probability is the chance of something happening. For example, flipping a coin has a probability of 1/2 for heads. "
                "Probability is used in games and predictions. "
                "Further reading: https://www.khanacademy.org/math/statistics-probability/probability-library; Book: 'Probably Pistachio' by Stuart J. Murphy."
            ),
            "simple equations": (
                "Simple equations use numbers and symbols to show equality, like x + 2 = 5. "
                "Solving equations helps in finding unknown values. "
                "Further reading: https://www.khanacademy.org/math/algebra-basics/alg-basics-eq-ineq; Book: 'Algebra for Beginners' by Reza Nazari."
            ),
            "rounding numbers": (
                "Rounding means making a number simpler but keeping its value close. For example, 47 rounded to the nearest ten is 50. "
                "Rounding is used in estimation and mental math. "
                "Further reading: https://www.khanacademy.org/math/arithmetic/arith-review-estimation-rounding; Book: 'Rounding Numbers' by Rebecca Wingard-Nelson."
            ),
            "estimation": (
                "Estimation is finding a value close to the actual answer. For example, estimating the number of candies in a jar. "
                "Estimation is useful when an exact answer is not needed. "
                "Further reading: https://www.khanacademy.org/math/arithmetic/arith-review-estimation-rounding; Book: 'Estimation' by David A. Adler."
            ),
            "division with remainder": (
                "Division with remainder is when a number does not divide evenly. For example, 7 ÷ 2 = 3 remainder 1. "
                "This is used in sharing and grouping objects. "
                "Further reading: https://www.khanacademy.org/math/arithmetic/arith-review-multiply-divide; Book: 'Division' by Sheila Cato."
            )
        },
        "english": {
            "noun": (
                "A noun is a word that names a person, place, thing, or idea. For example, 'dog', 'city', and 'happiness' are nouns. "
                "Nouns can be common (cat) or proper (London). "
                "Further reading: https://www.grammarly.com/blog/nouns/; Book: 'English Grammar in Use' by Raymond Murphy."
            ),
            "verb": (
                "A verb is a word that expresses an action or a state of being. For example, 'run', 'think', and 'is' are verbs. "
                "Verbs can show what someone does or what something is. "
                "Further reading: https://www.grammarly.com/blog/verbs/; Book: 'English Grammar in Use' by Raymond Murphy."
            ),
            "adjective": (
                "An adjective is a word that describes a noun. For example, 'blue', 'quick', and 'happy' are adjectives. "
                "Adjectives tell us more about nouns, like 'a tall building'. "
                "Further reading: https://www.grammarly.com/blog/adjective/; Book: 'English Grammar in Use' by Raymond Murphy."
            ),
            "sentence": (
                "A sentence is a group of words that expresses a complete thought. For example, 'The sun is shining.' "
                "A sentence starts with a capital letter and ends with a full stop, question mark, or exclamation mark. "
                "Further reading: https://www.grammarly.com/blog/sentence/; Book: 'English Grammar in Use' by Raymond Murphy."
            ),
            "alphabet": (
                "The alphabet is a set of letters used in a language. The English alphabet has 26 letters from A to Z. "
                "Learning the alphabet is the first step in reading and writing. "
                "Further reading: https://www.englishclub.com/english-letters-alphabet.htm; Book: 'Chicka Chicka Boom Boom' by Bill Martin Jr."
            ),
            "reading": (
                "Reading is the process of looking at and understanding written words. For example, reading a book or a sign. "
                "Reading helps us learn new things and enjoy stories. "
                "Further reading: https://www.readingrockets.org/; Book: 'The Reading Strategies Book' by Jennifer Serravallo."
            ),
            "writing": (
                "Writing is the act of forming letters and words on a surface. For example, writing a letter or a story. "
                "Writing helps us communicate ideas and information. "
                "Further reading: https://www.readingrockets.org/teaching/writing; Book: 'Writing Skills' by Diana Hanbury King."
            ),
            "pronoun": (
                "A pronoun is a word that takes the place of a noun. For example, 'he', 'she', 'it', and 'they' are pronouns. "
                "Pronouns help avoid repeating the same nouns. "
                "Further reading: https://www.grammarly.com/blog/pronouns/; Book: 'English Grammar in Use' by Raymond Murphy."
            ),
            "adverb": (
                "An adverb modifies a verb, adjective, or another adverb. For example, 'quickly', 'very', and 'well' are adverbs. "
                "Adverbs often tell us how, when, or where something happens. "
                "Further reading: https://www.grammarly.com/blog/adverbs/; Book: 'English Grammar in Use' by Raymond Murphy."
            ),
            "preposition": (
                "A preposition shows the relationship of a noun or pronoun to another word. For example, 'in', 'on', 'under', and 'with'. "
                "Prepositions tell us about place, time, and direction. "
                "Further reading: https://www.grammarly.com/blog/prepositions/; Book: 'English Grammar in Use' by Raymond Murphy."
            ),
            "conjunction": (
                "A conjunction joins words or groups of words. For example, 'and', 'but', and 'or' are conjunctions. "
                "Conjunctions help connect ideas in sentences. "
                "Further reading: https://www.grammarly.com/blog/conjunctions/; Book: 'English Grammar in Use' by Raymond Murphy."
            ),
            "interjection": (
                "An interjection expresses strong feeling or emotion. For example, 'Wow!', 'Oh!', and 'Oops!'. "
                "Interjections are often followed by an exclamation mark. "
                "Further reading: https://www.grammarly.com/blog/interjections/; Book: 'English Grammar in Use' by Raymond Murphy."
            ),
            "capital letter": (
                "A capital letter is used at the beginning of a sentence or proper noun. For example, 'London' and 'Sarah'. "
                "Capital letters show importance and start new sentences. "
                "Further reading: https://www.grammarly.com/blog/capitalization-rules/; Book: 'English Grammar in Use' by Raymond Murphy."
            ),
            "full stop": (
                "A full stop is used at the end of a sentence. For example, 'The cat sleeps.' "
                "It shows that a thought is complete. "
                "Further reading: https://www.grammarly.com/blog/period/; Book: 'English Grammar in Use' by Raymond Murphy."
            ),
            "question mark": (
                "A question mark is used at the end of a question. For example, 'How are you?' "
                "It shows that a sentence is asking something. "
                "Further reading: https://www.grammarly.com/blog/question-mark/; Book: 'English Grammar in Use' by Raymond Murphy."
            ),
            "comma": (
                "A comma is used to separate items in a list. For example, 'I bought apples, oranges, and bananas.' "
                "Commas also separate parts of sentences. "
                "Further reading: https://www.grammarly.com/blog/comma/; Book: 'English Grammar in Use' by Raymond Murphy."
            ),
            "exclamation mark": (
                "An exclamation mark shows strong feeling. For example, 'Wow!' or 'Stop!' "
                "It is used after interjections and exclamatory sentences. "
                "Further reading: https://www.grammarly.com/blog/exclamation-mark/; Book: 'English Grammar in Use' by Raymond Murphy."
            ),
            "vowel": (
                "A vowel is a, e, i, o, or u. Every English word has at least one vowel. "
                "Vowels are important for making syllables and words. "
                "Further reading: https://www.englishclub.com/pronunciation/vowels.htm; Book: 'Chicka Chicka Boom Boom' by Bill Martin Jr."
            ),
            "consonant": (
                "A consonant is any letter that is not a vowel. For example, b, c, d, f, etc. "
                "Consonants and vowels work together to form words. "
                "Further reading: https://www.englishclub.com/pronunciation/consonants.htm; Book: 'Chicka Chicka Boom Boom' by Bill Martin Jr."
            ),
            "syllable": (
                "A syllable is a unit of pronunciation. For example, 'cat' has one syllable, 'happy' has two. "
                "Syllables help us break words into parts for reading and spelling. "
                "Further reading: https://www.readingrockets.org/strategies/syllable_games; Book: 'Syllables' by Rebecca Felix."
            ),
            "rhyming words": (
                "Rhyming words sound the same at the end. For example, 'cat' and 'hat'. "
                "Rhymes are used in poems and songs. "
                "Further reading: https://www.readingrockets.org/strategies/rhyming; Book: 'Rhyming Dust Bunnies' by Jan Thomas."
            ),
            "opposite words": (
                "Opposite words have different meanings. For example, 'hot' and 'cold'. "
                "Learning opposites helps expand vocabulary. "
                "Further reading: https://www.englishclub.com/vocabulary/opposites-antonyms.htm; Book: 'Big and Small' by Britta Teckentrup."
            ),
            "synonyms": (
                "Synonyms are words with similar meanings. For example, 'happy' and 'joyful'. "
                "Using synonyms makes writing more interesting. "
                "Further reading: https://www.englishclub.com/vocabulary/synonyms.htm; Book: 'The Synonym Finder' by J.I. Rodale."
            ),
            "antonyms": (
                "Antonyms are words with opposite meanings. For example, 'up' and 'down'. "
                "Antonyms help us describe differences. "
                "Further reading: https://www.englishclub.com/vocabulary/opposites-antonyms.htm; Book: 'Big and Small' by Britta Teckentrup."
            ),
            "plural": (
                "Plural means more than one. For example, 'cats' is the plural of 'cat'. "
                "Plurals are formed in different ways, like adding -s or -es. "
                "Further reading: https://www.grammarly.com/blog/plural-nouns/; Book: 'English Grammar in Use' by Raymond Murphy."
            ),
            "singular": (
                "Singular means one. For example, 'dog' is singular, 'dogs' is plural. "
                "Singular and plural forms help us talk about quantity. "
                "Further reading: https://www.grammarly.com/blog/plural-nouns/; Book: 'English Grammar in Use' by Raymond Murphy."
            ),
            "story": (
                "A story is a description of imaginary or real events. For example, fairy tales and news reports are stories. "
                "Stories have a beginning, middle, and end. "
                "Further reading: https://www.readingrockets.org/strategies/story-maps; Book: 'The True Story of the Three Little Pigs' by Jon Scieszka."
            ),
            "poem": (
                "A poem is a piece of writing with rhythm and imagery. For example, 'Twinkle, Twinkle, Little Star' is a poem. "
                "Poems can rhyme and use creative language. "
                "Further reading: https://www.poetryfoundation.org/; Book: 'Where the Sidewalk Ends' by Shel Silverstein."
            ),
            "letter writing": (
                "Letter writing is a way to communicate in writing. For example, writing a thank-you note or an email. "
                "Letters have a greeting, body, and closing. "
                "Further reading: https://www.readingrockets.org/strategies/letter-writing; Book: 'The Jolly Postman' by Janet & Allan Ahlberg."
            ),
            "greeting": (
                "A greeting is a polite word or sign of welcome. For example, 'Hello', 'Good morning', and 'Hi'. "
                "Greetings are used at the start of conversations and letters. "
                "Further reading: https://www.englishclub.com/vocabulary/greetings.htm; Book: 'Say Hello!' by Rachel Isadora."
            ),
            "farewell": (
                "A farewell is a word or act of saying goodbye. For example, 'Goodbye', 'See you later', and 'Take care'. "
                "Farewells are used at the end of conversations and letters. "
                "Further reading: https://www.englishclub.com/vocabulary/greetings.htm; Book: 'Goodbye Friend! Hello Friend!' by Cori Doerrfeld."
            )
        },
        "science": {
            "plant": (
                "A plant is a living thing that grows in the ground and usually has leaves, stems, and roots. "
                "Plants make their own food through photosynthesis and provide oxygen. "
                "Example: Mango tree, maize plant. "
                "Further reading: https://www.britannica.com/science/plant; Book: 'The Magic School Bus Plants Seeds' by Joanna Cole."
            ),
            "animal": (
                "An animal is a living creature that moves and eats other things for energy. "
                "Animals can be wild or domestic, and include mammals, birds, fish, and insects. "
                "Example: Lion, goat, butterfly. "
                "Further reading: https://www.nationalgeographic.com/animals; Book: 'Animals: A Visual Encyclopedia' by DK Publishing."
            ),
            "water cycle": (
                "The water cycle is the journey water takes as it moves from the land to the sky and back again. "
                "It includes evaporation, condensation, precipitation, and collection. "
                "Example: Rain falls, water evaporates from lakes, forms clouds, and rains again. "
                "Further reading: https://www.kidsdiscover.com/quick-reads/water-cycle/; Book: 'The Drop in My Drink' by Meredith Hooper."
            ),
            "human body": (
                "The human body is made up of many parts that work together to keep us alive. "
                "Major systems include the circulatory, respiratory, digestive, and nervous systems. "
                "Example: The heart pumps blood, the lungs help us breathe. "
                "Further reading: https://kidshealth.org/en/kids/body.html; Book: 'The Human Body Book' by Steve Parker."
            ),
            "senses": (
                "The five senses are sight, hearing, taste, touch, and smell. "
                "They help us understand and interact with the world. "
                "Example: We use our eyes to see, ears to hear. "
                "Further reading: https://www.bbc.co.uk/bitesize/topics/z9yycdm; Book: 'My Five Senses' by Aliki."
            ),
            "food chain": (
                "A food chain shows how each living thing gets food. "
                "It starts with plants, then herbivores, then carnivores. "
                "Example: Grass → Grasshopper → Bird → Hawk. "
                "Further reading: https://www.nationalgeographic.org/encyclopedia/food-chain/; Book: 'Who Eats What?' by Patricia Lauber."
            ),
            "habitat": (
                "A habitat is the natural home of an animal or plant. "
                "Habitats include forests, deserts, rivers, and grasslands. "
                "Example: Fish live in water habitats, lions in savannas. "
                "Further reading: https://www.bbc.co.uk/bitesize/topics/zx882hv; Book: 'About Habitats: Forests' by Cathryn Sill."
            ),
            "weather": (
                "Weather is the condition of the atmosphere at a certain time. "
                "It includes temperature, rain, wind, and sunshine. "
                "Example: Sunny, rainy, windy, or cloudy days. "
                "Further reading: https://www.weatherwizkids.com/; Book: 'Weather' by Seymour Simon."
            ),
            "seasons": (
                "Seasons are times of the year with different weather. "
                "The four seasons are spring, summer, autumn, and winter. "
                "Example: In Africa, rainy and dry seasons are common. "
                "Further reading: https://www.metoffice.gov.uk/weather/learn-about/weather/seasons; Book: 'The Reasons for Seasons' by Gail Gibbons."
            ),
            "sun": (
                "The sun is the star at the center of our solar system. "
                "It provides light and heat for life on Earth. "
                "Example: Plants need sunlight to grow. "
                "Further reading: https://www.nasa.gov/audience/forstudents/k-4/stories/nasa-knows/what-is-the-sun-k4.html; Book: 'The Sun Is My Favorite Star' by Frank Asch."
            ),
            "moon": (
                "The moon is Earth's only natural satellite. "
                "It affects tides and can be seen in different phases. "
                "Example: Full moon, new moon. "
                "Further reading: https://www.nasa.gov/audience/forstudents/k-4/stories/nasa-knows/what-is-the-moon-k4.html; Book: 'The Moon Book' by Gail Gibbons."
            ),
            "stars": (
                "Stars are huge balls of burning gas in space. "
                "They form constellations and can be seen at night. "
                "Example: The North Star, Orion's Belt. "
                "Further reading: https://www.space.com/56-stars-formation-and-evolution-of-stars.html; Book: 'There Are Stars in the Sky' by Franklyn M. Branley."
            ),
            "earth": (
                "Earth is the planet we live on. "
                "It has land, water, air, and supports life. "
                "Example: Africa is one of Earth's continents. "
                "Further reading: https://www.nasa.gov/audience/forstudents/k-4/stories/nasa-knows/what-is-earth-k4.html; Book: 'Planet Earth/Inside Out' by Gail Gibbons."
            ),
            "air": (
                "Air is the mixture of gases we breathe. "
                "It contains oxygen, which is essential for life. "
                "Example: We need air to breathe. "
                "Further reading: https://www.ducksters.com/science/earth_science/air.php; Book: 'What Is the World Made Of?' by Kathleen Weidner Zoehfeld."
            ),
            "soil": (
                "Soil is the upper layer of earth where plants grow. "
                "It contains minerals, water, and organic matter. "
                "Example: Farmers grow crops in soil. "
                "Further reading: https://www.soils4kids.org/; Book: 'Dirt: The Scoop on Soil' by Natalie M. Rosinsky."
            ),
            "rocks": (
                "Rocks are solid mineral material forming part of the surface of the earth. "
                "There are three types: igneous, sedimentary, and metamorphic. "
                "Example: Granite, sandstone, marble. "
                "Further reading: https://www.bbc.co.uk/bitesize/topics/z9bbkqt; Book: 'Rocks, Fossils, and Arrowheads' by Laura Evert."
            ),
            "energy": (
                "Energy is what makes things move and work. "
                "It comes in forms like heat, light, and motion. "
                "Example: The sun gives us solar energy. "
                "Further reading: https://www.ducksters.com/science/energy.php; Book: 'Energy Makes Things Happen' by Kimberly Brubaker Bradley."
            ),
            "magnet": (
                "A magnet is an object that attracts iron. "
                "Magnets have north and south poles and are used in many devices. "
                "Example: Fridge magnets, compasses. "
                "Further reading: https://www.bbc.co.uk/bitesize/topics/zyttyrd; Book: 'What Makes a Magnet?' by Franklyn M. Branley."
            ),
            "light": (
                "Light helps us see things. "
                "It travels in straight lines and can be reflected or refracted. "
                "Example: Mirrors reflect light, water bends light. "
                "Further reading: https://www.bbc.co.uk/bitesize/topics/zbssgk7; Book: 'Light: Shadows, Mirrors, and Rainbows' by Natalie M. Rosinsky."
            ),
            "sound": (
                "Sound is what we hear. "
                "It is made by vibrations and travels through air, water, or solids. "
                "Example: Drums make sound by vibrating. "
                "Further reading: https://www.bbc.co.uk/bitesize/topics/zgffr82; Book: 'All About Sound' by Lisa Trumbauer."
            ),
            "force": (
                "A force is a push or pull. "
                "Forces can move objects or change their shape. "
                "Example: Kicking a ball, opening a door. "
                "Further reading: https://www.bbc.co.uk/bitesize/topics/zvpp34j; Book: 'Forces Make Things Move' by Kimberly Brubaker Bradley."
            ),
            "gravity": (
                "Gravity is the force that pulls things toward the earth. "
                "It keeps us on the ground and makes things fall. "
                "Example: An apple falling from a tree. "
                "Further reading: https://spaceplace.nasa.gov/what-is-gravity/en/; Book: 'Gravity Is a Mystery' by Franklyn M. Branley."
            ),
            "recycling": (
                "Recycling is reusing materials to make new things. "
                "It helps reduce waste and protect the environment. "
                "Example: Recycling plastic bottles into new products. "
                "Further reading: https://www.epa.gov/recycle; Book: 'Why Should I Recycle?' by Jen Green."
            ),
            "pollution": (
                "Pollution is making the environment dirty. "
                "It can harm plants, animals, and people. "
                "Example: Smoke from cars, plastic in rivers. "
                "Further reading: https://www.nationalgeographic.com/environment/article/pollution; Book: 'What a Waste' by Jess French."
            ),
            "healthy living": (
                "Healthy living means taking care of your body. "
                "It includes eating well, exercising, and getting enough sleep. "
                "Example: Eating fruits, playing sports. "
                "Further reading: https://kidshealth.org/en/kids/healthy-eating/; Book: 'Germs Are Not for Sharing' by Elizabeth Verdick."
            ),
            "disease": (
                "A disease is an illness that affects the body. "
                "Diseases can be caused by germs, poor nutrition, or genetics. "
                "Example: Malaria, flu, diabetes. "
                "Further reading: https://www.cdc.gov/diseasesconditions/; Book: 'What Are Germs?' by Katie Daynes."
            ),
            "medicine": (
                "Medicine is used to treat diseases. "
                "It can be in the form of pills, syrups, or injections. "
                "Example: Paracetamol for fever. "
                "Further reading: https://kidshealth.org/en/kids/medicines.html; Book: 'The Berenstain Bears Go to the Doctor' by Stan & Jan Berenstain."
            ),
            "safety": (
                "Safety means being free from danger. "
                "It involves following rules and using protective equipment. "
                "Example: Wearing a helmet when riding a bicycle. "
                "Further reading: https://www.safekids.org/safetytips; Book: 'Officer Buckle and Gloria' by Peggy Rathmann."
            ),
            "experiment": (
                "An experiment is a test to learn something new. "
                "It involves making observations and drawing conclusions. "
                "Example: Mixing vinegar and baking soda to see bubbles. "
                "Further reading: https://www.sciencebuddies.org/science-fair-projects/science-projects; Book: 'Ada Twist, Scientist' by Andrea Beaty."
            ),
            "photosynthesis": (
                "Photosynthesis is the process by which green plants use sunlight to make food from carbon dioxide and water. "
                "It produces oxygen and glucose. "
                "Example: Leaves turning sunlight into energy. "
                "Further reading: https://www.britannica.com/science/photosynthesis; Book: 'Photosynthesis: Changing Sunlight into Food' by Bobbie Kalman."
            ),
            "germination": (
                "Germination is the process by which a plant grows from a seed. "
                "It needs water, warmth, and air. "
                "Example: Beans sprouting in wet cotton. "
                "Further reading: https://www.bbc.co.uk/bitesize/topics/zpxnyrd/articles/z2vdjxs; Book: 'From Seed to Plant' by Gail Gibbons."
            ),
            "evaporation": (
                "Evaporation is the process of turning liquid into vapor. "
                "It happens when water is heated. "
                "Example: Puddles drying after rain. "
                "Further reading: https://www.weatherwizkids.com/weather-evaporation.htm; Book: 'Water Up, Down, and All Around' by Natalie M. Rosinsky."
            ),
            "condensation": (
                "Condensation is the process by which vapor becomes liquid. "
                "It forms clouds and dew. "
                "Example: Water droplets on a cold glass. "
                "Further reading: https://www.weatherwizkids.com/weather-condensation.htm; Book: 'Water Up, Down, and All Around' by Natalie M. Rosinsky."
            ),
            "precipitation": (
                "Precipitation is any form of water that falls from clouds. "
                "It includes rain, snow, sleet, and hail. "
                "Example: Rain falling from the sky. "
                "Further reading: https://www.weatherwizkids.com/weather-precipitation.htm; Book: 'Down Comes the Rain' by Franklyn M. Branley."
            ),
            "volcano": (
                "A volcano is an opening in the earth's crust that allows molten rock to escape. "
                "Volcanoes can erupt with lava, ash, and gases. "
                "Example: Mount Kilimanjaro in Tanzania. "
                "Further reading: https://www.britannica.com/science/volcano; Book: 'Volcanoes' by Seymour Simon."
            ),
            "earthquake": (
                "An earthquake is the shaking of the surface of the earth. "
                "It is caused by movement of tectonic plates. "
                "Example: Earthquakes in East Africa Rift Valley. "
                "Further reading: https://www.usgs.gov/programs/earthquake-hazards/earthquakes; Book: 'Earthquakes' by Seymour Simon."
            ),
            "tsunami": (
                "A tsunami is a large sea wave caused by an underwater earthquake. "
                "Tsunamis can cause flooding and damage. "
                "Example: 2004 Indian Ocean tsunami. "
                "Further reading: https://www.nationalgeographic.com/environment/natural-disasters/tsunami/; Book: 'Tsunamis' by Cari Meister."
            ),
            "fossil": (
                "A fossil is the remains or impression of a prehistoric organism. "
                "Fossils help scientists learn about ancient life. "
                "Example: Dinosaur bones, leaf imprints. "
                "Further reading: https://www.britannica.com/science/fossil; Book: 'Fossils Tell of Long Ago' by Aliki."
            ),
            "insect": (
                "An insect is a small animal with six legs and usually wings. "
                "Insects include ants, butterflies, and beetles. "
                "Example: Honeybee, mosquito. "
                "Further reading: https://www.britannica.com/animal/insect; Book: 'The Big Book of Bugs' by Yuval Zommer."
            ),
            "amphibian": (
                "An amphibian is an animal that lives both in water and on land. "
                "Amphibians include frogs, toads, and salamanders. "
                "Example: African bullfrog. "
                "Further reading: https://www.britannica.com/animal/amphibian; Book: 'Frogs' by Gail Gibbons."
            ),
            "reptile": (
                "A reptile is a cold-blooded animal with scales. "
                "Reptiles include snakes, lizards, and crocodiles. "
                "Example: Nile crocodile. "
                "Further reading: https://www.britannica.com/animal/reptile; Book: 'Snakes' by Gail Gibbons."
            ),
            "mammal": (
                "A mammal is a warm-blooded animal with hair or fur. "
                "Mammals give birth to live young and feed them milk. "
                "Example: Elephant, human, bat. "
                "Further reading: https://www.britannica.com/animal/mammal; Book: 'What Is a Mammal?' by Bobbie Kalman."
            ),
            "bird": (
                "A bird is a warm-blooded animal with feathers and wings. "
                "Birds lay eggs and most can fly. "
                "Example: Ostrich, eagle, sparrow. "
                "Further reading: https://www.britannica.com/animal/bird; Book: 'Birds' by Kevin Henkes."
            ),
            "fish": (
                "A fish is a cold-blooded animal that lives in water and has gills. "
                "Fish lay eggs and have scales. "
                "Example: Tilapia, catfish. "
                "Further reading: https://www.britannica.com/animal/fish; Book: 'Fish' by Jules Howard."
            ),
            "life cycle": (
                "A life cycle is the series of changes in the life of an organism. "
                "It includes birth, growth, reproduction, and death. "
                "Example: Butterfly life cycle: egg, larva, pupa, adult. "
                "Further reading: https://www.bbc.co.uk/bitesize/topics/z6882hv/articles/zttckqt; Book: 'The Very Hungry Caterpillar' by Eric Carle."
            ),
            "adaptation": (
                "Adaptation is a change by which an organism becomes better suited to its environment. "
                "Adaptations can be physical or behavioral. "
                "Example: Camels store fat in their humps for desert survival. "
                "Further reading: https://www.bbc.co.uk/bitesize/topics/zvhhvcw/articles/zxg7y4j; Book: 'What If You Had Animal Teeth?' by Sandra Markle."
            ),
            "camouflage": (
                "Camouflage is the coloring or patterns that help an animal blend in. "
                "It helps animals hide from predators or sneak up on prey. "
                "Example: Chameleons change color to match their surroundings. "
                "Further reading: https://www.britannica.com/science/camouflage-biology; Book: 'How to Hide a Lion' by Helen Stephens."
            ),
            "predator": (
                "A predator is an animal that hunts other animals for food. "
                "Predators have adaptations like sharp teeth or claws. "
                "Example: Lion, eagle. "
                "Further reading: https://www.bbc.co.uk/bitesize/topics/z6882hv/articles/z96vb9q; Book: 'Predators' by Paul Harrison."
            ),
            "prey": (
                "Prey is an animal that is hunted by another animal. "
                "Prey animals often have adaptations to escape predators. "
                "Example: Rabbit, antelope. "
                "Further reading: https://www.bbc.co.uk/bitesize/topics/z6882hv/articles/z96vb9q; Book: 'Prey' by Paul Harrison."
            ),
            "herbivore": (
                "A herbivore is an animal that eats only plants. "
                "Herbivores have flat teeth for grinding leaves. "
                "Example: Cow, giraffe. "
                "Further reading: https://www.britannica.com/animal/herbivore; Book: 'What Do Animals Eat?' by Brenda Stones."
            ),
            "carnivore": (
                "A carnivore is an animal that eats only other animals. "
                "Carnivores have sharp teeth for tearing meat. "
                "Example: Lion, crocodile. "
                "Further reading: https://www.britannica.com/animal/carnivore-mammal; Book: 'What Do Animals Eat?' by Brenda Stones."
            ),
            "omnivore": (
                "An omnivore is an animal that eats both plants and animals. "
                "Omnivores can adapt to many environments. "
                "Example: Human, baboon. "
                "Further reading: https://www.britannica.com/animal/omnivore; Book: 'What Do Animals Eat?' by Brenda Stones."
            )
        },
        "african studies": {
            "nile river": (
                "The Nile River is the longest river in Africa, flowing through several countries including Egypt and Sudan. "
                "It is vital for agriculture and transport. "
                "Example: Ancient Egyptians depended on the Nile for farming. "
                "Further reading: https://www.britannica.com/place/Nile-River; Book: 'The Nile River' by Allan Morey."
            ),
            "sahara desert": (
                "The Sahara is the largest hot desert in the world, located in North Africa. "
                "It covers over 9 million square kilometers. "
                "Example: Camels are used for transport in the Sahara. "
                "Further reading: https://www.britannica.com/place/Sahara-desert-Africa; Book: 'The Sahara Desert' by Molly Aloian."
            ),
            "ancient egypt": (
                "Ancient Egypt was a civilization of ancient North Africa, concentrated along the lower reaches of the Nile River. "
                "It is famous for pyramids, pharaohs, and hieroglyphics. "
                "Example: The Great Pyramid of Giza. "
                "Further reading: https://www.history.com/topics/ancient-egypt/ancient-egypt; Book: 'Ancient Egypt' by George Hart."
            ),
            "folktales": (
                "African folktales are traditional stories passed down through generations. "
                "They teach morals and explain natural events. "
                "Example: Anansi the Spider stories from West Africa. "
                "Further reading: https://www.panafricanalliance.com/african-folktales/; Book: 'Nelson Mandela's Favorite African Folktales' by Nelson Mandela."
            ),
            "baobab tree": (
                "The baobab tree is known as the tree of life in Africa. "
                "It stores water in its trunk and provides food and shelter. "
                "Example: Baobab fruit is rich in vitamin C. "
                "Further reading: https://www.britannica.com/plant/baobab-tree; Book: 'The Baobab Tree' by Clifford B. Hicks."
            ),
            "drum": (
                "Drums are important musical instruments in African culture. "
                "They are used in ceremonies, storytelling, and communication. "
                "Example: Djembe drum from West Africa. "
                "Further reading: https://www.africa.upenn.edu/afrfocus/afrifocus021999.html; Book: 'Drum Dream Girl' by Margarita Engle."
            ),
            "kente cloth": (
                "Kente cloth is a colorful fabric from Ghana. "
                "It is handwoven and worn during important events. "
                "Example: Chiefs wear kente during festivals. "
                "Further reading: https://www.britannica.com/topic/kente-cloth; Book: 'Kente Colors' by Debbi Chocolate."
            ),
            "masai": (
                "The Masai are a group of people living in Kenya and Tanzania. "
                "They are known for their cattle herding and colorful dress. "
                "Example: Masai jumping dance. "
                "Further reading: https://www.britannica.com/topic/Masai; Book: 'Masai and I' by Virginia Kroll."
            ),
            "swahili": (
                "Swahili is a widely spoken language in East Africa. "
                "It is used in trade, education, and government. "
                "Example: 'Jambo' means hello in Swahili. "
                "Further reading: https://www.britannica.com/topic/Swahili-language; Book: 'We All Went on Safari' by Laurie Krebs."
            ),
            "zulu": (
                "Zulu is a major ethnic group in South Africa. "
                "They have a rich history and are known for their beadwork and dance. "
                "Example: Zulu reed dance festival. "
                "Further reading: https://www.britannica.com/topic/Zulu-people; Book: 'Zulu Dog' by Anton Ferreira."
            ),
            "yoruba": (
                "Yoruba is a large ethnic group in Nigeria. "
                "They are known for their art, music, and religion. "
                "Example: Yoruba talking drums. "
                "Further reading: https://www.britannica.com/topic/Yoruba; Book: 'Yoruba Legends' by M.I. Ogumefu."
            ),
            "igbo": (
                "Igbo is one of the largest ethnic groups in Africa. "
                "They are known for their festivals and entrepreneurship. "
                "Example: New Yam Festival. "
                "Further reading: https://www.britannica.com/topic/Igbo; Book: 'Things Fall Apart' by Chinua Achebe."
            ),
            "ashanti": (
                "The Ashanti are a major ethnic group in Ghana. "
                "They are famous for their gold, kente cloth, and traditional stools. "
                "Example: The Golden Stool of Ashanti. "
                "Further reading: https://www.britannica.com/topic/Ashanti; Book: 'Ashanti to Zulu: African Traditions' by Margaret Musgrove."
            ),
            "timbuktu": (
                "Timbuktu is an ancient city in Mali, famous for its history and learning. "
                "It was a center of trade and Islamic scholarship. "
                "Example: Ancient manuscripts of Timbuktu. "
                "Further reading: https://www.britannica.com/place/Timbuktu; Book: 'Timbuktu: The Sahara's Fabled City of Gold' by Marq de Villiers."
            ),
            "mandela": (
                "Nelson Mandela was a leader in the fight against apartheid in South Africa. "
                "He became the first black president of South Africa in 1994. "
                "Example: Mandela's release from prison in 1990. "
                "Further reading: https://www.nelsonmandela.org/; Book: 'Long Walk to Freedom' by Nelson Mandela."
            )
        }
    },
    # SECONDARY LEVEL (at least 35 entries)
    "secondary": {
        "mathematics": {
            "algebra": (
                "Algebra is a branch of mathematics dealing with symbols and the rules for manipulating those symbols. For example, solving x + 2 = 5 gives x = 3. "
                "Algebra is used in problem-solving, science, and engineering. "
                "Further reading: https://www.khanacademy.org/math/algebra; Book: 'Algebra for Beginners' by Reza Nazari."
            ),
            "geometry": (
                "Geometry is the study of shapes, sizes, and properties of space. For example, calculating the area of a triangle or the circumference of a circle. "
                "Geometry is used in architecture, art, and navigation. "
                "Further reading: https://www.khanacademy.org/math/geometry; Book: 'Geometry: Seeing, Doing, Understanding' by Harold R. Jacobs."
            ),
            "trigonometry": (
                "Trigonometry deals with the relationships between the angles and sides of triangles. For example, using sine, cosine, and tangent to find unknown sides. "
                "Trigonometry is used in engineering, astronomy, and physics. "
                "Further reading: https://www.khanacademy.org/math/trigonometry; Book: 'Trigonometry' by I.M. Gelfand."
            ),
            "statistics": (
                "Statistics is the study of collecting, analyzing, presenting, and interpreting data. For example, calculating the average score in a class. "
                "Statistics is used in research, business, and government. "
                "Further reading: https://www.khanacademy.org/math/statistics-probability; Book: 'The Cartoon Guide to Statistics' by Larry Gonick."
            ),
            "probability": (
                "Probability measures the chance that an event will occur. For example, the probability of flipping a head on a coin is 1/2. "
                "Probability is used in games, insurance, and risk assessment. "
                "Further reading: https://www.khanacademy.org/math/statistics-probability/probability-library; Book: 'Probability For Dummies' by Deborah Rumsey."
            ),
            "quadratic equation": (
                "A quadratic equation is an equation of the form ax^2 + bx + c = 0. For example, x^2 - 5x + 6 = 0. "
                "Quadratic equations are solved using factoring, completing the square, or the quadratic formula. "
                "Further reading: https://www.khanacademy.org/math/algebra/quadratics; Book: 'Algebra for Beginners' by Reza Nazari."
            ),
            "simultaneous equations": (
                "Simultaneous equations are two or more equations solved together. For example, solving x + y = 5 and x - y = 1 gives x = 3, y = 2. "
                "They are used in business, science, and engineering. "
                "Further reading: https://www.khanacademy.org/math/algebra/systems-of-equations; Book: 'Algebra for Beginners' by Reza Nazari."
            ),
            "circle theorems": (
                "Circle theorems are rules for angles, lengths, and areas in circles. For example, the angle at the center is twice the angle at the circumference. "
                "Used in geometry and design. "
                "Further reading: https://www.bbc.co.uk/bitesize/guides/z2dg87h/revision/1; Book: 'Geometry: Seeing, Doing, Understanding' by Harold R. Jacobs."
            ),
            "vectors": (
                "Vectors have both magnitude and direction. For example, a force of 5N to the east. "
                "Vectors are used in physics, engineering, and navigation. "
                "Further reading: https://www.khanacademy.org/math/linear-algebra/vectors-and-spaces; Book: 'Vector Calculus' by Jerrold E. Marsden."
            ),
            "matrices": (
                "Matrices are rectangular arrays of numbers. For example, [[1, 2], [3, 4]]. "
                "Matrices are used in computer graphics, cryptography, and solving equations. "
                "Further reading: https://www.khanacademy.org/math/precalculus/precalc-matrices; Book: 'Elementary Linear Algebra' by Howard Anton."
            ),
            "logarithms": (
                "Logarithms are the inverse operation to exponentiation. For example, log10(100) = 2 because 10^2 = 100. "
                "Logarithms are used in science, engineering, and finance. "
                "Further reading: https://www.khanacademy.org/math/algebra2/exponential-and-logarithmic-functions; Book: 'Algebra and Trigonometry' by James Stewart."
            ),
            "indices": (
                "Indices (exponents) show how many times a number is multiplied by itself. For example, 2^3 = 2 x 2 x 2 = 8. "
                "Used in scientific notation and growth calculations. "
                "Further reading: https://www.khanacademy.org/math/algebra/exponents; Book: 'Algebra for Beginners' by Reza Nazari."
            ),
            "variation": (
                "Variation describes how one quantity changes with another. For example, direct variation: y = kx. "
                "Used in science and economics. "
                "Further reading: https://www.khanacademy.org/math/algebra2/variation; Book: 'Algebra for Beginners' by Reza Nazari."
            ),
            "sequence": (
                "A sequence is an ordered list of numbers, such as 2, 4, 6, 8. "
                "Sequences are used in patterns and coding. "
                "Further reading: https://www.khanacademy.org/math/algebra/sequences; Book: 'The Art of Problem Solving: Introduction to Counting & Probability' by David Patrick."
            ),
            "series": (
                "A series is the sum of the terms of a sequence. For example, 2 + 4 + 6 + 8. "
                "Series are used in finance and science. "
                "Further reading: https://www.khanacademy.org/math/algebra2/sequences-series; Book: 'The Art of Problem Solving: Introduction to Counting & Probability' by David Patrick."
            ),
            "coordinate geometry": (
                "Coordinate geometry uses algebra to study geometric problems. For example, finding the distance between two points (x1, y1) and (x2, y2). "
                "Used in mapping and navigation. "
                "Further reading: https://www.khanacademy.org/math/geometry-home/coordinate-geometry; Book: 'Geometry: Seeing, Doing, Understanding' by Harold R. Jacobs."
            ),
            "transformation": (
                "Transformation changes the position or size of a shape. For example, rotation, reflection, translation, and enlargement. "
                "Used in art, design, and robotics. "
                "Further reading: https://www.khanacademy.org/math/geometry/hs-geo-transformations; Book: 'Geometry: Seeing, Doing, Understanding' by Harold R. Jacobs."
            ),
            "bearing": (
                "Bearing is the direction or path along which something moves, measured in degrees from north. For example, a bearing of 090° is due east. "
                "Used in navigation and geography. "
                "Further reading: https://www.bbc.co.uk/bitesize/guides/z2dg87h/revision/2; Book: 'Practical Navigation for the Modern Boat Owner' by Pat Manley."
            ),
            "locus": (
                "A locus is a set of points satisfying certain conditions. For example, all points equidistant from a center form a circle. "
                "Used in geometry and engineering. "
                "Further reading: https://www.bbc.co.uk/bitesize/guides/z2dg87h/revision/3; Book: 'Geometry: Seeing, Doing, Understanding' by Harold R. Jacobs."
            ),
            "inequalities": (
                "Inequalities show the relationship between two expressions that are not equal. For example, x > 3. "
                "Used in economics and science. "
                "Further reading: https://www.khanacademy.org/math/algebra/linear-inequalities; Book: 'Algebra for Beginners' by Reza Nazari."
            ),
            "surds": (
                "Surds are irrational roots that cannot be simplified to remove the root. For example, √2. "
                "Used in advanced mathematics and engineering. "
                "Further reading: https://www.bbc.co.uk/bitesize/guides/z2dg87h/revision/4; Book: 'Algebra for Beginners' by Reza Nazari."
            ),
            "functions": (
                "A function is a relation between a set of inputs and a set of possible outputs. For example, f(x) = x^2. "
                "Functions are used in programming, science, and engineering. "
                "Further reading: https://www.khanacademy.org/math/algebra2/functions; Book: 'Algebra and Trigonometry' by James Stewart."
            ),
            "graphing": (
                "Graphing is drawing a diagram to represent data or equations. For example, plotting y = 2x + 1 on a graph. "
                "Used in science, business, and statistics. "
                "Further reading: https://www.khanacademy.org/math/algebra/linear-equations; Book: 'The Cartoon Guide to Statistics' by Larry Gonick."
            ),
            "permutations": (
                "Permutations are arrangements of objects in a specific order. For example, the number of ways to arrange 3 books is 3! = 6. "
                "Used in probability and computer science. "
                "Further reading: https://www.khanacademy.org/math/statistics-probability/probability-library; Book: 'The Art of Problem Solving: Introduction to Counting & Probability' by David Patrick."
            ),
            "combinations": (
                "Combinations are selections of items without regard to order. For example, choosing 2 fruits from apple, banana, and orange. "
                "Used in probability and statistics. "
                "Further reading: https://www.khanacademy.org/math/statistics-probability/probability-library; Book: 'The Art of Problem Solving: Introduction to Counting & Probability' by David Patrick."
            ),
            "binomial theorem": (
                "The binomial theorem describes the algebraic expansion of powers of a binomial. For example, (a + b)^2 = a^2 + 2ab + b^2. "
                "Used in algebra and probability. "
                "Further reading: https://www.khanacademy.org/math/algebra2/polynomial-functions/binomial-theorem; Book: 'Algebra for Beginners' by Reza Nazari."
            ),
            "differentiation": (
                "Differentiation is finding the derivative of a function. For example, the derivative of x^2 is 2x. "
                "Used in physics, engineering, and economics. "
                "Further reading: https://www.khanacademy.org/math/differential-calculus; Book: 'Calculus' by James Stewart."
            ),
            "integration": (
                "Integration is finding the area under a curve. For example, the integral of x is (1/2)x^2. "
                "Used in physics, engineering, and statistics. "
                "Further reading: https://www.khanacademy.org/math/integral-calculus; Book: 'Calculus' by James Stewart."
            ),
            "complex numbers": (
                "Complex numbers have a real and an imaginary part. For example, 3 + 4i. "
                "Used in engineering, physics, and mathematics. "
                "Further reading: https://www.khanacademy.org/math/algebra2/complex-numbers; Book: 'Algebra and Trigonometry' by James Stewart."
            ),
            "polynomials": (
                "Polynomials are expressions with more than one term. For example, x^2 + 3x + 2. "
                "Used in algebra, calculus, and science. "
                "Further reading: https://www.khanacademy.org/math/algebra/polynomial-factorization; Book: 'Algebra for Beginners' by Reza Nazari."
            ),
            "rational expressions": (
                "Rational expressions are ratios of polynomials. For example, (x+1)/(x-1). "
                "Used in algebra and calculus. "
                "Further reading: https://www.khanacademy.org/math/algebra2/rational-expressions-equations-functions; Book: 'Algebra for Beginners' by Reza Nazari."
            )
        },
        "english": {
            "summary": (
                "A summary is a brief statement of the main points of a text. For example, summarizing a story in a few sentences. "
                "Summarizing helps you focus on key information. "
                "Further reading: https://www.skillsyouneed.com/write/summary.html; Book: 'How to Write a Summary' by Liza Wiemer."
            ),
            "comprehension": (
                "Comprehension is understanding what you read. For example, after reading a passage, you answer questions about its main idea and details. "
                "Comprehension skills are essential for academic success. "
                "Further reading: https://www.readingrockets.org/strategies/comprehension; Book: 'Reading Comprehension Success in 20 Minutes a Day' by LearningExpress."
            ),
            "essay": (
                "An essay is a short piece of writing on a particular subject. For example, writing an argumentative essay with an introduction, body, and conclusion. "
                "Essay writing is important for exams and communication. "
                "Further reading: https://www.khanacademy.org/humanities/grammar/grammar-syntax/v/essay-writing; Book: 'The Only Grammar Book You'll Ever Need' by Susan Thurman."
            ),
            "literature": (
                "Literature refers to written works, especially those considered to have artistic merit. For example, novels, plays, and poems. "
                "Studying literature improves language and critical thinking. "
                "Further reading: https://www.britannica.com/art/literature; Book: 'How to Read Literature Like a Professor' by Thomas C. Foster."
            ),
            "drama": (
                "Drama is a mode of fictional representation through dialogue and performance. For example, Shakespeare's 'Romeo and Juliet.' "
                "Drama helps develop empathy and understanding of human behavior. "
                "Further reading: https://www.britannica.com/art/drama-literature; Book: 'The Norton Anthology of Drama.'"
            ),
            "poetry": (
                "Poetry is a form of literature that uses aesthetic and rhythmic qualities of language. For example, haikus and sonnets. "
                "Poetry enhances creativity and emotional expression. "
                "Further reading: https://www.poetryfoundation.org/; Book: 'The Poetry Handbook' by John Lennard."
            ),
            "prose": (
                "Prose is written or spoken language in its ordinary form. For example, novels and essays. "
                "Prose is used in most forms of communication. "
                "Further reading: https://www.masterclass.com/articles/what-is-prose; Book: 'Prose Style: A Contemporary Guide' by Robert Miles."
            ),
            "debate": (
                "A debate is a formal discussion on a particular topic. For example, a school debate on whether uniforms should be mandatory. "
                "Debate develops critical thinking and public speaking skills. "
                "Further reading: https://www.skillsyouneed.com/ips/debate.html; Book: 'The Debater's Guide' by Jon M. Ericson."
            ),
            "report writing": (
                "Report writing is presenting information clearly and concisely. For example, writing a science report on an experiment. "
                "Report writing is important in academics and business. "
                "Further reading: https://www.skillsyouneed.com/write/report-writing.html; Book: 'How to Write Reports and Proposals' by Patrick Forsyth."
            ),
            "letter writing": (
                "Letter writing is a way to communicate in writing. For example, writing a formal letter to a principal. "
                "Letter writing is used in personal and professional life. "
                "Further reading: https://www.skillsyouneed.com/write/letters.html; Book: 'How to Write Letters' by Crowther."
            ),
            "speech": (
                "A speech is a formal address or discourse. For example, writing a speech for a school event. "
                "Speech writing is important for leadership and public speaking. "
                "Further reading: https://www.skillsyouneed.com/write/speech.html; Book: 'TED Talks: The Official TED Guide to Public Speaking' by Chris Anderson."
            ),
            "article": (
                "An article is a piece of writing included with others in a newspaper or magazine. For example, a news article about a local event. "
                "Articles inform, persuade, or entertain readers. "
                "Further reading: https://www.skillsyouneed.com/write/articles.html; Book: 'Writing Feature Articles' by Brendan Hennessy."
            ),
            "narrative": (
                "A narrative is a spoken or written account of connected events. For example, telling a story about your childhood. "
                "Narratives are used in literature and everyday communication. "
                "Further reading: https://www.masterclass.com/articles/what-is-narrative-writing; Book: 'Narrative Writing' by George Hillocks Jr."
            ),
            "dialogue": (
                "Dialogue is a conversation between two or more people. For example, a conversation in a play. "
                "Dialogue makes stories more realistic and engaging. "
                "Further reading: https://www.masterclass.com/articles/how-to-write-dialogue; Book: 'Writing Dialogue' by Tom Chiarella."
            ),
            "characterization": (
                "Characterization is the creation of characters in a story. For example, describing a character's appearance and actions. "
                "Characterization makes stories more vivid and believable. "
                "Further reading: https://www.masterclass.com/articles/characterization-definition; Book: 'Characters & Viewpoint' by Orson Scott Card."
            ),
            "theme": (
                "Theme is the central topic of a text. For example, the theme of friendship in a novel. "
                "Themes give deeper meaning to stories. "
                "Further reading: https://literarydevices.net/theme/; Book: 'How to Read Literature Like a Professor' by Thomas C. Foster."
            ),
            "plot": (
                "Plot is the sequence of events in a story. For example, the events leading to the resolution of a conflict. "
                "Plot structure helps organize stories. "
                "Further reading: https://www.masterclass.com/articles/plot-of-a-story; Book: 'Story: Substance, Structure, Style and the Principles of Screenwriting' by Robert McKee."
            ),
            "setting": (
                "Setting is the time and place of a story. For example, a story set in Lagos, Nigeria. "
                "Setting provides context for the action. "
                "Further reading: https://www.masterclass.com/articles/setting-in-literature; Book: 'The Art of Setting in Fiction' by Anne Dillard."
            ),
            "conflict": (
                "Conflict is a struggle between opposing forces. For example, a character facing a difficult decision. "
                "Conflict drives the plot of a story. "
                "Further reading: https://literarydevices.net/conflict/; Book: 'Story: Substance, Structure, Style and the Principles of Screenwriting' by Robert McKee."
            ),
            "resolution": (
                "Resolution is the solution to a problem in a story. For example, the hero saves the day. "
                "Resolution brings closure to stories. "
                "Further reading: https://www.masterclass.com/articles/resolution-in-literature; Book: 'Story: Substance, Structure, Style and the Principles of Screenwriting' by Robert McKee."
            ),
            "point of view": (
                "Point of view is the perspective from which a story is told. For example, first-person or third-person narration. "
                "Point of view affects how readers experience a story. "
                "Further reading: https://www.masterclass.com/articles/point-of-view-in-writing; Book: 'Characters & Viewpoint' by Orson Scott Card."
            ),
            "tone": (
                "Tone is the author's attitude toward the subject. For example, a humorous or serious tone. "
                "Tone influences how readers feel about a story. "
                "Further reading: https://literarydevices.net/tone/; Book: 'The Elements of Style' by Strunk and White."
            ),
            "mood": (
                "Mood is the feeling created in the reader. For example, a suspenseful or joyful mood. "
                "Mood helps set the atmosphere of a story. "
                "Further reading: https://literarydevices.net/mood/; Book: 'The Elements of Style' by Strunk and White."
            ),
            "figurative language": (
                "Figurative language uses figures of speech to be more effective. For example, metaphors and similes. "
                "Figurative language makes writing more vivid. "
                "Further reading: https://literarydevices.net/figurative-language/; Book: 'A Handbook to Literature' by William Harmon."
            ),
            "simile": (
                "A simile compares two things using 'like' or 'as'. For example, 'as brave as a lion.' "
                "Similes make descriptions more interesting. "
                "Further reading: https://literarydevices.net/simile/; Book: 'A Handbook to Literature' by William Harmon."
            ),
            "metaphor": (
                "A metaphor compares two things without using 'like' or 'as'. For example, 'Time is a thief.' "
                "Metaphors create strong images in writing. "
                "Further reading: https://literarydevices.net/metaphor/; Book: 'A Handbook to Literature' by William Harmon."
            ),
            "personification": (
                "Personification gives human qualities to non-human things. For example, 'The wind whispered through the trees.' "
                "Personification makes writing more lively. "
                "Further reading: https://literarydevices.net/personification/; Book: 'A Handbook to Literature' by William Harmon."
            ),
            "hyperbole": (
                "Hyperbole is exaggerated statements not meant to be taken literally. For example, 'I've told you a million times.' "
                "Hyperbole adds emphasis to writing. "
                "Further reading: https://literarydevices.net/hyperbole/; Book: 'A Handbook to Literature' by William Harmon."
            ),
            "irony": (
                "Irony is the use of words to convey a meaning opposite to their literal meaning. For example, saying 'What a pleasant day' during a storm. "
                "Irony adds humor or emphasis. "
                "Further reading: https://literarydevices.net/irony/; Book: 'A Handbook to Literature' by William Harmon."
            )
        },
        "science": {
            "organic chemistry": (
                "Organic chemistry is the study of the structure, properties, and reactions of organic compounds and materials. For example, studying how alcohols and acids react. "
                "It is important in medicine, biology, and industry. "
                "Further reading: https://www.khanacademy.org/science/organic-chemistry; Book: 'Organic Chemistry' by Paula Yurkanis Bruice."
            ),
            "quantum mechanics": (
                "Quantum mechanics is a fundamental theory in physics describing the properties of nature on an atomic scale. For example, explaining how electrons move in atoms. "
                "It is used in electronics, chemistry, and computing. "
                "Further reading: https://www.khanacademy.org/science/physics/quantum-physics; Book: 'Quantum Physics' by Alastair I.M. Rae."
            ),
            "molecular biology": (
                "Molecular biology is the branch of biology that deals with the structure and function of the macromolecules essential to life. For example, DNA and proteins. "
                "It is key to genetics and biotechnology. "
                "Further reading: https://www.khanacademy.org/science/biology/central-dogma; Book: 'Molecular Biology of the Cell' by Bruce Alberts."
            ),
            "thermodynamics": (
                "Thermodynamics is the branch of physics that deals with heat and temperature and their relation to energy and work. For example, how engines convert fuel to motion. "
                "It is used in engineering, chemistry, and meteorology. "
                "Further reading: https://www.khanacademy.org/science/physics/thermodynamics; Book: 'Thermodynamics: An Engineering Approach' by Yunus Çengel."
            ),
            "genetics": (
                "Genetics is the study of genes, genetic variation, and heredity in living organisms. For example, how traits are inherited from parents. "
                "It is important in medicine, agriculture, and research. "
                "Further reading: https://www.khanacademy.org/science/biology/heredity; Book: 'Genetics: A Conceptual Approach' by Benjamin Pierce."
            ),
            "biochemistry": (
                "Biochemistry is the study of chemical processes within living organisms. For example, how enzymes help digest food. "
                "It connects biology and chemistry. "
                "Further reading: https://www.khanacademy.org/science/biology/chemistry--of-life; Book: 'Lehninger Principles of Biochemistry' by David L. Nelson."
            ),
            "cell biology": (
                "Cell biology is the study of cell structure and function. For example, how cells divide and communicate. "
                "It is fundamental to all life sciences. "
                "Further reading: https://www.khanacademy.org/science/biology/structure-of-a-cell; Book: 'Molecular Biology of the Cell' by Bruce Alberts."
            ),
            "ecology": (
                "Ecology is the study of interactions among organisms and their environment. For example, food webs in a forest. "
                "It helps us understand environmental issues. "
                "Further reading: https://www.khanacademy.org/science/biology/ecology; Book: 'Ecology: Concepts and Applications' by Manuel Molles."
            ),
            "evolutionary biology": (
                "Evolutionary biology is the study of the evolutionary processes that produced the diversity of life. For example, natural selection. "
                "It explains how species change over time. "
                "Further reading: https://www.khanacademy.org/science/biology/her/tree-of-life/a/evolution-and-natural-selection; Book: 'The Greatest Show on Earth' by Richard Dawkins."
            ),
            "astrophysics": (
                "Astrophysics is the branch of astronomy concerned with the physical nature of stars and other celestial bodies. For example, studying black holes and galaxies. "
                "It helps us understand the universe. "
                "Further reading: https://www.khanacademy.org/science/physics/space; Book: 'Astrophysics for People in a Hurry' by Neil deGrasse Tyson."
            )
        },
        "african studies": {
            "african union": (
                "The African Union is a continental union consisting of 55 member states located on the continent of Africa. For example, it works to promote peace and development. "
                "The AU addresses issues like health, security, and trade. "
                "Further reading: https://au.int/en/overview; Book: 'The African Union: Autocracy, Diplomacy and Peacebuilding in Africa' by Tony Karbo."
            ),
            "african philosophy": (
                "African philosophy is the philosophical discourse produced by indigenous Africans and their descendants. For example, Ubuntu philosophy emphasizes community. "
                "It explores African values, ethics, and worldviews. "
                "Further reading: https://www.britannica.com/topic/African-philosophy; Book: 'African Philosophy: An Anthology' by Emmanuel Chukwudi Eze."
            ),
            "post-colonial theory": (
                "Post-colonial theory analyzes the cultural legacy of colonialism and imperialism. For example, examining African literature after independence. "
                "It helps understand identity and resistance. "
                "Further reading: https://www.britannica.com/topic/postcolonialism; Book: 'The Post-Colonial Studies Reader' by Bill Ashcroft."
            ),
            "african literature": (
                "African literature refers to the literary works of the African continent. For example, novels by Chinua Achebe. "
                "It reflects African cultures, histories, and experiences. "
                "Further reading: https://www.britannica.com/art/African-literature; Book: 'Things Fall Apart' by Chinua Achebe."
            ),
            "african feminism": (
                "African feminism is a form of feminism developed by African women. For example, advocating for women's rights in Africa. "
                "It addresses gender equality and social justice. "
                "Further reading: https://en.wikipedia.org/wiki/African_feminism; Book: 'African Women Writing Resistance' by Jennifer Browdy."
            ),
            "african diaspora": (
                "The African diaspora refers to communities descended from native Africans living outside Africa. For example, African Americans in the United States. "
                "It explores migration, identity, and culture. "
                "Further reading: https://www.britannica.com/topic/African-diaspora; Book: 'The African Diaspora: A History Through Culture' by Patrick Manning."
            ),
            "african renaissance": (
                "The African Renaissance is a concept of renewed growth and development in Africa. For example, promoting education and innovation. "
                "It encourages cultural pride and progress. "
                "Further reading: https://en.wikipedia.org/wiki/African_Renaissance; Book: 'The African Renaissance: Roadmaps to the Challenge of Globalization' by Malegapuru William Makgoba."
            ),
            "pan-african congress": (
                "The Pan-African Congress was a series of meetings to address issues facing Africa due to European colonization. For example, the 1945 Congress in Manchester. "
                "It played a key role in African independence movements. "
                "Further reading: https://www.britannica.com/topic/Pan-Africanism; Book: 'Pan-Africanism: A History' by Hakim Adi."
            )
        },
        "advanced research": {
            "machine learning": (
                "Machine learning is a field of artificial intelligence that uses statistical techniques to give computer systems the ability to learn from data. For example, teaching a computer to recognize faces in photos. "
                "It is used in self-driving cars, healthcare, and finance. "
                "Further reading: https://www.coursera.org/learn/machine-learning; Book: 'Hands-On Machine Learning with Scikit-Learn, Keras, and TensorFlow' by Aurélien Géron."
            ),
            "renewable energy": (
                "Renewable energy is energy from sources that are naturally replenishing such as solar, wind, and hydro. For example, using solar panels to generate electricity. "
                "It helps reduce pollution and combat climate change. "
                "Further reading: https://www.nationalgeographic.com/environment/article/renewable-energy; Book: 'Renewable Energy: Power for a Sustainable Future' by Godfrey Boyle."
            ),
            "climate change": (
                "Climate change refers to long-term shifts in temperatures and weather patterns, mainly caused by human activities. For example, rising global temperatures. "
                "It affects weather, agriculture, and sea levels. "
                "Further reading: https://climate.nasa.gov/; Book: 'This Changes Everything' by Naomi Klein."
            ),
            "public health": (
                "Public health is the science of protecting and improving the health of people and their communities. For example, vaccination campaigns. "
                "It focuses on disease prevention and health promotion. "
                "Further reading: https://www.cdc.gov/publichealthgateway/; Book: 'Introduction to Public Health' by Mary-Jane Schneider."
            ),
            "entrepreneurship": (
                "Entrepreneurship is the process of designing, launching, and running a new business. For example, starting a technology company. "
                "Entrepreneurship drives innovation and economic growth. "
                "Further reading: https://www.entrepreneur.com/; Book: 'The Lean Startup' by Eric Ries."
            ),
            "artificial intelligence": (
                "Artificial intelligence is the simulation of human intelligence in machines. For example, voice assistants like Siri and Alexa. "
                "AI is used in robotics, healthcare, and customer service. "
                "Further reading: https://www.ibm.com/cloud/learn/what-is-artificial-intelligence; Book: 'Artificial Intelligence: A Guide for Thinking Humans' by Melanie Mitchell."
            ),
            "data science": (
                "Data science is the study of data to extract meaningful insights. For example, analyzing sales data to predict trends. "
                "It combines statistics, programming, and domain knowledge. "
                "Further reading: https://www.coursera.org/specializations/data-science-python; Book: 'Data Science for Business' by Foster Provost."
            ),
            "blockchain": (
                "Blockchain is a system of recording information in a way that makes it difficult to change or hack. For example, cryptocurrencies like Bitcoin. "
                "It is used in finance, supply chain, and voting systems. "
                "Further reading: https://www.ibm.com/topics/what-is-blockchain; Book: 'Blockchain Basics' by Daniel Drescher."
            ),
            "cybersecurity": (
                "Cybersecurity is the practice of protecting systems and networks from digital attacks. For example, using firewalls and encryption. "
                "It is essential for privacy and data protection. "
                "Further reading: https://www.cisa.gov/; Book: 'Cybersecurity for Beginners' by Raef Meeuwisse."
            ),
            "sustainable development": (
                "Sustainable development is development that meets the needs of the present without compromising the future. For example, using renewable resources and reducing waste. "
                "It balances economic, social, and environmental goals. "
                "Further reading: https://sdgs.un.org/goals; Book: 'Sustainable Development Goals Connectivity Dilemma' by Harri Paloheimo."
            )
        }

    },
    "counselling": {
        "academic counselling": (
            "What is academic counselling? Academic counselling helps students make informed decisions about their studies, career paths, and personal development. "
            "Who provides academic counselling? Academic counsellors, like Aivi, are trained to guide you on study skills, subject choices, and personal growth. "
            "How does academic counselling help? Aivi can guide you on how to study effectively, choose subjects, manage time, set goals, and overcome challenges. "
            "When should you seek academic counselling? You can ask for advice at any time, especially when you feel unsure, need motivation, or want to plan your future. "
            "You can ask for advice on any topic in your curriculum, and Aivi will provide support, motivation, and resources tailored to your level and needs. "
            "For example, you can say: 'Aivi, how do I improve in mathematics?' or 'Aivi, what should I do if I find science difficult?' "
            "Further reading: https://www.unesco.org/en/education/guidance-counselling; Book: 'Academic Advising: A Comprehensive Handbook' by Virginia N. Gordon."
        ),
        "study tips": (
            "Effective study habits include setting specific goals, creating a quiet study environment, taking regular breaks, and reviewing material frequently. "
            "Use active learning techniques like summarizing, teaching others, and practicing with questions. "
            "Stay organized with a planner and avoid last-minute cramming. "
            "Further reading: https://www.cornell.edu/academics/study-tips.cfm; Book: 'Make It Stick: The Science of Successful Learning' by Peter C. Brown."
        ),
        "time management": (
            "Good time management helps you balance school, home, and personal activities. "
            "Prioritize tasks, use a calendar, break big tasks into smaller steps, and avoid procrastination. "
            "Remember to schedule time for rest and hobbies. "
            "Further reading: https://www.skillsyouneed.com/ps/time-management.html; Book: 'Time Management for Students' by Beverly A. Potter."
        ),
        "subject choice": (
            "Choosing the right subjects depends on your interests, strengths, and career goals. "
            "Talk to teachers, research careers, and consider what subjects you enjoy and do well in. "
            "Don't be afraid to ask for advice from family, friends, or your academic counsellor. "
            "Further reading: https://www.prospects.ac.uk/careers-advice/what-can-i-do-with-my-degree; Book: 'The Student's Guide to Choosing a Major' by Laurence Shatkin."
        ),
        "motivation": (
            "Staying motivated can be hard, but setting clear goals, rewarding yourself for progress, and remembering your reasons for learning can help. "
            "Surround yourself with positive influences and don't hesitate to ask for support when needed. "
            "Further reading: https://www.mindtools.com/pages/article/motivation.htm; Book: 'Drive: The Surprising Truth About What Motivates Us' by Daniel H. Pink."
        ),
        "overcoming challenges": (
            "Everyone faces challenges in their studies. Identify the problem, seek help early, and break tasks into manageable steps. "
            "Use available resources like teachers, friends, and your academic counsellor. "
            "Remember, persistence is key. "
            "Further reading: https://www.skillsyouneed.com/ps/problems-solving.html; Book: 'Grit: The Power of Passion and Perseverance' by Angela Duckworth."
        ),
        "exam preparation": (
            "Start preparing for exams early. Review notes regularly, practice with past questions, and get enough sleep before the exam. "
            "Stay calm, plan your time, and read instructions carefully during the exam. "
            "Further reading: https://www.topuniversities.com/student-info/health-and-support/exam-preparation-ten-study-tips; Book: 'How to Pass Exams' by Dominic O'Brien."
        ),
        "career guidance": (
            "Career guidance helps you explore different professions, understand required skills, and plan your educational path. "
            "Research careers, talk to professionals, and seek internships or volunteer opportunities to gain experience. "
            "Further reading: https://www.careers.govt.nz/; Book: 'What Color Is Your Parachute?' by Richard N. Bolles."
        )
    }
}

def offline_search(query):
    """
    Recursively search the offline_data structure for a query string.
    Returns the first match found, including the level, subject, and topic.
    """
    query = query.lower()
    def recursive_search(data, path=None):
        if path is None:
            path = []
        if isinstance(data, dict):
            for k, v in data.items():
                result = recursive_search(v, path + [k])
                if result:
                    return result
        elif isinstance(data, str):
            topic = path[-1] if path else ''
            if query in topic.lower() or query in data.lower():
                # Format: [Level > Subject] Topic: Info
                if len(path) >= 3:
                    return f"[{path[0].title()} > {path[1].title()}] {path[2].title()}: {data}"
                elif len(path) == 2:
                    return f"[{path[0].title()}] {path[1].title()}: {data}"
                else:
                    return f"{topic.title()}: {data}"
        return None
    result = recursive_search(offline_data)
    return result if result else "No offline data found for your query."
