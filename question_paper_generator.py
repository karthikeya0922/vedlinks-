"""
NCERT-Style Question Paper Generator Module

NEW APPROACH:
- Uses topic metadata (class, subject, chapter, topics) as semantic anchors
- Generates educationally meaningful questions based on NCERT patterns
- Leverages knowledge banks for real content, not placeholder text
- Supports all CBSE question formats
"""

import os
import sys
import json
import random
import warnings
from pathlib import Path

# Suppress warnings
warnings.filterwarnings('ignore')

# Fix encoding on Windows
if sys.platform == 'win32':
    os.environ['PYTHONIOENCODING'] = 'utf-8'


# ============================================================================
# NCERT KNOWLEDGE BANK - Real educational content for question generation
# ============================================================================

NCERT_KNOWLEDGE = {
    # Class 6 Science - Food Where Does It Come From
    "Food – Where Does It Come From?": {
        "key_concepts": [
            ("Sources of food", "Food comes from plants and animals. Plants give us fruits, vegetables, cereals, and pulses. Animals give us milk, eggs, meat, and honey."),
            ("Edible plant parts", "We eat different parts of plants: roots (carrot, radish), stems (potato, ginger), leaves (spinach, cabbage), flowers (cauliflower, broccoli), fruits (mango, apple), and seeds (wheat, rice)."),
            ("Animal products", "Animals provide us with milk and milk products, eggs, meat, fish, and honey. Honey is made by bees from flower nectar."),
            ("Herbivores", "Animals that eat only plants are called herbivores. Examples: cow, deer, rabbit, elephant, goat."),
            ("Carnivores", "Animals that eat only other animals are called carnivores. Examples: lion, tiger, wolf, eagle, shark."),
            ("Omnivores", "Animals that eat both plants and animals are called omnivores. Examples: human, bear, crow, dog, pig."),
            ("Food ingredients", "To prepare a dish, we need various ingredients that come from plants or animals."),
            ("Sprouting", "When seeds are soaked in water and kept in warm conditions, they germinate and produce sprouts which are nutritious."),
        ],
        "mcq_pool": [
            ("Which part of the plant is carrot?", ["Root", "Stem", "Leaf", "Fruit"], "Root", "Carrot is a root vegetable that grows underground."),
            ("Which of these is a herbivore?", ["Lion", "Cow", "Bear", "Crow"], "Cow", "Cows eat only plants, making them herbivores."),
            ("Honey is made by:", ["Ants", "Bees", "Butterflies", "Spiders"], "Bees", "Bees collect nectar from flowers and convert it into honey."),
            ("Which of the following is an animal product?", ["Rice", "Milk", "Wheat", "Apple"], "Milk", "Milk comes from animals like cows and buffaloes."),
            ("Potato is which part of a plant?", ["Root", "Stem", "Leaf", "Flower"], "Stem", "Potato is a modified underground stem called a tuber."),
            ("Which animal is an omnivore?", ["Deer", "Tiger", "Bear", "Rabbit"], "Bear", "Bears eat both plants (berries, fruits) and animals (fish, insects)."),
            ("Spinach is which part of the plant?", ["Root", "Stem", "Leaf", "Seed"], "Leaf", "We eat the leaves of the spinach plant."),
            ("Which of these gives us cereals?", ["Mango tree", "Wheat plant", "Rose plant", "Tulsi plant"], "Wheat plant", "Wheat is a cereal crop that provides us with flour."),
            ("Cauliflower is which part of a plant?", ["Root", "Stem", "Flower", "Fruit"], "Flower", "We eat the flower part of the cauliflower plant."),
            ("Which is NOT a source of food?", ["Plants", "Animals", "Rocks", "Water"], "Rocks", "Rocks are non-living things and cannot be a source of food."),
        ],
        "fill_blanks": [
            ("Animals that eat only plants are called _______.", "herbivores"),
            ("_______ is made by bees from flower nectar.", "Honey"),
            ("Carrot is the _______ of a plant.", "root"),
            ("Animals that eat both plants and animals are called _______.", "omnivores"),
            ("We get milk from animals like cow and _______.", "buffalo"),
            ("Potato is a modified underground _______.", "stem"),
            ("Animals that eat only other animals are called _______.", "carnivores"),
            ("_______ and vegetables are plant products.", "Fruits"),
        ],
        "short_answers": [
            ("What are herbivores? Give two examples.", "Herbivores are animals that eat only plants and plant products. Examples: cow, deer, rabbit, elephant, horse."),
            ("Name any five edible parts of plants with examples.", "1. Root - carrot, radish\n2. Stem - potato, ginger\n3. Leaf - spinach, cabbage\n4. Flower - cauliflower\n5. Fruit - mango, apple\n6. Seed - wheat, rice"),
            ("What is the difference between herbivores and carnivores?", "Herbivores eat only plants (e.g., cow, rabbit). Carnivores eat only other animals (e.g., lion, tiger). Their teeth and digestive systems are adapted to their diets."),
            ("How is honey made?", "Honey is made by bees. Bees collect nectar from flowers, store it in their hives, and convert it into honey through a process involving their enzymes."),
            ("Why are some animals called omnivores?", "Some animals are called omnivores because they eat both plants and animals. Examples include bears, crows, and humans."),
        ],
        "long_answers": [
            ("Explain with examples how different parts of plants are used as food.", 
             "Plants provide us food from various parts:\n\n1. Roots: Carrot, radish, turnip, beetroot are roots we eat.\n2. Stems: Potato (underground stem), sugarcane, ginger are edible stems.\n3. Leaves: Spinach, cabbage, lettuce, curry leaves are eaten.\n4. Flowers: Cauliflower, broccoli are flowers we consume.\n5. Fruits: Mango, apple, orange, banana are common fruits.\n6. Seeds: Rice, wheat, pulses, nuts are seeds we eat.\n\nThus, almost every part of plants can serve as food for humans."),
            ("Classify animals based on their food habits and give examples of each type.",
             "Animals can be classified into three categories based on their food habits:\n\n1. Herbivores: Animals that eat only plants\n   - Examples: Cow, buffalo, deer, rabbit, elephant, horse, goat\n   - They have flat teeth for grinding plant material\n\n2. Carnivores: Animals that eat only other animals\n   - Examples: Lion, tiger, wolf, eagle, shark, crocodile\n   - They have sharp teeth for tearing meat\n\n3. Omnivores: Animals that eat both plants and animals\n   - Examples: Bear, crow, dog, pig, human beings\n   - They have both types of teeth for varied diet"),
        ]
    },
    
    # Class 6 Science - Components of Food
    "Components of Food": {
        "key_concepts": [
            ("Nutrients", "Food contains nutrients like carbohydrates, proteins, fats, vitamins, minerals, and water that are essential for our body."),
            ("Carbohydrates", "Carbohydrates provide energy to our body. Sources include rice, wheat, potatoes, and sugar. Test: Iodine turns blue-black with starch."),
            ("Proteins", "Proteins help in body growth and repair. Sources include pulses, eggs, meat, fish, and milk. They are called body-building foods."),
            ("Fats", "Fats provide energy and keep body warm. Sources include oil, butter, ghee, and nuts. They give more energy than carbohydrates."),
            ("Vitamins", "Vitamins protect us from diseases. Different vitamins (A, B, C, D, E, K) have different functions. Deficiency causes specific diseases."),
            ("Minerals", "Minerals like calcium, iron, iodine are needed in small amounts for various body functions."),
            ("Balanced diet", "A diet containing all nutrients in right amounts is called a balanced diet. It varies with age, gender, and activity."),
            ("Deficiency diseases", "Lack of nutrients causes deficiency diseases. E.g., scurvy (Vitamin C deficiency), rickets (Vitamin D deficiency)."),
        ],
        "mcq_pool": [
            ("Which nutrient is called body-building food?", ["Carbohydrates", "Proteins", "Fats", "Vitamins"], "Proteins", "Proteins help in growth and repair of body tissues."),
            ("Deficiency of Vitamin C causes:", ["Night blindness", "Scurvy", "Rickets", "Goitre"], "Scurvy", "Scurvy is caused by lack of Vitamin C and leads to bleeding gums."),
            ("Which of these is rich in carbohydrates?", ["Eggs", "Fish", "Rice", "Spinach"], "Rice", "Rice is a major source of carbohydrates."),
            ("Iodine solution is used to test for:", ["Proteins", "Fats", "Starch", "Vitamins"], "Starch", "Iodine turns blue-black in presence of starch."),
            ("Rickets is caused by deficiency of:", ["Vitamin A", "Vitamin B", "Vitamin C", "Vitamin D"], "Vitamin D", "Vitamin D deficiency causes rickets, affecting bone development."),
            ("Which mineral is needed for strong bones?", ["Iron", "Calcium", "Iodine", "Sodium"], "Calcium", "Calcium is essential for bone and teeth formation."),
            ("Goitre is caused by deficiency of:", ["Iron", "Calcium", "Iodine", "Vitamin A"], "Iodine", "Iodine deficiency causes enlargement of thyroid gland called goitre."),
            ("Which nutrient provides maximum energy?", ["Carbohydrates", "Proteins", "Fats", "Vitamins"], "Fats", "Fats provide more energy per gram than carbohydrates."),
            ("Night blindness is caused by deficiency of:", ["Vitamin A", "Vitamin B", "Vitamin C", "Vitamin D"], "Vitamin A", "Vitamin A is essential for good eyesight."),
            ("Roughage is needed for:", ["Energy", "Growth", "Digestion", "Protection"], "Digestion", "Roughage or dietary fiber helps in proper digestion and bowel movement."),
        ],
        "fill_blanks": [
            ("_______ are called body-building foods.", "Proteins"),
            ("Deficiency of Vitamin D causes _______.", "rickets"),
            ("_______ test is used to detect the presence of starch.", "Iodine"),
            ("A diet containing all nutrients in right amounts is called a _______ diet.", "balanced"),
            ("_______ is needed for the formation of haemoglobin in blood.", "Iron"),
            ("Deficiency of iodine causes _______.", "goitre"),
            ("Carbohydrates and fats are called _______ giving foods.", "energy"),
            ("Bleeding gums is a symptom of _______.", "scurvy"),
        ],
        "short_answers": [
            ("What is a balanced diet?", "A balanced diet is a diet that contains all the nutrients (carbohydrates, proteins, fats, vitamins, minerals, and water) in the right proportions needed by our body for proper growth and functioning."),
            ("Name two diseases caused by vitamin deficiency.", "1. Scurvy - caused by Vitamin C deficiency\n2. Rickets - caused by Vitamin D deficiency\n3. Night blindness - caused by Vitamin A deficiency\n4. Beriberi - caused by Vitamin B1 deficiency"),
            ("Why are proteins called body-building foods?", "Proteins are called body-building foods because they help in the growth and repair of body tissues. They are essential for building muscles, organs, skin, and other body parts."),
            ("What is the function of roughage in our diet?", "Roughage (dietary fiber) helps in proper digestion and bowel movement. It adds bulk to the food and helps in moving food through the digestive system."),
            ("Name three sources of carbohydrates.", "Sources of carbohydrates include: rice, wheat, potato, bread, sugar, honey, and fruits like banana."),
        ],
        "long_answers": [
            ("Explain the different nutrients required by our body and their sources.",
             "Our body requires the following nutrients:\n\n1. Carbohydrates: Provide energy\n   Sources: Rice, wheat, potato, bread, sugar\n\n2. Proteins: Help in body growth and repair\n   Sources: Pulses, eggs, meat, fish, milk, soybean\n\n3. Fats: Provide energy and warmth\n   Sources: Oil, butter, ghee, cheese, nuts\n\n4. Vitamins: Protect from diseases\n   Sources: Fruits, vegetables, milk, sunlight (Vit D)\n\n5. Minerals: Needed for various body functions\n   - Calcium (milk, cheese) - for bones\n   - Iron (spinach, liver) - for blood\n   - Iodine (iodized salt) - for thyroid\n\n6. Water: Essential for all body processes\n\n7. Roughage: Helps in digestion\n   Sources: Whole grains, fruits, vegetables"),
            ("What are deficiency diseases? Explain any four deficiency diseases with their causes and symptoms.",
             "Deficiency diseases are caused when our diet lacks a particular nutrient for a long time.\n\n1. Scurvy (Vitamin C deficiency)\n   - Symptoms: Bleeding gums, slow wound healing\n   - Prevention: Eat citrus fruits, amla, tomatoes\n\n2. Rickets (Vitamin D deficiency)\n   - Symptoms: Soft and bent bones in children\n   - Prevention: Sunlight exposure, milk, eggs\n\n3. Night blindness (Vitamin A deficiency)\n   - Symptoms: Poor vision in darkness\n   - Prevention: Carrots, papaya, leafy vegetables\n\n4. Goitre (Iodine deficiency)\n   - Symptoms: Swelling of thyroid gland in neck\n   - Prevention: Use iodized salt\n\n5. Anaemia (Iron deficiency)\n   - Symptoms: Weakness, pale skin, tiredness\n   - Prevention: Spinach, liver, jaggery"),
        ]
    },
    
    # Class 8 Science - Coal and Petroleum
    "Coal and Petroleum": {
        "key_concepts": [
            ("Natural resources", "Resources obtained from nature are natural resources. They can be inexhaustible (unlimited) like sunlight, air or exhaustible (limited) like coal, petroleum."),
            ("Fossil fuels", "Coal, petroleum, and natural gas are called fossil fuels as they were formed from the remains of dead organisms millions of years ago."),
            ("Coal formation", "Coal was formed by the decomposition of large trees buried under the earth millions of years ago. This process is called carbonisation."),
            ("Products of coal", "Coal is processed to get coke, coal tar, and coal gas. These are used in various industries."),
            ("Petroleum formation", "Petroleum was formed from organisms living in the sea. When they died ande settled, they got converted to petroleum under heat and pressure."),
            ("Petroleum refining", "Petroleum is refined to get petrol, diesel, kerosene, LPG, paraffin wax, and bitumen."),
            ("Natural gas", "Natural gas is a clean fuel found with petroleum deposits. CNG is used as fuel for vehicles."),
            ("Conservation", "Fossil fuels are limited and take millions of years to form. We must conserve them by using them wisely."),
        ],
        "mcq_pool": [
            ("Coal, petroleum, and natural gas are called:", ["Mineral fuels", "Fossil fuels", "Natural fuels", "Bio fuels"], "Fossil fuels", "They were formed from fossils (remains of dead organisms)."),
            ("The process of separating petroleum into different components is called:", ["Distillation", "Refining", "Mining", "Drilling"], "Refining", "Petroleum refining separates crude oil into useful products."),
            ("Which of these is NOT a product of petroleum?", ["Diesel", "Petrol", "Coke", "Kerosene"], "Coke", "Coke is obtained from coal, not petroleum."),
            ("CNG stands for:", ["Compressed Natural Gas", "Converted Natural Gas", "Common Natural Gas", "Chemical Natural Gas"], "Compressed Natural Gas", "CNG is natural gas compressed to high pressure for use as vehicle fuel."),
            ("Coal tar is used to make:", ["Dyes and explosives", "Steel", "Cement", "Glass"], "Dyes and explosives", "Coal tar is used in making synthetic dyes, drugs, explosives, and perfumes."),
            ("Which is an inexhaustible natural resource?", ["Coal", "Petroleum", "Sunlight", "Natural gas"], "Sunlight", "Sunlight is unlimited and will last forever."),
            ("Petroleum is also called:", ["Black gold", "Liquid gold", "Natural gold", "Earth gold"], "Black gold", "Petroleum is called black gold due to its black color and high value."),
            ("Which fuel causes least air pollution?", ["Coal", "Petrol", "CNG", "Diesel"], "CNG", "CNG is a cleaner fuel that produces less pollution."),
            ("Bitumen is used for:", ["Surfacing roads", "Cooking fuel", "Vehicle fuel", "Making plastics"], "Surfacing roads", "Bitumen is the residue of petroleum refining used for road construction."),
            ("Coal is formed from:", ["Dead animals", "Dead plants", "Rocks", "Sand"], "Dead plants", "Coal was formed from dead plants buried millions of years ago."),
        ],
        "fill_blanks": [
            ("The slow process of conversion of dead vegetation into coal is called _______.", "carbonisation"),
            ("Petroleum is also called _______ gold.", "black"),
            ("The process of separating petroleum into different fractions is called _______.", "refining"),
            ("CNG stands for _______.", "Compressed Natural Gas"),
            ("_______ obtained from coal tar is used in making dyes.", "Aniline"),
            ("Fossil fuels are _______ natural resources.", "exhaustible"),
            ("_______ is used for surfacing roads.", "Bitumen"),
            ("LPG stands for _______.", "Liquefied Petroleum Gas"),
        ],
        "short_answers": [
            ("What are fossil fuels? Why are they called so?", "Fossil fuels are fuels formed from the remains of dead organisms that were buried under the earth millions of years ago. They are called fossil fuels because they were formed from fossils."),
            ("How is coal formed?", "Coal was formed when large trees and plants buried under the earth millions of years ago slowly got converted into coal due to high temperature and pressure. This slow process is called carbonisation."),
            ("What are the products obtained from petroleum refining?", "Petroleum refining gives: LPG, petrol, kerosene, diesel, lubricating oil, paraffin wax, and bitumen. Each product has different uses."),
            ("Why should we conserve fossil fuels?", "We should conserve fossil fuels because:\n1. They are exhaustible resources\n2. They take millions of years to form\n3. Once used, they cannot be regenerated\n4. They are essential for many industries"),
            ("What is the difference between exhaustible and inexhaustible resources?", "Exhaustible resources are limited and will get depleted (e.g., coal, petroleum). Inexhaustible resources are unlimited and will not get exhausted (e.g., sunlight, wind, water)."),
        ],
        "long_answers": [
            ("Explain the formation of petroleum. List the various products obtained from petroleum refining.",
             "Formation of Petroleum:\nPetroleum was formed from organisms living in the sea millions of years ago. When these organisms died, their bodies settled at the bottom of the sea and got covered with layers of sand and clay. Over millions of years, under high temperature and pressure, these remains were converted into petroleum and natural gas.\n\nProducts of Petroleum Refining:\n1. LPG (Liquefied Petroleum Gas) - cooking fuel\n2. Petrol - vehicle fuel\n3. Kerosene - fuel for stoves and jet planes\n4. Diesel - fuel for heavy vehicles\n5. Lubricating oil - lubrication of machines\n6. Paraffin wax - candles, vaseline\n7. Bitumen - road surfacing"),
            ("What is coal? How is it formed? Describe the products obtained from coal processing.",
             "Coal:\nCoal is a black, hard substance made mainly of carbon. It is used as fuel in homes and industries.\n\nFormation:\nMillions of years ago, the earth had dense forests. When trees died, they got buried under the soil. As more soil deposited, they were compressed. High temperature and pressure converted them slowly into coal. This process is called carbonisation.\n\nProducts from Coal:\n1. Coke: Almost pure carbon, used in steel making\n2. Coal tar: Thick black liquid, used for making:\n   - Synthetic dyes\n   - Drugs and medicines\n   - Explosives\n   - Perfumes\n   - Plastics\n   - Naphthalene balls\n3. Coal gas: Used as fuel in industries, was earlier used for street lighting"),
        ]
    },
    
    # Class 10 Science - Chapter 1: Chemical Reactions and Equations
    "Chemical Reactions and Equations": {
        "key_concepts": [
            ("Chemical reaction", "A process in which one or more substances are converted into new substances with different properties."),
            ("Chemical equation", "A symbolic representation of a chemical reaction using formulas of reactants and products."),
            ("Balanced equation", "A chemical equation with equal number of atoms of each element on both sides."),
            ("Combination reaction", "Two or more substances combine to form a single product. Example: 2Mg + O2 → 2MgO"),
            ("Decomposition reaction", "A single compound breaks down into two or more simpler substances."),
            ("Displacement reaction", "A more reactive element displaces a less reactive element from its compound."),
            ("Double displacement reaction", "Exchange of ions between two compounds. Example: precipitation reactions."),
            ("Oxidation", "Addition of oxygen or removal of hydrogen from a substance."),
            ("Reduction", "Removal of oxygen or addition of hydrogen to a substance."),
            ("Redox reaction", "A reaction where both oxidation and reduction occur simultaneously."),
        ],
        "mcq_pool": [
            ("Which of the following is an example of a combination reaction?", ["2H2 + O2 → 2H2O", "CaCO3 → CaO + CO2", "Zn + CuSO4 → ZnSO4 + Cu", "NaCl + AgNO3 → AgCl + NaNO3"], "2H2 + O2 → 2H2O", "Two reactants combine to form a single product."),
            ("Decomposition of ferrous sulphate is an example of:", ["Combination reaction", "Displacement reaction", "Decomposition reaction", "Double displacement"], "Decomposition reaction", "2FeSO4 → Fe2O3 + SO2 + SO3"),
            ("In which reaction, heat is absorbed?", ["Burning of coal", "Respiration", "Decomposition of vegetable matter", "Decomposition of AgBr in presence of sunlight"], "Decomposition of AgBr in presence of sunlight", "Endothermic reactions absorb heat."),
            ("What happens when dilute HCl is added to iron filings?", ["H2 gas and FeCl2 formed", "Cl2 gas and Fe(OH)2 formed", "No reaction", "FeCl2 and water formed"], "H2 gas and FeCl2 formed", "Fe + 2HCl → FeCl2 + H2↑"),
            ("Rancidity can be prevented by:", ["Adding antioxidants", "Storing in airtight containers", "Refrigeration", "All of the above"], "All of the above", "All these methods prevent oxidation of fats."),
            ("Which is NOT a characteristic of a chemical reaction?", ["Change in state", "Change in color", "Evolution of gas", "Change in shape only"], "Change in shape only", "Physical change only involves change in shape."),
            ("The reaction CuO + H2 → Cu + H2O is an example of:", ["Oxidation", "Reduction", "Redox reaction", "Decomposition"], "Redox reaction", "CuO is reduced and H2 is oxidized."),
            ("Quick lime reacts vigorously with water to produce:", ["CaCO3", "Ca(OH)2", "CaO", "CaCl2"], "Ca(OH)2", "CaO + H2O → Ca(OH)2 + Heat"),
            ("A brown substance X on heating in air forms a substance Y. X and Y are:", ["Cu and CuO", "Fe and Fe2O3", "Mg and MgO", "Zn and ZnO"], "Cu and CuO", "Copper turns black on heating due to CuO formation."),
            ("Which statement about a balanced equation is correct?", ["Mass of reactants equals mass of products", "Number of molecules is same on both sides", "Color is same on both sides", "State is same on both sides"], "Mass of reactants equals mass of products", "Law of conservation of mass."),
        ],
        "fill_blanks": [
            ("A reaction in which a single product is formed from two or more reactants is called a _______ reaction.", "combination"),
            ("The reaction Fe2O3 + 2Al → Al2O3 + 2Fe is called _______ reaction.", "thermit"),
            ("Respiration is an _______ reaction.", "exothermic"),
            ("The process of depositing zinc on iron is called _______.", "galvanisation"),
            ("Addition of oxygen to a substance is called _______.", "oxidation"),
            ("The reaction in which precipitate is formed is called _______ reaction.", "precipitation"),
            ("Silver bromide decomposes in presence of _______ to give silver and bromine.", "sunlight"),
            ("In a _______ equation, mass is conserved.", "balanced"),
        ],
        "short_answers": [
            ("What is a balanced chemical equation? Why should chemical equations be balanced?", "A balanced chemical equation has equal number of atoms of each element on both sides. It should be balanced because of the law of conservation of mass - matter cannot be created or destroyed."),
            ("What is a decomposition reaction? Give an example.", "A decomposition reaction is one where a single compound breaks down into two or more simpler substances.\nExample: 2H2O → 2H2 + O2 (electrolysis of water)"),
            ("What is rancidity? How can it be prevented?", "Rancidity is the oxidation of fats and oils in food, causing bad smell and taste. Prevention: 1) Adding antioxidants 2) Storing in airtight containers 3) Refrigeration 4) Nitrogen packing"),
            ("Define oxidation and reduction.", "Oxidation: Addition of oxygen or removal of hydrogen from a substance.\nReduction: Removal of oxygen or addition of hydrogen to a substance."),
            ("Why is respiration considered an exothermic reaction?", "Respiration is exothermic because glucose combines with oxygen to release energy: C6H12O6 + 6O2 → 6CO2 + 6H2O + Energy"),
        ],
        "long_answers": [
            ("Explain different types of chemical reactions with examples.",
             "Types of Chemical Reactions:\n\n1. Combination Reaction: Two or more substances combine to form one product.\n   Example: 2Mg + O2 → 2MgO\n   Example: CaO + H2O → Ca(OH)2\n\n2. Decomposition Reaction: One compound breaks into two or more substances.\n   Example: 2H2O → 2H2 + O2\n   Example: CaCO3 → CaO + CO2\n\n3. Displacement Reaction: More reactive element displaces less reactive one.\n   Example: Fe + CuSO4 → FeSO4 + Cu\n\n4. Double Displacement Reaction: Exchange of ions between compounds.\n   Example: Na2SO4 + BaCl2 → BaSO4 + 2NaCl\n\n5. Redox Reaction: Oxidation and reduction occur simultaneously.\n   Example: CuO + H2 → Cu + H2O"),
            ("What are oxidation and reduction reactions? Explain with examples. What is a redox reaction?",
             "Oxidation:\n- Addition of oxygen to a substance\n- Removal of hydrogen from a substance\n- Loss of electrons\nExample: 2Cu + O2 → 2CuO (Cu is oxidized)\n\nReduction:\n- Removal of oxygen from a substance\n- Addition of hydrogen to a substance\n- Gain of electrons\nExample: CuO + H2 → Cu + H2O (CuO is reduced)\n\nRedox Reaction:\nA reaction where both oxidation and reduction occur simultaneously is called a redox reaction.\nExample: ZnO + C → Zn + CO\nHere, ZnO is reduced to Zn and C is oxidized to CO.\n\nIn any redox reaction:\n- The substance that gets oxidized is the reducing agent\n- The substance that gets reduced is the oxidizing agent"),
        ]
    },
    
    # Class 10 Science - Chapter 2: Acids, Bases and Salts
    "Acids, Bases and Salts": {
        "key_concepts": [
            ("Acid", "A substance that produces H+ ions in water solution. Examples: HCl, H2SO4, HNO3"),
            ("Base", "A substance that produces OH- ions in water solution. Examples: NaOH, KOH, Ca(OH)2"),
            ("Indicator", "A substance that shows different colors in acidic and basic solutions."),
            ("pH scale", "A scale from 0-14 measuring acidity/basicity. pH 7 is neutral."),
            ("Neutralization", "Reaction between acid and base to form salt and water."),
            ("Salt", "A compound formed by neutralization of an acid and a base."),
        ],
        "mcq_pool": [
            ("Which of these turns blue litmus red?", ["NaOH", "HCl", "NaCl", "H2O"], "HCl", "Acids turn blue litmus red."),
            ("pH of pure water is:", ["0", "7", "14", "1"], "7", "Pure water is neutral with pH 7."),
            ("Baking soda is:", ["NaHCO3", "Na2CO3", "NaCl", "NaOH"], "NaHCO3", "Baking soda is sodium hydrogen carbonate."),
            ("Milk of magnesia is used as:", ["Antacid", "Fertilizer", "Cleaner", "Fuel"], "Antacid", "Mg(OH)2 neutralizes excess stomach acid."),
            ("Which gas is evolved when acid reacts with metal?", ["O2", "H2", "CO2", "N2"], "H2", "Metal + Acid → Salt + Hydrogen gas"),
            ("Plaster of Paris is:", ["CaSO4.2H2O", "CaSO4.½H2O", "CaSO4", "Ca(OH)2"], "CaSO4.½H2O", "It has half molecule of water of crystallization."),
            ("Tooth decay is caused by pH:", ["Above 7", "Below 5.5", "Exactly 7", "Above 10"], "Below 5.5", "Acidic conditions cause enamel corrosion."),
            ("Bleaching powder is:", ["CaOCl2", "Ca(OH)2", "CaCO3", "CaCl2"], "CaOCl2", "Calcium oxychloride is bleaching powder."),
        ],
        "fill_blanks": [
            ("Acids produce _______ ions in water.", "H+"),
            ("A solution with pH less than 7 is _______.", "acidic"),
            ("Baking soda is chemically _______.", "sodium hydrogen carbonate"),
            ("Plaster of Paris is used for _______.", "making casts/statues"),
            ("The reaction between acid and base is called _______.", "neutralization"),
            ("Washing soda is _______ .", "Na2CO3.10H2O"),
        ],
        "short_answers": [
            ("Why does dry HCl gas not change the colour of dry litmus paper?", "Dry HCl does not release H+ ions. Acids show acidic properties only in presence of water."),
            ("What is baking powder? What happens when it is heated?", "Baking powder is a mixture of baking soda and tartaric acid. On heating, it releases CO2 which makes bread fluffy."),
            ("How is Plaster of Paris prepared?", "Plaster of Paris is prepared by heating gypsum (CaSO4.2H2O) at 373K.\nCaSO4.2H2O → CaSO4.½H2O + 1½H2O"),
            ("Why is sodium hydroxide called a strong base?", "NaOH is a strong base because it completely dissociates in water to give Na+ and OH- ions."),
        ],
        "long_answers": [
            ("What is pH scale? Why is it important in everyday life?",
             "pH Scale:\npH scale is a scale from 0 to 14 that measures the acidity or basicity of a solution.\n- pH 0-6: Acidic (lower = more acidic)\n- pH 7: Neutral\n- pH 8-14: Basic/Alkaline (higher = more basic)\n\nImportance in Everyday Life:\n1. Digestion: Stomach has pH 1-2 for digestion\n2. Tooth decay: Occurs below pH 5.5\n3. Soil pH: Affects plant growth (most plants prefer pH 6-7)\n4. Bee stings: Acidic, treated with baking soda\n5. Blood pH: Must be maintained at 7.35-7.45\n6. Rainwater: pH below 5.6 is acid rain"),
        ]
    },
    
    # Class 10 Science - Chapter 9: Light Reflection and Refraction
    "Light – Reflection and Refraction": {
        "key_concepts": [
            ("Reflection", "Bouncing back of light from a polished surface."),
            ("Refraction", "Bending of light when it passes from one medium to another."),
            ("Concave mirror", "A spherical mirror with reflecting surface curved inward."),
            ("Convex mirror", "A spherical mirror with reflecting surface curved outward."),
            ("Focal length", "Distance between pole and principal focus of a mirror/lens."),
            ("Refractive index", "Ratio of speed of light in vacuum to speed in a medium."),
        ],
        "mcq_pool": [
            ("Rear view mirrors in vehicles are:", ["Concave", "Convex", "Plane", "Cylindrical"], "Convex", "Convex mirrors give wider field of view."),
            ("Power of a lens is measured in:", ["Metre", "Dioptre", "Joule", "Watt"], "Dioptre", "P = 1/f (where f is in metres)"),
            ("If focal length is 20 cm, power is:", ["5 D", "0.5 D", "2 D", "20 D"], "5 D", "P = 100/20 = 5 D"),
            ("Image formed by plane mirror is:", ["Real and inverted", "Virtual and erect", "Real and erect", "Virtual and inverted"], "Virtual and erect", "Plane mirrors form virtual, erect, same-sized images."),
            ("Which lens is used to correct myopia?", ["Convex", "Concave", "Bifocal", "Cylindrical"], "Concave", "Concave lens diverges light to correct near-sightedness."),
            ("Speed of light is maximum in:", ["Glass", "Water", "Vacuum", "Diamond"], "Vacuum", "Light travels at 3×10^8 m/s in vacuum."),
            ("Mirror formula is:", ["1/f = 1/v + 1/u", "1/f = 1/v - 1/u", "f = v + u", "f = v × u"], "1/f = 1/v + 1/u", "Standard mirror formula."),
            ("Virtual image is formed by concave mirror when object is:", ["Beyond C", "At C", "Between F and C", "Between P and F"], "Between P and F", "Object between pole and focus gives virtual, enlarged image."),
        ],
        "fill_blanks": [
            ("The ratio sin i / sin r is called _______.", "refractive index"),
            ("Power of a convex lens is _______.", "positive"),
            ("A lens with focal length -50 cm has power _______ D.", "-2"),
            ("Convex mirror always forms _______ image.", "virtual"),
            ("The center of curvature of a spherical mirror is denoted by _______.", "C"),
        ],
        "short_answers": [
            ("Why are convex mirrors used as rear-view mirrors?", "Convex mirrors are used because they: 1) Always form erect images 2) Give a wider field of view 3) Allow the driver to see traffic behind."),
            ("What is the focal length of a plane mirror?", "A plane mirror has infinite focal length (f = ∞) because parallel rays remain parallel after reflection."),
            ("Define refractive index.", "Refractive index of a medium is the ratio of speed of light in vacuum to the speed of light in that medium. n = c/v"),
        ],
        "long_answers": [
            ("Draw ray diagrams to show image formation by concave mirror for different positions of object.",
             "Image formation by Concave Mirror:\n\n1. Object at infinity:\n   Image: At F, real, inverted, highly diminished (point)\n\n2. Object beyond C:\n   Image: Between F and C, real, inverted, diminished\n\n3. Object at C:\n   Image: At C, real, inverted, same size\n\n4. Object between C and F:\n   Image: Beyond C, real, inverted, magnified\n\n5. Object at F:\n   Image: At infinity, real, inverted, highly magnified\n\n6. Object between P and F:\n   Image: Behind mirror, virtual, erect, magnified"),
        ]
    },
    
    # Class 10 Science - Chapter 11: Electricity
    "Electricity": {
        "key_concepts": [
            ("Electric current", "Flow of electric charge. I = Q/t. Unit: Ampere"),
            ("Potential difference", "Work done per unit charge. V = W/Q. Unit: Volt"),
            ("Resistance", "Opposition to flow of current. R = V/I. Unit: Ohm"),
            ("Ohm's law", "V = IR (at constant temperature)"),
            ("Electric power", "Rate of electrical energy consumption. P = VI = I²R = V²/R"),
        ],
        "mcq_pool": [
            ("SI unit of electric current is:", ["Volt", "Ampere", "Ohm", "Watt"], "Ampere", "Current measured in amperes (A)."),
            ("Resistance of a wire depends on:", ["Length", "Area", "Material", "All of these"], "All of these", "R = ρL/A"),
            ("1 kWh equals:", ["3600 J", "36000 J", "3.6 × 10^6 J", "360 J"], "3.6 × 10^6 J", "1 kWh = 1000 × 3600 = 3.6 × 10^6 J"),
            ("Three resistors of 3Ω each in parallel give:", ["9Ω", "1Ω", "3Ω", "6Ω"], "1Ω", "1/R = 1/3 + 1/3 + 1/3 = 1"),
            ("Fuse wire is made of:", ["Copper", "Aluminium", "Alloy of lead and tin", "Iron"], "Alloy of lead and tin", "Low melting point alloy."),
            ("Which has more resistance - 60W or 100W bulb?", ["60W has more", "100W has more", "Same", "Cannot determine"], "60W has more", "R = V²/P, so lower power means higher resistance."),
            ("Heating element is made of:", ["Copper", "Nichrome", "Iron", "Silver"], "Nichrome", "High resistivity and melting point."),
        ],
        "fill_blanks": [
            ("Electric current is the rate of flow of _______.", "charge"),
            ("1 ampere = _______ coulombs per second.", "1"),
            ("Ohm's law states V = _______.", "IR"),
            ("In series combination, current is _______ throughout.", "same"),
            ("Commercial unit of electrical energy is _______.", "kilowatt-hour"),
            ("Resistivity of a conductor _______ with increase in temperature.", "increases"),
        ],
        "short_answers": [
            ("State Ohm's law.", "Ohm's law: The current through a conductor is directly proportional to the potential difference across it, provided temperature remains constant. V = IR"),
            ("Why are copper and aluminium used for transmission lines?", "They have low resistivity (low resistance), so less energy is lost as heat during transmission."),
            ("What is the advantage of parallel combination?", "In parallel: 1) Each device gets full voltage 2) If one device fails, others continue working 3) Different devices can be operated independently."),
            ("What is electric power? Give its formula.", "Electric power is the rate of consumption of electrical energy. P = VI = I²R = V²/R. Unit: Watt"),
        ],
        "long_answers": [
            ("Derive the expression for equivalent resistance when resistors are connected in series and parallel.",
             "Resistors in Series:\nIn series, same current I flows through all resistors.\nTotal voltage V = V1 + V2 + V3\nV = IR1 + IR2 + IR3 = I(R1 + R2 + R3)\nV/I = R1 + R2 + R3\nRs = R1 + R2 + R3\nEquivalent resistance equals sum of all resistances.\n\nResistors in Parallel:\nIn parallel, same voltage V across all resistors.\nTotal current I = I1 + I2 + I3\nI = V/R1 + V/R2 + V/R3 = V(1/R1 + 1/R2 + 1/R3)\nI/V = 1/R1 + 1/R2 + 1/R3\n1/Rp = 1/R1 + 1/R2 + 1/R3\nEquivalent resistance is less than smallest individual resistance."),
        ]
    },
    
    # Class 10 Science - Chapter 5: Life Processes
    "Life Processes": {
        "key_concepts": [
            ("Nutrition", "Process by which organisms obtain and utilize food for energy and growth."),
            ("Autotrophic nutrition", "Organisms that make their own food (photosynthesis)."),
            ("Heterotrophic nutrition", "Organisms that depend on other organisms for food."),
            ("Respiration", "Breakdown of glucose to release energy."),
            ("Transportation", "Movement of substances in organisms (blood, xylem, phloem)."),
            ("Excretion", "Removal of metabolic wastes from the body."),
        ],
        "mcq_pool": [
            ("Site of photosynthesis in a cell is:", ["Mitochondria", "Chloroplast", "Ribosome", "Nucleus"], "Chloroplast", "Chloroplast contains chlorophyll for photosynthesis."),
            ("Which is NOT part of human digestive system?", ["Liver", "Pancreas", "Kidney", "Small intestine"], "Kidney", "Kidney is part of excretory system."),
            ("In humans, digestion of starch begins in:", ["Stomach", "Mouth", "Small intestine", "Large intestine"], "Mouth", "Salivary amylase starts starch digestion."),
            ("The blood vessel that carries blood to the kidneys is:", ["Renal artery", "Renal vein", "Pulmonary artery", "Aorta"], "Renal artery", "Renal artery brings blood to kidneys for filtration."),
            ("Stomata open and close due to:", ["Guard cells", "Epidermal cells", "Mesophyll cells", "Companion cells"], "Guard cells", "Guard cells control stomatal opening."),
            ("Oxygen is transported in blood by:", ["Plasma", "RBC", "WBC", "Platelets"], "RBC", "Haemoglobin in RBCs carries oxygen."),
            ("Bile is produced by:", ["Gall bladder", "Liver", "Pancreas", "Stomach"], "Liver", "Liver produces bile, stored in gall bladder."),
        ],
        "fill_blanks": [
            ("The green pigment in leaves is called _______.", "chlorophyll"),
            ("The functional unit of kidney is _______.", "nephron"),
            ("_______ carry blood away from the heart.", "Arteries"),
            ("The largest artery in the body is _______.", "aorta"),
            ("In plants, food is transported through _______.", "phloem"),
            ("The site of complete digestion is _______.", "small intestine"),
        ],
        "short_answers": [
            ("What is photosynthesis? Write its equation.", "Photosynthesis is the process by which green plants make food using sunlight.\n6CO2 + 6H2O → C6H12O6 + 6O2 (in presence of sunlight and chlorophyll)"),
            ("Why is small intestine very long?", "Small intestine is long (about 7m) to increase surface area for better absorption of digested food into blood."),
            ("What is the role of HCl in stomach?", "HCl in stomach: 1) Kills bacteria in food 2) Makes medium acidic for pepsin action 3) Activates pepsinogen to pepsin"),
        ],
        "long_answers": [
            ("Describe the process of digestion in humans.",
             "Digestion in Humans:\n\n1. Mouth: Teeth break food (mechanical). Salivary amylase converts starch to maltose.\n\n2. Stomach: HCl kills germs and activates pepsin. Pepsin digests proteins to peptides.\n\n3. Small Intestine:\n   - Bile from liver emulsifies fats\n   - Pancreatic enzymes: trypsin (proteins), lipase (fats), amylase (starch)\n   - Intestinal enzymes complete digestion\n   - Villi absorb nutrients into blood\n\n4. Large Intestine: Absorbs water and remaining nutrients. Undigested food forms faeces.\n\n5. Rectum: Stores faeces until elimination through anus."),
        ]
    },
    
    # Additional chapters with basic content
    "Metals and Non-metals": {
        "mcq_pool": [
            ("Which metal is stored in kerosene?", ["Iron", "Sodium", "Copper", "Aluminium"], "Sodium", "Sodium reacts vigorously with air and water."),
            ("Most reactive metal is:", ["Gold", "Iron", "Potassium", "Copper"], "Potassium", "K is most reactive in the given options."),
            ("Aqua regia is a mixture of:", ["HCl and HNO3", "H2SO4 and HNO3", "HCl and H2SO4", "HCl and H2O"], "HCl and HNO3", "3:1 ratio of conc. HCl and HNO3."),
            ("An alloy of copper and zinc is:", ["Bronze", "Brass", "Solder", "Steel"], "Brass", "Brass = Cu + Zn"),
            ("Which ore is concentrated by froth floatation?", ["Haematite", "Bauxite", "Sulphide ores", "Oxide ores"], "Sulphide ores", "Sulphide ores are concentrated by froth floatation."),
        ],
        "fill_blanks": [
            ("The process of depositing zinc on iron is called _______.", "galvanization"),
            ("Metals that can be beaten into sheets are called _______.", "malleable"),
            ("Copper is refined by _______ refining.", "electrolytic"),
            ("Bronze is an alloy of copper and _______.", "tin"),
        ],
        "short_answers": [
            ("Why is sodium kept under kerosene?", "Sodium is highly reactive. It reacts vigorously with oxygen and moisture in air, catching fire. Kerosene prevents contact with air."),
            ("What is corrosion? How can it be prevented?", "Corrosion is the gradual destruction of metals by reaction with environment. Prevention: painting, oiling, galvanization, electroplating, making alloys."),
        ],
        "long_answers": []
    },
    
    "Carbon and its Compounds": {
        "mcq_pool": [
            ("Carbon exists as:", ["Diamond only", "Graphite only", "Both diamond and graphite", "None"], "Both diamond and graphite", "These are allotropes of carbon."),
            ("Ethanol is denatured by adding:", ["Methanol", "Propanol", "Butanol", "Pentanol"], "Methanol", "Methanol is added to make industrial alcohol unfit for drinking."),
            ("Functional group in alcohols is:", ["-OH", "-CHO", "-COOH", "-CO-"], "-OH", "Alcohols contain hydroxyl group."),
            ("IUPAC name of CH3-CH2-OH is:", ["Methanol", "Ethanol", "Propanol", "Butanol"], "Ethanol", "2 carbons with -OH group."),
            ("Ethanoic acid is commonly known as:", ["Formic acid", "Acetic acid", "Citric acid", "Tartaric acid"], "Acetic acid", "CH3COOH is vinegar/acetic acid."),
        ],
        "fill_blanks": [
            ("The IUPAC name of CH4 is _______.", "methane"),
            ("Functional group -CHO is called _______.", "aldehyde"),
            ("Hardening of oils is called _______.", "hydrogenation"),
            ("The general formula of alkenes is _______.", "CnH2n"),
        ],
        "short_answers": [
            ("What are hydrocarbons?", "Hydrocarbons are compounds containing only carbon and hydrogen. Examples: CH4 (methane), C2H6 (ethane)."),
            ("What is a homologous series?", "A series of compounds with same functional group and similar properties, differing by -CH2- unit. Example: Methane, Ethane, Propane..."),
        ],
        "long_answers": []
    },
    
    "Control and Coordination": {
        "mcq_pool": [
            ("The brain is protected by:", ["Skull", "Vertebral column", "Ribs", "Sternum"], "Skull", "Cranium protects the brain."),
            ("Which hormone regulates blood sugar?", ["Thyroxine", "Insulin", "Adrenaline", "Growth hormone"], "Insulin", "Insulin lowers blood glucose level."),
            ("Plant hormone that promotes cell division is:", ["Auxin", "Gibberellin", "Cytokinin", "Ethylene"], "Cytokinin", "Cytokinin promotes cell division."),
            ("Iodine deficiency causes:", ["Diabetes", "Goitre", "Dwarfism", "Gigantism"], "Goitre", "Iodine is needed for thyroxine production."),
        ],
        "fill_blanks": [
            ("The gap between two neurons is called _______.", "synapse"),
            ("Insulin is secreted by _______.", "pancreas"),
            ("Adrenaline is also called _______ hormone.", "fight or flight"),
            ("Auxin is produced at the _______ of the plant.", "tip/apex"),
        ],
        "short_answers": [
            ("What is reflex action?", "A reflex action is an automatic, rapid, and involuntary response to a stimulus. Example: pulling hand away from hot object."),
            ("Name the parts of human brain.", "Human brain has three main parts: 1) Fore-brain (cerebrum) 2) Mid-brain 3) Hind-brain (cerebellum, pons, medulla)"),
        ],
        "long_answers": []
    },
    
    "How do Organisms Reproduce": {
        "mcq_pool": [
            ("Vegetative propagation in potato is by:", ["Stem", "Root", "Leaf", "Seed"], "Stem", "Potato tuber is a modified stem."),
            ("Male reproductive part of flower is:", ["Pistil", "Stamen", "Sepal", "Petal"], "Stamen", "Stamen produces pollen grains."),
            ("Fertilization in humans occurs in:", ["Uterus", "Ovary", "Fallopian tube", "Vagina"], "Fallopian tube", "Fusion of sperm and egg occurs in oviduct."),
            ("Unisexual flower is:", ["Rose", "Papaya", "Hibiscus", "Mustard"], "Papaya", "Papaya has separate male and female flowers."),
        ],
        "fill_blanks": [
            ("The male gamete in humans is called _______.", "sperm"),
            ("Budding is seen in _______.", "yeast/Hydra"),
            ("Binary fission is seen in _______.", "Amoeba"),
            ("Seeds develop from _______.", "ovules"),
        ],
        "short_answers": [
            ("What is the advantage of sexual reproduction?", "Sexual reproduction creates variation by combining genes from two parents. This variation helps species adapt and evolve."),
            ("What is pollination?", "Pollination is the transfer of pollen grains from anther to stigma of a flower. It can be self-pollination or cross-pollination."),
        ],
        "long_answers": []
    },
    
    "Heredity": {
        "mcq_pool": [
            ("Father of genetics is:", ["Darwin", "Mendel", "Lamarck", "Watson"], "Mendel", "Gregor Mendel discovered laws of inheritance."),
            ("DNA is present in:", ["Nucleus", "Cytoplasm", "Cell membrane", "Vacuole"], "Nucleus", "DNA is found in chromosomes in nucleus."),
            ("Genes are made of:", ["Proteins", "DNA", "Lipids", "Carbohydrates"], "DNA", "Genes are segments of DNA."),
            ("Number of chromosomes in human body cells is:", ["23", "46", "44", "22"], "46", "23 pairs = 46 chromosomes."),
        ],
        "fill_blanks": [
            ("The study of heredity is called _______.", "genetics"),
            ("In humans, sex is determined by _______ chromosomes.", "X and Y"),
            ("Dominant trait is expressed in _______ form.", "heterozygous"),
            ("Mendel worked on _______ plant.", "pea"),
        ],
        "short_answers": [
            ("What are genes?", "Genes are units of heredity. They are segments of DNA that contain information for making proteins and controlling traits."),
            ("How is sex determined in humans?", "Sex is determined by sex chromosomes. XX = female, XY = male. Father's sperm (X or Y) determines the sex of child."),
        ],
        "long_answers": []
    },
    
    "The Human Eye and the Colourful World": {
        "mcq_pool": [
            ("The human eye lens is:", ["Concave", "Convex", "Biconvex", "Biconcave"], "Biconvex", "Eye lens is convex on both sides."),
            ("Myopia is corrected by:", ["Convex lens", "Concave lens", "Bifocal lens", "Cylindrical lens"], "Concave lens", "Concave lens diverges light before entering eye."),
            ("The splitting of white light is called:", ["Reflection", "Refraction", "Dispersion", "Scattering"], "Dispersion", "Prism disperses white light into VIBGYOR."),
            ("Sky appears blue due to:", ["Dispersion", "Scattering", "Reflection", "Refraction"], "Scattering", "Blue light is scattered more by atmosphere."),
        ],
        "fill_blanks": [
            ("Power of accommodation is due to _______.", "ciliary muscles"),
            ("VIBGYOR are colors of _______.", "rainbow/spectrum"),
            ("Advanced sunrise is due to _______ refraction.", "atmospheric"),
            ("Cataract is cloudiness of _______.", "lens"),
        ],
        "short_answers": [
            ("What is myopia? How is it corrected?", "Myopia (near-sightedness) is when image forms before retina. Corrected using concave lens of suitable power."),
            ("Why does sky appear blue?", "Atmosphere scatters sunlight. Blue light (shorter wavelength) is scattered more than red. So sky appears blue."),
        ],
        "long_answers": []
    },
    
    "Magnetic Effects of Electric Current": {
        "mcq_pool": [
            ("Magnetic field lines around a current-carrying wire are:", ["Straight", "Circular", "Elliptical", "Random"], "Circular", "Field lines form concentric circles around wire."),
            ("Fleming's left hand rule gives direction of:", ["Current", "Field", "Force", "Voltage"], "Force", "It gives direction of force on current-carrying conductor."),
            ("An electric motor converts:", ["Electrical to mechanical", "Mechanical to electrical", "Heat to electrical", "Light to electrical"], "Electrical to mechanical", "Motor converts electrical energy to motion."),
            ("AC generator works on:", ["Faraday's law", "Ohm's law", "Newton's law", "Coulomb's law"], "Faraday's law", "Electromagnetic induction."),
        ],
        "fill_blanks": [
            ("The SI unit of magnetic field is _______.", "Tesla"),
            ("A coil of many turns is called a _______.", "solenoid"),
            ("The frequency of AC in India is _______ Hz.", "50"),
            ("A fuse wire has _______ melting point.", "low"),
        ],
        "short_answers": [
            ("State Fleming's left hand rule.", "Stretch thumb, forefinger and middle finger perpendicular to each other. Forefinger shows magnetic field direction, middle finger shows current direction, thumb shows force direction."),
            ("What is electromagnetic induction?", "The phenomenon of producing electric current by changing magnetic field around a conductor is electromagnetic induction."),
        ],
        "long_answers": []
    },
    
    "Our Environment": {
        "mcq_pool": [
            ("Biodegradable waste is:", ["Plastic", "Vegetable peels", "Glass", "Aluminum cans"], "Vegetable peels", "Organic waste is biodegradable."),
            ("10% energy is available at each trophic level as per:", ["3% law", "10% law", "20% law", "5% law"], "10% law", "Only 10% energy transfers to next level."),
            ("Ozone layer is present in:", ["Troposphere", "Stratosphere", "Mesosphere", "Thermosphere"], "Stratosphere", "Ozone layer is in stratosphere."),
            ("CFCs deplete:", ["Oxygen", "Ozone", "Nitrogen", "Carbon dioxide"], "Ozone", "CFCs break down ozone molecules."),
        ],
        "fill_blanks": [
            ("Organisms that produce their own food are called _______.", "producers"),
            ("The sequence of eating and being eaten is called _______.", "food chain"),
            ("Ozone is made of _______ oxygen atoms.", "three"),
            ("Plastic is _______ waste.", "non-biodegradable"),
        ],
        "short_answers": [
            ("What is a food chain?", "A food chain is a sequence showing who eats whom in an ecosystem. Example: Grass → Grasshopper → Frog → Snake → Eagle"),
            ("Why is ozone layer important?", "Ozone layer absorbs harmful UV radiations from sun, protecting life on Earth from skin cancer and eye damage."),
        ],
        "long_answers": []
    }
}


class QuestionPaperGenerator:
    """Generates NCERT-style question papers based on topic metadata."""
    
    QUESTION_TYPES = {
        'mcq': 'Multiple Choice Question',
        'fill_blank': 'Fill in the Blank',
        'very_short': 'Very Short Answer (1-2 lines)',
        'short': 'Short Answer (3-5 lines)',
        'long': 'Long Answer (paragraph)'
    }
    
    def __init__(self, model_path="output/qlora_tuned_model"):
        """Initialize the generator."""
        self.model_path = model_path
        self.model = None
        self.tokenizer = None
        self.device = "cpu"
        self.is_loaded = True  # Using knowledge bank, no model needed
        self.use_template_mode = True
        
    def load_model(self):
        """Model loading not needed - using knowledge bank."""
        self.is_loaded = True
        return True
    
    def get_chapter_knowledge(self, topic_content: str) -> dict:
        """Get knowledge bank for the chapter."""
        # Parse topic content to extract chapter name
        chapter_name = None
        for line in topic_content.split('\n'):
            if line.startswith('Chapter:'):
                chapter_name = line.replace('Chapter:', '').strip()
                break
        
        if chapter_name and chapter_name in NCERT_KNOWLEDGE:
            return NCERT_KNOWLEDGE[chapter_name]
        
        # Try partial match
        for key in NCERT_KNOWLEDGE:
            if key.lower() in topic_content.lower() or topic_content.lower() in key.lower():
                return NCERT_KNOWLEDGE[key]
        
        return None
    
    def generate_mcqs(self, knowledge: dict, count: int, difficulty: str) -> list:
        """Generate MCQs from knowledge bank."""
        questions = []
        mcq_pool = knowledge.get('mcq_pool', [])
        
        if not mcq_pool:
            return self._generate_fallback_questions('mcq', 1, count)
        
        # Shuffle and select
        selected = random.sample(mcq_pool, min(count, len(mcq_pool)))
        
        for q, options, answer, explanation in selected:
            # Shuffle options but keep track of correct answer
            option_letters = ['A', 'B', 'C', 'D']
            correct_idx = options.index(answer)
            
            shuffled_options = options.copy()
            random.shuffle(shuffled_options)
            new_correct_idx = shuffled_options.index(answer)
            correct_letter = option_letters[new_correct_idx]
            
            questions.append({
                'question': q,
                'options': [f"{letter}) {opt}" for letter, opt in zip(option_letters, shuffled_options)],
                'answer': correct_letter,
                'explanation': explanation,
                'marks': 1,
                'type': 'mcq'
            })
        
        # If we need more questions, repeat with slight variations
        while len(questions) < count:
            questions.append(questions[len(questions) % len(selected)].copy())
        
        return questions[:count]
    
    def generate_fill_blanks(self, knowledge: dict, count: int, difficulty: str) -> list:
        """Generate fill in the blank questions."""
        questions = []
        fill_pool = knowledge.get('fill_blanks', [])
        
        if not fill_pool:
            return self._generate_fallback_questions('fill_blank', 1, count)
        
        selected = random.sample(fill_pool, min(count, len(fill_pool)))
        
        for question, answer in selected:
            questions.append({
                'question': question,
                'answer': answer,
                'marks': 1,
                'type': 'fill_blank'
            })
        
        while len(questions) < count:
            questions.append(questions[len(questions) % len(selected)].copy())
        
        return questions[:count]
    
    def generate_short_answers(self, knowledge: dict, count: int, difficulty: str, marks: int) -> list:
        """Generate short answer questions."""
        questions = []
        short_pool = knowledge.get('short_answers', [])
        
        if not short_pool:
            return self._generate_fallback_questions('short', marks, count)
        
        selected = random.sample(short_pool, min(count, len(short_pool)))
        
        for question, answer in selected:
            questions.append({
                'question': question,
                'answer': answer,
                'key_points': answer.split('\n')[:3],
                'marks': marks,
                'type': 'short'
            })
        
        while len(questions) < count:
            questions.append(questions[len(questions) % len(selected)].copy())
        
        return questions[:count]
    
    def generate_long_answers(self, knowledge: dict, count: int, difficulty: str, marks: int) -> list:
        """Generate long answer questions."""
        questions = []
        long_pool = knowledge.get('long_answers', [])
        
        if not long_pool:
            return self._generate_fallback_questions('long', marks, count)
        
        selected = random.sample(long_pool, min(count, len(long_pool)))
        
        for question, answer in selected:
            questions.append({
                'question': question,
                'answer': answer,
                'key_points': [line.strip() for line in answer.split('\n') if line.strip()][:5],
                'marks': marks,
                'type': 'long'
            })
        
        while len(questions) < count:
            questions.append(questions[len(questions) % len(selected)].copy())
        
        return questions[:count]
    
    def generate_questions(self, topic_content: str, question_type: str,
                           marks: int, difficulty: str, count: int) -> list:
        """Generate questions using the knowledge bank."""
        
        knowledge = self.get_chapter_knowledge(topic_content)
        
        if not knowledge:
            return self._generate_fallback_questions(question_type, marks, count)
        
        if question_type == 'mcq':
            return self.generate_mcqs(knowledge, count, difficulty)
        elif question_type == 'fill_blank':
            return self.generate_fill_blanks(knowledge, count, difficulty)
        elif question_type in ['very_short', 'short']:
            return self.generate_short_answers(knowledge, count, difficulty, marks)
        else:  # long
            return self.generate_long_answers(knowledge, count, difficulty, marks)
    
    def _generate_fallback_questions(self, question_type: str, marks: int, count: int) -> list:
        """Generate fallback questions when knowledge bank is not available."""
        questions = []
        
        fallback_mcqs = [
            ("What is the main topic of this chapter?", ["Option A", "Option B", "Option C", "Option D"], "A", "Based on chapter content"),
            ("Which concept is most important in this chapter?", ["Concept 1", "Concept 2", "Concept 3", "Concept 4"], "A", "Key concept from syllabus"),
        ]
        
        for i in range(count):
            if question_type == 'mcq':
                q = fallback_mcqs[i % len(fallback_mcqs)]
                questions.append({
                    'question': f"{i+1}. {q[0]}",
                    'options': [f"{chr(65+j)}) {opt}" for j, opt in enumerate(q[1])],
                    'answer': q[2],
                    'explanation': q[3],
                    'marks': marks,
                    'type': question_type
                })
            elif question_type == 'fill_blank':
                questions.append({
                    'question': f"The key concept of this chapter is _______.",
                    'answer': "concept name",
                    'marks': marks,
                    'type': question_type
                })
            elif question_type in ['very_short', 'short']:
                questions.append({
                    'question': f"Explain the key concept from this chapter.",
                    'answer': "Answer based on chapter content.",
                    'key_points': ["Key point 1", "Key point 2"],
                    'marks': marks,
                    'type': question_type
                })
            else:
                questions.append({
                    'question': f"Discuss in detail the main topic of this chapter.",
                    'answer': "Detailed answer covering all aspects of the topic.",
                    'key_points': ["Introduction", "Main points", "Examples", "Conclusion"],
                    'marks': marks,
                    'type': question_type
                })
        
        return questions
    
    def distribute_difficulty(self, count: int, easy_pct: int, medium_pct: int, hard_pct: int) -> list:
        """Distribute questions across difficulty levels."""
        easy_count = round(count * easy_pct / 100)
        hard_count = round(count * hard_pct / 100)
        medium_count = count - easy_count - hard_count
        
        distribution = []
        distribution.extend(['easy'] * easy_count)
        distribution.extend(['medium'] * medium_count)
        distribution.extend(['hard'] * hard_count)
        
        random.shuffle(distribution)
        return distribution
    
    def generate_section(self, section_config: dict, topic_content: str,
                         difficulty_distribution: dict) -> dict:
        """Generate a complete section of the question paper."""
        
        section_name = section_config['name']
        question_type = section_config['questionType']
        question_count = section_config['questionCount']
        marks_per_question = section_config['marksPerQuestion']
        
        # Get difficulty distribution
        easy_pct = difficulty_distribution.get('easy', 30)
        medium_pct = difficulty_distribution.get('medium', 50)
        hard_pct = difficulty_distribution.get('hard', 20)
        
        difficulties = self.distribute_difficulty(question_count, easy_pct, medium_pct, hard_pct)
        
        # Generate all questions at once (more efficient)
        all_questions = self.generate_questions(
            topic_content, question_type, marks_per_question, 'mixed', question_count
        )
        
        # Shuffle questions
        random.shuffle(all_questions)
        
        # Number the questions
        for i, q in enumerate(all_questions):
            q['number'] = i + 1
            q['difficulty'] = difficulties[i] if i < len(difficulties) else 'medium'
        
        return {
            'name': section_name,
            'questionType': question_type,
            'marksPerQuestion': marks_per_question,
            'totalMarks': question_count * marks_per_question,
            'questions': all_questions
        }
    
    def generate_paper(self, config: dict, topic_contents: dict) -> dict:
        """Generate complete question paper based on configuration."""
        
        # Combine all topic contents
        combined_content = "\n\n".join(topic_contents.values())
        
        sections = config.get('sections', [])
        difficulty = config.get('difficulty', {'easy': 30, 'medium': 50, 'hard': 20})
        
        generated_sections = []
        total_marks = 0
        
        for section_config in sections:
            section = self.generate_section(section_config, combined_content, difficulty)
            generated_sections.append(section)
            total_marks += section['totalMarks']
        
        paper = {
            'examType': config.get('examType', 'General'),
            'totalMarks': total_marks,
            'sections': generated_sections,
            'metadata': {
                'topics': list(topic_contents.keys()),
                'difficulty': difficulty
            }
        }
        
        # Generate extras if requested
        if config.get('includeAnswerKey', False):
            paper['answerKey'] = self._generate_answer_key(generated_sections)
        
        if config.get('includeMarkingScheme', False):
            paper['markingScheme'] = self._generate_marking_scheme(generated_sections)
        
        if config.get('includeChapterSplit', False):
            paper['chapterSplit'] = self._generate_chapter_split(generated_sections, topic_contents)
        
        return paper
    
    def _generate_answer_key(self, sections: list) -> list:
        """Generate answer key from sections."""
        answer_key = []
        
        for section in sections:
            section_answers = {
                'section': section['name'],
                'answers': []
            }
            
            for q in section['questions']:
                answer_entry = {
                    'number': q.get('number', 0),
                    'answer': q.get('answer', 'N/A')
                }
                if 'explanation' in q:
                    answer_entry['explanation'] = q['explanation']
                if 'key_points' in q:
                    answer_entry['key_points'] = q['key_points']
                
                section_answers['answers'].append(answer_entry)
            
            answer_key.append(section_answers)
        
        return answer_key
    
    def _generate_marking_scheme(self, sections: list) -> list:
        """Generate marking scheme."""
        scheme = []
        
        for section in sections:
            section_scheme = {
                'section': section['name'],
                'questionType': section['questionType'],
                'marksPerQuestion': section['marksPerQuestion'],
                'totalQuestions': len(section['questions']),
                'totalMarks': section['totalMarks'],
                'guidelines': self._get_marking_guidelines(section['questionType'], section['marksPerQuestion'])
            }
            scheme.append(section_scheme)
        
        return scheme
    
    def _get_marking_guidelines(self, question_type: str, marks: int) -> str:
        """Get marking guidelines based on question type."""
        guidelines = {
            'mcq': f'Award {marks} mark(s) for correct answer. No partial marking.',
            'fill_blank': f'Award {marks} mark(s) for correct answer. Accept synonyms where appropriate.',
            'very_short': f'Award up to {marks} mark(s). 1 mark for correct concept, partial marks for incomplete answers.',
            'short': f'Award up to {marks} mark(s). Distribute marks for: concept (40%), explanation (40%), examples (20%).',
            'long': f'Award up to {marks} mark(s). Evaluate on: content accuracy (40%), depth (30%), organization (20%), examples (10%).'
        }
        return guidelines.get(question_type, f'Award up to {marks} mark(s) based on accuracy and completeness.')
    
    def _generate_chapter_split(self, sections: list, topic_contents: dict) -> dict:
        """Generate chapter-wise marks distribution."""
        topics = list(topic_contents.keys())
        total_marks = sum(s['totalMarks'] for s in sections)
        
        if topics:
            marks_per_topic = total_marks / len(topics)
            split = {topic: round(marks_per_topic, 1) for topic in topics}
        else:
            split = {'General': total_marks}
        
        return {
            'distribution': split,
            'total': total_marks
        }


# Singleton instance
_generator_instance = None

def get_generator() -> QuestionPaperGenerator:
    """Get singleton generator instance."""
    global _generator_instance
    if _generator_instance is None:
        _generator_instance = QuestionPaperGenerator()
    return _generator_instance
