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
        "key_concepts": [
            ("Physical properties of metals", "Metals are lustrous, malleable, ductile, good conductors of heat and electricity. They are generally hard and have high melting points."),
            ("Physical properties of non-metals", "Non-metals are generally non-lustrous, brittle, poor conductors. They have low melting and boiling points."),
            ("Reactivity series", "Arrangement of metals in decreasing order of reactivity: K > Na > Ca > Mg > Al > Zn > Fe > Pb > H > Cu > Hg > Ag > Au"),
            ("Ionic bonding", "Transfer of electrons from metal to non-metal atoms forming oppositely charged ions that attract each other."),
            ("Extraction of metals", "Methods depend on reactivity: highly reactive - electrolysis, medium - reduction with carbon, least reactive - heating alone."),
            ("Corrosion", "Slow eating away of metals by reaction with oxygen, water, acids, or gases in the environment."),
            ("Alloys", "Homogeneous mixture of two or more metals, or metal with non-metal. Made to improve properties."),
            ("Amphoteric oxides", "Oxides that react with both acids and bases. Examples: Al2O3, ZnO"),
        ],
        "mcq_pool": [
            ("Which metal is stored in kerosene?", ["Iron", "Sodium", "Copper", "Aluminium"], "Sodium", "Sodium reacts vigorously with air and water."),
            ("Most reactive metal is:", ["Gold", "Iron", "Potassium", "Copper"], "Potassium", "K is most reactive in the given options."),
            ("Aqua regia is a mixture of:", ["HCl and HNO3", "H2SO4 and HNO3", "HCl and H2SO4", "HCl and H2O"], "HCl and HNO3", "3:1 ratio of conc. HCl and HNO3."),
            ("An alloy of copper and zinc is:", ["Bronze", "Brass", "Solder", "Steel"], "Brass", "Brass = Cu + Zn"),
            ("Which ore is concentrated by froth floatation?", ["Haematite", "Bauxite", "Sulphide ores", "Oxide ores"], "Sulphide ores", "Sulphide ores are concentrated by froth floatation."),
            ("Which metal is liquid at room temperature?", ["Sodium", "Mercury", "Aluminium", "Iron"], "Mercury", "Mercury (Hg) is the only metal liquid at room temperature."),
            ("The most abundant metal in Earth's crust is:", ["Iron", "Aluminium", "Copper", "Gold"], "Aluminium", "Aluminium makes up about 8% of Earth's crust."),
            ("Which oxide is amphoteric?", ["Na2O", "MgO", "Al2O3", "SO2"], "Al2O3", "Aluminium oxide reacts with both acids and bases."),
            ("Galvanization is coating of iron with:", ["Copper", "Zinc", "Tin", "Chromium"], "Zinc", "Zinc coating protects iron from rusting."),
            ("Which metal can be cut with a knife?", ["Iron", "Copper", "Sodium", "Aluminium"], "Sodium", "Sodium is a soft metal that can be cut with a knife."),
            ("Thermit reaction is used to:", ["Extract aluminium", "Join railway tracks", "Make brass", "Prevent rusting"], "Join railway tracks", "Fe2O3 + 2Al → 2Fe + Al2O3 produces molten iron."),
            ("Which is NOT a property of metals?", ["Sonorous", "Malleable", "Brittle", "Ductile"], "Brittle", "Brittleness is a property of non-metals."),
            ("Stainless steel contains:", ["Fe and C", "Fe, C, Cr, Ni", "Fe and Zn", "Fe and Cu"], "Fe, C, Cr, Ni", "Stainless steel contains iron, carbon, chromium, and nickel."),
            ("Which metal does not react with dilute HCl?", ["Zinc", "Iron", "Copper", "Magnesium"], "Copper", "Copper is below hydrogen in reactivity series."),
            ("Anodizing is done for:", ["Iron", "Copper", "Aluminium", "Zinc"], "Aluminium", "Anodizing forms a thick protective oxide layer on aluminium."),
        ],
        "fill_blanks": [
            ("The process of depositing zinc on iron is called _______.", "galvanization"),
            ("Metals that can be beaten into sheets are called _______.", "malleable"),
            ("Copper is refined by _______ refining.", "electrolytic"),
            ("Bronze is an alloy of copper and _______.", "tin"),
            ("The most reactive metal is _______.", "potassium"),
            ("Metals that can be drawn into wires are called _______.", "ductile"),
            ("_______ is used to cut iron and steel.", "Oxyacetylene torch"),
            ("The ore of aluminium is _______.", "bauxite"),
            ("Gold and platinum are called _______ metals.", "noble"),
            ("Rusting of iron requires _______ and _______.", "oxygen and water"),
            ("The extraction of metals from ores is called _______.", "metallurgy"),
            ("Sodium is stored in _______ to prevent reaction with air.", "kerosene"),
        ],
        "short_answers": [
            ("Why is sodium kept under kerosene?", "Sodium is highly reactive. It reacts vigorously with oxygen and moisture in air, catching fire. Kerosene prevents contact with air."),
            ("What is corrosion? How can it be prevented?", "Corrosion is the gradual destruction of metals by reaction with environment. Prevention: painting, oiling, galvanization, electroplating, making alloys."),
            ("Why is aluminium used for making cooking utensils?", "Aluminium is a good conductor of heat, lightweight, does not corrode easily due to oxide layer, and is relatively cheap."),
            ("What is an alloy? Why are alloys made?", "An alloy is a homogeneous mixture of metals. Alloys are made to: 1) Increase hardness 2) Increase resistance to corrosion 3) Lower melting point 4) Improve appearance."),
            ("Differentiate between metals and non-metals based on conductivity.", "Metals are good conductors of heat and electricity due to free electrons. Non-metals are poor conductors (insulators) except graphite which conducts electricity."),
            ("What is thermit reaction? Give its use.", "Thermit reaction: Fe2O3 + 2Al → 2Fe + Al2O3 + Heat. It produces molten iron at very high temperature. Used for welding railway tracks and joining broken machine parts."),
            ("Why do ionic compounds have high melting points?", "Ionic compounds have strong electrostatic forces between oppositely charged ions. Large amount of energy is needed to overcome these forces, hence high melting points."),
            ("What happens when metals react with water?", "Highly reactive metals (Na, K) react vigorously to produce hydroxide and H2. Moderately reactive metals (Mg, Zn) react slowly. Less reactive metals (Cu, Ag) don't react with water."),
        ],
        "long_answers": [
            ("Explain the reactivity series of metals. How is it useful in extraction of metals?",
             "Reactivity Series:\nThe arrangement of metals in decreasing order of their reactivity is called reactivity series.\n\nOrder: K > Na > Ca > Mg > Al > Zn > Fe > Pb > H > Cu > Hg > Ag > Au\n\nUse in Extraction:\n1. Highly reactive metals (K, Na, Ca, Al):\n   - Cannot be reduced by carbon\n   - Extracted by electrolysis of molten salts\n   - Example: Al from Al2O3 by electrolysis\n\n2. Moderately reactive metals (Zn, Fe, Pb):\n   - Reduced by heating with carbon or CO\n   - Example: ZnO + C → Zn + CO\n\n3. Less reactive metals (Cu, Hg, Ag):\n   - Extracted by heating their oxides alone\n   - Example: 2HgO → 2Hg + O2\n\n4. Least reactive metals (Au, Pt):\n   - Found in free state in nature\n   - No extraction needed"),
            ("Describe the process of extracting a metal from its ore. Take the example of zinc.",
             "Extraction of Zinc:\n\n1. Concentration of Ore:\n   - Zinc ore (ZnS - zinc blende) is concentrated by froth floatation\n   - Oil + water mixture separates ore from gangue\n\n2. Roasting:\n   - Concentrated ore is heated in excess air\n   - 2ZnS + 3O2 → 2ZnO + 2SO2\n   - Converts sulphide to oxide\n\n3. Reduction:\n   - Zinc oxide is reduced with carbon (coke)\n   - ZnO + C → Zn + CO\n   - Carried out at high temperature in blast furnace\n\n4. Refining:\n   - Impure zinc is purified by electrolytic refining\n   - Impure zinc = anode, pure zinc = cathode\n   - Electrolyte = zinc sulphate solution\n   - Pure zinc deposits on cathode"),
            ("What is corrosion? Explain the conditions necessary for rusting. How can rusting be prevented?",
             "Corrosion:\nThe slow deterioration of metals due to chemical reaction with environment (oxygen, water, acids, gases) is called corrosion.\n\nConditions for Rusting:\n1. Presence of oxygen (air)\n2. Presence of water (moisture)\n3. Presence of impurities (speeds up rusting)\n\nChemical equation:\n4Fe + 3O2 + 2xH2O → 2Fe2O3.xH2O (rust)\n\nPrevention of Rusting:\n\n1. Painting/Oiling/Greasing:\n   - Creates barrier between iron and air/moisture\n\n2. Galvanization:\n   - Coating iron with zinc layer\n   - Zinc protects even if coating is broken\n\n3. Electroplating:\n   - Coating with chromium, nickel, or tin\n\n4. Alloying:\n   - Making stainless steel (Fe + Cr + Ni)\n   - Chromium oxide forms protective layer\n\n5. Sacrificial protection:\n   - Attaching more reactive metal (zinc/magnesium) to iron"),
        ]
    },
    
    "Carbon and its Compounds": {
        "key_concepts": [
            ("Covalent bonding", "Sharing of electrons between atoms to achieve stable configuration. Carbon forms 4 covalent bonds."),
            ("Allotropes of carbon", "Different physical forms of same element. Diamond, graphite, fullerene are allotropes of carbon."),
            ("Saturated hydrocarbons", "Compounds with only single bonds between carbon atoms. Called alkanes. General formula: CnH2n+2"),
            ("Unsaturated hydrocarbons", "Compounds with double or triple bonds. Alkenes (C=C) and Alkynes (C≡C)."),
            ("Homologous series", "Series of compounds with same functional group, differing by -CH2- unit with similar chemical properties."),
            ("Functional groups", "Atoms or groups that determine the properties of organic compounds. Examples: -OH, -CHO, -COOH, -CO-"),
            ("Isomerism", "Same molecular formula but different structural arrangements giving different properties."),
            ("Combustion", "Burning of carbon compounds in oxygen to produce CO2, H2O, heat and light."),
        ],
        "mcq_pool": [
            ("Carbon exists as:", ["Diamond only", "Graphite only", "Both diamond and graphite", "None"], "Both diamond and graphite", "These are allotropes of carbon."),
            ("Ethanol is denatured by adding:", ["Methanol", "Propanol", "Butanol", "Pentanol"], "Methanol", "Methanol is added to make industrial alcohol unfit for drinking."),
            ("Functional group in alcohols is:", ["-OH", "-CHO", "-COOH", "-CO-"], "-OH", "Alcohols contain hydroxyl group."),
            ("IUPAC name of CH3-CH2-OH is:", ["Methanol", "Ethanol", "Propanol", "Butanol"], "Ethanol", "2 carbons with -OH group."),
            ("Ethanoic acid is commonly known as:", ["Formic acid", "Acetic acid", "Citric acid", "Tartaric acid"], "Acetic acid", "CH3COOH is vinegar/acetic acid."),
            ("Number of covalent bonds carbon can form:", ["1", "2", "3", "4"], "4", "Carbon has 4 valence electrons, forms 4 covalent bonds."),
            ("Which is a saturated hydrocarbon?", ["Ethene", "Ethyne", "Ethane", "Benzene"], "Ethane", "Ethane (C2H6) has only single bonds."),
            ("Soap molecule has:", ["Only hydrophilic end", "Only hydrophobic end", "Both hydrophilic and hydrophobic ends", "Neither"], "Both hydrophilic and hydrophobic ends", "Soap has ionic (hydrophilic) head and hydrocarbon (hydrophobic) tail."),
            ("Vinegar contains about:", ["5-8% acetic acid", "20% acetic acid", "50% acetic acid", "Pure acetic acid"], "5-8% acetic acid", "Vinegar is dilute acetic acid solution."),
            ("General formula of alkynes is:", ["CnH2n+2", "CnH2n", "CnH2n-2", "CnHn"], "CnH2n-2", "Alkynes have triple bond, formula CnH2n-2."),
            ("Buckminsterfullerene has:", ["60 carbon atoms", "12 carbon atoms", "72 carbon atoms", "100 carbon atoms"], "60 carbon atoms", "C60 is shaped like a football."),
            ("Addition of hydrogen is called:", ["Oxidation", "Hydrogenation", "Hydration", "Dehydration"], "Hydrogenation", "Hydrogenation adds H2 to unsaturated compounds."),
            ("Which compound shows substitution reaction?", ["Ethene", "Ethane", "Ethyne", "Benzene"], "Ethane", "Saturated compounds show substitution reactions."),
            ("Esterification is reaction between:", ["Acid and base", "Alcohol and acid", "Alcohol and alcohol", "Acid and acid"], "Alcohol and acid", "Alcohol + Carboxylic acid → Ester + Water"),
            ("Diamond is hard because:", ["It has ionic bonds", "C atoms in 3D network", "It has metallic bonds", "Weak forces between atoms"], "C atoms in 3D network", "Each carbon is bonded to 4 others in rigid 3D structure."),
        ],
        "fill_blanks": [
            ("The IUPAC name of CH4 is _______.", "methane"),
            ("Functional group -CHO is called _______.", "aldehyde"),
            ("Hardening of oils is called _______.", "hydrogenation"),
            ("The general formula of alkenes is _______.", "CnH2n"),
            ("Carbon forms _______ covalent bonds.", "4/four"),
            ("Compounds with same molecular formula but different structures are called _______.", "isomers"),
            ("The reaction of alcohol with carboxylic acid is called _______.", "esterification"),
            ("Graphite is used in pencils because it is _______ and _______.", "soft and slippery"),
            ("Soaps are _______ of fatty acids.", "sodium/potassium salts"),
            ("The process of converting vegetable oils to ghee is _______.", "hydrogenation"),
            ("Ethanol is produced by _______ of sugars.", "fermentation"),
            ("5-8% solution of acetic acid in water is called _______.", "vinegar"),
        ],
        "short_answers": [
            ("What are hydrocarbons?", "Hydrocarbons are compounds containing only carbon and hydrogen. Examples: CH4 (methane), C2H6 (ethane), C2H4 (ethene)."),
            ("What is a homologous series?", "A series of compounds with same functional group and similar properties, differing by -CH2- unit. Example: Methane, Ethane, Propane... They have same general formula."),
            ("Why does carbon form compounds mainly by covalent bonding?", "Carbon has 4 valence electrons. It cannot gain 4 or lose 4 electrons easily. So it shares electrons to complete its octet, forming covalent bonds."),
            ("Differentiate between saturated and unsaturated hydrocarbons.", "Saturated: Only single C-C bonds, formula CnH2n+2 (alkanes). Unsaturated: Have double (alkenes, CnH2n) or triple bonds (alkynes, CnH2n-2)."),
            ("What is the difference between soaps and detergents?", "Soaps are sodium/potassium salts of fatty acids. Detergents are ammonium/sulphonate salts. Detergents work in hard water but soaps form scum."),
            ("What happens when ethanol reacts with sodium?", "2C2H5OH + 2Na → 2C2H5ONa + H2. Sodium ethoxide is formed and hydrogen gas is evolved."),
            ("Why is graphite a good conductor but diamond is not?", "In graphite, each carbon is bonded to 3 others, leaving one free electron for conduction. In diamond, all 4 electrons are bonded, no free electrons."),
            ("What are micelles? How do soaps clean clothes?", "Micelles are clusters of soap molecules with hydrophobic tails inside and hydrophilic heads outside. The tails attract grease, heads dissolve in water, removing dirt."),
        ],
        "long_answers": [
            ("Explain the bonding in carbon compounds. Why can carbon form a large number of compounds?",
             "Bonding in Carbon:\n\n1. Covalent Bonding:\n   - Carbon has 4 valence electrons\n   - Cannot gain or lose 4 electrons easily\n   - Shares electrons to form covalent bonds\n   - Forms 4 covalent bonds\n\n2. Reasons for Large Number of Compounds:\n\n   a) Tetravalency:\n      - Carbon can form 4 bonds with other atoms\n      - Can bond with C, H, O, N, S, halogens\n\n   b) Catenation:\n      - Carbon atoms can bond with each other\n      - Forms long chains, branched chains, rings\n      - C-C bond is very strong\n\n   c) Multiple Bonding:\n      - Forms single, double, and triple bonds\n      - Gives alkanes, alkenes, alkynes\n\n   d) Isomerism:\n      - Same formula, different arrangements\n      - Increases variety of compounds\n\nExamples:\n- Straight chain: CH3-CH2-CH2-CH3 (butane)\n- Branched: CH3-CH(CH3)-CH3 (isobutane)\n- Ring: Cyclopropane, Benzene"),
            ("What are soaps and detergents? Explain the cleansing action of soap.",
             "Soaps:\n- Sodium or potassium salts of long-chain fatty acids\n- Made by saponification: Fat/Oil + NaOH → Soap + Glycerol\n- Example: C17H35COONa (sodium stearate)\n\nDetergents:\n- Sodium salts of long-chain sulphonic acids\n- Made from petroleum products\n- Work in hard water\n\nCleansing Action of Soap:\n\n1. Structure of Soap Molecule:\n   - Hydrophilic head (ionic, -COONa) - dissolves in water\n   - Hydrophobic tail (hydrocarbon chain) - dissolves in grease\n\n2. Micelle Formation:\n   - Soap molecules arrange around dirt/grease\n   - Hydrophobic tails attach to grease\n   - Hydrophilic heads face outward into water\n   - Forms spherical structure called micelle\n\n3. Cleaning Process:\n   - Grease gets trapped inside micelle\n   - Micelles dissolve in water\n   - Agitation (rubbing) helps lift dirt\n   - Rinsing removes micelles with dirt\n\nNote: Soaps don't work well in hard water because Ca²⁺ and Mg²⁺ form insoluble scum."),
            ("Describe the properties and uses of ethanol and ethanoic acid.",
             "ETHANOL (C2H5OH):\n\nProperties:\n1. Colorless liquid with pleasant smell\n2. Boiling point: 78°C\n3. Miscible with water in all proportions\n4. Burns with blue flame\n\nChemical Reactions:\n1. With sodium: 2C2H5OH + 2Na → 2C2H5ONa + H2\n2. Dehydration: C2H5OH → C2H4 + H2O (conc. H2SO4, heat)\n3. Oxidation: C2H5OH → CH3CHO → CH3COOH\n\nUses:\n- Alcoholic beverages\n- As solvent in medicines, perfumes\n- As fuel (mixed with petrol - gasohol)\n- In thermometers\n\nETHANOIC ACID (CH3COOH):\n\nProperties:\n1. Colorless liquid, pungent smell\n2. Freezes at 16.6°C (glacial acetic acid)\n3. Sour taste (found in vinegar 5-8%)\n\nChemical Reactions:\n1. With base: CH3COOH + NaOH → CH3COONa + H2O\n2. With carbonate: 2CH3COOH + Na2CO3 → 2CH3COONa + H2O + CO2\n3. Esterification: CH3COOH + C2H5OH → CH3COOC2H5 + H2O\n\nUses:\n- In food as vinegar\n- Preservative\n- Making esters for perfumes\n- Manufacture of rayon"),
        ]
    },
    
    "Control and Coordination": {
        "key_concepts": [
            ("Nervous system", "System that controls and coordinates body activities. Consists of brain, spinal cord, and nerves."),
            ("Neuron", "Basic unit of nervous system. Has cell body, dendrites (receive signals), and axon (transmit signals)."),
            ("Synapse", "Junction between two neurons where signals are transmitted chemically."),
            ("Reflex action", "Automatic, rapid, involuntary response to stimulus. Path: receptor → sensory neuron → spinal cord → motor neuron → effector."),
            ("Human brain", "Control center with forebrain (thinking), midbrain (vision, hearing), hindbrain (balance, vital functions)."),
            ("Hormones", "Chemical messengers secreted by endocrine glands. Travel through blood to target organs."),
            ("Plant hormones", "Auxin (growth, phototropism), Gibberellin (stem elongation), Cytokinin (cell division), Abscisic acid (inhibits growth), Ethylene (fruit ripening)."),
            ("Feedback mechanism", "Regulation of hormone levels. High levels inhibit further secretion, low levels stimulate secretion."),
        ],
        "mcq_pool": [
            ("The brain is protected by:", ["Skull", "Vertebral column", "Ribs", "Sternum"], "Skull", "Cranium protects the brain."),
            ("Which hormone regulates blood sugar?", ["Thyroxine", "Insulin", "Adrenaline", "Growth hormone"], "Insulin", "Insulin lowers blood glucose level."),
            ("Plant hormone that promotes cell division is:", ["Auxin", "Gibberellin", "Cytokinin", "Ethylene"], "Cytokinin", "Cytokinin promotes cell division."),
            ("Iodine deficiency causes:", ["Diabetes", "Goitre", "Dwarfism", "Gigantism"], "Goitre", "Iodine is needed for thyroxine production."),
            ("Which part of brain controls balance?", ["Cerebrum", "Cerebellum", "Medulla", "Pons"], "Cerebellum", "Cerebellum coordinates voluntary movements and balance."),
            ("Reflex action is controlled by:", ["Brain", "Spinal cord", "Muscles", "Heart"], "Spinal cord", "Reflex arcs pass through spinal cord for quick response."),
            ("Which hormone is called emergency hormone?", ["Insulin", "Thyroxine", "Adrenaline", "Growth hormone"], "Adrenaline", "Adrenaline prepares body for fight or flight response."),
            ("Phototropism in plants is due to:", ["Gibberellin", "Auxin", "Cytokinin", "Ethylene"], "Auxin", "Auxin causes bending towards light."),
            ("The longest cell in human body is:", ["Muscle cell", "Nerve cell", "Blood cell", "Bone cell"], "Nerve cell", "Neurons can be over a meter long."),
            ("Which gland is called master gland?", ["Thyroid", "Pituitary", "Adrenal", "Pancreas"], "Pituitary", "Pituitary controls other endocrine glands."),
            ("Diabetes is caused by deficiency of:", ["Thyroxine", "Adrenaline", "Insulin", "Growth hormone"], "Insulin", "Insulin regulates blood sugar levels."),
            ("Tropic movements in plants are:", ["Independent of stimulus", "Dependent on stimulus direction", "Random movements", "Very fast"], "Dependent on stimulus direction", "Tropic movements are directional responses to stimuli."),
            ("Which part of brain controls memory?", ["Cerebrum", "Cerebellum", "Medulla", "Hypothalamus"], "Cerebrum", "Cerebrum is the thinking part of brain."),
            ("Dwarfism is caused by deficiency of:", ["Thyroxine", "Insulin", "Growth hormone", "Adrenaline"], "Growth hormone", "Growth hormone from pituitary controls body growth."),
            ("Chemical transmission at synapse is by:", ["Ions", "Hormones", "Neurotransmitters", "Blood"], "Neurotransmitters", "Neurotransmitters carry signals across synapse."),
        ],
        "fill_blanks": [
            ("The gap between two neurons is called _______.", "synapse"),
            ("Insulin is secreted by _______.", "pancreas"),
            ("Adrenaline is also called _______ hormone.", "fight or flight"),
            ("Auxin is produced at the _______ of the plant.", "tip/apex"),
            ("The _______ controls involuntary actions like breathing.", "medulla"),
            ("Plant roots show positive _______ tropism.", "geo/gravi"),
            ("Thyroxine hormone contains _______.", "iodine"),
            ("The three main parts of brain are forebrain, midbrain, and _______.", "hindbrain"),
            ("_______ movement in Mimosa pudica is not a tropic movement.", "Thigmonastic/Touch"),
            ("The functional unit of nervous system is _______.", "neuron"),
            ("Gibberellins help in _______ elongation.", "stem"),
            ("Testosterone is the male _______ hormone.", "sex"),
        ],
        "short_answers": [
            ("What is reflex action?", "A reflex action is an automatic, rapid, and involuntary response to a stimulus. Example: pulling hand away from hot object. It is controlled by spinal cord."),
            ("Name the parts of human brain.", "Human brain has three main parts: 1) Fore-brain (cerebrum) - thinking, memory 2) Mid-brain - vision, hearing 3) Hind-brain (cerebellum, pons, medulla) - balance, vital functions."),
            ("What is the difference between nervous and hormonal control?", "Nervous control: Fast, through nerves, electrical impulses, short-lived effect. Hormonal control: Slow, through blood, chemical signals, long-lasting effect."),
            ("What are plant hormones? Name any four.", "Plant hormones are chemical substances that control plant growth and development. Examples: 1) Auxin - growth 2) Gibberellin - stem elongation 3) Cytokinin - cell division 4) Ethylene - fruit ripening."),
            ("How does chemical transmission take place at synapse?", "When impulse reaches axon end, neurotransmitters are released. They cross the synaptic cleft and bind to receptors on next neuron, generating new impulse."),
            ("What is feedback mechanism?", "Feedback mechanism regulates hormone levels. When hormone level is high, it inhibits further secretion. When low, it stimulates secretion. Example: Insulin-glucose regulation."),
            ("Differentiate between cerebrum and cerebellum.", "Cerebrum: Largest part, controls thinking, memory, voluntary actions, senses. Cerebellum: Controls balance, posture, coordination of voluntary movements."),
            ("What is the role of thyroid gland?", "Thyroid gland secretes thyroxine which controls metabolism, growth, and development. Deficiency causes goitre, cretinism, and myxoedema."),
        ],
        "long_answers": [
            ("Draw a well-labeled diagram of a neuron and describe its structure and function.",
             "Structure of Neuron:\n\n1. Cell Body (Cyton):\n   - Contains nucleus and cytoplasm\n   - Site of metabolic activities\n\n2. Dendrites:\n   - Short, branched projections\n   - Receive signals from other neurons\n   - Multiple dendrites per neuron\n\n3. Axon:\n   - Long, single fiber\n   - Transmits signals away from cell body\n   - Covered by myelin sheath (insulation)\n   - Ends in axon terminals\n\n4. Synapse:\n   - Junction between neurons\n   - Chemical transmission via neurotransmitters\n\nFunction:\n1. Sensory neurons: Carry signals from receptors to CNS\n2. Motor neurons: Carry signals from CNS to muscles/glands\n3. Relay neurons: Connect sensory and motor neurons in CNS\n\nSignal Transmission:\n- Electrical impulses travel along neuron\n- At synapse, chemical neurotransmitters carry signal\n- Impulse is regenerated in next neuron"),
            ("Describe the human brain and its functions.",
             "Human Brain:\n\nWeight: About 1.4 kg\nProtection: Skull and cerebrospinal fluid\n\nMain Parts:\n\n1. FOREBRAIN:\n   a) Cerebrum:\n      - Largest part (80% of brain)\n      - Two hemispheres connected by corpus callosum\n      - Functions: Thinking, memory, intelligence, voluntary actions\n      - Sensory areas receive and process information\n      - Motor areas control voluntary movements\n\n   b) Thalamus:\n      - Relay center for sensory information\n\n   c) Hypothalamus:\n      - Controls hunger, thirst, body temperature\n      - Links nervous and endocrine systems\n\n2. MIDBRAIN:\n   - Controls visual and auditory reflexes\n   - Connects forebrain and hindbrain\n\n3. HINDBRAIN:\n   a) Cerebellum:\n      - Controls balance and coordination\n      - Fine-tunes voluntary movements\n\n   b) Pons:\n      - Relay center, regulates breathing\n\n   c) Medulla Oblongata:\n      - Controls vital functions: breathing, heartbeat, blood pressure\n      - Controls reflexes like coughing, sneezing"),
            ("Explain the mechanism of hormone action with examples.",
             "Mechanism of Hormone Action:\n\n1. Secretion:\n   - Hormones are secreted by endocrine glands\n   - Released directly into blood\n\n2. Transport:\n   - Carried by blood to all parts of body\n\n3. Target Organ:\n   - Only specific organs with receptors respond\n   - Hormone binds to receptor on target cell\n\n4. Response:\n   - Triggers specific cellular response\n\nExamples:\n\n1. INSULIN:\n   - Secreted by: Pancreas (β cells)\n   - Target: Liver, muscles, fat cells\n   - Action: Lowers blood glucose by promoting glucose uptake\n   - Deficiency: Diabetes mellitus\n\n2. ADRENALINE:\n   - Secreted by: Adrenal glands\n   - Target: Heart, muscles, blood vessels\n   - Action: Increases heart rate, blood pressure, glucose release\n   - Called 'fight or flight' hormone\n\n3. THYROXINE:\n   - Secreted by: Thyroid gland\n   - Target: All cells\n   - Action: Controls metabolic rate\n   - Deficiency: Goitre, cretinism\n\nFeedback Mechanism:\n- High hormone level → inhibits secretion\n- Low hormone level → stimulates secretion"),
        ]
    },
    
    "How do Organisms Reproduce": {
        "key_concepts": [
            ("Reproduction", "Process by which organisms produce offspring to continue their species. Essential for species survival."),
            ("Asexual reproduction", "Single parent produces offspring identical to itself. No fusion of gametes. Examples: fission, budding, fragmentation."),
            ("Sexual reproduction", "Two parents contribute genetic material. Fusion of gametes produces variation in offspring."),
            ("Binary fission", "Parent cell divides into two equal daughter cells. Seen in Amoeba, bacteria."),
            ("Budding", "New organism grows as outgrowth from parent. Seen in Hydra, yeast."),
            ("Vegetative propagation", "New plants from vegetative parts like stem, root, leaf. Examples: potato (tuber), rose (cutting)."),
            ("Pollination", "Transfer of pollen from anther to stigma. Self-pollination or cross-pollination."),
            ("Fertilization", "Fusion of male and female gametes to form zygote. In humans, occurs in fallopian tube."),
        ],
        "mcq_pool": [
            ("Vegetative propagation in potato is by:", ["Stem", "Root", "Leaf", "Seed"], "Stem", "Potato tuber is a modified stem."),
            ("Male reproductive part of flower is:", ["Pistil", "Stamen", "Sepal", "Petal"], "Stamen", "Stamen produces pollen grains."),
            ("Fertilization in humans occurs in:", ["Uterus", "Ovary", "Fallopian tube", "Vagina"], "Fallopian tube", "Fusion of sperm and egg occurs in oviduct."),
            ("Unisexual flower is:", ["Rose", "Papaya", "Hibiscus", "Mustard"], "Papaya", "Papaya has separate male and female flowers."),
            ("DNA copying is essential for reproduction because:", ["It provides energy", "It creates variation", "It ensures inheritance of traits", "It produces food"], "It ensures inheritance of traits", "DNA carries genetic information to offspring."),
            ("Regeneration is seen in:", ["Amoeba", "Planaria", "Paramecium", "Yeast"], "Planaria", "Planaria can regenerate from small fragments."),
            ("The part of flower that develops into fruit is:", ["Ovary", "Ovule", "Stigma", "Style"], "Ovary", "Ovary becomes fruit after fertilization."),
            ("In human females, fertilized egg develops in:", ["Fallopian tube", "Uterus", "Ovary", "Vagina"], "Uterus", "Embryo implants and develops in uterus."),
            ("Pollen grains are produced in:", ["Anther", "Ovary", "Stigma", "Filament"], "Anther", "Anther is part of stamen that produces pollen."),
            ("Spore formation is seen in:", ["Rhizopus", "Hydra", "Amoeba", "Leishmania"], "Rhizopus", "Fungi like Rhizopus reproduce by spores."),
            ("Number of chromosomes in human sperm is:", ["46", "23", "44", "22"], "23", "Gametes have half the chromosome number (haploid)."),
            ("Contraceptive method that acts as barrier:", ["Copper-T", "Condom", "Oral pills", "Loop"], "Condom", "Condoms prevent sperm from reaching egg."),
            ("Menstrual cycle in females is:", ["21 days", "28 days", "35 days", "14 days"], "28 days", "Average menstrual cycle is 28 days."),
            ("Placenta connects:", ["Mother and fetus", "Ovary and uterus", "Uterus and vagina", "Egg and sperm"], "Mother and fetus", "Placenta provides nutrients and oxygen to fetus."),
            ("Test tube baby technique is:", ["IVF", "Cloning", "Hybridization", "Tissue culture"], "IVF", "In Vitro Fertilization - fertilization outside body."),
        ],
        "fill_blanks": [
            ("The male gamete in humans is called _______.", "sperm"),
            ("Budding is seen in _______.", "yeast/Hydra"),
            ("Binary fission is seen in _______.", "Amoeba"),
            ("Seeds develop from _______.", "ovules"),
            ("The process of fusion of male and female gametes is called _______.", "fertilization"),
            ("In flowers, pollen grains are produced by _______.", "anther"),
            ("The female reproductive organ of a flower is _______.", "pistil/carpel"),
            ("Zygote divides repeatedly to form an _______.", "embryo"),
            ("A _______ carries the developing embryo in humans.", "uterus"),
            ("Removal of unwanted pregnancy is called _______.", "abortion"),
            ("The period of development of embryo in uterus is called _______.", "gestation"),
            ("Organisms produced by asexual reproduction are called _______.", "clones"),
        ],
        "short_answers": [
            ("What is the advantage of sexual reproduction?", "Sexual reproduction creates variation by combining genes from two parents. This variation helps species adapt to changing environment and evolve over time."),
            ("What is pollination?", "Pollination is the transfer of pollen grains from anther to stigma of a flower. Self-pollination: within same flower. Cross-pollination: between different flowers by wind, insects, water."),
            ("Why is DNA copying essential for reproduction?", "DNA copying ensures that genetic information is passed from parent to offspring. It maintains species characteristics and also creates slight variations that help in evolution."),
            ("Differentiate between binary fission and budding.", "Binary fission: Parent divides into two equal parts (Amoeba). Budding: A small outgrowth develops and separates from parent (Hydra). Both are asexual reproduction."),
            ("What is the role of placenta?", "Placenta connects fetus to uterine wall. It provides nutrition and oxygen to fetus from mother's blood, removes waste, and produces hormones for pregnancy."),
            ("Why is vegetative propagation practiced for growing some plants?", "To grow plants that have lost ability to produce seeds, to preserve desirable characters, faster than growing from seeds, and to get genetically identical plants."),
            ("What changes occur in girls during puberty?", "Development of breasts, widening of hips, growth of pubic hair, start of menstruation, increase in height, and development of reproductive organs."),
            ("What are STDs? Name any two.", "Sexually Transmitted Diseases are infections spread through sexual contact. Examples: AIDS (HIV), Gonorrhoea, Syphilis, Herpes. Prevention: Use of condoms, single partner."),
        ],
        "long_answers": [
            ("Describe the male reproductive system in humans.",
             "Male Reproductive System:\n\n1. TESTES (pair):\n   - Located in scrotum (outside body for lower temperature)\n   - Produce sperm (spermatogenesis)\n   - Produce testosterone (male hormone)\n\n2. EPIDIDYMIS:\n   - Coiled tube on top of testis\n   - Stores and matures sperm\n\n3. VAS DEFERENS:\n   - Long tube carrying sperm from epididymis\n   - Joins with urethra\n\n4. ACCESSORY GLANDS:\n   a) Seminal vesicles - produce seminal fluid\n   b) Prostate gland - produces alkaline fluid\n   c) Cowper's gland - produces lubricating fluid\n   - Together form semen (sperm + fluids)\n\n5. URETHRA:\n   - Common passage for urine and semen\n   - Runs through penis\n\n6. PENIS:\n   - Copulatory organ\n   - Deposits sperm in female vagina\n\nFunction:\n- Production of sperm and testosterone\n- Transfer of sperm to female body"),
            ("Describe the female reproductive system in humans.",
             "Female Reproductive System:\n\n1. OVARIES (pair):\n   - Located in lower abdomen\n   - Produce eggs (ova) - one per month\n   - Produce hormones: estrogen, progesterone\n\n2. FALLOPIAN TUBES (Oviducts):\n   - Funnel-shaped openings near ovaries\n   - Capture released egg\n   - Site of fertilization\n   - Transport egg/embryo to uterus\n\n3. UTERUS (Womb):\n   - Pear-shaped muscular organ\n   - Thick inner lining (endometrium)\n   - Implantation of embryo occurs here\n   - Develops and nurtures fetus\n\n4. CERVIX:\n   - Narrow opening of uterus\n   - Connects to vagina\n\n5. VAGINA:\n   - Birth canal\n   - Receives penis during intercourse\n   - Passage for menstrual flow\n\nMenstrual Cycle (28 days):\n- Days 1-5: Menstruation (uterus lining sheds)\n- Days 6-13: Uterus lining rebuilds\n- Day 14: Ovulation (egg release)\n- Days 15-28: If no fertilization, lining prepares to shed"),
            ("Explain sexual reproduction in flowering plants.",
             "Sexual Reproduction in Flowering Plants:\n\n1. FLOWER STRUCTURE:\n   - Sepals: Protect flower bud\n   - Petals: Attract pollinators\n   - Stamens (male): Anther + Filament\n   - Pistil (female): Stigma + Style + Ovary\n\n2. POLLINATION:\n   - Transfer of pollen from anther to stigma\n   - Self-pollination: Same flower\n   - Cross-pollination: Different flowers\n   - By wind, water, insects, birds\n\n3. FERTILIZATION:\n   - Pollen grain on stigma → grows pollen tube\n   - Pollen tube travels through style to ovary\n   - Male gametes travel through tube\n   - One fuses with egg → zygote (embryo)\n   - One fuses with polar nuclei → endosperm\n   - This is double fertilization\n\n4. POST-FERTILIZATION:\n   - Ovule → Seed (contains embryo + food)\n   - Ovary → Fruit\n   - Sepals, petals, stamens wither\n\n5. SEED GERMINATION:\n   - Seed absorbs water\n   - Embryo grows\n   - Root emerges first (radicle)\n   - Then shoot (plumule)\n   - Develops into new plant"),
        ]
    },
    
    "Heredity": {
        "key_concepts": [
            ("Heredity", "Transmission of characters from parents to offspring through genes."),
            ("Variation", "Differences among individuals of same species. Caused by sexual reproduction and mutations."),
            ("Genes", "Units of heredity located on chromosomes. Segments of DNA that code for proteins."),
            ("Chromosomes", "Thread-like structures in nucleus containing DNA. Humans have 46 chromosomes (23 pairs)."),
            ("Dominant and Recessive", "Dominant trait expressed even with one copy (TT or Tt). Recessive needs two copies (tt)."),
            ("Mendel's Laws", "Law of segregation (alleles separate during gamete formation) and Law of independent assortment."),
            ("Sex determination", "In humans, XX = female, XY = male. Father's gamete determines sex of child."),
            ("Evolution", "Gradual change in organisms over generations due to natural selection acting on variations."),
        ],
        "mcq_pool": [
            ("Father of genetics is:", ["Darwin", "Mendel", "Lamarck", "Watson"], "Mendel", "Gregor Mendel discovered laws of inheritance."),
            ("DNA is present in:", ["Nucleus", "Cytoplasm", "Cell membrane", "Vacuole"], "Nucleus", "DNA is found in chromosomes in nucleus."),
            ("Genes are made of:", ["Proteins", "DNA", "Lipids", "Carbohydrates"], "DNA", "Genes are segments of DNA."),
            ("Number of chromosomes in human body cells is:", ["23", "46", "44", "22"], "46", "23 pairs = 46 chromosomes."),
            ("A cross between TT and tt gives:", ["All TT", "All tt", "All Tt", "TT and tt"], "All Tt", "F1 generation is all heterozygous."),
            ("Phenotypic ratio in F2 of monohybrid cross is:", ["1:2:1", "3:1", "9:3:3:1", "1:1"], "3:1", "3 dominant : 1 recessive in F2."),
            ("Sex chromosomes in human female are:", ["XY", "XX", "YY", "XO"], "XX", "Females have two X chromosomes."),
            ("Which is NOT true about acquired traits?", ["Develop during lifetime", "Not inherited", "Passed to offspring", "Due to environment"], "Passed to offspring", "Acquired traits are not inherited."),
            ("What is the probability of a boy child?", ["25%", "50%", "75%", "100%"], "50%", "Equal chance of X or Y sperm fertilizing."),
            ("Speciation occurs due to:", ["Genetic drift only", "Natural selection only", "Isolation and variation", "Cloning"], "Isolation and variation", "Geographic isolation leads to speciation."),
            ("Genotype of a heterozygous tall plant is:", ["TT", "Tt", "tt", "T"], "Tt", "Heterozygous has two different alleles."),
            ("Evolution is due to:", ["Mutation only", "Variation and natural selection", "Reproduction", "Growth"], "Variation and natural selection", "Natural selection acts on variations."),
            ("Analogous organs indicate:", ["Common ancestry", "Convergent evolution", "Divergent evolution", "No relation"], "Convergent evolution", "Similar function, different origin."),
            ("Homologous organs indicate:", ["Common ancestry", "Similar function", "Convergent evolution", "No relation"], "Common ancestry", "Same origin, different functions."),
            ("Fossils provide evidence for:", ["Mendel's laws", "Evolution", "Genetics", "Reproduction"], "Evolution", "Fossils show how organisms changed over time."),
        ],
        "fill_blanks": [
            ("The study of heredity is called _______.", "genetics"),
            ("In humans, sex is determined by _______ chromosomes.", "X and Y"),
            ("Dominant trait is expressed in _______ form.", "heterozygous"),
            ("Mendel worked on _______ plant.", "pea"),
            ("The physical appearance of an organism is called its _______.", "phenotype"),
            ("The genetic makeup of an organism is called its _______.", "genotype"),
            ("Mendel's F2 ratio for monohybrid cross is _______.", "3:1"),
            ("Chromosomes are made of _______ and proteins.", "DNA"),
            ("Variations are necessary for _______.", "evolution"),
            ("Organs with same origin but different functions are called _______.", "homologous"),
            ("The theory of natural selection was proposed by _______.", "Darwin"),
            ("Human beings have _______ pairs of autosomes.", "22"),
        ],
        "short_answers": [
            ("What are genes?", "Genes are units of heredity. They are segments of DNA located on chromosomes that contain information for making proteins and controlling traits."),
            ("How is sex determined in humans?", "Sex is determined by sex chromosomes. Females have XX, males have XY. Father's sperm carries either X or Y, determining child's sex."),
            ("What is the difference between phenotype and genotype?", "Genotype: Genetic makeup of organism (e.g., TT, Tt, tt). Phenotype: Physical appearance or expression of genes (e.g., tall, dwarf)."),
            ("Why do we see variations in offspring?", "Variations occur due to: 1) Sexual reproduction (mixing of genes from two parents) 2) Crossing over during meiosis 3) Random fertilization 4) Mutations."),
            ("What are homologous organs?", "Organs with same basic structure and origin but different functions. Examples: forelimbs of human, whale, bat. They indicate common ancestry."),
            ("What are analogous organs?", "Organs with similar function but different origin. Examples: wings of bird and insect. They indicate convergent evolution, not common ancestry."),
            ("State Mendel's law of segregation.", "During gamete formation, the two alleles of a gene separate (segregate) so that each gamete receives only one allele. Alleles reunite in offspring randomly."),
            ("Why are traits acquired during lifetime not inherited?", "Acquired traits affect body cells (somatic), not reproductive cells (germ cells). Only changes in germ cells can be passed to offspring."),
        ],
        "long_answers": [
            ("Explain Mendel's monohybrid cross with an example. What was his conclusion?",
             "Mendel's Monohybrid Cross:\n\n1. Cross: Pure tall (TT) × Pure dwarf (tt) pea plants\n\n2. F1 Generation:\n   - All plants were tall (Tt)\n   - Phenotype: All tall\n   - Genotype: All heterozygous (Tt)\n\n3. F2 Generation (F1 × F1):\n   Cross: Tt × Tt\n   \n   Punnett Square:\n        T       t\n   T    TT      Tt\n   t    Tt      tt\n   \n   Genotypic ratio: 1 TT : 2 Tt : 1 tt\n   Phenotypic ratio: 3 Tall : 1 Dwarf (3:1)\n\n4. Conclusions:\n   - Traits are controlled by factors (genes)\n   - Each trait has two alleles\n   - One allele is dominant (T), one recessive (t)\n   - Alleles separate during gamete formation\n   - Recessive trait reappears in F2"),
            ("How is sex determined in human beings? Explain with a diagram.",
             "Sex Determination in Humans:\n\n1. Chromosomes:\n   - Humans have 46 chromosomes (23 pairs)\n   - 22 pairs are autosomes\n   - 1 pair are sex chromosomes\n\n2. Sex Chromosomes:\n   - Female: XX (homogametic)\n   - Male: XY (heterogametic)\n\n3. Gamete Formation:\n   - All eggs carry X chromosome\n   - Sperm carry either X or Y\n\n4. Determination:\n   \n   Mother (XX)  ×  Father (XY)\n   Eggs: X         Sperm: X or Y\n   \n   If X sperm fertilizes → XX → Girl\n   If Y sperm fertilizes → XY → Boy\n   \n   Probability: 50% boy, 50% girl\n\n5. Conclusion:\n   - Father determines sex of child\n   - Mother contributes only X chromosome\n   - Sex ratio is 1:1"),
            ("How do traits get expressed? Explain with the example of height in pea plants.",
             "Trait Expression:\n\n1. Genes and Proteins:\n   - Genes are segments of DNA\n   - Genes code for proteins (enzymes)\n   - Proteins (enzymes) control biochemical reactions\n   - Reactions determine traits\n\n2. Example - Height in Pea Plants:\n   \n   Gene T (dominant) → codes for enzyme → produces growth hormone → TALL plant\n   Gene t (recessive) → defective enzyme → less/no hormone → dwarf plant\n\n3. Genotype → Phenotype:\n   - TT: Two copies of T → full enzyme → Tall\n   - Tt: One T, one t → enough enzyme → Tall (T dominant)\n   - tt: No T → no/less enzyme → Dwarf\n\n4. Dominant and Recessive:\n   - Dominant allele produces functional protein\n   - Even one copy is enough for expression\n   - Recessive allele may produce non-functional protein\n   - Needs two copies to show effect\n\n5. Summary:\n   Gene → Protein → Biochemical reaction → Trait"),
        ]
    },
    
    "The Human Eye and the Colourful World": {
        "key_concepts": [
            ("Human eye", "Natural optical device with lens, retina, cornea. Acts like a camera to form images."),
            ("Power of accommodation", "Ability of eye lens to change focal length using ciliary muscles to focus at different distances."),
            ("Myopia", "Near-sightedness. Image forms before retina. Corrected by concave lens."),
            ("Hypermetropia", "Far-sightedness. Image forms behind retina. Corrected by convex lens."),
            ("Dispersion", "Splitting of white light into seven colors (VIBGYOR) by prism."),
            ("Scattering", "Deflection of light by particles. Blue light scattered more than red (shorter wavelength)."),
            ("Rainbow", "Natural spectrum formed by dispersion of sunlight by water droplets."),
            ("Tyndall effect", "Scattering of light by colloidal particles making path of light visible."),
        ],
        "mcq_pool": [
            ("The human eye lens is:", ["Concave", "Convex", "Biconvex", "Biconcave"], "Biconvex", "Eye lens is convex on both sides."),
            ("Myopia is corrected by:", ["Convex lens", "Concave lens", "Bifocal lens", "Cylindrical lens"], "Concave lens", "Concave lens diverges light before entering eye."),
            ("The splitting of white light is called:", ["Reflection", "Refraction", "Dispersion", "Scattering"], "Dispersion", "Prism disperses white light into VIBGYOR."),
            ("Sky appears blue due to:", ["Dispersion", "Scattering", "Reflection", "Refraction"], "Scattering", "Blue light is scattered more by atmosphere."),
            ("The least distance of distinct vision for normal eye is:", ["10 cm", "25 cm", "50 cm", "100 cm"], "25 cm", "Normal near point is 25 cm."),
            ("Retina is equivalent to:", ["Film", "Lens", "Shutter", "Aperture"], "Film", "Retina acts like camera film, receives image."),
            ("Presbyopia is corrected by:", ["Concave lens", "Convex lens", "Bifocal lens", "Cylindrical lens"], "Bifocal lens", "Bifocal has both concave and convex parts."),
            ("Danger signals are red because:", ["Red is bright", "Red scatters least", "Red is visible", "Red attracts attention"], "Red scatters least", "Red light travels longest distance without scattering."),
            ("The part of eye that controls amount of light is:", ["Lens", "Iris", "Retina", "Cornea"], "Iris", "Iris controls pupil size and light entry."),
            ("During sunset, sun appears red because:", ["Sun emits red light", "Blue light scattered away", "Red is reflected", "Atmosphere is red"], "Blue light scattered away", "More scattering of blue light in thick atmosphere."),
            ("Image on retina is:", ["Virtual and erect", "Real and erect", "Real and inverted", "Virtual and inverted"], "Real and inverted", "Eye lens forms real, inverted image on retina."),
            ("Stars appear to twinkle due to:", ["Dispersion", "Refraction", "Atmospheric refraction", "Scattering"], "Atmospheric refraction", "Changing refractive index of atmosphere."),
            ("The color with shortest wavelength is:", ["Red", "Violet", "Green", "Yellow"], "Violet", "Violet has shortest wavelength in visible spectrum."),
            ("Cataract can be corrected by:", ["Spectacles", "Medicine", "Surgery", "Exercise"], "Surgery", "Cloudy lens is replaced with artificial lens."),
            ("Aqueous humour is found:", ["Behind lens", "Between cornea and lens", "On retina", "In optic nerve"], "Between cornea and lens", "Aqueous humour is in front chamber of eye."),
        ],
        "fill_blanks": [
            ("Power of accommodation is due to _______.", "ciliary muscles"),
            ("VIBGYOR are colors of _______.", "rainbow/spectrum"),
            ("Advanced sunrise is due to _______ refraction.", "atmospheric"),
            ("Cataract is cloudiness of _______.", "lens"),
            ("The normal near point of eye is _______ cm.", "25"),
            ("Light sensitive cells in retina are _______ and _______.", "rods and cones"),
            ("Far point of normal eye is at _______.", "infinity"),
            ("Red light has _______ wavelength than violet.", "longer"),
            ("Rainbow is formed due to _______ and total internal reflection.", "dispersion"),
            ("The black opening in eye that controls light is _______.", "pupil"),
            ("A person with myopia cannot see _______ objects clearly.", "distant"),
            ("_______ effect makes the path of light visible in forest.", "Tyndall"),
        ],
        "short_answers": [
            ("What is myopia? How is it corrected?", "Myopia (near-sightedness) is when image forms before retina due to elongated eyeball or thick lens. Corrected using concave lens of suitable power which diverges light rays."),
            ("Why does sky appear blue?", "Atmosphere scatters sunlight. Blue light has shorter wavelength and is scattered more than red. Scattered blue light reaches our eyes from all directions, making sky appear blue."),
            ("Why do stars twinkle?", "Starlight passes through atmosphere with varying refractive index. This causes apparent position and brightness to keep changing, making stars appear to twinkle."),
            ("What is dispersion of light?", "Splitting of white light into its seven constituent colors (VIBGYOR) when passed through a prism. It occurs because different colors have different wavelengths and bend differently."),
            ("Why does the sun appear red at sunrise and sunset?", "At sunrise/sunset, sunlight travels longer path through atmosphere. Blue light gets scattered away. Only red light with longest wavelength reaches us, making sun appear red."),
            ("What is presbyopia? How is it corrected?", "Presbyopia is age-related defect where eye cannot focus on nearby objects due to weakening of ciliary muscles. Corrected using bifocal lens (both convex and concave)."),
            ("What is the function of iris?", "Iris controls the size of pupil, thus regulating amount of light entering the eye. In bright light, pupil contracts. In dim light, pupil dilates."),
            ("Why are danger signals red?", "Red light has longest wavelength and scatters least. It can travel long distances through fog and smoke, remaining visible from far away."),
        ],
        "long_answers": [
            ("Draw a labeled diagram of human eye and explain its structure and working.",
             "Structure of Human Eye:\n\n1. CORNEA:\n   - Transparent front part\n   - Maximum refraction occurs here\n\n2. IRIS:\n   - Colored muscular diaphragm\n   - Controls pupil size\n\n3. PUPIL:\n   - Central opening in iris\n   - Controls light entry\n\n4. EYE LENS:\n   - Biconvex, crystalline\n   - Fine-tuned focusing\n   - Changes shape for accommodation\n\n5. CILIARY MUSCLES:\n   - Attached to lens\n   - Control lens shape\n\n6. RETINA:\n   - Light-sensitive screen\n   - Contains rods (dim light) and cones (color)\n\n7. OPTIC NERVE:\n   - Transmits signals to brain\n\nWorking:\n1. Light enters through cornea\n2. Pupil controls light amount\n3. Lens focuses light on retina\n4. Real, inverted image forms on retina\n5. Rods/cones convert to electrical signals\n6. Optic nerve sends to brain\n7. Brain interprets as erect image"),
            ("Explain the defects of vision and their correction.",
             "Defects of Vision:\n\n1. MYOPIA (Near-sightedness):\n   Cause: Eyeball too long or lens too curved\n   Effect: Image forms before retina\n   Symptom: Cannot see distant objects clearly\n   Correction: Concave lens (diverges light)\n\n2. HYPERMETROPIA (Far-sightedness):\n   Cause: Eyeball too short or lens too flat\n   Effect: Image forms behind retina\n   Symptom: Cannot see nearby objects clearly\n   Correction: Convex lens (converges light)\n\n3. PRESBYOPIA (Old age):\n   Cause: Ciliary muscles weaken with age\n   Effect: Cannot change lens shape properly\n   Symptom: Cannot focus on near objects\n   Correction: Bifocal lens\n\n4. ASTIGMATISM:\n   Cause: Uneven curvature of cornea\n   Effect: Blurred vision at all distances\n   Correction: Cylindrical lens\n\n5. CATARACT:\n   Cause: Lens becomes cloudy (opaque)\n   Treatment: Surgery to replace lens"),
            ("Explain dispersion of light through a prism and formation of rainbow.",
             "Dispersion of Light:\n\n1. Definition:\n   Splitting of white light into seven colors\n\n2. Through Prism:\n   - White light enters prism\n   - Different colors refract differently\n   - Violet bends most, red bends least\n   - Colors spread out: VIBGYOR\n   (Violet, Indigo, Blue, Green, Yellow, Orange, Red)\n\n3. Reason:\n   - Different wavelengths travel at different speeds in glass\n   - Violet has shortest wavelength, slows most\n   - Red has longest wavelength, slows least\n\nFormation of Rainbow:\n\n1. Conditions needed:\n   - Sun behind observer\n   - Water droplets in front\n\n2. Process in water droplet:\n   - Sunlight enters droplet (refraction)\n   - Dispersion occurs inside\n   - Total internal reflection\n   - Light exits droplet (refraction)\n\n3. Rainbow formation:\n   - Each color exits at different angle\n   - Millions of droplets work together\n   - Red on outer arc, violet on inner\n\n4. Types:\n   - Primary rainbow: One internal reflection\n   - Secondary rainbow: Two internal reflections (inverted colors)"),
        ]
    },
    
    "Magnetic Effects of Electric Current": {
        "key_concepts": [
            ("Magnetic field", "Region around magnet where magnetic force is experienced. Represented by field lines."),
            ("Electromagnetic induction", "Production of electric current by changing magnetic field. Discovered by Faraday."),
            ("Electric motor", "Device converting electrical energy to mechanical energy using magnetic effect of current."),
            ("Electric generator", "Device converting mechanical energy to electrical energy using electromagnetic induction."),
            ("Fleming's left hand rule", "Gives direction of force on current-carrying conductor in magnetic field."),
            ("Fleming's right hand rule", "Gives direction of induced current in electromagnetic induction."),
            ("Solenoid", "Coil of many turns behaving like bar magnet when current flows through it."),
            ("Fuse", "Safety device that melts and breaks circuit when current exceeds safe limit."),
        ],
        "mcq_pool": [
            ("Magnetic field lines around a current-carrying wire are:", ["Straight", "Circular", "Elliptical", "Random"], "Circular", "Field lines form concentric circles around wire."),
            ("Fleming's left hand rule gives direction of:", ["Current", "Field", "Force", "Voltage"], "Force", "It gives direction of force on current-carrying conductor."),
            ("An electric motor converts:", ["Electrical to mechanical", "Mechanical to electrical", "Heat to electrical", "Light to electrical"], "Electrical to mechanical", "Motor converts electrical energy to motion."),
            ("AC generator works on:", ["Faraday's law", "Ohm's law", "Newton's law", "Coulomb's law"], "Faraday's law", "Electromagnetic induction."),
            ("A solenoid acts like:", ["Capacitor", "Bar magnet", "Resistor", "Battery"], "Bar magnet", "Solenoid has north and south poles like bar magnet."),
            ("The function of commutator in motor is:", ["Increase current", "Reverse current direction", "Decrease current", "Store energy"], "Reverse current direction", "Commutator reverses current every half rotation."),
            ("1 unit of electricity equals:", ["1 kW", "1 kWh", "1 W", "1 Wh"], "1 kWh", "1 unit = 1 kilowatt-hour."),
            ("Earth wire is connected to:", ["Live wire", "Metal body of appliance", "Neutral wire", "Fuse"], "Metal body of appliance", "Earth wire provides safety path for current."),
            ("Short circuit occurs when:", ["Current is low", "Live and neutral touch", "Fuse is removed", "Resistance is high"], "Live and neutral touch", "Direct contact causes very high current."),
            ("Color of live wire in India is:", ["Green", "Black", "Red/Brown", "Blue"], "Red/Brown", "Live wire carries current to appliance."),
            ("Which effect is used in electric bell?", ["Heating", "Magnetic", "Chemical", "Light"], "Magnetic", "Electromagnet attracts and releases hammer."),
            ("Direct current is produced by:", ["AC generator", "DC generator", "Transformer", "Motor"], "DC generator", "DC generator has commutator for unidirectional current."),
            ("Transformer works on:", ["DC only", "AC only", "Both AC and DC", "Neither"], "AC only", "Transformers need changing current for induction."),
            ("MCB works on:", ["Heating effect", "Magnetic effect", "Chemical effect", "Both heating and magnetic"], "Both heating and magnetic", "MCB uses both effects for protection."),
            ("Inside solenoid, magnetic field is:", ["Zero", "Uniform and strong", "Weak", "Random"], "Uniform and strong", "Field lines are straight and parallel inside solenoid."),
        ],
        "fill_blanks": [
            ("The SI unit of magnetic field is _______.", "Tesla"),
            ("A coil of many turns is called a _______.", "solenoid"),
            ("The frequency of AC in India is _______ Hz.", "50"),
            ("A fuse wire has _______ melting point.", "low"),
            ("The phenomenon of producing electric current by changing magnetic field is _______.", "electromagnetic induction"),
            ("In domestic circuits, all appliances are connected in _______.", "parallel"),
            ("The rate of change of magnetic flux induces _______.", "emf/voltage"),
            ("Electric motor uses _______ effect of current.", "magnetic"),
            ("The rotating part of electric motor is called _______.", "armature"),
            ("Overloading can cause _______ in circuits.", "fire"),
            ("The device that changes AC voltage is _______.", "transformer"),
            ("Color of neutral wire is _______.", "black"),
        ],
        "short_answers": [
            ("State Fleming's left hand rule.", "Stretch thumb, forefinger and middle finger perpendicular to each other. Forefinger shows magnetic field (B), middle finger shows current (I), thumb shows force (F) direction."),
            ("What is electromagnetic induction?", "The phenomenon of producing electric current by changing magnetic field around a conductor is electromagnetic induction. Discovered by Michael Faraday."),
            ("Why is earth wire necessary?", "Earth wire provides low resistance path to ground. If live wire touches metal body, current flows to ground through earth wire instead of through person, preventing shock."),
            ("What is short circuit?", "When live and neutral wires come in direct contact (due to damaged insulation), resistance becomes very low and current becomes very high. This is short circuit."),
            ("What is the function of fuse?", "Fuse protects circuit from overloading. When current exceeds safe limit, fuse wire melts and breaks circuit, preventing fire and damage to appliances."),
            ("Differentiate between AC and DC.", "AC: Current direction changes periodically. DC: Current flows in one direction. AC is used for power transmission (transformers work). DC is used in batteries."),
            ("State Fleming's right hand rule.", "Stretch thumb, forefinger, and middle finger perpendicular. Thumb: direction of motion, Forefinger: magnetic field direction, Middle finger: induced current direction."),
            ("Why are thick wires used for high current appliances?", "Thick wires have low resistance. Low resistance means less heat produced (H = I²Rt). This prevents fire hazard and energy loss."),
        ],
        "long_answers": [
            ("Explain the principle and working of an electric motor.",
             "Electric Motor:\n\nPrinciple:\nA current-carrying conductor in magnetic field experiences a force.\n\nConstruction:\n1. Armature: Rectangular coil of insulated copper wire\n2. Field magnets: Strong permanent or electromagnets\n3. Split ring commutator: Two halves of a ring\n4. Brushes: Carbon brushes pressing on commutator\n5. Axle: Supports rotating coil\n\nWorking:\n1. Current enters coil through brush B1\n2. Current flows through coil in ABCD direction\n3. Using Fleming's left hand rule:\n   - AB side experiences downward force\n   - CD side experiences upward force\n4. Coil rotates clockwise\n5. After half rotation, commutator reverses current\n6. Forces reverse, but rotation continues\n7. Continuous rotation occurs\n\nUses:\n- Electric fans, mixers, washing machines\n- Water pumps, drills, vehicles"),
            ("Explain the principle and working of an AC generator.",
             "AC Generator:\n\nPrinciple:\nElectromagnetic induction - when magnetic flux through a coil changes, emf is induced.\n\nConstruction:\n1. Armature: Rectangular coil of insulated copper wire\n2. Field magnets: Strong permanent magnets (N-S poles)\n3. Slip rings: Two rings connected to coil ends\n4. Brushes: Carbon brushes touching slip rings\n5. Axle: For rotating the coil\n\nWorking:\n1. Coil rotated in magnetic field by external force\n2. As coil rotates, magnetic flux changes\n3. By Faraday's law, emf is induced\n4. During first half rotation:\n   - Flux increases then decreases\n   - Current in one direction\n5. During second half:\n   - Flux changes in opposite sense\n   - Current reverses direction\n6. Result: Alternating current (AC)\n\nEmf equation: e = NABω sin(ωt)\n\nNote: DC generator has commutator instead of slip rings to get unidirectional current."),
            ("Describe domestic electric circuits and safety measures.",
             "Domestic Electric Circuits:\n\n1. SUPPLY:\n   - 220V AC at 50 Hz\n   - Main supply through meter to distribution box\n\n2. WIRES:\n   - Live wire (red/brown): Carries current to appliance\n   - Neutral wire (black): Return path for current\n   - Earth wire (green): Safety grounding\n\n3. CONNECTION:\n   - All appliances connected in parallel\n   - Each gets same voltage (220V)\n   - Independent operation\n\n4. SAFETY DEVICES:\n\n   a) Fuse:\n      - Thin wire with low melting point\n      - Melts when current exceeds rated value\n      - Connected in live wire\n\n   b) MCB (Miniature Circuit Breaker):\n      - Uses magnetic/heating effect\n      - Trips (switches off) on overload\n      - Can be reset\n\n   c) Earthing:\n      - Metal body connected to earth\n      - Current flows to ground if fault occurs\n\n5. HAZARDS:\n   - Short circuit: Live touches neutral\n   - Overloading: Too many appliances\n   - Damaged insulation\n\n6. PRECAUTIONS:\n   - Never touch live wire\n   - Don't overload sockets\n   - Use proper earthing\n   - Replace damaged wires\n   - Use proper rated fuse"),
        ]
    },
    
    "Our Environment": {
        "key_concepts": [
            ("Ecosystem", "Self-sustaining unit of living organisms and their non-living environment interacting with each other."),
            ("Food chain", "Linear sequence of organisms where each is eaten by the next. Energy flows from producers to consumers."),
            ("Food web", "Network of interconnected food chains in an ecosystem."),
            ("Trophic levels", "Steps in food chain: producers (1st), primary consumers (2nd), secondary consumers (3rd), tertiary (4th)."),
            ("10% law", "Only 10% energy transfers from one trophic level to next. 90% lost as heat."),
            ("Biodegradable waste", "Waste that can be broken down by microorganisms. Examples: food scraps, paper, leaves."),
            ("Non-biodegradable waste", "Waste that cannot be broken down easily. Examples: plastic, glass, metals."),
            ("Ozone layer", "Layer of O3 in stratosphere protecting Earth from harmful UV radiation."),
        ],
        "mcq_pool": [
            ("Biodegradable waste is:", ["Plastic", "Vegetable peels", "Glass", "Aluminum cans"], "Vegetable peels", "Organic waste is biodegradable."),
            ("10% energy is available at each trophic level as per:", ["3% law", "10% law", "20% law", "5% law"], "10% law", "Only 10% energy transfers to next level."),
            ("Ozone layer is present in:", ["Troposphere", "Stratosphere", "Mesosphere", "Thermosphere"], "Stratosphere", "Ozone layer is in stratosphere."),
            ("CFCs deplete:", ["Oxygen", "Ozone", "Nitrogen", "Carbon dioxide"], "Ozone", "CFCs break down ozone molecules."),
            ("First trophic level consists of:", ["Herbivores", "Carnivores", "Producers", "Decomposers"], "Producers", "Green plants are producers at first level."),
            ("Energy flow in ecosystem is:", ["Cyclic", "Unidirectional", "Bidirectional", "Random"], "Unidirectional", "Energy flows from sun to producers to consumers."),
            ("Which is NOT a greenhouse gas?", ["CO2", "Methane", "Nitrogen", "Water vapor"], "Nitrogen", "Nitrogen is not a greenhouse gas."),
            ("Biological magnification refers to:", ["Increase in organism size", "Accumulation of toxins", "Growth of population", "Evolution"], "Accumulation of toxins", "Toxins concentrate at higher trophic levels."),
            ("Decomposers are:", ["Autotrophs", "Heterotrophs", "Producers", "Herbivores"], "Heterotrophs", "Decomposers like bacteria, fungi are heterotrophs."),
            ("Which is a primary consumer?", ["Lion", "Snake", "Grasshopper", "Frog"], "Grasshopper", "Grasshopper eats plants (herbivore)."),
            ("The percentage of solar energy captured by producers is:", ["1%", "10%", "50%", "90%"], "1%", "Only about 1% of solar energy is captured by plants."),
            ("Acid rain is caused by:", ["CO2", "O2", "SO2 and NO2", "H2O"], "SO2 and NO2", "These gases form acids with water."),
            ("UNEP stands for:", ["United Nations Environment Programme", "Universal Nature Environment Plan", "United National Ecology Project", "Union for Natural Environment Protection"], "United Nations Environment Programme", "UNEP is the global environmental authority."),
            ("Ozone hole is largest over:", ["Africa", "Antarctica", "Asia", "America"], "Antarctica", "Ozone depletion is highest over Antarctica."),
            ("Which helps in nutrient cycling?", ["Producers", "Consumers", "Decomposers", "Sunlight"], "Decomposers", "Decomposers return nutrients to soil."),
        ],
        "fill_blanks": [
            ("Organisms that produce their own food are called _______.", "producers"),
            ("The sequence of eating and being eaten is called _______.", "food chain"),
            ("Ozone is made of _______ oxygen atoms.", "three"),
            ("Plastic is _______ waste.", "non-biodegradable"),
            ("The full form of CFC is _______.", "Chlorofluorocarbon"),
            ("In food chain, energy flow is _______.", "unidirectional"),
            ("Organisms that eat only plants are called _______.", "herbivores"),
            ("_______ are called nature's cleansers.", "Decomposers"),
            ("Green plants are at _______ trophic level.", "first"),
            ("The layer of ozone absorbs _______ rays.", "ultraviolet/UV"),
            ("Accumulation of pesticides in food chain is called _______.", "biological magnification"),
            ("Components of ecosystem are biotic and _______.", "abiotic"),
        ],
        "short_answers": [
            ("What is a food chain?", "A food chain is a sequence showing who eats whom in an ecosystem. Energy flows from producers to consumers. Example: Grass → Grasshopper → Frog → Snake → Eagle"),
            ("Why is ozone layer important?", "Ozone layer in stratosphere absorbs harmful UV radiations from sun.  It protects life on Earth from skin cancer, eye damage, and harm to crops and marine life."),
            ("What is biological magnification?", "It is the increase in concentration of harmful chemicals like pesticides at each trophic level. Top predators have highest concentration as they eat many organisms below them."),
            ("Differentiate between biodegradable and non-biodegradable wastes.", "Biodegradable: Broken down by microorganisms (paper, food). Non-biodegradable: Cannot be decomposed easily (plastic, glass). Non-biodegradable accumulates and pollutes."),
            ("What is the 10% law?", "Only about 10% of energy at each trophic level is passed to next level. Rest 90% is used in life processes and lost as heat. This limits food chain to 3-4 levels."),
            ("How do CFCs damage ozone layer?", "CFCs release chlorine atoms when exposed to UV. One chlorine atom can destroy thousands of ozone molecules by acting as catalyst:"),
            ("What is an ecosystem?", "An ecosystem is a self-sustaining unit consisting of living organisms (plants, animals, microbes) and their non-living environment (air, water, soil) interacting together."),
            ("Why are food chains generally short?", "Due to 10% law, energy decreases at each level. After 3-4 levels, energy is too little to support more consumers. So food chains are usually 3-4 levels only."),
        ],
        "long_answers": [
            ("What are the components of an ecosystem? Explain with examples.",
             "Components of Ecosystem:\n\n1. ABIOTIC COMPONENTS (Non-living):\n   a) Climatic factors: Temperature, light, humidity, rainfall\n   b) Edaphic factors: Soil type, minerals, pH\n   c) Topographic factors: Altitude, slope\n   d) Inorganic substances: Water, CO2, O2, nitrogen\n   e) Organic substances: Proteins, carbohydrates in dead matter\n\n2. BIOTIC COMPONENTS (Living):\n\n   a) Producers (Autotrophs):\n      - Make own food by photosynthesis\n      - Examples: Green plants, algae, cyanobacteria\n      - First trophic level\n\n   b) Consumers (Heterotrophs):\n      - Depend on others for food\n      \n      i) Primary consumers (Herbivores):\n         - Eat plants\n         - Examples: Deer, rabbit, grasshopper\n         - Second trophic level\n      \n      ii) Secondary consumers (Carnivores):\n         - Eat herbivores\n         - Examples: Frog, small fish\n         - Third trophic level\n      \n      iii) Tertiary consumers (Top carnivores):\n         - Eat secondary consumers\n         - Examples: Lion, eagle, shark\n         - Fourth trophic level\n   \n   c) Decomposers:\n      - Break down dead organisms\n      - Examples: Bacteria, fungi\n      - Return nutrients to soil"),
            ("Explain the flow of energy in an ecosystem.",
             "Energy Flow in Ecosystem:\n\n1. SOURCE OF ENERGY:\n   - Sun is ultimate source\n   - About 1% captured by plants\n\n2. ENERGY CAPTURE:\n   - Plants convert solar energy to chemical energy\n   - Stored in glucose through photosynthesis\n   - This energy enters the ecosystem\n\n3. ENERGY TRANSFER:\n   Trophic Level 1 (Producers): 100% of captured energy\n   ↓ (10% transferred)\n   Trophic Level 2 (Primary consumers): 10%\n   ↓ (10% transferred)\n   Trophic Level 3 (Secondary consumers): 1%\n   ↓ (10% transferred)\n   Trophic Level 4 (Tertiary consumers): 0.1%\n\n4. 10% LAW (Lindeman):\n   - Only 10% energy passes to next level\n   - 90% lost as:\n     * Heat during respiration\n     * Undigested material\n     * Excretion\n\n5. CHARACTERISTICS:\n   - Flow is unidirectional (not cyclic)\n   - Amount decreases at each level\n   - Limits food chain to 3-4 levels\n   - Pyramids of energy are always upright\n\n6. DECOMPOSERS:\n   - Get energy from all levels (dead matter)\n   - Release nutrients back to soil"),
            ("What is ozone layer? How is it being depleted? What are the effects?",
             "Ozone Layer:\n\n1. WHAT IS OZONE:\n   - Molecule with 3 oxygen atoms (O3)\n   - Found in stratosphere (15-35 km)\n   - Acts as shield against UV rays\n\n2. OZONE FORMATION:\n   - UV splits O2 → O + O\n   - O + O2 → O3 (ozone)\n   - Natural balance is maintained\n\n3. DEPLETION BY CFCs:\n   - CFCs used in refrigerators, ACs, aerosols\n   - CFCs rise to stratosphere\n   - UV breaks CFC, releasing chlorine\n   - Cl + O3 → ClO + O2\n   - ClO + O → Cl + O2\n   - One Cl destroys thousands of O3\n\n4. OZONE HOLE:\n   - Largest over Antarctica\n   - Discovered in 1985\n   - Seasonal thinning of ozone\n\n5. EFFECTS OF DEPLETION:\n   - Increased UV reaching Earth\n   - Skin cancer increases\n   - Eye cataracts\n   - Weakened immune system\n   - Damage to crops\n   - Harm to marine organisms\n   - Climate change\n\n6. SOLUTIONS:\n   - Montreal Protocol (1987)\n   - Ban on CFCs\n   - Use of alternatives (HFCs)\n   - International cooperation"),
        ]
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
