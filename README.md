### CSA Unit 3 Data for Social Good Project Planning Guide

#### **Step 1: Choose your user**
**User:** Avian Veterinary Student
**User Story:** As an avian veterinary student, I want to identify groups of similar birds so I can study them for my final exams.
**Dataset:** Names, Conservation Status, Colors, Diets of birds

**Possible Questions:**
1. What are the conservation statuses of different birds?
2. What are the most common colors among birds?
3. How many birds have a specific diet?
4. What is the average length of bird names?

---
#### **Step 2: UML Diagram**
**Class: UserStory**
- **Attributes:**
  - birdNames (String[])
  - conservationStatus (String[])
  - colors (String[])
  - diets (String[])
  - birds (Bird[])

- **Methods:**
  - createBirds()
  - getAllStatuses()
  - calcAverageNameLength()
  - toString()

**Class: Bird**
- **Attributes:**
  - name (String)
  - status (String)
  - color (String)
  - diet (String)

- **Methods:**
  - getName()
  - getStatus()
  - toString()

---
#### **Step 3: User Interaction**
Users should be able to:
1. View all bird data.
2. Retrieve conservation statuses.
3. Identify bird colors and diets.
4. Calculate the average bird name length.

**Pseudocode for User Interaction:**
```
Display menu options to the user
If user selects 1, print all bird data
If user selects 2, print conservation statuses
If user selects 3, print bird colors and diets
If user selects 4, print average name length
```
---
#### **Step 4: Decomposing the Problem**

**Class: UserStory**

**Method: getAllStatuses()**
- **Precondition(s):** conservationStatus array is initialized and contains valid data.
- **Postcondition(s):** Returns a formatted string with all conservation statuses.

**Pseudocode:**
```
Initialize an empty string result
Loop through conservationStatus array
    Append each status to result with a newline
Return result
```

**Method: calcAverageNameLength()**
- **Precondition(s):** birdNames array is initialized and contains valid data.
- **Postcondition(s):** Returns the average length of all bird names.

**Pseudocode:**
```
Initialize totalLength to 0
Loop through birdNames array
    Add length of each name to totalLength
Return totalLength divided by number of birds
```
---
#### **End of Project Reflection**
**Describe your project:**
The project is a bird data analysis program that allows an avian veterinary student to retrieve information about different bird species, including their conservation status, color, and diet. It also provides statistical analysis, such as average name length.

**Two things I’m proud of:**
1. Successfully implemented a structured object-oriented program with multiple classes.
2. Efficiently processed and displayed large datasets using 1D arrays.

**One thing I would improve:**
I would add a user input feature to allow interactive filtering of birds based on color, diet, or conservation status.
