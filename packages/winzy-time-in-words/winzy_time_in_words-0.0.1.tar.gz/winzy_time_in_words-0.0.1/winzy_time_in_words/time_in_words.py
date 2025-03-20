import datetime

def time_in_words(hour, minute):
    # List of words for numbers
    num_to_words = ["twelve", "one", "two", "three", "four", 
                    "five", "six", "seven", "eight", "nine", 
                    "ten", "eleven", "twelve", "thirteen", 
                    "fourteen", "quarter", "sixteen", 
                    "seventeen", "eighteen", "nineteen", 
                    "twenty", "twenty one", "twenty two", 
                    "twenty three", "twenty four", "twenty five", 
                    "twenty six", "twenty seven", "twenty eight", 
                    "twenty nine", "half"]
    
    if minute == 0:
        return f"{num_to_words[hour]} o'clock"
    elif minute == 15:
        return f"Quarter past {num_to_words[hour]}"
    elif minute == 30:
        return f"Half past {num_to_words[hour]}"
    elif minute == 45:
        return f"Quarter to {num_to_words[(hour % 12) + 1]}"
    elif minute < 30:
        if minute == 1:
            return f"One minute past {num_to_words[hour]}"
        else:
            return f"{num_to_words[minute]} minutes past {num_to_words[hour]}"
    else:
        if minute == 59:
            return f"One minute to {num_to_words[(hour % 12) + 1]}"
        else:
            return f"{num_to_words[60 - minute]} minutes to {num_to_words[(hour % 12) + 1]}"

def mainrun():
    # Get the current time
    now = datetime.datetime.now()
    hour = now.hour % 12  # Convert to 12-hour format
    minute = now.minute
    
    # Get the time in words
    time_words = time_in_words(hour, minute)
    
    # Print the time in words
    print(f"The time is {time_words}.")

if __name__ == "__main__":
    mainrun()

