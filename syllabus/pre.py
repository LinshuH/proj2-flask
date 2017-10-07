"""
Pre-process a syllabus (class schedule) file. 

"""
import arrow   # Dates and times
import logging
logging.basicConfig(format='%(levelname)s:%(message)s',
                    level=logging.INFO)
log = logging.getLogger(__name__)

base = arrow.now()   # Default, replaced if file has 'begin: ...'

def process(raw):
    """
    Line by line processing of syllabus file.  Each line that needs
    processing is preceded by 'head: ' for some string 'head'.  Lines
    may be continued if they don't contain ':'.  If # is the first
    non-blank character on a line, it is a comment ad skipped. 
    """
    field = None
    entry = { }
    cooked = [ ] 
    
    for line in raw:
        log.debug("Line: {}".format(line))
        line = line.strip()  # Line is every line in the txt file(raw)
        if len(line) == 0 or line[0]=="#" :
            log.debug("Skipping")
            continue
        parts = line.split(':')  # parts contain two parts, term before :(field) and after column(content).
        if len(parts) == 1 and field:
            entry[field] = entry[field] + line + " "  # entry is a dictionary, parts is the text in the raw, entry is the intermediate dictionary to match the field and content.
            continue
        if len(parts) == 2: 
            field = parts[0]
            content = parts[1]
        else:
            raise ValueError("Trouble with line: '{}'\n".format(line) + 
                "Split into |{}|".format("|".join(parts)))

        if field == "begin":
            try:
                base = arrow.get(content, "MM/DD/YYYY")
                # print("Base date {}".format(base.isoformat()))
 
            except:
                raise ValueError("Unable to parse date {}".format(content))

        elif field == "week":
	 
            if entry:
                cooked.append(entry)
                entry = { }
            entry['topic'] = ""
            entry['project'] = "" 
            entry['week'] = content +  "\n Start date: {}".format(base.date().isoformat()) 
    
            #Find which week need to been highlight

            today = arrow.now('US/Pacific')      
            week_start = base
            week_end = week_start.shift(weeks=+1)

            if (today >= week_start) and (today < week_end):
                #this week need to be highlight
                entry['highlight'] = True
            else:            
                entry['hightlight'] = False

            base = base.replace(days=+7)

            # a new key in entry dictionary, the value is either true or false, if the answer is ture, tne high light. 
	   
        elif field == 'topic' or field == 'project':
            entry[field] = content

        else:
            raise ValueError("Syntax error in line: {}".format(line))
       
        



    if entry:
        cooked.append(entry)
 
    return cooked


def main():
    f = open("data/schedule.txt")
    parsed = process(f)
    print(parsed)
 

if __name__ == "__main__":
    main()
 
