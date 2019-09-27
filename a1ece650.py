import sys
import re
import numpy as np
### YOUR MAIN CODE GOES HERE

### sample code to read from stdin.
### make sure to remove all spurious print statements as required
### by the assignment

def perp( a1 ) :
    b = [0, 0]
    b[0] = -a1[1]
    b[1] = a1[0]
    return b

# line segment a given by endpoints a1, a2
# line segment b given by endpoints b1, b2
# return
def seg_intersect(a1,a2, b1,b2) :
    da = a2-a1
    db = b2-b1
    dp = a1-b1
    dap = perp(da)
    denom = np.dot( dap, db)
    num = np.dot( dap, dp )
    return (num / denom.astype(float))*db + b1

def intersect_on_line(x1, x2, x3, x4) :
    tdenom = (x4[0]-x3[0])*(x1[1]-x2[1])-(x1[0]-x2[0])*(x4[1]-x3[1])
    if tdenom == 0: # Lines are co-linear
        print 'coincident'
        return 2
    ta = abs(((x3[1]-x4[1])*(x1[0]-x3[0])-(x4[0]-x3[0])*(x1[1]-x3[1]))/tdenom)
    tb = abs(((x1[1]-x2[1])*(x1[0]-x3[0])-(x2[0]-x1[0])*(x1[1]-x3[1]))/tdenom)
    if ta >= 0 and ta <= 1 and tb >= 0 and tb <= 1 :
        return 1
    return 0

def find_ints_on_line(x1, x2, int_list):
    int_list_line = []
    int_list_dist = []
    int_list_sorted = []
    for int in int_list:
        xprod = (int[1]-x1[1])*(x2[0]-x1[0])-(int[0]-x1[0])*(x2[1]-x1[1])
        # because of float intercept, could be non-zero
        if abs(xprod) > np.finfo(np.float32).eps:
            continue
        dotproduct = (int[0]-x1[0])*(x2[0]-x1[0])+(int[1]-x1[1])*(x2[1]-x1[1])
        if dotproduct < 0:
            continue
        length = (x2[0]-x1[0])*(x2[0]-x1[0])+(x2[1]-x1[1])*(x2[1]-x1[1])
        if dotproduct > length:
            continue
        int_list_line.append(int)
        int_list_dist.append(dotproduct)
    sort_order = sorted(range(len(int_list_dist)), key=lambda k: int_list_dist[k])
    for elem in sort_order:
        int_list_sorted.append(int_list_line[elem])
    # int_list_dist, int_list_line = zip(*sorted(zip(int_list_dist, int_list_line)))
    return list(int_list_sorted)


def getKeysByValue(dictOfElements, valueToFind):
    listOfKeys = list()
    listOfItems = dictOfElements.items()
    for item  in listOfItems:
        if item[1][0] == valueToFind[0] and item[1][1] == valueToFind[1]:
            listOfKeys.append(item[0])
    return  listOfKeys

def line_length(x1, x2):
    return (x2[0]-x1[0])*(x2[0]-x1[0])+(x2[1]-x1[1])*(x2[1]-x1[1])

def add_to_endpoints(x1):
    val_exist = False
    for val in endpoints:
        if np.array_equal(val, x1):
            val_exist = True
    if val_exist == False:
        endpoints.append(x1)

def add_to_intercepts(x1):
    val_exist = False
    for val in intercepts:
        if np.array_equal(val, x1):
            val_exist = True
    if val_exist == False:
        intercepts.append(x1)

def add_to_line_int(x1, x2):
    val_exist = False
    for val in lines_with_intercepts:
        if np.array_equal(val, x1) and np.array_equal(val, x2):
            val_exist = True
    if val_exist == False:
        lines_with_intercepts.append([x1, x2])

def add_coincident_lines(x1,x2,x3,x4):
    sum_length = line_length(x1, x2) + line_length(x3, x4)
    x14 = line_length(x1, x4)
    x13 = line_length(x1, x3)
    x24 = line_length(x2, x4)
    x23 = line_length(x2, x3)
    if  x14 > sum_length or \
        x24 > sum_length or \
        x13 > sum_length or \
        x23 > sum_length:
            return 0 #lines do not overlap
    if  x14 + x23 == sum_length:
        # lines intersect at a point
        if x13 == 0:
            add_to_intercepts(x1)
            add_to_endpoints(x2)
            add_to_endpoints(x4)
        if x14 == 0:
            add_to_intercepts(x1)
            add_to_endpoints(x2)
            add_to_endpoints(x3)
        if x23 == 0:
            add_to_endpoints(x1)
            add_to_intercepts(x2)
            add_to_endpoints(x4)
        if x24 == 0:
            add_to_endpoints(x1)
            add_to_intercepts(x2)
            add_to_endpoints(x3)
        add_to_line_int(x1, x2)
        add_to_line_int(x3, x4)
        return 0
    if  x13 == 0 and x24 == 0 or \
        x23 == 0 and x14 == 0:
            #lines are exactly overlapping, use endpoints as intercepts
            add_to_intercepts(x1)
            add_to_intercepts(x2)
            add_to_line_int(x1, x2)
            return 0
    else:
        add_to_line_int(x1, x2)
        add_to_line_int(x3, x4)
        #lines partially overlap but points do not.
        if x13 + x14 > x23 + x24: #overlap of x2
            add_to_intercepts(x2)
            if x13 + x23 > x14 + x24:
                add_to_intercepts(x4)
                add_to_endpoints(x3)
            else:
                add_to_intercepts(x3)
                add_to_endpoints(x4)
            add_to_endpoints(x1)

            return 0
        if x13 + x14 < x23 + x24:
            add_to_intercepts(x1)
            if x13 + x23 < x14 + x24:
                add_to_intercepts(x4)
                add_to_endpoints(x3)
            else:
                add_to_intercepts(x3)
                add_to_endpoints(x4)
            add_to_endpoints(x2)
            return 0
        if x13 + x14 == x23 + x24: #one of the points overlaps
            if x13 == 0:
                add_to_intercepts(x1)
                if x12 > x14:
                    add_to_intercepts(x4)
                    add_to_endpoints(x2)
                else:
                    add_to_endpoints(x4)
                    add_to_intercepts(x2)
                return 0
            if x14 == 0:
                add_to_intercepts(x1)
                if x12 > x13:
                    add_to_intercepts(x3)
                    add_to_endpoints(x2)
                else:
                    add_to_endpoints(x3)
                    add_to_intercepts(x2)
                return 0
            if x23 == 0:
                add_to_intercepts(x2)
                if x12 > x24:
                    add_to_intercepts(x4)
                    add_to_endpoints(x2)
                else:
                    add_to_endpoints(x4)
                    add_to_intercepts(x2)
                return 0
            if x24 == 0:
                add_to_intercepts(x2)
                if x12 > x23:
                    add_to_intercepts(x3)
                    add_to_endpoints(x2)
                else:
                    add_to_endpoints(x3)
                    add_to_intercepts(x2)
                return 0

def add_vertices(v1, v2, I):
    if v1[0] <> I[0] or v1[1] <> I[1]:
        add_to_endpoints(v1)
    if v2[0] <> I[0] or v2[1] <> I[1]:
        add_to_endpoints(v2)
    add_to_intercepts(I)
    # We have now added the endpoints and intercepts accordingly.
    # declare that the endpoints define a line which contains at least one intercept
    add_to_line_int(v1,v2)


def make_edges(lines, ints):
    index = 1
    for line in lines:
        sorted_ints = find_ints_on_line(line[0], line[1], ints)
        sorted_ints[:0] = [line[0]]
        sorted_ints.append(line[1])
        counter = 1
        for val in sorted_ints:
            if counter == 1:
                prev_val = val
                counter = counter + 1
                continue
            else:
                key = getKeysByValue(V, prev_val)
                key2 = getKeysByValue(V, val)
                item_exist = False
                list_E = list(E.keys())
                for edge_index in list_E:
                    if E[edge_index] == [key[0], key2[0]]:
                        item_exist = True
                if item_exist == False:
                    E.update({index:[key[0], key2[0]]})
                    counter = counter + 1
                    index = index + 1
                prev_val = val


def make_graph(line):
    # 1. Build the Vertices tuple
    keys = list(streets.keys())
    keys2 = list(streets.keys())

    # create vertices per street
    for key in keys:
        keys2.remove(key) # remove current street from the future compare
        counter = 0
        for points in streets[key]:
            coord_x1 = int(points.split(",")[0])
            coord_y1 = int(points.split(",")[1])
            a2 = np.array([coord_x1,coord_y1])
            if points == streets[key][0]:
                a1 = a2
                continue
            for key2 in keys2:
                for points2 in streets[key2]:
                    coord_x2 = int(points2.split(",")[0])
                    coord_y2 = int(points2.split(",")[1])
                    b2 = np.array([coord_x2,coord_y2])
                    if points2 == streets[key2][0]:
                        b1 = b2
                        continue
                    if intersect_on_line(a1,a2, b1, b2) == 1:
                        I = seg_intersect(a1,a2, b1,b2)
                        add_vertices(a1, a2, I)
                        add_vertices(b1, b2, I)
                    # if intersect_on_line == 2:
                    #     add_coincident_lines(a1,a2,b1,b2)
                    b1 = b2
            a1 = a2

    counter = 0
    for val in endpoints:
        counter = counter + 1
        V.update({counter:val})
    for val in intercepts:
        counter = counter + 1
        V.update({counter:val})

    print 'V = {'
    for elem in V:
        x = V[elem][0]
        y = V[elem][1]
        print('   {:.0f}:\t({:.2f},{:.2f})'.format(elem, x, y))
    print '}'
    # 2. Build the Edges tuple
    make_edges(lines_with_intercepts, intercepts)
    #  print E
    print 'E = {'
    counter = 0
    for elem in E:
        counter = counter + 1
        if counter == len(E.keys()):
            print('   <{},{}>'.format(E[elem][0], E[elem][1]))
        else:
            print('   <{},{}>,'.format(E[elem][0], E[elem][1]))
    print '}'

def streets_add(line):
    # Parse line for "Streetname"
    streetname = line.split('"')[1]
    keys = list(streets.keys())
    for key in keys:
        if key.lower() == streetname.lower() :
            sys.stdout.write("Error: The street '" + streetname + "' already exists.")
            return(0)
    vertices = line.split('"')[2].replace(" ","").replace(")(",")!!(").replace("\n","").replace("(","").replace(")","").split("!!")
    streets.update({streetname:vertices})
    return 1

def streets_change(line):
    streetname = line.split('"')[1]
    keys = list(streets.keys())
    street_exists = False
    for key in keys:
        if key.lower() == streetname.lower() :
            street_exists = True
    if street_exists == False:
        sys.stdout.write("Error: The street '" + streetname + "' does not exist.")
        return(0)
    streets_remove(line)
    vertices = line.split('"')[2].replace(" ","").replace(")(",")!!(").replace("\n","").replace("(","").replace(")","").split("!!")
    streets.update({streetname:vertices})
    return 1

def streets_remove(line):
    streetname = line.split('"')[1]
    keys = list(streets.keys())
    street_exists = False
    for key in keys:
        if key.lower() == streetname.lower() :
            streets.pop(key)
            street_exists = True
    if street_exists == False:
        sys.stdout.write("Error: The street '" + streetname + "' does not exist.")
        return(0)
    return 1

def validate(line):
    # 1. Check that line structure is as follows, @ "<name>" (n,n)*
    # Where @ = one letter command
    # Where * indicates zero or more sets of (n,n) coordinates
    # 1.1 Check for @
    first_char = line[:1]
    first_space = line[1:2]
    r = re.compile(r'[a-z,A-Z]+')
    v = r.findall(first_char)
    if (first_space <> " " or v == []) and first_char not in ['g','G'] :
        line = line.replace('\n',"")
        sys.stdout.write("Error: The function is incomplete for '" + line + "'")
        return 0
    #1.2 Check for "<street name>"
    first_quote = line[2:3]
    if first_quote <> '"' and first_char not in ['g','G']:
        line = line.replace('\n',"")
        sys.stdout.write("Error: The formatting for streetname is invalid in '" + line + "'")
        return 0
    try:
        streetname = line.split('"')[1]
        r = re.compile(r'[a-zA-Z ]+')
        v = r.findall(streetname)
        if v <> [streetname] :
            streetname.replace('\n',"")
            sys.stdout.write("Error: The streetname '" + streetname + "' contains invalid characters.")
            return 0
        #1.3 If any text exists after the last '"', it needs to match the format of (n,n)
        rest = line.split('"')[2].replace('\n',"")
        r = re.compile(r'[-,0-9() ]+')
        v = r.findall(rest)
        if v <> [rest] and rest <> "":
            sys.stdout.write("Error: The listed coordinates '" + rest + "' contains invalid characters.")
            return 0
        vertices = line.split('"')[2].replace(" ","").replace(")(",")!!(").replace("\n","").split("!!")
        r = re.compile(r'[(][-]?[0-9]+,[-]?[0-9]+\)')
        for e in vertices:
            v = r.findall(e)
            if v <> [e] and e <> '':
                line = line.replace('\n',"")
                sys.stdout.write( "Error: The co-ordinates in '" + line + "' were invalid"  )
                return 0
    except:
        if first_char not in ['g', 'G']:
            sys.stdout.write("Error: Text after the function is missing in '" + line + "'" )
            return 0

    # 2. Check if function character is valid
    r = re.compile(r'[acrg]+')
    v = r.findall(first_char)
    if v == [] :
        line = line.replace('\n',"")
        sys.stdout.write( "Error: The function '" + line[:1] + "' is not valid in '" + line + "'" )
        return 0

    return 1 # Success message


# Make global dictionaries for storing the data
streets = {}
lines = {}
V = {}
E = {}
endpoints = []
intercepts = []
lines_with_intercepts = []
# Make a global error response to catch issues
err_response = ""

while True:
    line = sys.stdin.readline()
    line = line.strip(" ")
    if line == '': # use Ctrl-Z to escape
        break
    if validate(line) == 0 :
        # An error was encountered. Write a newline to stdout
        sys.stdout.write('\n')
    else:
        if line[:1] in ['a', "A"]:
            if streets_add(line) == 0:
                sys.stdout.write('\n')
            print streets
        if line[:1] in ['c', 'C']:
            if streets_change(line) == 0:
                sys.stdout.write('\n')
        if line[:1] in ['r', 'R']:
            if streets_remove(line) == 0:
                sys.stdout.write('\n')
        if line[:1] in ['g', 'G']:
            # reset all variables
            lines = {}
            V = {}
            E = {}
            endpoints = []
            intercepts = []
            lines_with_intercepts = []
            make_graph(line)
        # print 'read a line:', line

print 'Finished reading input'
# return exit code 0 on successful termination
sys.exit(0)

if __name__ == '__main__':
    main()
