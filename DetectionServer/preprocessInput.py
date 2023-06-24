import pickle
import re

def extract_domain_features(domain_name):
    domain_name = domain_name.strip().lower()
    if not domain_name:
        return [0]
    try:
            tld, sld = domain_name.split(".")[-2:]
    except ValueError:
        print(f"Skipping invalid domain name: {domain_name}")
        return [0]  # Skip invalid domain names

    # Calculate lengths of top-level domain and second-level domain
    tld_length = len(tld)
    sld_length = len(sld)

    # Calculate length and level of the domain name
    domain_length = len(domain_name)
    domain_level = len(domain_name.split("."))
    other_level = max(domain_length - (tld_length + sld_length + 2),0)
    

    # Check if domain name includes "www" or an IP address
    includes_www = int(domain_name.startswith("www."))
    #includes_ip = int(bool(re.match(r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}", domain_name)))

     # Calculate length of longest consonant string
    consonant_string = re.sub("[aeiouyAEIOUY\W\d]+", " ", domain_name)
    consonant_lengths = [len(word) for word in consonant_string.split()]
    longest_consonant = max(consonant_lengths, default=0)
    shortest_consonant =  min(consonant_lengths) if len(consonant_lengths) > 1 else 0
    diff_consonant = longest_consonant - shortest_consonant

    # Calculate length of longest vowel sequence
    vowel_string = re.sub("[^aeiouyAEIOUY]+", " ", domain_name)
    vowel_lengths = [len(word) for word in vowel_string.split()]
    longest_vowel = max(vowel_lengths, default=0)
    shortest_vowel =  min(vowel_lengths) if len(vowel_lengths) > 1 else 0
    diff_vowel = longest_vowel - shortest_vowel

    # Calculate length of longest character string
    char_lengths = [len(word) for word in re.findall(r"[a-zA-Z]+", domain_name)]
    longest_char = max(char_lengths, default=0)
    shortest_char =  min(char_lengths) if len(char_lengths) > 1 else 0
    diff_char = longest_char - shortest_char

    # Calculate length of longest string of numbers
    num_lengths = [len(word) for word in re.findall(r"\d+", domain_name)]
    longest_num = max(num_lengths, default=0)
    shortest_num = min(num_lengths) if len(num_lengths) > 1 else 0
    diff_num = longest_num - shortest_num

     # Calculate average length of consonant strings
    avg_consonant = sum(consonant_lengths) / len(consonant_lengths) if len(consonant_lengths) > 0 else 0

    # Calculate average length of vowel strings
    avg_vowel = sum(vowel_lengths) / len(vowel_lengths) if len(vowel_lengths) > 0 else 0
    
    # Calculate average length of character strings
    avg_char = sum(char_lengths) / len(char_lengths) if len(char_lengths) > 0 else 0
    
    # Calculate average length of alphanumeric strings
    avg_alnum = sum(num_lengths) / len(num_lengths) if len(num_lengths) > 0 else 0

    # Calculate the number of different consonants in the domain name
    consonants = set(re.sub("[aeiouyAEIOUY\W\d]+", "", domain_name))
    num_consonants = len(consonants)
    pct_consonants = round(num_consonants / 20 , 3)

    num_cons = len(re.findall(r"[bcdfghjklmnpqrstvwxz]", domain_name, re.IGNORECASE))
    ratio_consonants = round(num_cons / domain_length , 3)

    # Calculate the number of different vowels in the domain name
    vowels = set(re.sub("[^aeiouyAEIOUY]+", "", domain_name))
    num_vowels = len(vowels)
    pct_vowels = round(num_vowels / 6 , 3)

    num_vow = len(re.findall(r"[aeiouy]", domain_name, re.IGNORECASE))
    ratio_vowels = round(num_vow / domain_length , 3)

    # Calculate the number of different letters in the domain name
    num_letters = num_consonants + num_vowels
    pct_letters = round(num_letters / 26 , 3)

    num_alpha = len(re.findall(r"[a-z]", domain_name, re.IGNORECASE))
    ratio_letters = round(num_alpha / domain_length , 3)

    # Calculate the number of different numbers in the domain name
    numbers = set(re.findall(r"\d+", domain_name))
    num_numbers = len(numbers)
    pct_numbers = round(num_numbers / 10 , 3)

    num_num = len(re.findall(r"\d", domain_name))
    ratio_numbers = round(num_num / domain_length , 3)

    # Calculate the number of different special characters in the domain name
    #punctuation marks, symbols, whitespace, and underscores
    special_chars = set(re.findall(r"[\W_]+", domain_name))
    num_special_chars = len(special_chars)
    #There are 32 special characters in total !, @, #, $, %, ^, &, *, (, ), -, _, +, =, {, }, [, ], |, \, ;, :, ", ', ,, ., <, >, ?, /, ~, " ".
    pct_special_chars = round(num_special_chars / 32 , 3)

    num_sc = len(re.findall(r"[\W_]", domain_name))
    ratio_special_chars = round(num_sc / domain_length , 3)
    
    return  [tld, sld, domain_length ,tld_length, sld_length ,other_level,domain_level,includes_www ,longest_consonant , longest_vowel, longest_char, longest_num , avg_consonant, avg_vowel, avg_char, avg_alnum , diff_consonant, diff_vowel, diff_char,diff_num , num_consonants , num_vowels, num_letters, num_numbers, num_special_chars,pct_consonants,pct_vowels,pct_letters,pct_numbers,pct_special_chars,ratio_consonants,ratio_vowels,ratio_letters,ratio_numbers,ratio_special_chars]

# Load LabelEncoder objects and scaler object
with open('XGBoost/le_domTLD.pkl','rb') as f:
    le_domTLD = pickle.load(f)

with open('XGBoost/le_domSLD.pkl','rb') as f:
    le_domSLD = pickle.load(f)

with open('XGBoost/scaler.pkl','rb') as f:
    scaler = pickle.load(f)


def preprocess_input(input_domainname):
  
  result=extract_domain_features(input_domainname)
  # Check unique values of categorical columns
  unique_domTLD = set([result[0]])
  unique_domSLD = set([result[1]])
  # Check if unique values match the classes of LabelEncoder objects
  if not unique_domTLD.issubset(le_domTLD.classes_):
    le_domTLD.fit(list(le_domTLD.classes_) + list(unique_domTLD))

  if not unique_domSLD.issubset(le_domSLD.classes_):
    le_domSLD.fit(list(le_domSLD.classes_) + list(unique_domSLD))

  # Encode categorical columns
  result[0] = le_domTLD.transform([result[0]])[0]
  result[1] = le_domSLD.transform([result[1]])[0]

  # Transform your dataset using the scaler
  result_norm = scaler.transform([result])
  return result_norm

#print(preprocess_input("google.com"))

